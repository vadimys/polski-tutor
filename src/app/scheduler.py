"""Щоденне нагадування у ПЕРСОНАЛЬНУ годину кожного учня — простий in-process цикл.

Цикл прокидається на початку кожної години й нагадує тим, у кого `lesson_hour`
збігається з поточною годиною (локальний пояс). Дефолт години — `settings.lesson_hour`
(08:00); кожен може змінити свою через /przypomnienie. Ретеншн-очищення denied —
раз на добу. Для одного-кількох користувачів цього досить; воркер/cron не потрібен.
"""

from __future__ import annotations

import asyncio
import html
import logging
from datetime import date, timedelta

from aiogram import Bot
from redis.asyncio import Redis

from app.bot.keyboards import coach_kb, exam_result_kb
from app.config import settings
from app.domain.models import MODULE_LABELS
from app.services import access, assignments, clock, exam_dates, gdpr, goals, state

logger = logging.getLogger(__name__)

_PURGE_HOUR = 3  # ретеншн-очищення denied-користувачів — раз на добу вночі
_EXAM_HOUR = 9  # exam-lifecycle (напередодні/день/post-exam) — раз на добу зранку
_NUDGE_TTL = 90_000  # ~25 год — дедуп-мітка нагадування самоскидається щодоби
_EXAM_TTL = 40 * 24 * 3600  # дедуп exam-повідомлень (довше за вікно до/після іспиту)

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def _already_nudged(user_id: int, today: str) -> bool:
    """Чи вже слали нагадування сьогодні (Redis → переживає рестарт бота)."""
    return bool(await _r().exists(f"polski:nudge:{user_id}:{today}"))


async def _mark_nudged(user_id: int, today: str) -> None:
    await _r().set(f"polski:nudge:{user_id}:{today}", "1", ex=_NUDGE_TTL)


async def _claim(key: str) -> bool:
    """Атомарно «займає» разову подію (exam-lifecycle) — True, якщо ще не було."""
    return bool(await _r().set(key, "1", nx=True, ex=_EXAM_TTL))


async def _exam_lifecycle(bot: Bot, today: date) -> None:
    """Раз на добу: напередодні іспиту — поради, у день — powodzenia, після — «як пройшло?»."""
    for uid in await state.all_user_ids():
        if uid == settings.admin_id or not await access.is_allowed(uid, settings.admin_id):
            continue
        inf = await access.info(uid)
        if inf.role == "teacher" or not (inf.confirmed and inf.exam_date):
            continue
        d = exam_dates.days_left(inf.exam_date, today)
        if d is None:
            continue
        try:
            if d == 1 and await _claim(f"exl:before:{uid}:{inf.exam_date}"):
                await bot.send_message(
                    uid,
                    "📅 <b>Завтра твій іспит B1!</b> Поради: сьогодні відпочинь і виспись, "
                    "звечора склади документи (паспорт), приходь на місце завчасно. "
                    "Ти готувався — вір у себе! 🍀",
                )
            elif d == 0 and await _claim(f"exl:day:{uid}:{inf.exam_date}"):
                await bot.send_message(uid, "🍀 <b>Powodzenia na egzaminie!</b> Ти впораєшся 💪")
            elif d < 0 and inf.exam_result == "":
                await access.set_exam_result(uid, "pending")  # питаємо один раз
                await bot.send_message(
                    uid, "📅 Твій іспит уже позаду. <b>Як пройшло?</b>", reply_markup=exam_result_kb()
                )
        except Exception:  # noqa: BLE001
            logger.exception("exam lifecycle failed uid=%s", uid)


async def _assignment_reminders(bot: Bot, today: date) -> None:
    """Раз на добу: нагадати учням про завдання з дедлайном завтра/сьогодні (лише невиконані)."""
    phases = {
        (today + timedelta(days=1)).isoformat(): ("завтра", "⏰ <b>Завтра дедлайн</b> завдання"),
        today.isoformat(): ("today", "⏰ <b>Сьогодні останній день</b> для завдання"),
    }
    for iso, (tag, head) in phases.items():
        for a in await assignments.due_on(iso):
            for uid in await assignments.pending_students(a):
                if not await _claim(f"asgn:rem:{a['id']}:{uid}:{tag}"):
                    continue
                try:
                    await bot.send_message(
                        uid,
                        f"{head}:\n<b>{html.escape(a['title'])}</b>\n\n"
                        "Відкрий меню «📝 Завдання», щоб позначити виконаним.",
                    )
                except Exception:  # noqa: BLE001
                    logger.exception("assignment reminder failed uid=%s aid=%s", uid, a["id"])


