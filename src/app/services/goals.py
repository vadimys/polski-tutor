"""Прогресія: денна ціль (хв) + серія + XP/рівні + заморозка стріку. Стан у Redis.

Час не міряємо секундоміром — оцінюємо за завершеними активностями. XP — «валюта»,
що живить рівні й досягнення; денна ціль — у хвилинах. Серія = дні поспіль з виконаною
ціллю (прапорці по датах); заморозка бриджить один пропущений день, якщо є запас.
"""

from __future__ import annotations

import math
from datetime import timedelta

from redis.asyncio import Redis

from app.config import settings
from app.services import clock

_redis: Redis | None = None

DEFAULT_GOAL = 15
GOAL_CHOICES = (10, 20, 30)

# оцінка тривалості активності (хв)
MODULE_MIN = {"pisanie": 12, "mowienie": 8, "sluchanie": 7, "czytanie": 5, "gramatyka": 5}
LESSON_MIN = 10
REVIEW_MIN = 5

# XP за активність
XP_GRADED_BASE = 10  # + бонус за бал (score/10)
XP_LESSON = 12
XP_REVIEW = 8

MAX_FREEZE = 2  # запас «заморозок» стріку

_MIN_TTL = 3 * 24 * 3600
_MET_TTL = 45 * 24 * 3600


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _today() -> str:
    return clock.today_local().isoformat()


# --- рівні ---


def level_start_xp(level: int) -> int:
    """XP, потрібне, щоб ДОСЯГТИ рівня (L≥1): 25·(L-1)·L → L1=0, L2=50, L3=150, L4=300…"""
    return 25 * (level - 1) * level


def level_of(xp: int) -> int:
    """Рівень за сумарним XP (обернене до level_start_xp)."""
    return max(1, int((1 + math.isqrt(1 + 4 * xp // 25)) // 2))


# --- ціль (налаштування) ---


async def get_goal(user_id: int) -> int:
    v = await _r().get(f"polski:goal:{user_id}")
    return int(v) if v else DEFAULT_GOAL


async def set_goal(user_id: int, minutes: int) -> None:
    await _r().set(f"polski:goal:{user_id}", int(minutes))


async def today_minutes(user_id: int) -> int:
    v = await _r().get(f"polski:min:{user_id}:{_today()}")
    return int(v) if v else 0


# --- XP ---


async def get_xp(user_id: int) -> int:
    v = await _r().get(f"polski:xp:{user_id}")
    return int(v) if v else 0


async def award_bonus_xp(user_id: int, xp: int) -> int:
    """Нарахувати XP без хвилин/типу (нагорода за місію тощо). Повертає новий сумарний XP."""
    return int(await _r().incrby(f"polski:xp:{user_id}", xp))


# --- заморозки ---


async def get_freeze(user_id: int) -> int:
    v = await _r().get(f"polski:freeze:{user_id}")
    return int(v) if v is not None else MAX_FREEZE


async def _set_freeze(user_id: int, n: int) -> None:
    await _r().set(f"polski:freeze:{user_id}", max(0, min(MAX_FREEZE, n)))


# --- серія ---


async def current_streak(user_id: int) -> int:
    """Дні поспіль (до сьогодні) з виконаною ціллю. Сьогодні без цілі не рве серію."""
    r = _r()
    today = clock.today_local()
    d = today
    if not await r.get(f"polski:goalmet:{user_id}:{today.isoformat()}"):
        d = today - timedelta(days=1)
    n = 0
    while await r.get(f"polski:goalmet:{user_id}:{d.isoformat()}"):
        n += 1
        d -= timedelta(days=1)
    return n


async def maybe_freeze(user_id: int) -> bool:
    """Бридж пропущеного вчора дня заморозкою (виклик раз на день, у нагадуванні).

    True — заморозку застосовано (серія збережена). Ідемпотентно."""
    r = _r()
    today = clock.today_local()
    y = (today - timedelta(days=1)).isoformat()
    yy = (today - timedelta(days=2)).isoformat()
    if await r.get(f"polski:goalmet:{user_id}:{y}"):
        return False  # учора й так виконано
    if not await r.get(f"polski:goalmet:{user_id}:{yy}"):
        return False  # не було активної серії — нічого рятувати
    freeze = await get_freeze(user_id)
    if freeze <= 0:
        return False
    await r.set(f"polski:goalmet:{user_id}:{y}", "F", ex=_MET_TTL)  # F = день врятовано заморозкою
    await _set_freeze(user_id, freeze - 1)
    return True


# --- зарахування активності ---


async def today_count(user_id: int, kinds: list[str]) -> int:
    """Скільки активностей заданих типів зроблено сьогодні (для місій)."""
    r = _r()
    total = 0
    for k in kinds:
        v = await r.get(f"polski:act:{user_id}:{_today()}:{k}")
        total += int(v) if v else 0
    return total


async def week_goal_days(user_id: int) -> int:
    """Скільки днів денну ціль виконано за останні 7 днів (для тижневої місії)."""
    r = _r()
    today = clock.today_local()
    n = 0
    for i in range(7):
        d = (today - timedelta(days=i)).isoformat()
        if await r.get(f"polski:goalmet:{user_id}:{d}"):
            n += 1
    return n


async def add(user_id: int, minutes: int, xp: int, kind: str | None = None) -> dict:
    """Зарахувати активність (хвилини + XP + тип). Повертає підсумок."""
    r = _r()
    if kind:
        ak = f"polski:act:{user_id}:{_today()}:{kind}"
        if int(await r.incr(ak)) == 1:
            await r.expire(ak, _MIN_TTL)
    prev_xp = await get_xp(user_id)
    new_xp = int(await r.incrby(f"polski:xp:{user_id}", xp))

    key = f"polski:min:{user_id}:{_today()}"
    prev_min = int(await r.get(key) or 0)
    total_min = int(await r.incrby(key, minutes))
    if prev_min == 0:
        await r.expire(key, _MIN_TTL)

    goal = await get_goal(user_id)
    reached_now = prev_min < goal <= total_min
    if reached_now:
        await r.set(f"polski:goalmet:{user_id}:{_today()}", "1", ex=_MET_TTL)
    streak = await current_streak(user_id)
    if reached_now and streak and streak % 7 == 0:  # +заморозка за кожні 7 днів серії
        await _set_freeze(user_id, await get_freeze(user_id) + 1)

    return {
        "today": total_min,
        "goal": goal,
        "reached_now": reached_now,
        "streak": streak,
        "xp": new_xp,
        "level": level_of(new_xp),
        "leveled_up": level_of(new_xp) > level_of(prev_xp),
    }


async def record_module(user_id: int, module_value: str, score: int | None = None) -> dict:
    xp = XP_GRADED_BASE + (round(score / 10) if score is not None else 0)
    return await add(user_id, MODULE_MIN.get(module_value, 5), xp, kind=module_value)


async def status(user_id: int) -> dict:
    """Зведення для показу (без зарахування)."""
    today = await today_minutes(user_id)
    goal = await get_goal(user_id)
    xp = await get_xp(user_id)
    lvl = level_of(xp)
    return {
        "today": today,
        "goal": goal,
        "done": today >= goal,
        "streak": await current_streak(user_id),
        "xp": xp,
        "level": lvl,
        "to_next": level_start_xp(lvl + 1) - xp,
        "freeze": await get_freeze(user_id),
    }
