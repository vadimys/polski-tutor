"""Завдання викладача з дедлайнами: створення, трекінг виконання, нагадування.

Таргет завдання: `group_id>0` → учні цієї групи; `group_id=0` → учні викладача
«без групи» (referred_by=teacher_id, group_id=0) — так само, як у ростері /uczniowie.
Учень позначає «виконано» вручну; викладач бачить X/N. Нагадування напередодні
дедлайну й у день — зі scheduler. Рендери — чисті функції (тестовані).
"""

from __future__ import annotations

import html
from datetime import date

from sqlalchemy import func, select

from app.db.base import session_factory
from app.db.models import Assignment, AssignmentDone, User


def parse_deadline(text: str, today: date) -> str | None:
    """Парс дедлайну учителя: 'YYYY-MM-DD', 'DD.MM.YYYY' або 'DD.MM' (рік — поточний/наступний).
    None — якщо не дата або в минулому."""
    t = (text or "").strip()
    d: date | None = None
    try:
        if "-" in t:
            d = date.fromisoformat(t)
        elif "." in t:
            parts = [p for p in t.split(".") if p]
            if len(parts) == 3:
                dd, mm, yy = int(parts[0]), int(parts[1]), int(parts[2])
                d = date(yy if yy > 100 else 2000 + yy, mm, dd)
            elif len(parts) == 2:
                dd, mm = int(parts[0]), int(parts[1])
                d = date(today.year, mm, dd)
                if d < today:
                    d = date(today.year + 1, mm, dd)
    except (ValueError, IndexError):
        return None
    if d is None or d < today:
        return None
    return d.isoformat()


def deadline_label(iso: str, today: date) -> str:
    """Людський підпис дедлайну для учня (терміновість наочна)."""
    try:
        d = (date.fromisoformat(iso) - today).days
    except ValueError:
        return ""
    if d < 0:
        return f"⏰ протерміновано на {-d} дн"
    if d == 0:
        return "⏰ <b>дедлайн сьогодні</b>"
    if d == 1:
        return "⏰ дедлайн завтра"
    return f"⏳ ще {d} дн (до {iso})"


# --- запис / зчитування ---


async def create(teacher_id: int, group_id: int, title: str, deadline: str) -> int:
    async with session_factory()() as s:
        a = Assignment(
            teacher_id=teacher_id, group_id=group_id, title=title[:200].strip(), deadline=deadline
        )
        s.add(a)
        await s.commit()
        await s.refresh(a)
        return a.id


async def get(assignment_id: int) -> dict | None:
    async with session_factory()() as s:
        a = await s.get(Assignment, assignment_id)
        if a is None:
            return None
        return {
            "id": a.id,
            "teacher_id": a.teacher_id,
            "group_id": a.group_id,
            "title": a.title,
            "deadline": a.deadline,
        }


async def delete_one(assignment_id: int) -> None:
    async with session_factory()() as s:
        a = await s.get(Assignment, assignment_id)
        if a is not None:
            await s.delete(a)
            await s.commit()


async def _target_ids(teacher_id: int, group_id: int) -> list[int]:
    from app.services import groups  # відкладено — уникаємо циклів

    return await (groups.members(group_id) if group_id else groups.ungrouped(teacher_id))


async def for_group(teacher_id: int, group_id: int) -> list[dict]:
    """Завдання групи (найближчий дедлайн спершу) з лічильником виконання X/N."""
    async with session_factory()() as s:
        rows = list(
            (
                await s.execute(
                    select(Assignment)
                    .where(Assignment.teacher_id == teacher_id, Assignment.group_id == group_id)
                    .order_by(Assignment.deadline.asc())
                )
            ).scalars().all()
        )
        ids = [a.id for a in rows] or [0]
        done_counts = dict(
            (
                await s.execute(
                    select(AssignmentDone.assignment_id, func.count())
                    .where(AssignmentDone.assignment_id.in_(ids))
                    .group_by(AssignmentDone.assignment_id)
                )
            ).all()
        )
    total = len(await _target_ids(teacher_id, group_id))
    return [
        {
            "id": a.id,
            "title": a.title,
            "deadline": a.deadline,
            "done": int(done_counts.get(a.id, 0)),
            "total": total,
        }
        for a in rows
    ]


