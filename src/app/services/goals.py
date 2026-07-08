"""Денна ціль навчання у хвилинах + серія днів її досягнення.

Час не міряємо секундоміром — оцінюємо за завершеними активностями (кожна має
типову тривалість). Стан у Redis (як limits.py): лічильник хвилин на день + прапорці
«ціль виконано» по датах (для серії). Ціль (налаштування) — теж у Redis.
"""

from __future__ import annotations

from datetime import timedelta

from redis.asyncio import Redis

from app.config import settings
from app.services import clock

_redis: Redis | None = None

DEFAULT_GOAL = 15  # хв/день за замовчуванням
GOAL_CHOICES = (10, 20, 30)  # легко / норм / інтенсив

# оцінка тривалості активності (хв) — груба, для відчуття прогресу
MODULE_MIN = {"pisanie": 12, "mowienie": 8, "sluchanie": 7, "czytanie": 5, "gramatyka": 5}
LESSON_MIN = 10
REVIEW_MIN = 5

_MIN_TTL = 3 * 24 * 3600  # лічильник хвилин живе кілька днів
_MET_TTL = 45 * 24 * 3600  # прапорці «ціль виконано» — щоб рахувати серію назад


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _today() -> str:
    return clock.today_local().isoformat()


async def get_goal(user_id: int) -> int:
    v = await _r().get(f"polski:goal:{user_id}")
    return int(v) if v else DEFAULT_GOAL


async def set_goal(user_id: int, minutes: int) -> None:
    await _r().set(f"polski:goal:{user_id}", int(minutes))


async def today_minutes(user_id: int) -> int:
    v = await _r().get(f"polski:min:{user_id}:{_today()}")
    return int(v) if v else 0


async def current_streak(user_id: int) -> int:
    """Скільки днів поспіль (до сьогодні) виконано денну ціль. Сьогодні ще без цілі
    не рве серію — рахуємо від учора."""
    r = _r()
    today = clock.today_local()
    d = today
    if not await r.get(f"polski:goalmet:{user_id}:{today.isoformat()}"):
        d = today - timedelta(days=1)  # сьогодні ще не виконано — серія «жива» від учора
    n = 0
    while await r.get(f"polski:goalmet:{user_id}:{d.isoformat()}"):
        n += 1
        d -= timedelta(days=1)
    return n


async def add(user_id: int, minutes: int) -> dict:
    """Зарахувати активність. Повертає {today, goal, reached_now, streak}."""
    r = _r()
    key = f"polski:min:{user_id}:{_today()}"
    prev = int(await r.get(key) or 0)
    total = int(await r.incrby(key, minutes))
    if prev == 0:
        await r.expire(key, _MIN_TTL)
    goal = await get_goal(user_id)
    reached_now = prev < goal <= total
    if reached_now:
        await r.set(f"polski:goalmet:{user_id}:{_today()}", "1", ex=_MET_TTL)
    return {
        "today": total,
        "goal": goal,
        "reached_now": reached_now,
        "streak": await current_streak(user_id),
    }


async def record_module(user_id: int, module_value: str) -> dict:
    return await add(user_id, MODULE_MIN.get(module_value, 5))


async def status(user_id: int) -> dict:
    """{today, goal, done, streak} — для показу без зарахування."""
    today = await today_minutes(user_id)
    goal = await get_goal(user_id)
    return {
        "today": today,
        "goal": goal,
        "done": today >= goal,
        "streak": await current_streak(user_id),
    }
