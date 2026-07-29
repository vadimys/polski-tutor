"""Тренажер дієслів: адаптивний підбір (частіше питає те, де помилявся).

Лічильники помилок — Redis-хеш verbs:wrong:<uid> (field="gi:vi" → к-сть). Правильна
відповідь зменшує лічильник, хибна — збільшує. Підбір — чиста функція (тестується):
до половини сесії — «болючі» дієслова, решта — випадкові. Прогрес B1 не рухає —
це навчальний тренажер, як і курс граматики.
"""

from __future__ import annotations

import random

from redis.asyncio import Redis

from app import verbs
from app.config import settings

_redis: Redis | None = None
DRILL_SIZE = 5


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(uid: int) -> str:
    return f"verbs:wrong:{uid}"


async def record_answer(uid: int, gi: int, vi: int, ok: bool) -> None:
    """Оновити лічильник «болючості» дієслова: помилка +1, успіх −1 (не нижче 0)."""
    field = f"{gi}:{vi}"
    if ok:
        cur = int(await _r().hget(_key(uid), field) or 0)
        if cur <= 1:
            await _r().hdel(_key(uid), field)
        else:
            await _r().hincrby(_key(uid), field, -1)
    else:
        await _r().hincrby(_key(uid), field, 1)


async def wrong_coords(uid: int) -> list[tuple[int, int]]:
    raw = await _r().hgetall(_key(uid))
    out: list[tuple[int, int]] = []
    for f in raw:
        try:
            gi, vi = str(f).split(":")
            out.append((int(gi), int(vi)))
        except ValueError:
            continue
    return out


def pick_drill(
    coords: list[tuple[int, int]],
    wrongs: list[tuple[int, int]],
    k: int = DRILL_SIZE,
    rng: random.Random | None = None,
) -> list[tuple[int, int, int]]:
    """Скласти сесію тренажера: (gi, vi, person). До k//2 — «болючі», решта — випадкові.

    coords — усі доступні (gi, vi); wrongs — де помилявся. Дієслова не повторюються,
    особа (0-5) — випадкова на кожне питання. Чиста функція (rng інʼєктиться в тестах).
    """
    rng = rng or random.Random()
    pool = list(coords)
    chosen: list[tuple[int, int]] = []
    hurt = [c for c in wrongs if c in pool]
    rng.shuffle(hurt)
    for c in hurt[: max(1, k // 2)] if hurt else []:
        chosen.append(c)
        pool.remove(c)
    rng.shuffle(pool)
    chosen += pool[: k - len(chosen)]
    return [(gi, vi, rng.randrange(6)) for gi, vi in chosen]


async def build_drill(uid: int) -> list[tuple[int, int, int]]:
    coords = [(gi, vi) for gi, vi, _ in verbs.all_verbs()]
    return pick_drill(coords, await wrong_coords(uid))