async def _seconds_until_next_hour() -> float:
    now = clock.now_local()
    target = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    return (target - now).total_seconds()


async def _personal_nudge(user_id: int) -> str:
    """Персональне нагадування: фокус на найслабший модуль + днів до іспиту."""
    st = await state.load(user_id)
    weakest = MODULE_LABELS[st.weakest_module()]
    inf = await access.info(user_id)
    tail = ""
    if inf.confirmed and inf.exam_date:
        try:
            days = max(0, (date.fromisoformat(inf.exam_date) - clock.today_local()).days)
            tail = f" До іспиту <b>{days}</b> днів."
        except ValueError:
            tail = ""
    froze = await goals.maybe_freeze(user_id)  # врятувати серію за вчора, якщо є заморозка
    g = await goals.status(user_id)
    goal_line = f"🎯 Ціль дня: <b>{g['goal']}</b> хв"
    if g["streak"]:
        goal_line += f" · 🔥 <b>{g['streak']}</b> дн поспіль — не гасимо серію!"
    freeze_line = "🧊 <i>Пропущений день врятовано заморозкою — серія жива!</i>\n" if froze else ""
    return (
        f"🌅 <b>Dzień dobry!</b> Час для польської.{tail}\n"
        f"{freeze_line}{goal_line}\n"
        f"Сьогодні варто підтягнути: <b>{weakest}</b>.\n"
        "Тисни <b>⚡ Навчатись зараз</b> — сам підберу найкорисніше 👇"
    )


async def _nudge_due(bot: Bot, hour: int, today: str) -> int:
    """Нагадати всім, у кого персональна година = поточній (раз на добу, дедуп у Redis)."""
    sent = 0
    for uid in await state.all_user_ids():
        if not await access.is_allowed(uid, settings.admin_id):
            continue  # не турбуємо не-схвалених
        st = await state.load(uid)
        if st.role == "teacher":
            continue  # викладач не готується до власного іспиту — особистий нудж не шлемо
        if st.lesson_hour != hour or await _already_nudged(uid, today):
            continue
        try:
            await bot.send_message(uid, await _personal_nudge(uid), reply_markup=coach_kb())
            await _mark_nudged(uid, today)
            sent += 1
        except Exception:
            logger.exception("nudge failed uid=%s", uid)
    return sent


async def _run_hour(bot: Bot, purged_on: str | None) -> str | None:
    """Робота однієї години: персональні нудж(і) + (раз/добу) ретеншн і exam/завдання."""
    now = clock.now_local()
    today = clock.today_local().isoformat()
    sent = await _nudge_due(bot, now.hour, today)
    if sent:
        logger.info("Nudge о %02d:00 → %d users", now.hour, sent)
    if now.hour == _PURGE_HOUR and purged_on != today:  # ретеншн — раз на добу
        purged_on = today
        try:
            purged = await gdpr.purge_stale(clock.today_local())
            if purged:
                logger.info("Retention: видалено %d denied-користувачів", purged)
        except Exception:
            logger.exception("retention purge failed")
    if now.hour == _EXAM_HOUR:  # exam-lifecycle + нагадування завдань — раз на добу
        await _exam_lifecycle(bot, clock.today_local())
        await _assignment_reminders(bot, clock.today_local())
    return purged_on


async def daily_nudge_loop(bot: Bot) -> None:
    purged_on: str | None = None
    try:  # катч-ап поточної години при старті: рестарт у межах години не «з'їдає» роботу
        purged_on = await _run_hour(bot, purged_on)
    except Exception:
        logger.exception("initial hour run failed")
    while True:
        try:
            await asyncio.sleep(await _seconds_until_next_hour())
            purged_on = await _run_hour(bot, purged_on)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("nudge loop error; retry in 60s")
            await asyncio.sleep(60)
