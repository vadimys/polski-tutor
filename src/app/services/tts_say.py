"""Реєстр «озвуч це» для кнопок 🔊 Послухати.

callback_data обмежений 64 байтами — польську фразу туди не покласти. Тому текст
стешимо в Redis під коротким id (хеш тексту), а кнопка несе лише id. Після першого
озвучення кешуємо Telegram file_id — повторний тап миттєвий, без повторної генерації.
"""

from __future__ import annotations

import hashlib
from contextlib import suppress

from aiogram import Bot
from aiogram.types import BufferedInputFile, Message
from redis.asyncio import Redis

from app.config import settings

_redis: Redis | None = None
_TTL = 365 * 24 * 3600  # 12 міс — вимова кешується надовго (Azure F0-ліміт майже не витрачається)
_FID_VER = "5"  # бамп → ігноруємо старий кеш file_id (додано варіант темпу «повільніше»)


def _tag(slow: bool) -> str:
    return "s" if slow else "n"  # нормальний / сповільнений темп — окремі file_id


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def sid_for(text: str) -> str:
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:14]  # noqa: S324 (не крипто)


async def stash(text: str) -> str:
    """Зберегти текст для озвучення, повернути короткий id для callback_data."""
    text = text.strip()
    sid = sid_for(text)
    await _r().set(f"polski:say:txt:{sid}", text, ex=_TTL)
    return sid


def _as_str(v: object) -> str | None:
    if v is None:
        return None
    return v.decode() if isinstance(v, bytes) else str(v)


async def fetch(sid: str) -> str | None:
    return _as_str(await _r().get(f"polski:say:txt:{sid}"))


async def get_file_id(sid: str, *, slow: bool = False) -> str | None:
    return _as_str(await _r().get(f"polski:say:fid:{_FID_VER}:{_tag(slow)}:{sid}"))


async def set_file_id(sid: str, file_id: str, *, slow: bool = False) -> None:
    await _r().set(f"polski:say:fid:{_FID_VER}:{_tag(slow)}:{sid}", file_id, ex=_TTL)


async def send_voice(
    bot: Bot, chat_id: int, text: str, *, caption: str | None = None,
    filename: str = "audio.ogg", slow: bool = False, reply_markup=None,  # noqa: ANN001
) -> Message | None:
    """Надіслати озвучення тексту з кешем file_id: синтез (Azure/piper) РАЗ, далі всі
    покази — миттєво з Telegram за file_id (жодних повторних викликів TTS). Для фіксованого
    аудіо (аудіювання/діалоги) — тримає витрату Azure обмеженою. slow=True → сповільнений
    темп (окремий кеш). None → синтез не вдався."""
    sid = sid_for(text)
    fid = await get_file_id(sid, slow=slow)
    if fid:
        with suppress(Exception):
            return await bot.send_voice(chat_id, fid, caption=caption, reply_markup=reply_markup)
        # file_id протух → ре-синтез нижче
    from app.integrations import tts
    from app.services import uxlock

    # живий індикатор «записую аудіо…» на весь час синтезу (щоб не виглядало як зависання)
    async with uxlock.typing(bot, chat_id, "record_voice"):
        data = await tts.synthesize(text, slow=slow)
    if not data:
        return None
    msg = await bot.send_voice(
        chat_id, BufferedInputFile(data, filename=filename), caption=caption,
        reply_markup=reply_markup,
    )
    if msg and msg.voice:
        await set_file_id(sid, msg.voice.file_id, slow=slow)
    return msg


async def lock(sid: str, *, slow: bool = False) -> bool:
    """Взяти лок на генерацію (анти-дубль подвійного тапу). True — узято щойно."""
    return bool(await _r().set(f"polski:say:lock:{_tag(slow)}:{sid}", "1", nx=True, ex=30))


async def unlock(sid: str, *, slow: bool = False) -> None:
    await _r().delete(f"polski:say:lock:{_tag(slow)}:{sid}")


# --- «одне голосове за раз»: попереднє прибираємо, щоб не накопичувались ---


async def forget_voice(bot: Bot, chat_id: int) -> None:
    """Видалити попереднє озвучене голосове в цьому чаті (якщо було)."""
    key = f"polski:say:msg:{chat_id}"
    mid = await _r().get(key)
    if mid:
        with suppress(Exception):
            await bot.delete_message(chat_id, int(mid))
        await _r().delete(key)


async def remember_voice(chat_id: int, message_id: int) -> None:
    await _r().set(f"polski:say:msg:{chat_id}", str(message_id), ex=3600)
