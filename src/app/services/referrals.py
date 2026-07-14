"""Учнівські реферали (word-of-mouth) — учень запрошує друга (skill referrals).

Окремо від teacher-атрибуції (`User.referred_by`): це учень→друг, зв'язок у Redis.
Double-sided: друг за посиланням `?start=r<uid>` отримує trial, а запрошувач —
бонусні дні доступу, КОЛИ друг оформить підписку (fraud-захист: реальна оплата,
рівно один раз на друга, себе не запросиш).
"""

from __future__ import annotations

from redis.asyncio import Redis

from app.config import settings


def link(bot_username: str, user_id: int) -> str:
    return f"https://t.me/{bot_username}?start=r{user_id}"


def parse(payload: str) -> int | None:
    """`r<digits>` → id запрошувача; інакше None (t/g — не наш префікс)."""
    p = (payload or "").strip()
    if p.startswith("r") and p[1:].isdigit():
        return int(p[1:])
    return None


_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def record_invite(invitee: int, referrer: int) -> None:
    """Зафіксувати, що invitee прийшов від referrer (лише ПЕРШИЙ referrer «прилипає»).
    Лічильник invited інкрементуємо лише коли зв'язок реально закріпився (не завищуємо,
    якщо друг клікнув чуже посилання другим)."""
    if invitee == referrer:
        return
    if await _r().set(f"ref:by:{invitee}", str(referrer), nx=True):
        await _r().sadd(f"ref:inv:{referrer}", str(invitee))


async def on_subscription(invitee: int) -> int | None:
    """Друг оформив підписку → повертає id запрошувача для винагороди (рівно один раз)."""
    raw = await _r().get(f"ref:by:{invitee}")
    if not raw:
        return None
    referrer = int(raw)
    if referrer == invitee:
        return None
    if not await _r().sadd(f"ref:rewok:{referrer}", str(invitee)):
        return None  # цього друга вже зараховано
    return referrer


async def stats(referrer: int) -> dict:
    return {
        "invited": int(await _r().scard(f"ref:inv:{referrer}") or 0),
        "rewarded": int(await _r().scard(f"ref:rewok:{referrer}") or 0),
    }
