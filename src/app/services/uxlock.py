"""Короткочасний per-user лок для повільних стартів (антидубль команд, що генерують
контент). Приклад: юзер нетерпляче тисне /sluchanie, потім меню — щоб не стартувати
дві вправи одночасно, беремо лок на час підготовки."""

from __future__ import annotations

from redis.asyncio import Redis

from app.config import settings

_redis: Redis | None = None


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
