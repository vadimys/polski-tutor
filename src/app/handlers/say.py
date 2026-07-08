"""🔊 Послухати — озвучення слова/фрази польською (piper TTS).

Кнопка несе короткий id (див. services/tts_say). Перший тап: синтез piper →
send_voice + кеш file_id. Наступні тапи: миттєвий send_voice за file_id.
"""

from __future__ import annotations

from contextlib import suppress

from aiogram import F, Router
from aiogram.types import BufferedInputFile, CallbackQuery

from app.integrations import tts
from app.services import tts_say

router = Router()


@router.callback_query(F.data.startswith("say:"))
async def cb_say(cb: CallbackQuery) -> None:
    sid = cb.data.split(":", 1)[1]

    # уже озвучували — відправляємо миттєво за кешованим file_id
    fid = await tts_say.get_file_id(sid)
    if fid:
        await cb.answer()
        with suppress(Exception):
            await cb.message.answer_voice(fid)
        return

    text = await tts_say.fetch(sid)
    if not text:
        await cb.answer("Аудіо застаріло — відкрий розділ ще раз 🙂", show_alert=True)
        return
    if not tts.available():
        await cb.answer("Озвучення тимчасово недоступне", show_alert=True)
        return

    await cb.answer("🔊 Озвучую…")
    data = await tts.synthesize(text)
    if not data:
        await cb.answer("Не вдалось озвучити 😔", show_alert=True)
        return
    msg = await cb.message.answer_voice(BufferedInputFile(data, filename="say.ogg"))
    if msg and msg.voice:  # закешувати file_id для миттєвого повтору
        await tts_say.set_file_id(sid, msg.voice.file_id)
