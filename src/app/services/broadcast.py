"""Розсилка/оголошення адміна по сегментах користувачів.

Сегменти рахуємо з наявних даних (User/Session/Payment). Надсилання — best-effort,
з легким тротлінгом (ліміт Telegram). Адміна не турбуємо.
"""

from __future__ import annotations

import asyncio
from datetime import timedelta

from aiogram import Bot
from sqlalchemy import func, select

from app.config import settings
from app.db.base import session_factory
from app.db.models import Payment, Session, User
from app.services import clock

SEGMENTS = {
    "all": "усі",
    "students": "учні",
    "teachers": "викладачі",
    "paying": "платні",
    "trial": "на trial",
    "inactive": "неактивні 7+ дн",
}


def label(segment: str) -> str:
    return SEGMENTS.get(segment, segment)


async def recipients(segment: str) -> list[int]:
    """Id користувачів сегмента (лише схвалені, без адміна)."""
    aid = settings.admin_id
    now = clock.now_local()
    d7 = now - timedelta(days=7)
    async with session_factory()() as s:
        users = [
            u for u in (await s.execute(select(User))).scalars().all()
            if u.id != aid and u.access_status == "approved"
        ]
        paying = {
            r[0] for r in (await s.execute(select(func.distinct(Payment.user_id)))).all()
        }
        active7 = {
            r[0] for r in (
                await s.execute(select(func.distinct(Session.user_id)).where(Session.created_at >= d7))
            ).all()
        }
    if segment == "teachers":
        pool = [u for u in users if u.role == "teacher"]
    elif segment == "students":
        pool = [u for u in users if u.role == "student"]
    elif segment == "paying":
        pool = [u for u in users if u.id in paying]
    elif segment == "trial":
        pool = [u for u in users if u.role == "student" and u.id not in paying]
    elif segment == "inactive":
        pool = [u for u in users if u.id not in active7]
    else:  # all
        pool = users
    return [u.id for u in pool]


async def send(bot: Bot, ids: list[int], text: str) -> tuple[int, int]:
    """Розіслати текст; повертає (доставлено, не вдалося). Легкий тротлінг."""
    sent = failed = 0
    for uid in ids:
        try:
            await bot.send_message(uid, text)
            sent += 1
        except Exception:  # noqa: BLE001 — недоступний чат тощо
            failed += 1
        await asyncio.sleep(0.05)  # ~20 повідомлень/с — у межах ліміту Telegram
    return sent, failed
