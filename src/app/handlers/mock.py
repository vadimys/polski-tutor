"""Офіційний МОК — секції Читання / Граматика з реального пробного тесту B1."""

from __future__ import annotations

import html
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot import quiz
from app.bot.keyboards import menu_kb, mock_kb, mock_menu_kb, to_menu_kb
from app.domain.models import Module
from app.services import goals, mock, progress
from app.services import state as user_state

router = Router()

_SECTION_MODULE = {"czytanie": Module.CZYTANIE, "gramatyka": Module.GRAMATYKA}
_SECTION_LABEL = {"czytanie": "📖 Читання", "gramatyka": "🔤 Граматика"}


class Mock(StatesGroup):
    active = State()


@router.message(Command("mok"))
async def cmd_mock(message: Message) -> None:
    await message.answer(
        "📋 <b>Офіційний МОК</b> — питання з реального пробного тесту Держкомісії B1.\n"
        "Обери секцію (поріг складання модуля — 50%):",
        reply_markup=mock_menu_kb(),
    )


async def _send_item(message: Message, section: str, idx: int) -> None:
    items = mock.section_items(section)
    it = items[idx]
    ctx = f"<i>{html.escape(it.context)}</i>\n\n" if it.context else ""
    await message.answer(
        f"<b>{_SECTION_LABEL[section]} · {idx + 1}/{len(items)}</b>\n\n"
        f"{ctx}{html.escape(it.question)}",
        reply_markup=mock_kb(it.options, idx),
    )


@router.callback_query(F.data.startswith("mock:"))
async def cb_start(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    section = cb.data.split(":", 1)[1]
    if section == "open":  # кнопка з головного меню → показати вибір секції
        await cb.message.answer(
            "📋 <b>Офіційний МОК</b> — питання з реального пробного тесту Держкомісії B1.\n"
            "Обери секцію (поріг складання модуля — 50%):",
            reply_markup=mock_menu_kb(),
        )
        return
    if section not in _SECTION_MODULE:
        return
    items = mock.section_items(section)
    await state.set_state(Mock.active)
    await state.update_data(section=section, idx=0, correct=0)
    await cb.message.answer(
        f"▶️ <b>{_SECTION_LABEL[section]}</b> — {len(items)} завдань з офіційного тесту. "
        "Відповідай, наприкінці — результат."
    )
    await _send_item(cb.message, section, 0)


@router.callback_query(Mock.active, F.data == "mk:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "⏹ МОК завершено достроково — <b>без оцінки</b> (готовність рухає лише повністю пройдена секція).",
        reply_markup=menu_kb(),
    )


@router.callback_query(Mock.active, F.data.startswith("mk:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    section, idx, correct = data["section"], data["idx"], data["correct"]

    chosen = await quiz.read_answer(cb, idx)
    if chosen is None:  # стале/дубль/зіпсовано — уже оброблено
        return

    items = mock.section_items(section)
    it = items[idx]
    if await quiz.show_verdict(cb, chosen, it.correct, it.options, it.question, it.explain):
        correct += 1

    idx += 1
    await state.update_data(idx=idx, correct=correct)
    if idx < len(items):
        await _send_item(cb.message, section, idx)
    else:
        await _finalize(cb.message, cb.from_user.id, state, section, correct, len(items))


async def _finalize(
    message: Message, user_id: int, state: FSMContext, section: str, correct: int, total: int
) -> None:
    await state.clear()
    pct = round(correct / total * 100) if total else 0
    passed = "✅ склав би модуль" if pct >= 50 else "❌ поки нижче порога (50%)"
    await user_state.update_readiness(user_id, _SECTION_MODULE[section].value, pct)
    await progress.record_mock_pass(user_id, section, pct)  # гейт готовності «під іспитом»
    await message.answer(
        f"🏁 <b>{_SECTION_LABEL[section]} — результат: {correct}/{total} ({pct}%)</b>\n"
        f"{passed}. Готовність оновлено.",
        reply_markup=menu_kb() if pct >= 50 else to_menu_kb(),
    )
    if c := await goals.pop_celebration(user_id):
        await message.answer(c)
