"""Тижнева квота на «Розмову з екзаменатором» — захист тонкої маржі.

Повна розмова = ~7 AI-викликів (діалог Haiku + оцінка Sonnet) ≈ $0.05-0.07, тож
щоденні розмови зʼїли б 40-50% нетто-виручки підписки. Обмежуємо: підписник ~3/тиждень
(~18-23% виручки — прийнятно), trial — 1 пробна/тиждень. Це ОКРЕМИЙ лічильник (не
loкальний ліміт 30 AI/день, який стосується звичайних дрилів).
"""

from __future__ import annotations

from redis.asyncio import Redis

from app.config import settings
from app.services import clock

WEEKLY_SUB = 3  # розмов/тиждень для підписників
WEEKLY_TRIAL = 1  # для trial — 1 пробна, щоб відчути killer-фічу

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(user_id: int) -> str:
    y, w, _ = clock.today_local().isocalendar()
    return f"sim:week:{user_id}:{y}-{w:02d}"


async def _limit(user_id: int) -> int:
    from app.services import billing

    return WEEKLY_SUB if await billing.has_payments(user_id) else WEEKLY_TRIAL


async def used(user_id: int) -> int:
    v = await _r().get(_key(user_id))
    return int(v) if v else 0


async def remaining(user_id: int) -> int:
    return max(0, await _limit(user_id) - await used(user_id))


async def consume(user_id: int) -> None:
    """Списати одну розмову (на СТАРТІ розмови, не за кожну репліку). TTL ~9 днів."""
    key = _key(user_id)
    await _r().incr(key)
    await _r().expire(key, 9 * 24 * 3600)
