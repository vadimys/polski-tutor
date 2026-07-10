"""Білінг: підписка через Telegram Stars продовжує доступ + облік оплат.

Оплата йде на акаунт бота (Stars). Тут ми лише: продовжуємо `access_until`,
логуємо Payment (для звітності й атрибуції викладачу) і рахуємо платних учнів.
"""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select

from app.db.base import session_factory
from app.db.models import Payment, User
from app.services import clock


def _extended_until(current_until: str, today: date, days: int) -> str:
    """Нова дата кінця: продовжуємо від пізнішого з (сьогодні, поточний кінець)."""
    base = today
    if current_until:
        try:
            cur = date.fromisoformat(current_until)
            base = max(base, cur)
        except ValueError:
            pass
    return (base + timedelta(days=days)).isoformat()


async def apply_subscription(user_id: int, days: int, stars: int, charge_id: str) -> str:
    """Продовжити доступ на days і залогувати оплату. Повертає новий until (ISO)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            u = User(id=user_id)
            s.add(u)
        until = _extended_until(u.access_until, clock.today_local(), days)
        u.access_status = "approved"
        u.access_until = until
        s.add(Payment(user_id=user_id, stars=stars, days=days, charge_id=charge_id))
        await s.commit()
        return until


async def referrer_of(user_id: int) -> int:
    """Id викладача, який привів цього учня (0 — органічний)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        return u.referred_by if u else 0


async def paying_student_ids(teacher_id: int) -> set[int]:
    """Учні цього викладача, що мають ≥1 оплату (для дашборду/revenue share)."""
    async with session_factory()() as s:
        rows = await s.execute(
            select(Payment.user_id)
            .join(User, User.id == Payment.user_id)
            .where(User.referred_by == teacher_id)
        )
        return {r[0] for r in rows.all()}


async def total_stars_from_referrals(teacher_id: int) -> int:
    """Сумарно Stars від приведених учнів (основа для revenue share)."""
    async with session_factory()() as s:
        val = await s.execute(
            select(func.coalesce(func.sum(Payment.stars), 0))
            .join(User, User.id == Payment.user_id)
            .where(User.referred_by == teacher_id)
        )
        return int(val.scalar() or 0)
