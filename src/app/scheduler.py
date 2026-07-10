"""Щоденне нагадування у ПЕРСОНАЛЬНУ годину кожного учня — простий in-process цикл.

Цикл прокидається на початку кожної години й нагадує тим, у кого `lesson_hour`
збігається з поточною годиною (локальний пояс). Дефолт години — `settings.lesson_hour`
(08:00); кожен може змінити свою через /przypomnienie. Ретеншн-очищення denied —
раз на добу. Для одного-кількох користувачів цього досить; воркер/cron не потрібен.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import date, timedelta

from aiogram import Bot

from app.bot.keyboards import coach_kb
from app.config import settings
from app.domain.models import MODULE_LABELS
from app.services import access, clock, gdpr, goals, state

logger = logging.getLogger(__name__)

_PURGE_HOUR = 3  # ретеншн-очищення denied-користувачів — раз на добу вночі


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


async def _nudge_due(bot: Bot, hour: int, today: str, sent_on: dict[int, str]) -> int:
    """Нагадати всім, у кого персональна година = поточній (раз на добу, з дедуплікацією)."""
    sent = 0
    for uid in await state.all_user_ids():
        if not await access.is_allowed(uid, settings.admin_id):
            continue  # не турбуємо не-схвалених
        st = await state.load(uid)
        if st.lesson_hour != hour or sent_on.get(uid) == today:
            continue
        try:
            await bot.send_message(uid, await _personal_nudge(uid), reply_markup=coach_kb())
            sent_on[uid] = today
            sent += 1
        except Exception:
            logger.exception("nudge failed uid=%s", uid)
    return sent


async def daily_nudge_loop(bot: Bot) -> None:
    sent_on: dict[int, str] = {}  # uid → дата останнього нагадування (дедуплікація в межах доби)
    purged_on: str | None = None
    while True:
        try:
            await asyncio.sleep(await _seconds_until_next_hour())
            now = clock.now_local()
            today = clock.today_local().isoformat()
            sent = await _nudge_due(bot, now.hour, today, sent_on)
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
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("nudge loop error; retry in 60s")
            await asyncio.sleep(60)
