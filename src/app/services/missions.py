"""Місії — щоденний виклик (ротація) + тижнева ціль. Нагорода: бонусний XP (раз).

Прогрес рахуємо з лічильників активностей у goals (за типом/днем) і met-прапорців
(тижнева). Виконання нараховує XP один раз (прапорець «claimed» у Redis).
"""

from __future__ import annotations

import hashlib
from typing import TypedDict

from redis.asyncio import Redis

from app.config import settings
from app.services import clock, goals

_redis: Redis | None = None


class DailyMission(TypedDict):
    id: str
    kinds: list[str]
    n: int
    desc: str
    xp: int


class WeeklyMission(TypedDict):
    id: str
    days: int
    desc: str
    xp: int


_ALL_KINDS = ["lesson", "review", "pisanie", "mowienie", "sluchanie", "czytanie", "gramatyka"]

# щоденні місії (детермінована ротація). Прогрес = сума вправ заданих типів за день.
_DAILY: list[DailyMission] = [
    {"id": "lesson", "kinds": ["lesson"], "n": 1, "desc": "📖 Пройди урок дня", "xp": 15},
    {"id": "listen", "kinds": ["sluchanie"], "n": 1, "desc": "🎧 Зроби одне аудіювання", "xp": 15},
    {"id": "write", "kinds": ["pisanie"], "n": 1, "desc": "✍️ Напиши один текст/лист", "xp": 20},
    {"id": "speak", "kinds": ["mowienie"], "n": 1, "desc": "🗣 Дай одну усну відповідь", "xp": 20},
    {"id": "drill", "kinds": ["czytanie", "gramatyka"], "n": 1, "desc": "🎯 Одне тренування", "xp": 15},
    {"id": "review", "kinds": ["review"], "n": 1, "desc": "🔁 Одне повторення слів", "xp": 15},
    {"id": "double", "kinds": _ALL_KINDS, "n": 2, "desc": "💪 Зроби 2 будь-які вправи", "xp": 18},
    {"id": "prod2", "kinds": ["pisanie", "mowienie"], "n": 2,
     "desc": "🗣✍️ 2 продуктивні (письмо/мовлення)", "xp": 28},
    {"id": "listenread", "kinds": ["sluchanie", "czytanie"], "n": 2,
     "desc": "🎧📖 Аудіювання + читання", "xp": 22},
    {"id": "grammar2", "kinds": ["gramatyka"], "n": 2, "desc": "🔤 2 граматичні дрили", "xp": 20},
    {"id": "reviewlesson", "kinds": ["review", "lesson"], "n": 2,
     "desc": "📖🔁 Урок + повторення", "xp": 20},
    {"id": "triple", "kinds": _ALL_KINDS, "n": 3, "desc": "🔥 3 вправи за день", "xp": 30},
]

_WEEKLY: WeeklyMission = {
    "id": "week5", "days": 5, "desc": "🗓 Виконай денну ціль 5 днів цього тижня", "xp": 60
}


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def daily_mission(user_id: int, date_iso: str) -> DailyMission:
    """Детермінована щоденна місія (ротація за user+дата)."""
    h = hashlib.sha1(f"{user_id}:{date_iso}".encode()).hexdigest()  # noqa: S324
    return _DAILY[int(h, 16) % len(_DAILY)]


async def _claim_once(user_id: int, mission_id: str, period: str, xp: int) -> bool:
    """Нарахувати XP один раз за період (day/week). True, якщо нараховано щойно."""
    key = f"polski:miss:{user_id}:{period}:{mission_id}"
    if await _r().set(key, "1", nx=True, ex=8 * 24 * 3600):
        await goals.award_bonus_xp(user_id, xp)
        return True
    return False


async def status(user_id: int) -> dict:
    """{daily: {..., progress, done, claimed_now}, weekly: {...}}. Нараховує XP при виконанні."""
    today = clock.today_local().isoformat()
    week = f"{clock.today_local().isocalendar().year}W{clock.today_local().isocalendar().week}"

    dm = daily_mission(user_id, today)
    dprog = await goals.today_count(user_id, dm["kinds"])
    ddone = dprog >= dm["n"]
    dclaim = await _claim_once(user_id, dm["id"], today, dm["xp"]) if ddone else False

    wprog = await goals.week_goal_days(user_id)
    wdone = wprog >= _WEEKLY["days"]
    wclaim = await _claim_once(user_id, _WEEKLY["id"], week, _WEEKLY["xp"]) if wdone else False

    return {
        "daily": {**dm, "progress": min(dprog, dm["n"]), "done": ddone, "claimed_now": dclaim},
        "weekly": {
            **_WEEKLY, "progress": min(wprog, _WEEKLY["days"]), "done": wdone, "claimed_now": wclaim
        },
    }
