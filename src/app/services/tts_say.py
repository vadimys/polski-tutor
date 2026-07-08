"""Реєстр «озвуч це» для кнопок 🔊 Послухати.

callback_data обмежений 64 байтами — польську фразу туди не покласти. Тому текст
стешимо в Redis під коротким id (хеш тексту), а кнопка несе лише id. Після першого
озвучення кешуємо Telegram file_id — повторний тап миттєвий, без повторної генерації.
"""

from __future__ import annotations

import hashlib

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


async def fetch(sid: str) -> str | None:
    return await _r().get(f"polski:say:txt:{sid}")


async def get_file_id(sid: str) -> str | None:
    return await _r().get(f"polski:say:fid:{sid}")


async def set_file_id(sid: str, file_id: str) -> None:
    await _r().set(f"polski:say:fid:{sid}", file_id, ex=_TTL)
