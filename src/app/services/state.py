"""Персистенція стану учня — PostgreSQL (SQLAlchemy async).

Публічний API (load/save/update_readiness/all_user_ids) незмінний — хендлери
працюють як раніше; змінилося лише сховище (Redis-JSON → Postgres) заради
надійності, бекапів і майбутньої аналітики/контролю доступу.
"""

from __future__ import annotations

from sqlalchemy import delete, select

from app.config import settings
from app.db.base import session_factory
from app.db.models import AssignmentDone, Session, User
from app.domain.models import UserState


def _to_state(u: User) -> UserState:
    return UserState(
        user_id=u.id,
        level=u.level,
        streak=u.streak,
        last_lesson=u.last_lesson,
        placement_done=u.placement_done,
        lesson_hour=u.lesson_hour,
        role=u.role,
        group_id=u.group_id,
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


async def set_lesson_hour(user_id: int, hour: int) -> None:
    """Персональна година щоденного нагадування (0–23, локальний пояс)."""
    hour = max(0, min(23, hour))
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            u = User(id=user_id, lesson_hour=hour)
            s.add(u)
        else:
            u.lesson_hour = hour
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
        # мітки виконання завдань — теж прогрес; чистимо, щоб авто-залік не «залипав»
        await s.execute(delete(AssignmentDone).where(AssignmentDone.user_id == user_id))
        u = await s.get(User, user_id)
        if u is not None:
            u.readiness = {}
            u.level = ""
            u.streak = 0
            u.last_lesson = ""
            u.placement_done = False
        await s.commit()


async def full_reset(user_id: int) -> None:
    """Повний wipe навчання (старт із нуля): сесії+готовність+рівень+стрік+placement (PG),
    гейміфікація (XP/бейджі/лічильники), колода помилок, прапорці моків, повторення слів.
    Зберігає акаунт/доступ/роль/дату іспиту."""
    await reset_progress(user_id)  # sessions + AssignmentDone + рівень/готовність/стрік/placement
    from app.services import goals, mistakes, progress, vocab  # відкладено — уникаємо циклів

    await goals.reset(user_id)
    await mistakes.clear(user_id)
    await progress.reset_marks(user_id)
    await vocab.reset(user_id)


async def update_readiness(user_id: int, module_value: str, pct: int) -> None:
    """Лог сесії (сирий бал) + перерахунок ЧЕСНОЇ готовності з історії.

    Єдина точка для ВСІХ вправ (письмо/мовлення/тренування/мок/аудіювання).
    Готовність більше НЕ ковзне середнє — рахується з усієї історії сесій
    (обсяг + різні дні + свіжість), див. progress.compute.
    """
    from app.services import assignments, goals, progress, viewas  # відкладено — уникаємо циклів

    mode = await viewas.get(user_id)
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        real_role = u.role if u is not None else "student"
        # превʼю-режим (роль teacher АБО адмін у view-as=teacher): практика НЕ рухає
        # готовність/XP/місії/серію — і чесно повідомляємо про це після вправи
        if viewas.role_for(mode, real_role) == "teacher":
            await goals.push_celebration(
                user_id, "🔎 <i>Превʼю-режим: цей результат НЕ зараховується у твій прогрес.</i>"
            )
            return
        if u is None:
            u = User(id=user_id, lesson_hour=settings.lesson_hour)
            s.add(u)
        s.add(Session(user_id=user_id, module=module_value, score=pct))
        await s.commit()

    stats = await progress.compute(user_id)  # чесна готовність із повної історії
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is not None:
            u.readiness = progress.pcts(stats)
            await s.commit()
    await goals.record_module(user_id, module_value, score=pct)  # час + XP у прогресію
    done = await assignments.on_session(user_id)  # авто-залік завдань, чий модуль-ціль виконано
    if done:  # реальна нотифікація учня (буфер святкування — хендлер покаже після вправи)
        await goals.push_celebration(
            user_id, "🤖 <b>Завдання зараховано автоматично:</b> " + ", ".join(done)
        )
