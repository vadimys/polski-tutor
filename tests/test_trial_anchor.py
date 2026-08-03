"""Чесніший trial: відлік прив'язується до ПЕРШОЇ справжньої вправи (access.anchor_trial).

Умови: тільки trial (approved, скінченний until, без оплат); referred_by=0→14, інакше 30;
одноразово (прапорець); НЕ вкорочує; placement/мок (celebrate=False) НЕ запускають.
"""

from __future__ import annotations

from datetime import timedelta

from app.db.base import session_factory
from app.db.models import Payment, User
from app.services import access, billing, clock


async def _user(uid, *, until, status="approved", referred_by=0, role="student"):
    async with session_factory()() as s:
        u = User(id=uid, access_status=status, role=role, referred_by=referred_by)
        u.access_until = until
        s.add(u)
        await s.commit()


async def _until(uid):
    return (await access.info(uid)).until


# ─────────────────────────── базова прив'язка ───────────────────────────
async def test_anchor_extends_organic_to_today_plus_14(db, fake_redis):
    # зареєструвався давно, вікно майже вийшло → перша вправа має дати повні 14 днів
    old = (clock.today_local() + timedelta(days=1)).isoformat()
    await _user(-9101, until=old, referred_by=0)
    assert await access.anchor_trial(-9101) is True
    assert await _until(-9101) == (clock.today_local() + timedelta(days=14)).isoformat()


async def test_anchor_referral_uses_30(db, fake_redis):
    old = (clock.today_local() + timedelta(days=2)).isoformat()
    await _user(-9102, until=old, referred_by=555)
    assert await access.anchor_trial(-9102) is True
    assert await _until(-9102) == (clock.today_local() + timedelta(days=30)).isoformat()


async def test_anchor_is_one_shot(db, fake_redis):
    await _user(-9103, until=(clock.today_local() + timedelta(days=1)).isoformat())
    assert await access.anchor_trial(-9103) is True
    # другий раз — no-op (прапорець), навіть якщо дата вже інша
    async with session_factory()() as s:
        u = await s.get(User, -9103)
        u.access_until = (clock.today_local() + timedelta(days=1)).isoformat()  # штучно вкоротили
        await s.commit()
    assert await access.anchor_trial(-9103) is False
    assert await _until(-9103) == (clock.today_local() + timedelta(days=1)).isoformat()  # не чіпав


async def test_anchor_never_shortens(db, fake_redis):
    # вже має доступ довший за 14 днів (напр. підтверджена дата іспиту) → не вкорочуємо
    far = (clock.today_local() + timedelta(days=60)).isoformat()
    await _user(-9104, until=far)
    assert await access.anchor_trial(-9104) is False
    assert await _until(-9104) == far


async def test_anchor_skips_paid(db, fake_redis):
    await _user(-9105, until=(clock.today_local() + timedelta(days=1)).isoformat())
    async with session_factory()() as s:
        s.add(Payment(user_id=-9105, teacher_id=0, stars=300, days=30, charge_id="x"))
        await s.commit()
    assert await billing.has_payments(-9105) is True
    assert await access.anchor_trial(-9105) is False  # платник — фіксований період


async def test_anchor_skips_unlimited(db, fake_redis):
    await _user(-9106, until="")  # '' = безстроково (admin/спец)
    assert await access.anchor_trial(-9106) is False
    assert await _until(-9106) == ""


async def test_anchor_skips_absent_user(db, fake_redis):
    assert await access.anchor_trial(-9107) is False


# ─────────────────────────── інтеграція з update_readiness ───────────────────────────
async def test_real_exercise_anchors(db, fake_redis):
    await _user(-9108, until=(clock.today_local() + timedelta(days=1)).isoformat())
    from app.services import state as user_state

    await user_state.update_readiness(-9108, "gramatyka", 80)  # celebrate=True (справжня вправа)
    assert await _until(-9108) == (clock.today_local() + timedelta(days=14)).isoformat()


async def test_placement_does_not_anchor(db, fake_redis):
    start = (clock.today_local() + timedelta(days=1)).isoformat()
    await _user(-9109, until=start)
    from app.services import state as user_state

    await user_state.update_readiness(-9109, "gramatyka", 80, celebrate=False)  # placement/мок
    assert await _until(-9109) == start  # відлік НЕ переставлено
