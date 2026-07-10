"""Білінг: продовження доступу підпискою (чиста логіка дат)."""

from datetime import date

from app.config import settings
from app.services.billing import _extended_until, discounted, plan_base

T = date(2026, 7, 10)


def test_plan_base_monthly_vs_annual():
    assert plan_base("m") == (settings.sub_stars, settings.sub_days)
    assert plan_base("y") == (settings.sub_year_stars, settings.sub_year_days)
    assert plan_base("будь-що") == (settings.sub_stars, settings.sub_days)  # дефолт — місяць


def test_discounted_only_for_referred():
    assert discounted(300, referred=False) == 300  # органічний — повна ціна
    pct = settings.referral_discount_pct
    assert discounted(300, referred=True) == round(300 * (100 - pct) / 100)
    assert discounted(2000, referred=True) == round(2000 * (100 - pct) / 100)
    assert discounted(1, referred=True) >= 1  # ніколи не 0 (мін. 1 ⭐)


def test_extends_from_current_end_when_active():
    # підписка ще активна → додаємо дні до поточного кінця (не втрачаємо залишок)
    assert _extended_until("2026-08-01", T, 30) == "2026-08-31"


def test_extends_from_today_when_expired_or_empty():
    assert _extended_until("2026-06-01", T, 30) == "2026-08-09"  # протерміновано
    assert _extended_until("", T, 30) == "2026-08-09"  # ніколи не було
    assert _extended_until("сміття", T, 30) == "2026-08-09"  # биті дані
