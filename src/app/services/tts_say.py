"""Реєстр «озвуч це» для кнопок 🔊 Послухати.

callback_data обмежений 64 байтами — польську фразу туди не покласти. Тому текст
стешимо в Redis під коротким id (хеш тексту), а кнопка несе лише id. Після першого
озвучення кешуємо Telegram file_id — повторний тап миттєвий, без повторної генерації.
"""

from __future__ import annotations

import hashlib
from contextlib import suppress

from aiogram import Bot
from redis.asyncio import Redis

from app.config import settings

_redis: Redis | None = None
_TTL = 30 * 24 * 3600  # 30 днів — кнопка живе в старому повідомленні


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


async def get_file_id(sid: str) -> str | None:
    return _as_str(await _r().get(f"polski:say:fid:{sid}"))


async def set_file_id(sid: str, file_id: str) -> None:
    await _r().set(f"polski:say:fid:{sid}", file_id, ex=_TTL)


async def lock(sid: str) -> bool:
    """Взяти лок на генерацію (анти-дубль подвійного тапу). True — узято щойно."""
    return bool(await _r().set(f"polski:say:lock:{sid}", "1", nx=True, ex=30))


async def unlock(sid: str) -> None:
    await _r().delete(f"polski:say:lock:{sid}")


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
