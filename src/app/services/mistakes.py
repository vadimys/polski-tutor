"""Колода помилок: логуємо неправильні відповіді MCQ і даємо їх повторно опрацювати.

Світова практика: цільове повернення до власних помилок закріплює найкраще.
Стан у Redis (hash за user: qhash → item). Дедуп за текстом питання; правильно
відповів у режимі опрацювання → прибираємо з колоди.
"""

from __future__ import annotations

import hashlib
import json

from redis.asyncio import Redis

from app.config import settings

_redis: Redis | None = None
_CAP = 60  # максимум помилок у колоді (щоб не розросталась)


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(user_id: int) -> str:
    return f"polski:mist:{user_id}"


def _qhash(question: str) -> str:
    return hashlib.sha1(question.strip().encode("utf-8")).hexdigest()[:12]  # noqa: S324


async def add(
    user_id: int, module: str, question: str, options: list[str], correct: int, explain: str
) -> None:
    """Записати помилку в колоду (дедуп за питанням, з обмеженням розміру)."""
    r = _r()
    h = _qhash(question)
    if not await r.hexists(_key(user_id), h) and await r.hlen(_key(user_id)) >= _CAP:
        return  # колода повна — не додаємо нових (наявні оновлюються)
    item = json.dumps(
        {"module": module, "q": question, "opts": list(options), "correct": int(correct),
         "explain": explain or ""},
        ensure_ascii=False,
    )
    await r.hset(_key(user_id), h, item)


async def count(user_id: int) -> int:
    return int(await r.hlen(_key(user_id))) if (r := _r()) else 0


async def all_items(user_id: int) -> list[dict]:
    raw = await _r().hgetall(_key(user_id))
    return [{"h": h, **json.loads(v)} for h, v in raw.items()]


async def resolve(user_id: int, qhash: str) -> None:
    """Прибрати помилку з колоди (опрацьована правильно)."""
    await _r().hdel(_key(user_id), qhash)


async def clear(user_id: int) -> None:
    await _r().delete(_key(user_id))
