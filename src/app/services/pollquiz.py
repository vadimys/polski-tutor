"""Нативні quiz-poll Telegram для коротких MCQ.

Стан сесії зберігаємо в Redis за poll_id, бо відповідь приходить окремим апдейтом
(poll_answer) без FSM. Кожне питання — окремий quiz-poll; після відповіді рушій
надсилає наступний або фіналізує.

Ліміти Telegram: питання ≤300, варіант ≤100, пояснення ≤200, 2–10 варіантів.
Якщо контент не вкладається (довгі тексти читання) — fits() поверне False, і
викличний код лишиться на інлайн-кнопках.
"""

from __future__ import annotations

import json
from typing import Any

from aiogram import Bot
from aiogram.types import InputPollOption
from redis.asyncio import Redis

from app.config import settings

_TTL = 3600
_Q_MAX, _OPT_MAX, _EXPL_MAX = 290, 100, 200  # 290: лишаємо запас під префікс «N/total ·»

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(poll_id: str) -> str:
    return f"pollquiz:{poll_id}"


def fits(items: list[dict[str, Any]]) -> bool:
    """Чи всі елементи вкладаються в ліміти Telegram quiz-poll."""
    for it in items:
        if len(str(it.get("q", ""))) > _Q_MAX:
            return False
        opts = it.get("opts", [])
        if not (2 <= len(opts) <= 10):
            return False
        if any(len(str(o)) > _OPT_MAX for o in opts):
            return False
        if not (0 <= int(it.get("correct", -1)) < len(opts)):
            return False
    return True


async def send_item(bot: Bot, session: dict[str, Any]) -> None:
    """Надсилає quiz-poll для поточного item і зберігає контекст під його poll_id."""
    item = session["items"][session["idx"]]
    total = len(session["items"])
    question = f"{session['idx'] + 1}/{total} · {item['q']}"
    explanation = (item.get("explain") or "").strip()[:_EXPL_MAX] or None
    msg = await bot.send_poll(
        session["chat_id"],
        question=question[:300],
        options=[InputPollOption(text=str(o)[:_OPT_MAX]) for o in item["opts"]],
        type="quiz",
        correct_option_id=int(item["correct"]),
        explanation=explanation,
        is_anonymous=False,
    )
    await _r().set(_key(msg.poll.id), json.dumps(session), ex=_TTL)


async def start(
    bot: Bot,
    *,
    chat_id: int,
    user_id: int,
    kind: str,
    items: list[dict[str, Any]],
    module: str | None = None,
    title: str = "",
) -> None:
    if not items:
        return
    session = {
        "kind": kind,
        "module": module,
        "title": title,
        "items": items,
        "idx": 0,
        "correct": 0,
        "user_id": user_id,
        "chat_id": chat_id,
    }
    await send_item(bot, session)


async def pop(poll_id: str) -> dict[str, Any] | None:
    """Забрати контекст сесії за poll_id (і видалити його — відповідь одноразова)."""
    r = _r()
    raw = await r.get(_key(poll_id))
    if raw is None:
        return None
    await r.delete(_key(poll_id))
    return json.loads(raw)
