"""Атрибуція джерел трафіку (маркетингові кампанії): звідки прийшов користувач.

`?start=<мітка>`, яка НЕ є рефералом (r/t/g) і схожа на кампанійну мітку
(`fb_wielun`, `flyer`, `ig`…), фіксується як джерело користувача — first-touch
(перше «прилипає»), унікальні. Для реклами: скільки людей прийшло з кожного каналу.
Адміна не рахуємо. Дешево, Redis, переживає рестарт (volume).
"""

from __future__ import annotations

import re

from redis.asyncio import Redis

from app.config import settings

_SRC_RE = re.compile(r"^[a-z0-9_]{2,32}$")
_REF_PREFIX = ("r", "t", "g")  # реферальні payload (r123/t123/g123) — не джерела

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def parse_source(payload: str) -> str | None:
    """payload → нормалізована мітка джерела або None.

    Відсікає порожнє, несхоже на мітку й реферальні payload (r<цифри>/t<…>/g<…>)."""
    p = (payload or "").strip().lower()
    if not _SRC_RE.match(p):
        return None
    if p[0] in _REF_PREFIX and p[1:].isdigit():
        return None
    return p


async def record(user_id: int, payload: str) -> str | None:
    """Зафіксувати джерело користувача (first-touch). Повертає мітку, якщо записано
    вперше, інакше None (уже мав джерело / це не мітка / це адмін)."""
    src = parse_source(payload)
    if src is None or user_id == settings.admin_id:
        return None
    r = _r()
    if await r.set(f"attr:user:{user_id}", src, nx=True):
        await r.sadd(f"attr:src:{src}", str(user_id))
        await r.sadd("attr:sources", src)
        return src
    return None


async def report() -> list[tuple[str, int]]:
    """[(джерело, унікальних користувачів)] спадно за кількістю."""
    r = _r()
    out: list[tuple[str, int]] = []
    for raw in await r.smembers("attr:sources"):
        src = raw.decode() if isinstance(raw, bytes) else str(raw)
        out.append((src, int(await r.scard(f"attr:src:{src}") or 0)))
    return sorted(out, key=lambda x: (-x[1], x[0]))


def link(bot_username: str, source: str) -> str:
    """Веб-лінк із міткою (коли t.me живий)."""
    return f"https://t.me/{bot_username}?start={source}"


def tg_link(bot_username: str, source: str) -> str:
    """Прямий app-лінк із міткою (працює попри падіння t.me)."""
    return f"tg://resolve?domain={bot_username}&start={source}"
