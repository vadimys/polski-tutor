"""Білінг: підписка через Telegram Stars продовжує доступ + облік оплат.

Оплата йде на акаунт бота (Stars). Тут ми лише: продовжуємо `access_until`,
логуємо Payment (для звітності й атрибуції викладачу) і рахуємо платних учнів.
"""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.db.base import session_factory
from app.db.models import Payment, User
from app.services import clock


def plan_base(kind: str) -> tuple[int, int]:
    """Базова ціна плану (stars, days) до знижки. 'y' — річний, інакше місячний."""
    if kind == "y":
        return settings.sub_year_stars, settings.sub_year_days
    return settings.sub_stars, settings.sub_days


def discounted(stars: int, referred: bool) -> int:
    """Ціна з реферальною знижкою, якщо учня привів викладач (referred=True)."""
    if not referred:
        return stars
    return max(1, round(stars * (100 - settings.referral_discount_pct) / 100))


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
    """Продовжити доступ на days і залогувати оплату. Повертає новий until (ISO).

    Ідемпотентно за charge_id: повторна доставка того самого платежу (ретрай Telegram)
    НЕ подовжує доступ удруге — повертає поточний until."""
    async with session_factory()() as s:
        if charge_id:  # дедуп: цей платіж уже оброблено?
            dup = await s.execute(select(Payment.id).where(Payment.charge_id == charge_id))
            if dup.first() is not None:
                u = await s.get(User, user_id)
                return u.access_until if u else ""
        u = await s.get(User, user_id)
        if u is None:
            u = User(id=user_id)
            s.add(u)
        until = _extended_until(u.access_until, clock.today_local(), days)
        u.access_status = "approved"
        u.access_until = until
        # teacher_id фіксуємо на МОМЕНТ оплати (атрибуція revenue-share не «пливе»,
        # якщо учень згодом перейде до іншого викладача)
        s.add(
            Payment(
                user_id=user_id, teacher_id=u.referred_by, stars=stars, days=days, charge_id=charge_id
            )
        )
        try:
            await s.commit()
        except IntegrityError:  # гонка: цей charge_id уже зафіксовано (partial UNIQUE)
            await s.rollback()
            u2 = await s.get(User, user_id)
            return u2.access_until if u2 else ""
        return until


async def referrer_of(user_id: int) -> int:
    """Id викладача, який привів цього учня (0 — органічний)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        return u.referred_by if u else 0


async def paying_student_ids(teacher_id: int) -> set[int]:
    """Учні, чиї оплати атрибутовані цьому викладачу на момент оплати (revenue share)."""
    async with session_factory()() as s:
        rows = await s.execute(select(Payment.user_id).where(Payment.teacher_id == teacher_id))
        return {r[0] for r in rows.all()}


async def total_stars_from_referrals(teacher_id: int) -> int:
    """Сумарно Stars, атрибутованих цьому викладачу (незмінно після переходу учня)."""
    async with session_factory()() as s:
        val = await s.execute(
            select(func.coalesce(func.sum(Payment.stars), 0)).where(Payment.teacher_id == teacher_id)
        )
        return int(val.scalar() or 0)
