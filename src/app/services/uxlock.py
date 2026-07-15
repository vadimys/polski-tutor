"""Короткочасний per-user лок для повільних стартів (антидубль команд, що генерують
контент). Приклад: юзер нетерпляче тисне /sluchanie, потім меню — щоб не стартувати
дві вправи одночасно, беремо лок на час підготовки."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager, suppress

from aiogram import Bot
from redis.asyncio import Redis

from app.config import settings

_redis: Redis | None = None


async def _keepalive(bot: Bot, chat_id: int, action: str) -> None:
    """Тримати індикатор дії (typing/record_voice/upload_document) доки триває повільна
    операція — оновлюємо кожні 4с (Telegram сам гасить статус ~через 5с)."""
    with suppress(asyncio.CancelledError, Exception):
        while True:
            await bot.send_chat_action(chat_id, action)
            await asyncio.sleep(4)


@asynccontextmanager
async def typing(bot: Bot, chat_id: int, action: str = "typing"):
    """`async with uxlock.typing(bot, chat_id): <повільна операція>` — весь час показує
    «пише…/записує…», щоб не виглядало як зависання."""
    task = asyncio.create_task(_keepalive(bot, chat_id, action))
    try:
        yield
    finally:
        task.cancel()


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def acquire(key: str, ttl: int = 40) -> bool:
    """True — лок узято щойно (можна працювати). False — вже зайнято (дубль)."""
    try:
        return bool(await _r().set(f"uxlock:{key}", "1", nx=True, ex=ttl))
    except Exception:  # noqa: BLE001 — Redis лежить → не блокуємо користувача
        return True


async def release(key: str) -> None:
    try:
        await _r().delete(f"uxlock:{key}")
    except Exception:  # noqa: BLE001
        pass
