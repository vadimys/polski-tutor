"""Зіставлення (dopasowanie) — офіційний тип завдання Czytanie Zad III/IV.

Вставити фрагменти в текст або добрати заголовок до абзацу. Опорні фрагменти
показуємо ОДИН раз (список A–H), далі по одному пропуску з літерними кнопками +
миттєвий вердикт (тренувальний режим). Це РЕАЛЬНЕ екзам-завдання → рухає готовність
(на відміну від керованої практики). У повний мок /egzamin інтегрується окремо.
"""

from __future__ import annotations

import html
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import content
from app.bot import quiz
from app.bot.keyboards import match_kb, menu_kb, to_menu_kb
from app.services import goals
from app.services import state as user_state

router = Router()

_LABEL = {"czytanie": "📖 Читання", "gramatyka": "🔤 Граматика"}


class Match(StatesGroup):
    active = State()


async def _intro(message: Message) -> None:
    tasks = content.all_match_tasks()
    if not tasks:
        await message.answer("Завдання на зіставлення поки недоступні.", reply_markup=to_menu_kb())
        return
    b = InlineKeyboardBuilder()
    for i, t in enumerate(tasks):
        b.button(text=t.title, callback_data=f"match:begin:{i}")
    b.button(text="⬅️ Меню", callback_data="menu:home")
    b.adjust(1)
    await message.answer(
        "🧩 <b>Зіставлення (dopasowanie)</b>\n"
        "Офіційний тип завдання: вставити фрагменти в текст або добрати заголовки. "
        "Фрагменти показую списком (A, B, C…), ти обираєш літеру на кожен пропуск.\n\n"
        "Обери завдання:",
        reply_markup=b.as_markup(),
    )


async def _send_prompt(message: Message, prompts: list[str], n_options: int, pos: int) -> None:
    await message.answer(
        f"🧩 Пропуск <b>{pos + 1}/{len(prompts)}</b>\n\n{html.escape(prompts[pos])}\n\n"
        "Обери фрагмент (літера):",
        reply_markup=match_kb(n_options, pos),
    )


@router.message(Command("dopasowanie"))
async def cmd_match(message: Message) -> None:
    await _intro(message)


@router.callback_query(F.data == "match:open")
async def cb_open(cb: CallbackQuery) -> None:
    await cb.answer()
    await _intro(cb.message)


@router.callback_query(F.data.startswith("match:begin:"))
async def cb_begin(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    idx = int(cb.data.split(":")[2])
    tasks = content.all_match_tasks()
    if idx >= len(tasks):
        await cb.message.answer("Завдання недоступне.", reply_markup=to_menu_kb())
        return
    t = tasks[idx]
    await state.set_state(Match.active)
    await state.update_data(
        section=t.section, options=list(t.options), prompts=list(t.prompts),
        key=list(t.key), explains=list(t.explain), pos=0, correct=0,
    )
    opts_list = "\n".join(
        f"<b>{chr(65 + i)})</b> {html.escape(o)}" for i, o in enumerate(t.options)
    )
    await cb.message.answer(
        f"🧩 <b>{html.escape(t.title)}</b>\n\n{t.intro}\n\n🔤 <b>Фрагменти:</b>\n{opts_list}"
    )
    await _send_prompt(cb.message, t.prompts, len(t.options), 0)


@router.callback_query(Match.active, F.data == "ma:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "⏹ Зіставлення завершено — <b>без оцінки</b> (готовність рухає лише пройдене повністю).",
        reply_markup=menu_kb(),
    )


@router.callback_query(Match.active, F.data.startswith("ma:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    prompts, options, key, explains = (
        data["prompts"], data["options"], data["key"], data["explains"],
    )
    pos, correct, section = data["pos"], data["correct"], data["section"]

    chosen = await quiz.read_answer(cb, pos)
    if chosen is None:  # стале/дубль/зіпсовано
        return

    if await quiz.show_verdict(cb, chosen, key[pos], options, prompts[pos], explains[pos]):
        correct += 1

    pos += 1
    await state.update_data(pos=pos, correct=correct)
    if pos < len(prompts):
        await _send_prompt(cb.message, prompts, len(options), pos)
    else:
        await _finalize(cb.message, cb.from_user.id, state, correct, len(prompts), section)


async def _finalize(
    message: Message, user_id: int, state: FSMContext, correct: int, total: int, section: str
) -> None:
    await state.clear()
    score = round(correct / total * 100) if total else 0
    await user_state.update_readiness(user_id, section, score)  # рухає готовність + час/XP
    emoji = "🎉" if score >= 80 else "👍" if score >= 50 else "💪"
    await message.answer(
        f"{emoji} <b>Зіставлення: {correct}/{total} ({score}%)</b>\n"
        f"Готовність {_LABEL.get(section, section)} оновлено.",
        reply_markup=menu_kb() if score >= 50 else to_menu_kb(),
    )
    if c := await goals.pop_celebration(user_id):
        await message.answer(c)
