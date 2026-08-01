"""Інтеграційні тести оплати на РЕАЛЬНІЙ БД (in-memory SQLite fixture).

Захищають грошовий шлях: ідемпотентність за charge_id (ретрай Telegram не подовжує
доступ удвічі й не дублює Payment), стекування різних платежів, оплата поверх активного
trial. DB-only.
"""

from __future__ import annotations

from datetime import timedelta

from sqlalchemy import func, select

from app.db.base import session_factory
from app.db.models import Payment
from app.services import access, billing, clock


async def _payment_count(uid: int) -> int:
    async with session_factory()() as s:
        return (
            await s.execute(select(func.count()).select_from(Payment).where(Payment.user_id == uid))
        ).scalar() or 0


async def test_apply_subscription_idempotent_same_charge(db):
    """Повторна доставка того самого charge_id: доступ НЕ подовжується вдруге, Payment один."""
    await access.grant_trial(-6001, "u", referred_by=0, days=1)
    first = await billing.apply_subscription(-6001, days=30, stars=300, charge_id="chg-1")
    again = await billing.apply_subscription(-6001, days=30, stars=300, charge_id="chg-1")
    assert again == first, "той самий charge_id не має рухати until"
    assert await _payment_count(-6001) == 1, "дубль charge_id не має створювати другий Payment"


async def test_apply_subscription_stacks_different_charges(db):
    """Різні charge_id — доступ продовжується далі, два Payment-рядки."""
    await access.grant_trial(-6002, "u", referred_by=0, days=1)
    await billing.apply_subscription(-6002, days=30, stars=300, charge_id="a")
    second = await billing.apply_subscription(-6002, days=30, stars=300, charge_id="b")
    # точна дата (не лише second>first — це пропустило б off-by-one): 1 trial + 30 + 30
    assert second == (clock.today_local() + timedelta(days=61)).isoformat()
    assert await _payment_count(-6002) == 2


async def test_pay_during_trial_stacks_on_trial_end(db):
    """Оплата поверх активного trial: рахуємо від кінця trial, а не від сьогодні."""
    trial_until = await access.grant_trial(-6003, "u", referred_by=0, days=30)
    paid_until = await billing.apply_subscription(-6003, days=30, stars=300, charge_id="c")
    expected = (clock.today_local() + timedelta(days=60)).isoformat()  # 30 trial + 30 підписка
    assert paid_until == expected, f"очікували {expected}, отримали {paid_until} (trial={trial_until})"


async def test_has_payments_flips(db):
    await access.grant_trial(-6004, "u", referred_by=0, days=1)
    assert await billing.has_payments(-6004) is False
    await billing.apply_subscription(-6004, days=30, stars=300, charge_id="d")
    assert await billing.has_payments(-6004) is True


async def test_apply_subscription_creates_user_if_missing(db):
    """Оплата від користувача без рядка (крайній кейс) — створює approved-доступ."""
    until = await billing.apply_subscription(-6005, days=30, stars=300, charge_id="e")
    assert until == (clock.today_local() + timedelta(days=30)).isoformat()
    assert await access.is_allowed(-6005, admin_id=0) is True


async def test_plan_base_month_and_year():
    """Чиста функція тарифів (без БД)."""
    assert billing.plan_base("y") == (billing.settings.sub_year_stars, billing.settings.sub_year_days)
    assert billing.plan_base("m") == (billing.settings.sub_stars, billing.settings.sub_days)
