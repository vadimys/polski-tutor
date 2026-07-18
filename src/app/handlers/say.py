"""🔊 Послухати — озвучення слова/фрази польською (piper TTS).

Кнопка несе короткий id (див. services/tts_say). Перший тап: синтез piper →
send_voice + кеш file_id. Наступні тапи: миттєвий send_voice за file_id.
"""

from __future__ import annotations

import html
import os
import tempfile
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from app.config import settings
from app.integrations import speech, tts
from app.services import tts_say

router = Router()


def _speed_kb(sid: str, *, slow: bool) -> InlineKeyboardMarkup:
    """Перемикач темпу під голосовим: нормальний ↔ повільніший (для навчання)."""
    if slow:
        btn = InlineKeyboardButton(text="🐇 Звичайна швидкість", callback_data=f"say:{sid}")
    else:
        btn = InlineKeyboardButton(text="🐢 Повільніше", callback_data=f"say:slow:{sid}")
    return InlineKeyboardMarkup(inline_keyboard=[[btn]])


@router.message(Command("tts"))
async def cmd_tts(message: Message) -> None:
    """Адмін-діагностика вимови: синтез piper + звірка через Whisper (що РЕАЛЬНО звучить).
    Показує й код-поінти вводу (щоб зловити комбіновані діакритики). /tts <текст>"""
    if message.from_user.id != settings.admin_id:
        return
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Використання: <code>/tts &lt;текст&gt;</code>")
        return
    txt = parts[1].strip()
    if not tts.available():
        await message.answer("TTS недоступний.")
        return
    data = await tts.synthesize(txt)
    if not data:
        await message.answer("Синтез не вдався 😔")
        return
    codes = " ".join(f"U+{ord(c):04X}" for c in txt)
    await message.answer_voice(
        BufferedInputFile(data, filename="tts.ogg"),
        caption=f"🔊 <b>{html.escape(txt)}</b>\n<code>{codes}</code>",
    )
    if speech.available():  # прогнати власним Whisper — що реально вимовлено
        fd, p = tempfile.mkstemp(suffix=".ogg")
        os.close(fd)
        try:
            with open(p, "wb") as f:
                f.write(data)
            heard = await speech.transcribe(p)
        finally:
            with suppress(OSError):
                os.remove(p)
        await message.answer(f"🎧 Whisper почув: «{html.escape(heard) or '—'}»")


@router.callback_query(F.data.startswith("say:slow:"))
async def cb_say_slow(cb: CallbackQuery) -> None:
    await _send_say(cb, cb.data.split(":", 2)[2], slow=True)


@router.callback_query(F.data.startswith("say:") & ~F.data.startswith("say:slow:"))
async def cb_say(cb: CallbackQuery) -> None:
    await _send_say(cb, cb.data.split(":", 1)[1], slow=False)


async def _send_say(cb: CallbackQuery, sid: str, *, slow: bool) -> None:
    """Надіслати озвучення тексту (нормальний/повільний темп) із перемикачем швидкості."""
    kb = _speed_kb(sid, slow=slow)

    # уже озвучували в цьому темпі — відправляємо миттєво за кешованим file_id
    fid = await tts_say.get_file_id(sid, slow=slow)
    if fid:
        await cb.answer()
        await tts_say.forget_voice(cb.bot, cb.message.chat.id)  # прибрати попереднє
        with suppress(Exception):
            msg = await cb.message.answer_voice(fid, reply_markup=kb)
            await tts_say.remember_voice(cb.message.chat.id, msg.message_id)
        return

    text = await tts_say.fetch(sid)
    if not text:
        await cb.answer("Аудіо застаріло — відкрий розділ ще раз 🙂", show_alert=True)
        return
    if not tts.available():
        await cb.answer("Озвучення тимчасово недоступне", show_alert=True)
        return

    # анти-дубль: якщо озвучення вже готується (подвійний тап) — не генеруємо вдруге
    if not await tts_say.lock(sid, slow=slow):
        await cb.answer("⏳ Аудіо вже готується…")
        return

    await cb.answer("🐢 Готую повільне аудіо…" if slow else "🔊 Готую аудіо…")
    try:
        with suppress(Exception):  # видимий індикатор «надсилає голосове…» у чаті
            await cb.bot.send_chat_action(cb.message.chat.id, "upload_voice")
        data = await tts.synthesize(text, slow=slow)
        if not data:
            await cb.message.answer("Не вдалось озвучити 😔 Спробуй ще раз.")
            return
        await tts_say.forget_voice(cb.bot, cb.message.chat.id)  # прибрати попереднє
        msg = await cb.message.answer_voice(BufferedInputFile(data, filename="say.ogg"), reply_markup=kb)
        if msg.voice:  # закешувати file_id для миттєвого повтору
            await tts_say.set_file_id(sid, msg.voice.file_id, slow=slow)
        await tts_say.remember_voice(cb.message.chat.id, msg.message_id)
    finally:
        await tts_say.unlock(sid, slow=slow)
