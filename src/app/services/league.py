"""Тижнева ліга XP — глобальний рейтинг усіх учнів за XP цього тижня (Duolingo-механіка).

Скидається щопонеділка (ключ за ISO-тижнем + TTL). Redis sorted-set: ZINCRBY при кожному
нарахуванні XP, ZREVRANGE для топу, ZREVRANK для позиції — масштабується без сканування.
Приватність: чужі бачать НЕ @username, а стабільний анонімний аліас (без PII).
"""

from __future__ import annotations

from typing import cast

from redis.asyncio import Redis

from app.config import settings
from app.services import clock

_redis: Redis | None = None
TOP_N = 10

# анонімні аліаси (польський колорит) — стабільні per-uid, без персональних даних
_ADJ = ["Szybki", "Mądry", "Dzielny", "Wesoły", "Sprytny", "Uparty", "Cichy", "Zwinny",
        "Waleczny", "Bystry", "Śmiały", "Pilny"]
_NOUN = ["Żubr", "Bocian", "Orzeł", "Sokół", "Ryś", "Jeż", "Borsuk", "Wilk",
         "Zając", "Łoś", "Dzik", "Kot"]


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key() -> str:
    y, w, _ = clock.today_local().isocalendar()
    return f"polski:league:{y}-{w:02d}"


def alias(user_id: int) -> str:
    """Стабільний анонімний нік (напр. «Szybki Bocian»). Той самий для одного uid."""
    a = _ADJ[user_id % len(_ADJ)]
    n = _NOUN[(user_id // len(_ADJ)) % len(_NOUN)]
    return f"{a} {n}"


def days_to_reset() -> int:
    """Скільки днів до скидання ліги (наступний понеділок)."""
    return 7 - clock.today_local().weekday()


async def add_xp(user_id: int, xp: int) -> None:
    """Додати XP цього тижня (викликається з goals.add ЛИШЕ для учнів, xp>0)."""
    if xp <= 0:
        return
    key = _key()
    await _r().zincrby(key, xp, str(user_id))
    await _r().expire(key, 9 * 24 * 3600)  # переживає тиждень, самоскидається


async def forget(user_id: int) -> None:
    """Прибрати користувача з ліги (ст.17 / canary-cleanup). Ключ per-тиждень + TTL,
    але видаляємо явно з поточного тижня, бо uid — MEMBER, не в назві ключа."""
    await _r().zrem(_key(), str(user_id))


async def top(n: int = TOP_N) -> list[tuple[int, int]]:
    """Топ-N цього тижня: [(uid, xp)] за спаданням XP."""
    raw = cast("list[tuple[str, float]]", await _r().zrevrange(_key(), 0, n - 1, withscores=True))
    return [(int(uid), int(score)) for uid, score in raw]


async def rank_of(user_id: int) -> tuple[int | None, int]:
    """(rank 1-based або None якщо ще без XP, xp) для користувача."""
    r = _r()
    rk = cast("int | None", await r.zrevrank(_key(), str(user_id)))
    sc = cast("float | None", await r.zscore(_key(), str(user_id)))
    return (None if rk is None else rk + 1), int(sc or 0)


_MEDALS = ("🥇", "🥈", "🥉")


def render(rows: list[tuple[int, int]], me_id: int, me_rank: int | None, me_xp: int) -> str:
    """Екран ліги: топ + твоя позиція + дні до скидання."""
    if not rows:
        return (
            "🏆 <b>Ліга тижня</b>\n\n"
            "Цього тижня ще ніхто не набрав XP. Зроби вправу — і очолиш рейтинг! 💪"
        )
    lines = [
        "🏆 <b>Ліга тижня</b>",
        f"<i>Рейтинг за XP цього тижня. До скидання: {days_to_reset()} дн.</i>\n",
    ]
    in_top = False
    for i, (uid, xp) in enumerate(rows):
        rank = i + 1
        mark = _MEDALS[rank - 1] if rank <= 3 else f"{rank}."
        if uid == me_id:
            lines.append(f"{mark} <b>{alias(uid)} — {xp} XP ← ти</b>")
            in_top = True
        else:
            lines.append(f"{mark} {alias(uid)} — {xp} XP")
    if not in_top:  # користувач поза топом — показуємо його позицію окремо
        lines.append("…")
        pos = f"{me_rank}." if me_rank else "—"
        lines.append(f"{pos} <b>{alias(me_id)} — {me_xp} XP ← ти</b>")
    return "\n".join(lines)
