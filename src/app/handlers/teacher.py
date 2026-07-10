"""Дашборд викладача: прогрес приведених учнів (/uczniowie).

Головна винагорода партнера-викладача — бачити свій клас: готовність до B1,
скільки модулів ≥50%, найслабший модуль, серія й активність. Дані — з тих самих
sessions, що й у учня (progress.compute); учень погодився при вході за посиланням.
Доступно лише роль=teacher.
"""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import to_menu_kb
from app.domain.models import MODULE_LABELS, Module
from app.services import access, clock, progress, quest
from app.services import state as user_state

router = Router()


def _activity(days_since: int) -> str:
    if days_since <= 0:
        return " · активн. сьогодні"
    if days_since < 999:
        return f" · {days_since} дн тому"
    return ""


def _row(d: dict) -> str:
    """Один рядок класу (чиста функція — тестована)."""
    warn = " ⚠️ trial завершився" if d["expired"] else ""
    head = f"👤 <b>{html.escape(d['name'])}</b> — 🏁 {d['overall']}% · {d['passed']}/5 ≥50%{warn}"
    if not d["started"]:
        return head + "\n   <i>ще не проходив вправ</i>"
    streak = f" · 🔥 {d['streak']}" if d["streak"] else ""
    return head + f"\n   📉 {d['weak_label']} {d['weak_pct']}%{streak}{_activity(d['days_since'])}"


async def _gather(student_id: int) -> dict:
    inf = await access.info(student_id)
    stats = await progress.compute(student_id)
    pcts = progress.pcts(stats)
    started = any(s.attempts for s in stats.values())
    weak = min(Module, key=lambda m: pcts.get(m.value, 0))
    days_since = min((s.days_since for s in stats.values() if s.attempts), default=999)
    st = await user_state.load(student_id)
    name = f"@{inf.username}" if inf.username else f"id{student_id}"
    return {
        "name": name,
        "overall": quest.overall_pct(pcts),
        "passed": sum(1 for v in pcts.values() if v >= 50),
        "started": started,
        "weak_label": MODULE_LABELS[weak].split()[0] + " " + MODULE_LABELS[weak].split()[1],
        "weak_pct": pcts.get(weak.value, 0),
        "streak": st.streak,
        "days_since": days_since,
        "expired": access.is_expired(inf, clock.today_local()),
    }


async def _send_class(message: Message, teacher_id: int, bot_username: str) -> None:
    students = await access.students_of(teacher_id)
    link = f"https://t.me/{bot_username}?start=t{teacher_id}"
    if not students:
        await message.answer(
            "👩‍🏫 <b>Твій клас</b> — поки порожній.\n\n"
            "Поділись реферальним посиланням з учнями — кожен, хто зайде за ним, "
            "отримає безкоштовний доступ, а ти бачитимеш його прогрес тут:\n"
            f"<code>{link}</code>",
            reply_markup=to_menu_kb(),
        )
        return
    rows = [_row(await _gather(sid)) for sid in students]
    await message.answer(
        f"👩‍🏫 <b>Твій клас — {len(students)} учнів</b>\n"
        "<i>🏁 — готовність до B1; N/5 — модулів ≥50%; 📉 — найслабше.</i>\n\n"
        + "\n\n".join(rows)
        + f"\n\n🔗 Запросити ще: <code>{link}</code>",
        reply_markup=to_menu_kb(),
    )


async def _guard_teacher(message: Message, user_id: int) -> bool:
    inf = await access.info(user_id)
    if inf.role != "teacher":
        await message.answer(
            "👩‍🏫 Цей розділ — для викладачів. Хочеш навчати учнів через бота? "
            "Натисни /start і обери «Я викладач».",
            reply_markup=to_menu_kb(),
        )
        return False
    return True


@router.message(Command("uczniowie"))
async def cmd_class(message: Message) -> None:
    if not await _guard_teacher(message, message.from_user.id):
        return
    me = await message.bot.get_me()
    await _send_class(message, message.from_user.id, me.username or "")


@router.callback_query(F.data == "teacher:class")
async def cb_class(cb: CallbackQuery) -> None:
    await cb.answer()
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    me = await cb.bot.get_me()
    await _send_class(cb.message, cb.from_user.id, me.username or "")
