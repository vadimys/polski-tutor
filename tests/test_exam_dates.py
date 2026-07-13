from datetime import date

from app.services import exam_dates


def test_upcoming_filters_past():
    up = exam_dates.upcoming(date(2026, 7, 1))
    assert up == ["2026-10-17", "2026-12-05"]


def test_is_official_rejects_fake_dates():
    assert exam_dates.is_official("2026-12-05")
    assert not exam_dates.is_official("2026-12-06")  # не сесія
    assert not exam_dates.is_official("2099-01-01")


def test_label_ukrainian():
    assert exam_dates.label("2026-12-05") == "5 грудня 2026"
    assert exam_dates.label("2026-10-17") == "17 жовтня 2026"


def test_days_left_signed():
    t = date(2026, 7, 13)
    assert exam_dates.days_left("2026-07-20", t) == 7
    assert exam_dates.days_left("2026-07-13", t) == 0
    assert exam_dates.days_left("2026-07-01", t) == -12  # минув
    assert exam_dates.days_left("", t) is None
    assert exam_dates.days_left("не-дата", t) is None


def test_status_phases():
    t = date(2026, 7, 13)
    assert exam_dates.status("2026-12-05", True, t) == "future"
    assert exam_dates.status("2026-07-13", True, t) == "today"
    assert exam_dates.status("2026-07-01", True, t) == "past"
    assert exam_dates.status("2026-12-05", False, t) == "none"  # не підтверджено
    assert exam_dates.status("", True, t) == "none"
