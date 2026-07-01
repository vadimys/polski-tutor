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
from app.services import limits, speaking
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
    label = speaking._KIND_LABEL[task.kind]
    await state.set_state(Speaking.waiting)
    await state.update_data(task_id=task.id)
    await message.answer(
        f"🗣 <b>Мовлення — {label}</b> ({speaking.SOURCE})\n\n{html.escape(task.prompt)}\n\n"
        "Запиши <b>голосове</b> польською (≈ 30–60 секунд) — розпізнаю й оціню за офіційними "
        "критеріями (wykonanie / gramatyka / słownictwo). (/menu — вийти)"
    )


async def _give_photo(message: Message, state: FSMContext) -> None:
    if not speech.available():
        await message.answer(
            "🎤 Розпізнавання голосу тимчасово недоступне. Спробуй пізніше.",
            reply_markup=to_menu_kb(),
        )
        return
    task = speaking.pick_photo()
    await state.set_state(Speaking.waiting)
    await state.update_data(task_id=task.id)
    await message.answer_photo(
        task.photo_url,
        caption=(
            f"🗣 <b>Мовлення — {speaking._KIND_LABEL['opis']}</b>\n\n{html.escape(task.prompt)}\n\n"
            "Запиши <b>голосове</b> польською — оціню за офіційними критеріями. "
            f"(<i>{html.escape(task.photo_source)}</i>) (/menu — вийти)"
        ),
    )


@router.message(Command("mowienie"))
async def cmd_speaking(message: Message, state: FSMContext) -> None:
    await _give_task(message, state)


@router.message(Command("opis"))
async def cmd_opis(message: Message, state: FSMContext) -> None:
    await _give_photo(message, state)


@router.callback_query(F.data == "speaking:start")
async def cb_speaking(cb: CallbackQuery, state: FSMContext) -> None:
    await _give_task(cb.message, state)
    await cb.answer()


@router.callback_query(F.data == "speaking:photo")
async def cb_photo(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _give_photo(cb.message, state)


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
    if not await limits.allow_ai(message.from_user.id):
        await message.answer(
            f"📝 Я почув:\n«{html.escape(transcript)}»\n\n"
            "🚫 Денний ліміт AI-фідбеку вичерпано. Спробуй мовлення завтра 🙂",
            reply_markup=to_menu_kb(),
        )
        return

    fb, scores = await speaking.feedback(task, transcript)
    if not fb:
        await message.answer(
            f"📝 Я почув:\n«{html.escape(transcript)}»\n\nAI-фідбек тимчасово недоступний.",
            reply_markup=to_menu_kb(),
        )
        return

    header = f"📝 <b>Я почув:</b>\n«{html.escape(transcript)}»\n\n"
    if scores is not None:
        wyk, gram, slow = scores
        wyk = min(wyk, task.max_wykonanie)
        gram, slow = min(gram, 8), min(slow, 8)
        pct = speaking.readiness_pct(task, wyk, gram, slow)
        header += (
            "📊 <b>Офіційні критерії</b> (оцінюване з транскрипту):\n"
            f"• Wykonanie zadania: <b>{wyk}</b>/{task.max_wykonanie}\n"
            f"• Gramatyka: <b>{gram}</b>/8\n"
            f"• Słownictwo i styl: <b>{slow}</b>/8\n"
            "• Poprawność fonetyczna i płynność: лише на аудіо (не з тексту)\n\n"
        )
        await user_state.update_readiness(message.from_user.id, Module.MOWIENIE.value, pct)

    await message.answer(header + fb, reply_markup=to_menu_kb())


@router.message(Speaking.waiting, F.text, ~F.text.startswith("/"))
async def on_text_instead(message: Message) -> None:
    await message.answer("🎤 Надішли саме <b>голосове</b> повідомлення (натисни й утримуй мікрофон).")
