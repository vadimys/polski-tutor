"""Головне меню + дашборд прогресу."""

from __future__ import annotations

from datetime import date

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import menu_kb, to_menu_kb
from app.bot.ui import bar
from app.domain.models import MODULE_LABELS, Module
from app.services import access, clock, progress, vocab
from app.services import state as user_state

router = Router()

_MENU_TEXT = "📋 <b>Меню</b> — обери, чим займемось:"


def _user_days_left(inf) -> int | None:
    if not (inf.confirmed and inf.exam_date):
        return None
    try:
        return max(0, (date.fromisoformat(inf.exam_date) - clock.today_local()).days)
    except ValueError:
        return None


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer(_MENU_TEXT, reply_markup=menu_kb())


@router.callback_query(F.data == "menu:home")
async def cb_menu(cb: CallbackQuery) -> None:
    await cb.message.answer(_MENU_TEXT, reply_markup=menu_kb())
    await cb.answer()


async def _render_progress(user_id: int) -> str:
    st = await user_state.load(user_id)
    inf = await access.info(user_id)
    days_left = _user_days_left(inf)
    total_words, due_n = await vocab.counts(user_id, clock.today_local())
    total_sessions, last7 = await progress.counts(user_id)

    exam_line = f"📅 До іспиту: <b>{days_left}</b> днів" if days_left is not None else "📅 Дата іспиту не підтверджена"
    lines = [
        f"📊 <b>Прогрес</b> · рівень <b>{st.level or '—'}</b> · стрік <b>{st.streak}</b> 🔥",
        exam_line,
        f"🏋️ Вправ усього: <b>{total_sessions}</b> · за 7 днів: <b>{last7}</b>",
        f"📚 Слова: <b>{total_words}</b> · на повторення: <b>{due_n}</b>\n",
    ]
    if st.readiness:
        lines.append("<b>Готовність за модулями</b> (мета — 50%, зі стрілкою тренду):")
        for mod in Module:
            pct = st.readiness.get(mod.value, 0)
            mark = "✅" if pct >= 50 else "🔸"
            arrow = progress.trend(await progress.recent_scores(user_id, mod.value))
            lines.append(f"{mark} {MODULE_LABELS[mod]} {arrow}\n  {bar(pct)}")
        lines.append("\n" + progress.projection(st.readiness, days_left is not None, days_left))
    else:
        lines.append("Спершу пройди стартовий тест (/test), щоб я визначив готовність.")
    return "\n".join(lines)


@router.message(Command("postep"))
async def cmd_progress(message: Message) -> None:
    await message.answer(await _render_progress(message.from_user.id), reply_markup=to_menu_kb())


@router.callback_query(F.data == "progress:show")
async def cb_progress(cb: CallbackQuery) -> None:
    await cb.message.answer(await _render_progress(cb.from_user.id), reply_markup=to_menu_kb())
    await cb.answer()
