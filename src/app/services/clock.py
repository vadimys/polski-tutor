"""Час у локальному поясі учня + лічильник днів до іспиту."""

from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.config import settings


def tz() -> ZoneInfo:
    return ZoneInfo(settings.timezone)


def now_local() -> datetime:
    return datetime.now(tz())


def today_local() -> date:
    return now_local().date()


def days_to_exam() -> int:
    """Скільки днів лишилось до іспиту (0, якщо вже минув)."""
    exam = date.fromisoformat(settings.exam_date)
    return max(0, (exam - today_local()).days)
