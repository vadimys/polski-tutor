"""Білінг: продовження доступу підпискою (чиста логіка дат)."""

from datetime import date

from app.services.billing import _extended_until

T = date(2026, 7, 10)


def test_extends_from_current_end_when_active():
    # підписка ще активна → додаємо дні до поточного кінця (не втрачаємо залишок)
    assert _extended_until("2026-08-01", T, 30) == "2026-08-31"


def test_extends_from_today_when_expired_or_empty():
    assert _extended_until("2026-06-01", T, 30) == "2026-08-09"  # протерміновано
    assert _extended_until("", T, 30) == "2026-08-09"  # ніколи не було
    assert _extended_until("сміття", T, 30) == "2026-08-09"  # биті дані
