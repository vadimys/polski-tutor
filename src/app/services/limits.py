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


def _key(user_id: int) -> str:
    return f"polski:ai:{user_id}:{clock.today_local().isoformat()}"


async def allow_ai(user_id: int) -> bool:
    """True, якщо користувач ще в межах денного ліміту AI (інкрементує лічильник)."""
    if settings.admin_id and user_id == settings.admin_id:
        return True
    r = _r()
    n = await r.incr(_key(user_id))
    if n == 1:
        await r.expire(_key(user_id), 90_000)  # ~25 год — самоскидання щодоби
    return n <= settings.ai_daily_limit


async def refund_ai(user_id: int) -> None:
    """Повернути юніт квоти, якщо AI-виклик не вдався (щоб фейл не палив ліміт)."""
    if settings.admin_id and user_id == settings.admin_id:
        return
    r = _r()
    raw = await r.get(_key(user_id))
    if raw and int(raw) > 0:
        await r.decr(_key(user_id))
