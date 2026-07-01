"""Модуль письма (Pisanie): офіційний набір (a+b) → фідбек за офіційною шкалою /30."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import menu_kb, to_menu_kb
from app.domain.models import Module
from app.services import limits, writing
from app.services import state as user_state

router = Router()

MIN_WORDS = 5  # захист від «.» замість тексту
MAX_CHARS = 4000  # захист від cost-abuse: обсяг B1 ~30–175 слів, 4000 символів — з великим запасом


class Writing(StatesGroup):
    await_a = State()
    await_b = State()


async def _give_set(message: Message, state: FSMContext) -> None:
    ws = writing.pick_set()
    await state.set_state(Writing.await_a)
    await state.update_data(set_id=ws.id, text_a="")
    await message.answer(
        f"✍️ <b>Письмо — набір ({writing.SOURCE})</b>\n\n"
        f"Як на іспиті: <b>два завдання</b>, обидва з цього набору.\n\n"
        f"<b>Завдання a</b> ({ws.a.genre}, ~{ws.a.words} слів):\n{html.escape(ws.a.prompt)}\n\n"
        f"<b>Завдання b</b> ({ws.b.genre}, ~{ws.b.words} слів):\n{html.escape(ws.b.prompt)}\n\n"
        "Спершу напиши польською <b>завдання a</b> одним повідомленням. (/menu — вийти)"
    )


@router.message(Command("pisanie"))
async def cmd_writing(message: Message, state: FSMContext) -> None:
    await _give_set(message, state)


@router.callback_query(F.data == "writing:start")
async def cb_writing(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _give_set(cb.message, state)


@router.message(Writing.await_a, F.text, ~F.text.startswith("/"))
async def on_task_a(message: Message, state: FSMContext) -> None:
    if len(message.text.split()) < MIN_WORDS:
        await message.answer("Напиши, будь ласка, повноцінний текст завдання a 🙂")
        return
    if len(message.text) > MAX_CHARS:
        await message.answer(f"Текст задовгий (>{MAX_CHARS} символів). На іспиті B1 обсяг невеликий — скороти 🙂")
        return
    await state.update_data(text_a=message.text)
    await state.set_state(Writing.await_b)
    data = await state.get_data()
    ws = writing.set_by_id(data["set_id"])
    b = ws.b if ws else None
    hint = f"({b.genre}, ~{b.words} слів)" if b else ""
    await message.answer(f"✅ Прийнято. Тепер напиши <b>завдання b</b> {hint}.")


@router.message(Writing.await_b, F.text, ~F.text.startswith("/"))
async def on_task_b(message: Message, state: FSMContext) -> None:
    if len(message.text.split()) < MIN_WORDS:
        await message.answer("Напиши, будь ласка, повноцінний текст завдання b 🙂")
        return
    if len(message.text) > MAX_CHARS:
        await message.answer(f"Текст задовгий (>{MAX_CHARS} символів). На іспиті B1 обсяг невеликий — скороти 🙂")
        return
    data = await state.get_data()
    ws = writing.set_by_id(data["set_id"])
    text_a = data.get("text_a", "")
    await state.clear()
    if ws is None:
        await message.answer("Набір загубився — почнімо заново.", reply_markup=menu_kb())
        return
    if not await limits.allow_ai(message.from_user.id):
        await message.answer(
            "🚫 Денний ліміт AI-фідбеку вичерпано. Тренування/МОК/повторення — без ліміту 👍 "
            "Письмо — завтра.",
            reply_markup=to_menu_kb(),
        )
        return

    await message.answer("🔍 Оцінюю за офіційними критеріями (wykonanie / środki / poprawność)…")
    fb, scores = await writing.feedback(ws, text_a, message.text)
    if not fb:
        await message.answer("AI тимчасово недоступний — спробуй пізніше.", reply_markup=to_menu_kb())
        return

    header = ""
    if scores is not None:
        wyk, sr, popr = scores
        total = wyk + sr + popr
        passed = "✅ склав би" if total >= 15 else "❌ поки нижче порога"
        header = (
            "📊 <b>Офіційна шкала (0-30):</b>\n"
            f"• Wykonanie zadania: <b>{wyk}</b>/10\n"
            f"• Środki językowe: <b>{sr}</b>/10\n"
            f"• Poprawność językowa: <b>{popr}</b>/10\n"
            f"• <b>Разом: {total}/30</b> — поріг 15/30 ({passed})\n\n"
        )
        pct = round(total / 30 * 100)
        await user_state.update_readiness(message.from_user.id, Module.PISANIE.value, pct)

    await message.answer(header + fb, reply_markup=to_menu_kb())
