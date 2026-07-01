"""Контроль доступу: запити, схвалення адміном, терміни, перевірка дозволу.

Правила терміну (за специфікацією користувача):
- дата не підтверджена  → доступ +6 місяців;
- дата < 6 місяців       → +6 місяців (мінімум);
- дата ≥ 6 місяців       → до дати іспиту.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from app.db.base import session_factory
from app.db.models import User
from app.services import clock

SIX_MONTHS_DAYS = 182


def compute_access_until(exam_date: str, confirmed: bool, today: date) -> date:
    """Кінцева дата доступу за правилами."""
    six = today + timedelta(days=SIX_MONTHS_DAYS)
    if not confirmed or not exam_date:
        return six
    try:
        exam = date.fromisoformat(exam_date)
    except ValueError:
        return six
    return exam if exam > six else six


def extend_until(current_until: str, exam_date: str) -> str:
    """Подовжити доступ до дати іспиту, якщо вона ПІЗНІШЕ за поточний кінець.

    Сценарій: доступ дали на 6 міс (дата не підтв.); користувач зареєструвався й
    дав реальну дату — якщо вона за межами поточного вікна, продовжуємо до неї.
    """
    if not exam_date:
        return current_until
    if not current_until:
        return exam_date
    return max(current_until, exam_date)


@dataclass
class AccessInfo:
    status: str  # new / pending / approved / denied
    until: str
    exam_date: str
    confirmed: bool
    username: str


async def info(user_id: int) -> AccessInfo:
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            return AccessInfo("new", "", "", False, "")
        return AccessInfo(u.access_status, u.access_until, u.exam_date, u.exam_date_confirmed, u.username)


async def is_allowed(user_id: int, admin_id: int) -> bool:
    """Чи має користувач активний доступ (адмін — завжди)."""
    if admin_id and user_id == admin_id:
        return True
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None or u.access_status != "approved":
            return False
        if not u.access_until:
            return True
        return u.access_until >= clock.today_local().isoformat()


async def request_access(user_id: int, username: str, exam_date: str, confirmed: bool) -> None:
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            u = User(id=user_id)
            s.add(u)
        u.username = username or ""
        u.exam_date = exam_date or ""
        u.exam_date_confirmed = confirmed
        u.access_status = "pending"
        u.requested_at = clock.now_local().isoformat(timespec="minutes")
        await s.commit()


async def approve(user_id: int) -> str:
    """Схвалити; повертає дату кінця доступу (ISO) або '' якщо користувача немає."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            return ""
        until = compute_access_until(u.exam_date, u.exam_date_confirmed, clock.today_local())
        u.access_status = "approved"
        u.access_until = until.isoformat()
        u.decided_at = clock.now_local().isoformat(timespec="minutes")
        await s.commit()
        return until.isoformat()


async def set_exam_date(user_id: int, exam_date: str) -> str:
    """Підтвердити дату іспиту; подовжити доступ до неї, якщо треба. Повертає новий until."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            return ""
        u.exam_date = exam_date
        u.exam_date_confirmed = True
        if u.access_status == "approved":
            u.access_until = extend_until(u.access_until, exam_date)
        await s.commit()
        return u.access_until


async def deny(user_id: int) -> None:
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            u = User(id=user_id)
            s.add(u)
        u.access_status = "denied"
        u.decided_at = clock.now_local().isoformat(timespec="minutes")
        await s.commit()
