"""Персистенція стану учня — PostgreSQL (SQLAlchemy async).

Публічний API (load/save/update_readiness/all_user_ids) незмінний — хендлери
працюють як раніше; змінилося лише сховище (Redis-JSON → Postgres) заради
надійності, бекапів і майбутньої аналітики/контролю доступу.
"""

from __future__ import annotations

from sqlalchemy import select

from app.config import settings
from app.db.base import session_factory
from app.db.models import User
from app.domain.models import UserState


def _to_state(u: User) -> UserState:
    return UserState(
        user_id=u.id,
        level=u.level,
        streak=u.streak,
        last_lesson=u.last_lesson,
        placement_done=u.placement_done,
        lesson_hour=u.lesson_hour,
        readiness=dict(u.readiness or {}),
    )


async def load(user_id: int) -> UserState:
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            return UserState(user_id=user_id, lesson_hour=settings.lesson_hour)
        return _to_state(u)


async def save(state: UserState) -> None:
    async with session_factory()() as s:
        u = await s.get(User, state.user_id)
        if u is None:
            u = User(id=state.user_id)
            s.add(u)
        u.level = state.level
        u.streak = state.streak
        u.last_lesson = state.last_lesson
        u.placement_done = state.placement_done
        u.lesson_hour = state.lesson_hour
        u.readiness = dict(state.readiness)  # переприсвоєння → SQLAlchemy побачить зміну
        await s.commit()


async def all_user_ids() -> list[int]:
    async with session_factory()() as s:
        rows = await s.execute(select(User.id))
        return [r[0] for r in rows.all()]


async def update_readiness(user_id: int, module_value: str, pct: int) -> None:
    """Згладжене оновлення готовності модуля (середнє старого й нового)."""
    st = await load(user_id)
    old = st.readiness.get(module_value, pct)
    st.readiness[module_value] = round((old + pct) / 2)
    await save(st)
