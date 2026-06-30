"""Персистенція стану учня в Redis (JSON-документ на користувача)."""

from __future__ import annotations

import json
from dataclasses import asdict, fields

from redis.asyncio import Redis

from app.config import settings
from app.domain.models import UserState

_redis: Redis | None = None
USERS_KEY = "polski:users"  # множина всіх user_id (для планувальника)


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(user_id: int) -> str:
    return f"polski:user:{user_id}"


async def load(user_id: int) -> UserState:
    """Стан користувача; новий — з дефолтами (година уроку з конфігу)."""
    raw = await _r().get(_key(user_id))
    if not raw:
        return UserState(user_id=user_id, lesson_hour=settings.lesson_hour)
    data = json.loads(raw)
    known = {f.name for f in fields(UserState)}
    return UserState(**{k: v for k, v in data.items() if k in known})


async def save(state: UserState) -> None:
    await _r().set(_key(state.user_id), json.dumps(asdict(state), ensure_ascii=False))
    await _r().sadd(USERS_KEY, state.user_id)


async def all_user_ids() -> list[int]:
    ids = await _r().smembers(USERS_KEY)
    return [int(i) for i in ids]
