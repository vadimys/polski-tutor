"""Модуль мовлення (Mówienie): тема → голосове → Whisper → AI-фідбек."""

from __future__ import annotations

import html
import logging
import os
import tempfile

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import menu_kb, to_menu_kb
from app.domain.models import Module
from app.integrations import speech
from app.services import speaking
from app.services import state as user_state

logger = logging.getLogger(__name__)
router = Router()


class Speaking(StatesGroup):
    waiting = State()


async def _give_task(message: Message, state: FSMContext) -> None:
    if not speech.available():
        await message.answer(
            "🎤 Розпізнавання голосу тимчасово недоступне. Спробуй пізніше.",
            reply_markup=to_menu_kb(),
        )
        return
    task = speaking.pick_task()
    await state.set_state(Speaking.waiting)
    await state.update_data(task_id=task.id)
    await message.answer(
        f"🗣 <b>Мовлення (Mówienie)</b>\n\n{html.escape(task.prompt)}\n\n"
        "Запиши <b>голосове</b> польською (≈ 30–60 секунд) — я розпізнаю й дам фідбек "
        "по граматиці й лексиці. (/menu — вийти)"
    )


@router.message(Command("mowienie"))
async def cmd_speaking(message: Message, state: FSMContext) -> None:
    await _give_task(message, state)


@router.callback_query(F.data == "speaking:start")
async def cb_speaking(cb: CallbackQuery, state: FSMContext) -> None:
    await _give_task(cb.message, state)
    await cb.answer()


@router.message(Speaking.waiting, F.voice)
async def on_voice(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    task = speaking.task_by_id(data.get("task_id", ""))
    await state.clear()
    if task is None:
        await message.answer("Завдання загубилось — почнімо заново.", reply_markup=menu_kb())
        return

    await message.answer("🎧 Слухаю й розпізнаю…")
    fd, path = tempfile.mkstemp(suffix=".oga")
    os.close(fd)
    try:
        await message.bot.download(message.voice, destination=path)
        transcript = await speech.transcribe(path)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

    if not transcript:
        await message.answer(
            "Не вдалося розпізнати голос 😕 Спробуй ще раз, чіткіше й ближче до мікрофона.",
            reply_markup=to_menu_kb(),
        )
        return

    fb, score = await speaking.feedback(task, transcript)
    if not fb:
        await message.answer(
            f"📝 Я почув:\n«{html.escape(transcript)}»\n\nAI-фідбек тимчасово недоступний.",
            reply_markup=to_menu_kb(),
        )
        return

    header = f"📝 <b>Я почув:</b>\n«{html.escape(transcript)}»\n\n"
    if score is not None:
        st = await user_state.load(message.from_user.id)
        old = st.readiness.get(Module.MOWIENIE.value, score)
        st.readiness[Module.MOWIENIE.value] = round((old + score) / 2)
        await user_state.save(st)
        header += f"📊 Орієнтовна оцінка: <b>{score}%</b> (поріг — 50%)\n\n"

    await message.answer(header + fb, reply_markup=to_menu_kb())


@router.message(Speaking.waiting, F.text, ~F.text.startswith("/"))
async def on_text_instead(message: Message) -> None:
    await message.answer("🎤 Надішли саме <b>голосове</b> повідомлення (натисни й утримуй мікрофон).")