async def for_student(user_id: int) -> list[dict]:
    """Завдання, що таргетять цього учня (за групою або як «без групи» учня викладача)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            return []
        if u.group_id:
            cond = Assignment.group_id == u.group_id
        elif u.referred_by:
            cond = (Assignment.teacher_id == u.referred_by) & (Assignment.group_id == 0)
        else:
            return []
        rows = list(
            (
                await s.execute(select(Assignment).where(cond).order_by(Assignment.deadline.asc()))
            ).scalars().all()
        )
        done = set(
            (
                await s.execute(
                    select(AssignmentDone.assignment_id).where(AssignmentDone.user_id == user_id)
                )
            ).scalars().all()
        )
    return [
        {"id": a.id, "title": a.title, "deadline": a.deadline, "done": a.id in done} for a in rows
    ]


async def mark_done(assignment_id: int, user_id: int) -> None:
    async with session_factory()() as s:
        exists = (
            await s.execute(
                select(AssignmentDone.id).where(
                    AssignmentDone.assignment_id == assignment_id,
                    AssignmentDone.user_id == user_id,
                )
            )
        ).scalar_one_or_none()
        if exists is None:
            s.add(AssignmentDone(assignment_id=assignment_id, user_id=user_id))
            await s.commit()


async def due_on(iso_day: str) -> list[dict]:
    """Завдання з дедлайном рівно в цей день (для нагадувань scheduler)."""
    async with session_factory()() as s:
        rows = list(
            (
                await s.execute(select(Assignment).where(Assignment.deadline == iso_day))
            ).scalars().all()
        )
    return [
        {
            "id": a.id,
            "teacher_id": a.teacher_id,
            "group_id": a.group_id,
            "title": a.title,
            "deadline": a.deadline,
        }
        for a in rows
    ]


async def pending_students(assignment: dict) -> list[int]:
    """Учні-таргети завдання, які ще НЕ позначили «виконано»."""
    ids = await _target_ids(assignment["teacher_id"], assignment["group_id"])
    async with session_factory()() as s:
        done = set(
            (
                await s.execute(
                    select(AssignmentDone.user_id).where(
                        AssignmentDone.assignment_id == assignment["id"]
                    )
                )
            ).scalars().all()
        )
    return [i for i in ids if i not in done]


# --- чисті рендери ---


def render_student(rows: list[dict], today: date) -> str:
    if not rows:
        return (
            "📝 <b>Завдання</b>\n\nПоки немає активних завдань від викладача.\n"
            "<i>Якщо навчаєшся сам — завдання зʼявляться, коли долучишся до групи викладача.</i>"
        )
    lines = ["📝 <b>Завдання від викладача</b>\n"]
    for r in rows:
        tick = "✅ " if r["done"] else "◻️ "
        lines.append(f"{tick}<b>{html.escape(r['title'])}</b>\n   {deadline_label(r['deadline'], today)}")
    return "\n".join(lines)


def render_teacher(rows: list[dict], title: str, today: date) -> str:
    head = f"📝 <b>Завдання · {html.escape(title)}</b>"
    if not rows:
        return head + "\n\nПоки немає завдань. Створи перше 👇"
    lines = [head, ""]
    for r in rows:
        done_all = "✅" if r["total"] and r["done"] >= r["total"] else "👥"
        lines.append(
            f"• <b>{html.escape(r['title'])}</b>\n"
            f"   {deadline_label(r['deadline'], today)} · {done_all} виконали {r['done']}/{r['total']}"
        )
    return "\n".join(lines)
