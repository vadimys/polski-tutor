"""Запити на повне обнулення прогресу (документовані; виконує лише адмін).

Користувач не може сам обнулити прогрес — лише подати запит із причиною. Запит
зберігається (Redis-хеш) для документації, адмін бачить хто/коли/чому й вирішує.
"""

from __future__ import annotations

from redis.asyncio import Redis

from app.config import settings

_KEY = "reset:reqs"  # hash: field=user_id → "isoDate|reason"
_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def request(user_id: int, reason: str, at: str) -> None:
    await _r().hset(_KEY, str(user_id), f"{at}|{reason}")


async def get(user_id: int) -> tuple[str, str] | None:
    raw = await _r().hget(_KEY, str(user_id))
    if not raw:
        return None
    at, _, reason = str(raw).partition("|")
    return at, reason


async def clear(user_id: int) -> None:
    await _r().hdel(_KEY, str(user_id))


async def pending() -> dict[int, tuple[str, str]]:
    """{user_id: (at, reason)} — усі відкриті запити (для адмін-огляду)."""
    raw = await _r().hgetall(_KEY)
    out: dict[int, tuple[str, str]] = {}
    for k, v in raw.items():
        at, _, reason = str(v).partition("|")
        out[int(k)] = (at, reason)
    return out
