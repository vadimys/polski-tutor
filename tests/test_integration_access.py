"""Інтеграційні тести доступ-lifecycle на РЕАЛЬНІЙ БД (in-memory SQLite fixture).

Захищають шлях, на якому впав перший живий користувач (@marinamgr, 2026-07-30):
grant_trial для нового/легасі-рядка з access_until=NULL робив max(None, str) → TypeError.
Ці тести ловили б його ще в CI. DB-only — Redis/AI не потрібні.
"""

from __future__ import annotations

from datetime import timedelta

from sqlalchemy import select

from app.db.base import session_factory
from app.db.models import User
from app.services import access, clock


async def _insert_user(uid: int, *, access_until, status: str = "approved", role: str = "student"):
    """Вставити рядок напряму (щоб відтворити легасі-стан, зокрема access_until=NULL)."""
    async with session_factory()() as s:
        u = User(id=uid, access_status=status, role=role)
        u.access_until = access_until
        s.add(u)
        await s.commit()


# ─────────────────────────── marina-регресія ───────────────────────────
async def test_grant_trial_brand_new_user_no_typeerror(db):
    """Новий користувач (рядок ще не створено): access_until=None на момент max()."""
    until = await access.grant_trial(-5001, "canary", referred_by=0, days=14)
    assert until, "grant_trial має повернути непорожній ISO-until"
    assert until == (clock.today_local() + timedelta(days=14)).isoformat()


async def test_grant_trial_legacy_null_until(db):
    """ТОЧНИЙ баг marina: наявний НЕ-схвалений рядок із access_until=NULL (стара БД) →
    grant не має кинути TypeError і має видати trial-вікно (pending ≠ unlimited)."""
    await _insert_user(-5002, access_until=None, status="pending")
    until = await access.grant_trial(-5002, "u", referred_by=0, days=30)  # не має кинути TypeError
    assert until == (clock.today_local() + timedelta(days=30)).isoformat()


async def test_grant_trial_never_shortens(db):
    """Повторний grant на менший строк не вкорочує наявне вікно (max)."""
    long_until = await access.grant_trial(-5003, "u", referred_by=0, days=30)
    short = await access.grant_trial(-5003, "u", referred_by=0, days=1)
    assert short == long_until, "менший trial НЕ повинен вкорочувати доступ"


async def test_grant_trial_does_not_demote_teacher(db):
    """Викладач лишається викладачем І зберігає безстроковий доступ ('' не вкорочується)."""
    await _insert_user(-5004, access_until="", role="teacher")
    await access.grant_trial(-5004, "u", referred_by=0, days=14)
    inf = await access.info(-5004)
    assert inf.role == "teacher"
    assert inf.until == "", "безстроковий доступ ('') НЕ можна вкорочувати до today+14"


async def test_grant_trial_preserves_unlimited_access(db):
    """Approved + '' (безстроково, напр. адмін/спец-доступ) не демоутиться grant_trial."""
    await _insert_user(-5008, access_until="", status="approved")
    until = await access.grant_trial(-5008, "u", referred_by=0, days=14)
    assert until == "", "unlimited має лишитись unlimited"
    assert await access.is_allowed(-5008, admin_id=0) is True


async def test_extend_days_preserves_unlimited(db):
    await _insert_user(-5009, access_until="", status="approved")
    assert await access.extend_days(-5009, 7) == ""


async def test_extend_days_null_safe(db):
    """churn-продовження теж NULL-safe для легасі-рядка (не-unlimited стан)."""
    await _insert_user(-5005, access_until=None, status="denied")
    until = await access.extend_days(-5005, 7)
    assert until == (clock.today_local() + timedelta(days=7)).isoformat()


async def test_extend_days_missing_user_returns_empty(db):
    assert await access.extend_days(-5006, 7) == ""


# ─────────────────────────── гейт-матриця ───────────────────────────
async def test_gate_new_user_denied(db):
    assert await access.is_allowed(-5100, admin_id=0) is False


async def test_gate_approved_unlimited_allowed(db):
    """Порожній access_until = безстроково (учні-викладачі, спец-доступ)."""
    await _insert_user(-5101, access_until="")
    assert await access.is_allowed(-5101, admin_id=0) is True


async def test_gate_approved_future_allowed(db):
    future = (clock.today_local() + timedelta(days=5)).isoformat()
    await _insert_user(-5102, access_until=future)
    assert await access.is_allowed(-5102, admin_id=0) is True
    assert access.is_expired(await access.info(-5102), clock.today_local()) is False


async def test_gate_approved_past_blocked_and_expired(db):
    past = (clock.today_local() - timedelta(days=1)).isoformat()
    await _insert_user(-5103, access_until=past)
    assert await access.is_allowed(-5103, admin_id=0) is False
    assert access.is_expired(await access.info(-5103), clock.today_local()) is True


async def test_gate_denied_blocked(db):
    await _insert_user(-5104, access_until="", status="denied")
    assert await access.is_allowed(-5104, admin_id=0) is False


async def test_gate_today_boundary_allowed(db):
    """Останній оплачений день (access_until == сьогодні): is_allowed використовує >=."""
    today = clock.today_local().isoformat()
    await _insert_user(-5108, access_until=today)
    assert await access.is_allowed(-5108, admin_id=0) is True
    assert access.is_expired(await access.info(-5108), clock.today_local()) is False


async def test_gate_admin_short_circuit(db):
    """admin_id проходить гейт навіть без рядка в БД."""
    assert await access.is_allowed(-5105, admin_id=-5105) is True


async def test_grant_trial_persists_referrer_once(db):
    """referred_by виставляється один раз і не перезатирається наступним grant."""
    await access.grant_trial(-5106, "u", referred_by=111, days=14)
    await access.grant_trial(-5106, "u", referred_by=222, days=14)
    async with session_factory()() as s:
        u = await s.get(User, -5106)
        assert u is not None and u.referred_by == 111


async def test_grant_trial_row_actually_written(db):
    await access.grant_trial(-5107, "u", referred_by=0, days=14)
    async with session_factory()() as s:
        rows = (await s.execute(select(User.id).where(User.id == -5107))).all()
        assert len(rows) == 1
