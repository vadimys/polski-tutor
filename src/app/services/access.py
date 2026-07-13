"""Контроль доступу: запити, схвалення адміном, терміни, перевірка дозволу.

Правила терміну (за специфікацією користувача):
- дата не підтверджена  → доступ +6 місяців;
- дата < 6 місяців       → +6 місяців (мінімум);
- дата ≥ 6 місяців       → до дати іспиту.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy import select

from app.db.base import session_factory
from app.db.models import User
from app.services import clock

SIX_MONTHS_DAYS = 182
TEACHER_ACCESS_DAYS = 365  # викладачу — довгий доступ (поновлюваний; MVP — рік)


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
    role: str = "student"  # student / teacher / admin
    referred_by: int = 0


async def info(user_id: int) -> AccessInfo:
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            return AccessInfo("new", "", "", False, "")
        return AccessInfo(
            u.access_status, u.access_until, u.exam_date, u.exam_date_confirmed,
            u.username, u.role, u.referred_by,
        )


def is_expired(inf: AccessInfo, today: date) -> bool:
    """Доступ був схвалений, але термін (trial/вікно) уже минув."""
    return inf.status == "approved" and bool(inf.until) and inf.until < today.isoformat()


def parse_referral(payload: str) -> int | None:
    """Розібрати deep-link payload 't<teacher_id>' → id викладача (або None)."""
    p = (payload or "").strip()
    if p.startswith("t") and p[1:].isdigit():
        return int(p[1:])
    return None


async def ensure_admin(admin_id: int) -> None:
    """Нормалізувати рядок адміна: role=admin + approved (щоб не показувавсь як
    pending-учень і не потрапляв у статистику учнів). Викликається на старті."""
    if not admin_id:
        return
    async with session_factory()() as s:
        u = await s.get(User, admin_id)
        if u is None:
            u = User(id=admin_id)
            s.add(u)
        u.role = "admin"
        u.access_status = "approved"
        await s.commit()


async def is_teacher(user_id: int) -> bool:
    """Чи це схвалений викладач (для валідації реферального посилання)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        return bool(u and u.role == "teacher" and u.access_status == "approved")


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


async def request_teacher(user_id: int, username: str) -> None:
    """Заявка на роль викладача — у чергу до адміна (role лишається student до схвалення)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            u = User(id=user_id)
            s.add(u)
        u.username = username or ""
        u.access_status = "pending"
        u.requested_at = clock.now_local().isoformat(timespec="minutes")
        await s.commit()


async def approve_teacher(user_id: int) -> str:
    """Схвалити як ВИКЛАДАЧА: role=teacher + довгий доступ. Повертає until (ISO)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            return ""
        until = (clock.today_local() + timedelta(days=TEACHER_ACCESS_DAYS)).isoformat()
        u.role = "teacher"
        u.access_status = "approved"
        u.access_until = until
        u.decided_at = clock.now_local().isoformat(timespec="minutes")
        await s.commit()
        return until


async def grant_trial(
    user_id: int,
    username: str,
    referred_by: int,
    days: int,
    exam_date: str = "",
    confirmed: bool = False,
) -> str:
    """Авто-доступ учню на `days` днів БЕЗ черги до адміна (self-serve / реферал).

    referred_by = id викладача (0 — органічний). Повертає until (ISO)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            u = User(id=user_id)
            s.add(u)
        trial_until = (clock.today_local() + timedelta(days=days)).isoformat()
        u.username = username or ""
        if u.role != "teacher":  # не перетворюємо викладача назад на учня
            u.role = "student"
        if referred_by and not u.referred_by:  # не перезатираємо наявну атрибуцію
            u.referred_by = referred_by
        if exam_date:
            u.exam_date = exam_date
            u.exam_date_confirmed = confirmed
        u.access_status = "approved"
        u.access_until = max(u.access_until, trial_until)  # НЕ вкорочуємо наявний доступ
        u.requested_at = clock.now_local().isoformat(timespec="minutes")
        u.decided_at = clock.now_local().isoformat(timespec="minutes")
        await s.commit()
        return u.access_until


async def students_of(teacher_id: int) -> list[int]:
    """Id учнів, приведених цим викладачем (для майбутнього дашборду)."""
    async with session_factory()() as s:
        rows = await s.execute(select(User.id).where(User.referred_by == teacher_id))
        return [r[0] for r in rows.all()]


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
