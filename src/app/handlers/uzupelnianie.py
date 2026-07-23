"""Вписати форму (free-fill) — офіційний тип Gramatyka Zad IV.

Учень ВПИСУЄ форму дієслова текстом (не вибір!). Показуємо інструкцію+приклад раз,
далі по одному пропуску: користувач пише відповідь → нормалізована звірка з
прийнятними варіантами (services.freefill) → миттєвий вердикт. Реальне екзам-завдання
→ рухає готовність граматики. У повний мок /egzamin інтегрується окремо.
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
from app.bot.keyboards import fill_kb, menu_kb_for, to_menu_kb
from app.services import freefill, goals
from app.services import state as user_state

router = Router()

_LABEL = {"czytanie": "📖 Читання", "gramatyka": "🔤 Граматика"}


class Fill(StatesGroup):
    active = State()


def _correct_line(accepted: list[str]) -> str:
    """Канонічна правильна відповідь (+ варіанти, якщо є)."""
    main = f"<b>{html.escape(accepted[0])}</b>"
    if len(accepted) > 1:
        main += " / " + " / ".join(html.escape(x) for x in accepted[1:])
    return main


async def _intro(message: Message) -> None:
    tasks = content.all_fill_tasks()
    if not tasks:
        await message.answer("Завдання «впиши форму» поки недоступні.", reply_markup=to_menu_kb())
        return
    b = InlineKeyboardBuilder()
    for i, t in enumerate(tasks):
        b.button(text=t.title, callback_data=f"fill:begin:{i}")
    b.button(text="⬅️ Меню", callback_data="menu:home")
    b.adjust(1)
    await message.answer(
        "✏️ <b>Впиши форму (uzupełnianie)</b>\n"
        "Офіційний тип завдання: вписати правильну форму слова. Відповідь <b>пишеш "
        "текстом</b> — я одразу скажу, правильно чи ні, з поясненням.\n"
        "💡 Порада: вимкни автовиправлення/T9 у клавіатурі — воно псує польські слова.\n"
        "\nОбери завдання:",
        reply_markup=b.as_markup(),
    )


async def _send_prompt(message: Message, prompts: list[str], pos: int) -> None:
    await message.answer(
        f"✏️ Пропуск <b>{pos + 1}/{len(prompts)}</b>\n\n{html.escape(prompts[pos])}\n\n"
        "<i>Напиши правильну форму одним повідомленням:</i>",
        reply_markup=fill_kb(pos),
    )


@router.message(Command("formy"))
async def cmd_fill(message: Message) -> None:
    await _intro(message)


@router.callback_query(F.data == "fill:open")
async def cb_open(cb: CallbackQuery) -> None:
    await cb.answer()
    await _intro(cb.message)


@router.callback_query(F.data.startswith("fill:begin:"))
async def cb_begin(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    idx = int(cb.data.split(":")[2])
    tasks = content.all_fill_tasks()
    if idx >= len(tasks):
        await cb.message.answer("Завдання недоступне.", reply_markup=to_menu_kb())
        return
    t = tasks[idx]
    await state.set_state(Fill.active)
    await state.update_data(
        section=t.section, prompts=list(t.prompts),
        accepted=[list(a) for a in t.accepted], explains=list(t.explain), pos=0, correct=0,
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="▶️ Розпочати", callback_data="fill:go")
    kb.button(text="⬅️ Меню", callback_data="ff:stop")
    kb.adjust(1)
    await cb.message.answer(
        f"✏️ <b>{html.escape(t.title)}</b>\n\n{t.intro}", reply_markup=kb.as_markup()
    )


@router.callback_query(Fill.active, F.data == "fill:go")
async def cb_go(cb: CallbackQuery, state: FSMContext) -> None:
    """Старт: прибрати кнопки з інтро → перше завдання (шлеться у відповідь на тап → скролиться)."""
    await cb.answer()
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    await _send_prompt(cb.message, data["prompts"], 0)


@router.callback_query(Fill.active, F.data == "ff:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "⏹ Завдання завершено — <b>без оцінки</b> (готовність рухає лише пройдене повністю).",
        reply_markup=await menu_kb_for(cb.from_user.id),
    )


async def _advance(message: Message, user_id: int, state: FSMContext) -> None:
    data = await state.get_data()
    pos, prompts = data["pos"] + 1, data["prompts"]
    await state.update_data(pos=pos)
    if pos < len(prompts):
        await _send_prompt(message, prompts, pos)
    else:
        await _finalize(message, user_id, state, data["correct"], len(prompts), data["section"])


@router.callback_query(Fill.active, F.data.startswith("ff:skip:"))
async def cb_skip(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    pos = data["pos"]
    if int(cb.data.split(":")[2]) != pos:  # стала кнопка / дубль
        await cb.answer("Це питання вже пройдено 🙂")
        return
    await cb.answer()
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    accepted, explains = data["accepted"], data["explains"]
    await cb.message.answer(
        f"⏭ Поправна відповідь: {_correct_line(accepted[pos])}\n💡 {explains[pos]}"
    )
    await _advance(cb.message, cb.from_user.id, state)


@router.message(Fill.active, F.text)
async def on_answer(message: Message, state: FSMContext) -> None:
    if len((message.text or "").strip()) > 200:  # форма — це слово/коротка фраза
        await message.answer("Форма — це слово чи коротка фраза. Напиши коротше ✍️")
        return
    data = await state.get_data()
    pos, accepted, explains = data["pos"], data["accepted"], data["explains"]
    ok = freefill.is_correct(message.text or "", accepted[pos])
    if ok:
        verdict = f"✔️ <b>Dobrze!</b> {html.escape(message.text.strip())}"
        await state.update_data(correct=data["correct"] + 1)
    else:
        verdict = f"❌ Poprawnie: {_correct_line(accepted[pos])}"
    await message.answer(f"{verdict}\n💡 {explains[pos]}")
    await _advance(message, message.from_user.id, state)


async def _finalize(
    message: Message, user_id: int, state: FSMContext, correct: int, total: int, section: str
) -> None:
    await state.clear()
    score = round(correct / total * 100) if total else 0
    await user_state.update_readiness(user_id, section, score)  # рухає готовність + час/XP
    emoji = "🎉" if score >= 80 else "👍" if score >= 50 else "💪"
    await message.answer(
        f"{emoji} <b>Впиши форму: {correct}/{total} ({score}%)</b>\n"
        f"Готовність {_LABEL.get(section, section)} оновлено.",
        reply_markup=(await menu_kb_for(user_id)) if score >= 50 else to_menu_kb(),
    )
    if c := await goals.pop_celebration(user_id):
        await message.answer(c)
