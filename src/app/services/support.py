"""Support-inbox: звернення користувачів (проблема / ідея) з чергою і статусами.

Зберігаємо в Redis-хеші (для одного-кількох користувачів достатньо). Кожен тікет:
{uid, name, cat, text, status, at}. status: new → closed (відповіли/закрили).
"""

from __future__ import annotations

import json

from redis.asyncio import Redis

from app.config import settings

_TICKETS = "support:tickets"
_SEQ = "support:seq"
_CAT = {"problem": "🛠 Проблема", "idea": "💡 Ідея"}
_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def cat_label(cat: str) -> str:
    return _CAT.get(cat, cat)


async def create(user_id: int, name: str, category: str, text: str, at: str) -> int:
    tid = int(await _r().incr(_SEQ))
    await _r().hset(
        _TICKETS,
        str(tid),
        json.dumps(
            {"uid": user_id, "name": name, "cat": category, "text": text[:1000],
             "status": "new", "at": at}
        ),
    )
    return tid


async def get(tid: int) -> dict | None:
    raw = await _r().hget(_TICKETS, str(tid))
    return json.loads(raw) if raw else None


async def set_status(tid: int, status: str) -> None:
    raw = await _r().hget(_TICKETS, str(tid))
    if raw:
        t = json.loads(raw)
        t["status"] = status
        await _r().hset(_TICKETS, str(tid), json.dumps(t))


async def all_tickets(open_only: bool = True) -> list[tuple[int, dict]]:
    """[(tid, ticket)] — найновіші спершу; open_only → лише не закриті."""
    raw = await _r().hgetall(_TICKETS)
    items = [(int(k), json.loads(v)) for k, v in raw.items()]
    if open_only:
        items = [it for it in items if it[1].get("status") != "closed"]
    return sorted(items, key=lambda it: it[0], reverse=True)


async def count_open() -> int:
    return len(await all_tickets(open_only=True))


def render_ticket(tid: int, t: dict) -> str:
    import html as _h

    st = "🟢 нове" if t.get("status") != "closed" else "☑️ закрито"
    return (
        f"🎫 <b>Тікет #{tid}</b> · {cat_label(t.get('cat', ''))} · {st}\n"
        f"Від: {_h.escape(t.get('name', ''))} (id <code>{t.get('uid')}</code>)\n"
        f"Коли: {t.get('at', '')}\n\n{_h.escape(t.get('text', ''))}"
    )
