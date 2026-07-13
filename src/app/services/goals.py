"""Прогресія: денна ціль (хв) + серія + XP/рівні + заморозка стріку.

DURABLE-стан (XP, ціль, заморозки, серія+дата) — у Postgres (User.gamify), щоб не
втратити при flushdb Redis. Ефемерне денне (лічильник хвилин, лічильники активностей
за типом, прапорці «ціль виконано» для тижневої місії, святкування) — у Redis.
Наявні Redis-значення мігруються ліниво при першому доступі.
"""

from __future__ import annotations

import math
from datetime import timedelta

from redis.asyncio import Redis

from app.config import settings
from app.db.base import session_factory
from app.db.models import User
from app.services import clock

_redis: Redis | None = None

DEFAULT_GOAL = 15
GOAL_CHOICES = (10, 20, 30)

MODULE_MIN = {"pisanie": 12, "mowienie": 8, "sluchanie": 7, "czytanie": 5, "gramatyka": 5}
LESSON_MIN = 10
REVIEW_MIN = 5

XP_GRADED_BASE = 10
XP_LESSON = 12
XP_REVIEW = 8

MAX_FREEZE = 2

_MIN_TTL = 3 * 24 * 3600
_MET_TTL = 45 * 24 * 3600  # прапорці «ціль виконано» — лише для тижневої місії

_DEFAULT = {"xp": 0, "goal": DEFAULT_GOAL, "freeze": MAX_FREEZE, "streak": 0, "last": ""}


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _today() -> str:
    return clock.today_local().isoformat()


# --- рівні (чисті функції) ---


def level_start_xp(level: int) -> int:
    return 25 * (level - 1) * level


