"""Групи (класи) викладача: створення, перейменування, склад, резолв join-лінку.

Учень має ОДНУ групу (User.group_id; 0 = без групи). Вхід за ?start=g<group_id>.
"""

from __future__ import annotations

from sqlalchemy import func, select

from app.db.base import session_factory
from app.db.models import Group, User


async def create(teacher_id: int, name: str) -> int:
    async with session_factory()() as s:
        g = Group(teacher_id=teacher_id, name=name[:64].strip() or "Група")
        s.add(g)
        await s.commit()
        await s.refresh(g)
        return g.id


async def rename(group_id: int, name: str) -> None:
    async with session_factory()() as s:
        g = await s.get(Group, group_id)
        if g is not None:
            g.name = name[:64].strip() or g.name
            await s.commit()


async def get(group_id: int) -> dict | None:
    async with session_factory()() as s:
        g = await s.get(Group, group_id)
        return {"id": g.id, "teacher_id": g.teacher_id, "name": g.name} if g else None


async def list_for(teacher_id: int) -> list[dict]:
    """Групи викладача з к-стю учнів (найновіші спершу)."""
    async with session_factory()() as s:
        groups = list(
            (
                await s.execute(
                    select(Group).where(Group.teacher_id == teacher_id).order_by(Group.id.desc())
                )
            ).scalars().all()
        )
        counts = dict(
            (
                await s.execute(
                    select(User.group_id, func.count())
                    .where(User.referred_by == teacher_id)
                    .group_by(User.group_id)
                )
            ).all()
        )
    return [{"id": g.id, "name": g.name, "n": int(counts.get(g.id, 0))} for g in groups]


async def members(group_id: int) -> list[int]:
    async with session_factory()() as s:
        rows = await s.execute(select(User.id).where(User.group_id == group_id))
        return [r[0] for r in rows.all()]


async def ungrouped(teacher_id: int) -> list[int]:
    """Учні викладача без групи (зайшли за загальним лінком t<teacher>)."""
    async with session_factory()() as s:
        rows = await s.execute(
            select(User.id).where(User.referred_by == teacher_id, User.group_id == 0)
        )
        return [r[0] for r in rows.all()]
