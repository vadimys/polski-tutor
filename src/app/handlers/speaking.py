"""Модуль мовлення (Mówienie): тема → голосове → Whisper → AI-фідбек."""

from __future__ import annotations

import html
import logging
import os
import re
import tempfile

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import cancel_kb, menu_kb, to_menu_kb
from app.domain.models import Module
from app.integrations import speech, tts
from app.services import goals, guidance, limits, speaking, tts_say
from app.services import state as user_state

logger = logging.getLogger(__name__)
router = Router()

MAX_VOICE_SEC = 180  # захист від DoS: довге голосове = навантаження Whisper/CPU + диск
MAX_VOICE_BYTES = 10 * 1024 * 1024  # 10 МБ


class Speaking(StatesGroup):
    waiting = State()


class Guided(StatesGroup):
    active = State()  # керована практика комунікативної ситуації (крок-за-кроком)


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
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Показати зразок", callback_data=f"guide:spk:{task.kind}")
    if guidance.guided_available(task.kind):  # усі типи мовлення → є керована практика
        kb.button(text="🪜 Пройти по кроках", callback_data=f"guided:start:{task.id}")
    kb.button(text="🚫 Скасувати", callback_data="nav:cancel")
    kb.adjust(1)
    await message.answer(
        f"🗣 <b>Мовлення — {label}</b> ({speaking.SOURCE})\n\n{html.escape(task.prompt)}\n\n"
        f"{guidance.speaking_instruction(task.kind)}\n\n"
        "🎤 Готовий — запиши <b>голосове</b> польською (≈ 30–60 секунд).",
        reply_markup=kb.as_markup(),
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
            f"🎤 Запиши <b>голосове</b> польською. (<i>{html.escape(task.photo_source)}</i>)"
        ),
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Показати зразок", callback_data="guide:spk:opis")
    kb.button(text="🪜 Пройти по кроках", callback_data=f"guided:start:{task.id}")
    kb.button(text="🚫 Скасувати", callback_data="nav:cancel")
    kb.adjust(1)
    await message.answer(guidance.speaking_instruction("opis"), reply_markup=kb.as_markup())


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


@router.callback_query(F.data.startswith("guide:spk:"))
async def cb_example(cb: CallbackQuery) -> None:
    kind = cb.data.split(":", 2)[2]
    await cb.answer()
    example = guidance.speaking_example(kind)
    markup = None
    if tts.available():  # 🔊 почути зразкову відповідь польською
        plain = re.sub(r"<[^>]+>", "", example)  # без HTML-тегів для озвучення
        kb = InlineKeyboardBuilder()
        kb.button(text="🔊 Послухати зразок", callback_data=f"say:{await tts_say.stash(plain)}")
        markup = kb.as_markup()
    await cb.message.answer(example, reply_markup=markup)


# --- Керована практика (крок-за-кроком) для комунікативної ситуації ---


@router.callback_query(F.data.startswith("guided:start:"))
async def cb_guided_start(cb: CallbackQuery, state: FSMContext) -> None:
    task_id = cb.data.split(":", 2)[2]
    task = speaking.task_by_id(task_id)
    await cb.answer()
    if task is None:
        await cb.message.answer("Завдання загубилось — почни знову: /mowienie")
        return
    await state.set_state(Guided.active)
    await state.update_data(task_id=task_id, kind=task.kind, step=0, lines=[])
    if task.kind == "opis" and task.photo_url:
        await cb.message.answer_photo(
            task.photo_url,
            caption="🪜 <b>Керована практика</b> — опишемо фото по кроках, наприкінці запишеш усе голосом.",
        )
    else:
        await cb.message.answer(
            "🪜 <b>Керована практика</b> — пройдемо по кроках, а наприкінці складеш усе "
            "разом і запишеш голосом.\n\n"
            f"🎭 <b>Завдання:</b>\n{html.escape(task.prompt)}"
        )
    await cb.message.answer(guidance.guided_speak_step(task.kind, 0), reply_markup=cancel_kb())


@router.message(Guided.active, F.text, ~F.text.startswith("/"))
async def on_guided_step(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    kind = data.get("kind", "sytuacja")
    step = int(data.get("step", 0))
    lines = list(data.get("lines", []))
    task_id = data.get("task_id", "")
    if len(message.text.strip()) < 2:
        await message.answer("Напиши, будь ласка, повноцінну репліку польською 🙂")
        return
    lines.append(message.text.strip())
    step += 1
    if step < guidance.guided_speak_n(kind):
        await state.update_data(step=step, lines=lines)
        await message.answer("✅ Прийнято.")
        await message.answer(guidance.guided_speak_step(kind, step), reply_markup=cancel_kb())
        return

    await state.clear()
    dialogue = "\n".join(f"{i + 1}. {html.escape(ln)}" for i, ln in enumerate(lines))
    kb = InlineKeyboardBuilder()
    kb.button(text="🎤 Виконати самостійно й здати", callback_data=f"guided:record:{task_id}")
    kb.button(text="🏠 Меню", callback_data="menu:home")
    kb.adjust(1)
    await message.answer(
        "🎉 <b>Готово!</b> Ось твоя репліка з 5 кроків:\n\n"
        f"{dialogue}\n\n"
        "ℹ️ Це <b>тренування</b> — у готовність не зараховується (на іспиті підказок не буде). "
        "Щоб підняти готовність — <b>запиши це саме голосом</b> самостійно 👇",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("guided:record:"))
async def cb_guided_record(cb: CallbackQuery, state: FSMContext) -> None:
    task_id = cb.data.split(":", 2)[2]
    task = speaking.task_by_id(task_id)
    await cb.answer()
    if task is None:
        await cb.message.answer("Завдання загубилось — /mowienie")
        return
    await state.set_state(Speaking.waiting)
    await state.update_data(task_id=task_id)
    if task.kind == "opis" and task.photo_url:
        await cb.message.answer_photo(
            task.photo_url,
            caption=(
                "🎤 Тепер опиши це фото <b>голосом</b> самостійно.\n"
                "Оціню за офіційними критеріями — і це піде в прогрес."
            ),
            reply_markup=cancel_kb(),
        )
    else:
        await cb.message.answer(
            f"🎤 Запиши <b>голосове</b> польською за завданням:\n\n{html.escape(task.prompt)}\n\n"
            "Оціню за офіційними критеріями — і це піде в прогрес.",
            reply_markup=cancel_kb(),
        )


@router.message(Speaking.waiting, F.voice)
async def on_voice(message: Message, state: FSMContext) -> None:
    # Ліміти на розмір/тривалість — до завантаження й транскрипції (лишаємось у waiting для повтору)
    if (message.voice.duration or 0) > MAX_VOICE_SEC:
        await message.answer(
            f"🎤 Голосове задовге (максимум {MAX_VOICE_SEC} с). "
            "Для мовлення B1 достатньо 30–90 секунд — запиши коротше 🙂"
        )
        return
    if (message.voice.file_size or 0) > MAX_VOICE_BYTES:
        await message.answer("🎤 Файл завеликий. Запиши коротше голосове (30–90 секунд).")
        return
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
        await limits.refund_ai(message.from_user.id)  # виклик не вдався — не палимо квоту
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
    if c := await goals.pop_celebration(message.from_user.id):
        await message.answer(c)


@router.message(Speaking.waiting, F.text, ~F.text.startswith("/"))
async def on_text_instead(message: Message) -> None:
    await message.answer(
        "🎤 Надішли саме <b>голосове</b> повідомлення (натисни й утримуй мікрофон).\n"
        "Передумав? Тисни 🚫 Скасувати.",
        reply_markup=cancel_kb(),
    )