def level_of(xp: int) -> int:
    return max(1, int((1 + math.isqrt(1 + 4 * xp // 25)) // 2))


# --- durable-стан у Postgres (User.gamify) ---


async def _get(user_id: int) -> dict:
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        g = dict(u.gamify) if (u and u.gamify) else None
    if g is None:
        g = await _migrate_from_redis(user_id)  # перший доступ — забрати старі Redis-значення
    return {**_DEFAULT, **g}


async def _set(user_id: int, g: dict) -> None:
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            u = User(id=user_id, lesson_hour=settings.lesson_hour)
            s.add(u)
        u.gamify = {**_DEFAULT, **g}
        await s.commit()


async def _legacy_streak(user_id: int) -> int:
    """Старий стрік — з goalmet-прапорців Redis (для одноразової міграції)."""
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


async def _migrate_from_redis(user_id: int) -> dict:
    """Забрати наявні XP/ціль/заморозки/серію з Redis у Postgres (одноразово)."""
    r = _r()
    today = clock.today_local()
    goalv = await r.get(f"polski:goal:{user_id}")
    freezev = await r.get(f"polski:freeze:{user_id}")
    last = ""
    if await r.get(f"polski:goalmet:{user_id}:{today.isoformat()}"):
        last = today.isoformat()
    elif await r.get(f"polski:goalmet:{user_id}:{(today - timedelta(days=1)).isoformat()}"):
        last = (today - timedelta(days=1)).isoformat()
    g = {
        "xp": int(await r.get(f"polski:xp:{user_id}") or 0),
        "goal": int(goalv) if goalv else DEFAULT_GOAL,
        "freeze": int(freezev) if freezev is not None else MAX_FREEZE,
        "streak": await _legacy_streak(user_id),
        "last": last,
    }
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is not None:  # для неіснуючого користувача не створюємо запис
            u.gamify = g
            await s.commit()
    return g


async def reset(user_id: int) -> None:
    """Повне обнулення гейміфікації: durable gamify (PG) + денні/легасі лічильники (Redis)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is not None:
            u.gamify = {}
            await s.commit()
    r = _r()
    for pat in (
        f"polski:min:{user_id}:*", f"polski:act:{user_id}:*", f"polski:goalmet:{user_id}:*",
    ):
        async for key in r.scan_iter(pat):
            await r.delete(key)
    await r.delete(
        f"polski:celeb:{user_id}", f"polski:xp:{user_id}",
        f"polski:goal:{user_id}", f"polski:freeze:{user_id}", f"polski:streak:{user_id}",
    )


async def get_goal(user_id: int) -> int:
    return int((await _get(user_id))["goal"])


async def set_goal(user_id: int, minutes: int) -> None:
    g = await _get(user_id)
    g["goal"] = int(minutes)
    await _set(user_id, g)


async def get_xp(user_id: int) -> int:
    return int((await _get(user_id))["xp"])


async def award_bonus_xp(user_id: int, xp: int) -> int:
    g = await _get(user_id)
    g["xp"] = int(g["xp"]) + xp
    await _set(user_id, g)
    return int(g["xp"])


async def get_freeze(user_id: int) -> int:
    return int((await _get(user_id))["freeze"])


async def current_streak(user_id: int) -> int:
    """Серія жива, якщо ціль виконано сьогодні або вчора; інакше 0."""
    g = await _get(user_id)
    today = clock.today_local()
    alive = {today.isoformat(), (today - timedelta(days=1)).isoformat()}
    return int(g["streak"]) if g["last"] in alive else 0


async def maybe_freeze(user_id: int) -> bool:
    """Бридж пропущеного вчора дня заморозкою (виклик раз на день у нагадуванні)."""
    g = await _get(user_id)
    today = clock.today_local()
    y = (today - timedelta(days=1)).isoformat()
    yy = (today - timedelta(days=2)).isoformat()
    if g["last"] == y or g["last"] != yy or int(g["freeze"]) <= 0:
        return False  # учора виконано / не було активної серії / нема заморозки
    g["last"] = y  # день врятовано — серія тягнеться далі
    g["freeze"] = int(g["freeze"]) - 1
    await _set(user_id, g)
    return True


# --- ефемерні денні лічильники (Redis) ---


async def today_minutes(user_id: int) -> int:
    v = await _r().get(f"polski:min:{user_id}:{_today()}")
    return int(v) if v else 0


async def today_count(user_id: int, kinds: list[str]) -> int:
    r = _r()
    total = 0
    for k in kinds:
        v = await r.get(f"polski:act:{user_id}:{_today()}:{k}")
        total += int(v) if v else 0
    return total


async def week_goal_days(user_id: int) -> int:
    r = _r()
    today = clock.today_local()
    n = 0
    for i in range(7):
        if await r.get(f"polski:goalmet:{user_id}:{(today - timedelta(days=i)).isoformat()}"):
            n += 1
    return n


async def _is_teacher(user_id: int) -> bool:
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        return bool(u and u.role == "teacher")


async def add(user_id: int, minutes: int, xp: int, kind: str | None = None) -> dict:
    """Зарахувати активність (хвилини + XP + тип). Оновлює durable-стан і денні лічильники.

    Викладач — превʼю-режим: НЕ нараховуємо XP/серію/місії (як update_readiness)."""
    if await _is_teacher(user_id):
        return await _get(user_id)
    r = _r()
    if kind:
        ak = f"polski:act:{user_id}:{_today()}:{kind}"
        if int(await r.incr(ak)) == 1:
            await r.expire(ak, _MIN_TTL)

    key = f"polski:min:{user_id}:{_today()}"
    prev_min = int(await r.get(key) or 0)
    total_min = int(await r.incrby(key, minutes))
    if prev_min == 0:
        await r.expire(key, _MIN_TTL)

    g = await _get(user_id)
    prev_xp = int(g["xp"])
    g["xp"] = prev_xp + xp
    goal = int(g["goal"])
    reached_now = prev_min < goal <= total_min
    today, tstr = clock.today_local(), _today()
    ystr = (today - timedelta(days=1)).isoformat()
    if reached_now:
        await r.set(f"polski:goalmet:{user_id}:{tstr}", "1", ex=_MET_TTL)  # для тижневої місії
        if g["last"] != tstr:
            g["streak"] = int(g["streak"]) + 1 if g["last"] == ystr else 1
            g["last"] = tstr
            if int(g["streak"]) % 7 == 0:
                g["freeze"] = min(MAX_FREEZE, int(g["freeze"]) + 1)

    level = level_of(int(g["xp"]))
    leveled_up = level > level_of(prev_xp)
    await _set(user_id, g)

    if reached_now or leveled_up:  # відкласти святкування — хендлер покаже після вправи
        parts = []
        if leveled_up:
            parts.append(f"🎉 <b>Новий рівень {level}!</b> ⭐")
        if reached_now:
            parts.append(f"🎯 <b>Денну ціль виконано!</b> 🔥 Серія {g['streak']} дн.")
        await r.set(f"polski:celeb:{user_id}", "\n".join(parts), ex=180)

    return {
        "today": total_min,
        "goal": goal,
        "reached_now": reached_now,
        "streak": int(g["streak"]) if reached_now else await current_streak(user_id),
        "xp": int(g["xp"]),
        "level": level,
        "leveled_up": leveled_up,
    }


async def record_module(user_id: int, module_value: str, score: int | None = None) -> dict:
    xp = XP_GRADED_BASE + (round(score / 10) if score is not None else 0)
    return await add(user_id, MODULE_MIN.get(module_value, 5), xp, kind=module_value)


async def pop_celebration(user_id: int) -> str | None:
    """Забрати відкладене святкування (level-up / ціль виконано), якщо є. Одноразово."""
    r = _r()
    key = f"polski:celeb:{user_id}"
    msg = await r.get(key)
    if msg is None:
        return None
    await r.delete(key)
    return msg.decode() if isinstance(msg, bytes) else str(msg)


async def status(user_id: int) -> dict:
    """Зведення для показу (без зарахування)."""
    g = await _get(user_id)
    today = await today_minutes(user_id)
    goal = int(g["goal"])
    xp = int(g["xp"])
    lvl = level_of(xp)
    return {
        "today": today,
        "goal": goal,
        "done": today >= goal,
        "streak": await current_streak(user_id),
        "xp": xp,
        "level": lvl,
        "to_next": level_start_xp(lvl + 1) - xp,
        "freeze": int(g["freeze"]),
    }
