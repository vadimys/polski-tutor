"""Per-user денний ліміт AI-вправ (контроль витрат на Anthropic).

Лічильник у Redis із добовим TTL. Адмін — без ліміту. Викликати БЕЗПОСЕРЕДНЬО
перед AI-викликом (фідбек письма/мовлення, генерація уроку).
"""

from __future__ import annotations

from redis.asyncio import Redis

from app.config import settings
from app.services import clock

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def allow_ai(user_id: int) -> bool:
    """True, якщо користувач ще в межах денного ліміту AI (інкрементує лічильник)."""
    if settings.admin_id and user_id == settings.admin_id:
        return True
    key = f"polski:ai:{user_id}:{clock.today_local().isoformat()}"
    r = _r()
    n = await r.incr(key)
    if n == 1:
        await r.expire(key, 90_000)  # ~25 год — самоскидання щодоби
    return n <= settings.ai_daily_limit
