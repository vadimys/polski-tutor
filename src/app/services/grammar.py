"""Прогрес розділу «Граматика» — окремий від готовності до B1.

Зберігаємо лише множину пройдених уроків у Redis (grammar:done:<uid>). Навчання тут
самодостатнє: не рухає B1-готовність/XP/серію — це чистий курс для розуміння мови.
"""

from __future__ import annotations

from redis.asyncio import Redis

from app import grammar
from app.config import settings

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(uid: int) -> str:
    return f"grammar:done:{uid}"


async def mark_done(uid: int, lesson_id: str) -> None:
    await _r().sadd(_key(uid), lesson_id)


async def done_set(uid: int) -> set[str]:
    return {str(x) for x in await _r().smembers(_key(uid))}


async def is_done(uid: int, lesson_id: str) -> bool:
    return bool(await _r().sismember(_key(uid), lesson_id))


def module_progress(done: set[str], module: grammar.Module) -> tuple[int, int]:
    """(пройдено, усього) уроків модуля — чиста функція (тестується)."""
    total = len(module.lessons)
    got = sum(1 for ls in module.lessons if ls.id in done)
    return got, total


def overall_pct(done: set[str]) -> int:
    ids = grammar.all_lesson_ids()
    return round(len([i for i in ids if i in done]) / len(ids) * 100) if ids else 0
