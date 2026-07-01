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
