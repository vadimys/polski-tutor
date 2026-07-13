"""Легкий трекінг використання фіч (Redis-лічильники) — для адмін-аналітики.

Жодного контенту повідомлень — лише НАЗВА фічі (команда / префікс callback) +
скільки разів і скільки унікальних користувачів. Дешево, переживає рестарт (volume).
Адмін у трекінг не потрапляє (щоб не спотворювати статистику тестами).
"""

from __future__ import annotations

from redis.asyncio import Redis

from app.config import settings

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def feature_of(raw: str) -> str | None:
    """Нормалізує подію у назву фічі: '/lekcja' → 'cmd:lekcja', 'lesson:start' → 'cb:lesson'.

    Адмінські (ac:/adm:) і порожні — ігноруємо (None)."""
    raw = (raw or "").strip()
    if not raw:
        return None
    if raw.startswith("/"):
        cmd = raw[1:].split()[0].split("@")[0].lower()
        return f"cmd:{cmd}" if cmd else None
    prefix = raw.split(":")[0]
    if not prefix or prefix in ("ac", "adm"):
        return None
    return f"cb:{prefix}"


async def track(user_id: int, raw: str) -> None:
    feat = feature_of(raw)
    if not feat:
        return
    r = _r()
    await r.incr(f"stat:feat:{feat}")
    await r.sadd(f"stat:featu:{feat}", str(user_id))


async def feature_report() -> list[tuple[str, int, int]]:
    """[(feature, hits, unique_users)] відсортовано за hits (спадно)."""
    r = _r()
    out: list[tuple[str, int, int]] = []
    async for key in r.scan_iter("stat:feat:*"):
        feat = key[len("stat:feat:"):]
        hits = int(await r.get(key) or 0)
        uniq = int(await r.scard(f"stat:featu:{feat}") or 0)
        out.append((feat, hits, uniq))
    return sorted(out, key=lambda x: x[1], reverse=True)
