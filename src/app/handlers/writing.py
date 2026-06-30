"""Модуль письма (Pisanie): завдання → учень пише → AI-фідбек за критеріями B1."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import menu_kb, to_menu_kb
from app.domain.models import Module
from app.services import state as user_state
from app.services import writing

router = Router()


class Writing(StatesGroup):
    waiting = State()


async def _give_task(message: Message, state: FSMContext) -> None:
    task = writing.pick_task()
    await state.set_state(Writing.waiting)
    await state.update_data(task_id=task.id)
    await message.answer(
        f"✍️ <b>Письмо ({html.escape(task.genre)})</b>\n\n"
        f"{html.escape(task.prompt)}\n\n"
        "Напиши свій текст польською <b>одним повідомленням</b> — я оціню за критеріями B1 "
        "і покажу виправлення. (/menu — вийти)"
    )


@router.message(Command("pisanie"))
async def cmd_writing(message: Message, state: FSMContext) -> None:
    await _give_task(message, state)


@router.callback_query(F.data == "writing:start")
async def cb_writing(cb: CallbackQuery, state: FSMContext) -> None:
    await _give_task(cb.message, state)
    await cb.answer()


@router.message(Writing.waiting, F.text, ~F.text.startswith("/"))
async def on_essay(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    task = writing.task_by_id(data.get("task_id", ""))
    await state.clear()
    if task is None:
        await message.answer("Завдання загубилось — почнімо заново.", reply_markup=menu_kb())
        return

    await message.answer("🔍 Перевіряю твій текст…")
    fb, score = await writing.feedback(task, message.text)
    if not fb:
        await message.answer(
            "AI тимчасово недоступний — спробуй пізніше.", reply_markup=to_menu_kb()
        )
        return

    # оновити готовність модуля Pisanie (згладжено: середнє старого й нового)
    header = ""
    if score is not None:
        st = await user_state.load(message.from_user.id)
        old = st.readiness.get(Module.PISANIE.value, score)
        st.readiness[Module.PISANIE.value] = round((old + score) / 2)
        await user_state.save(st)
        header = f"📊 Орієнтовна оцінка: <b>{score}%</b> (поріг іспиту — 50%)\n\n"

    await message.answer(header + fb, reply_markup=to_menu_kb())
