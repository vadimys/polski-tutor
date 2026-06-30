"""Головне меню + дашборд прогресу."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import menu_kb, to_menu_kb
from app.bot.ui import bar
from app.domain.models import MODULE_LABELS, Module
from app.services import clock, vocab
from app.services import state as user_state

router = Router()

_MENU_TEXT = "📋 <b>Меню</b> — обери, чим займемось:"


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer(_MENU_TEXT, reply_markup=menu_kb())


@router.callback_query(F.data == "menu:home")
async def cb_menu(cb: CallbackQuery) -> None:
    await cb.message.answer(_MENU_TEXT, reply_markup=menu_kb())
    await cb.answer()


async def _render_progress(user_id: int) -> str:
    st = await user_state.load(user_id)
    total, due_n = await vocab.counts(user_id, clock.today_local())
    lines = [
        f"📊 <b>Прогрес</b> · рівень <b>{st.level or '—'}</b> · стрік <b>{st.streak}</b> 🔥",
        f"📅 До іспиту: <b>{clock.days_to_exam()}</b> днів",
        f"📚 Слова: <b>{total}</b> · на повторення сьогодні: <b>{due_n}</b>\n",
    ]
    if st.readiness:
        lines.append("<b>Готовність за модулями</b> (мета — 50% у кожному):")
        for mod in Module:
            pct = st.readiness.get(mod.value, 0)
            mark = "✅" if pct >= 50 else "🔸"
            lines.append(f"{mark} {MODULE_LABELS[mod]}\n  {bar(pct)}")
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
