from datetime import date

from app.services import srs


def test_promote_and_cap():
    assert srs.on_correct(1) == 2
    assert srs.on_correct(4) == 5
    assert srs.on_correct(5) == 5  # стеля


def test_wrong_resets():
    assert srs.on_wrong(4) == 1
    assert srs.on_wrong(2) == 1


def test_next_due():
    today = date(2026, 6, 30)
    assert srs.next_due(1, today) == "2026-07-01"
    assert srs.next_due(3, today) == "2026-07-07"
    assert srs.next_due(5, today) == "2026-08-04"


def test_is_due():
    today = date(2026, 6, 30)
    assert srs.is_due("", today) is True
    assert srs.is_due("2026-06-29", today) is True
    assert srs.is_due("2026-06-30", today) is True
    assert srs.is_due("2026-07-01", today) is False
