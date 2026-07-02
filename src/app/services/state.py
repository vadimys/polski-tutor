"""Персистенція стану учня — PostgreSQL (SQLAlchemy async).

Публічний API (load/save/update_readiness/all_user_ids) незмінний — хендлери
працюють як раніше; змінилося лише сховище (Redis-JSON → Postgres) заради
надійності, бекапів і майбутньої аналітики/контролю доступу.
"""

from __future__ import annotations

from sqlalchemy import delete, select

from app.config import settings
from app.db.base import session_factory
from app.db.models import Session, User
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


async def reset_progress(user_id: int) -> None:
    """Обнулити НАВЧАННЯ (рівень/готовність/стрік/історія вправ), зберігши акаунт,
    доступ і дату іспиту. Словник (SRS) скидається окремо через vocab.reset."""
    async with session_factory()() as s:
        await s.execute(delete(Session).where(Session.user_id == user_id))
        u = await s.get(User, user_id)
        if u is not None:
            u.readiness = {}
            u.level = ""
            u.streak = 0
            u.last_lesson = ""
            u.placement_done = False
        await s.commit()


async def update_readiness(user_id: int, module_value: str, pct: int) -> None:
    """Згладжене оновлення готовності (середнє) + лог сесії (сирий бал) — атомарно.

    Єдина точка для ВСІХ вправ (письмо/мовлення/тренування/мок/аудіювання).
    """
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            u = User(id=user_id, lesson_hour=settings.lesson_hour)
            s.add(u)
        current = dict(u.readiness or {})
        old = current.get(module_value, pct)
        current[module_value] = round((old + pct) / 2)
        u.readiness = current
        s.add(Session(user_id=user_id, module=module_value, score=pct))
        await s.commit()
