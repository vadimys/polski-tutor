"""Аналітика прогресу: статистика вправ, тренди по модулях, прогноз готовності."""

from __future__ import annotations

from datetime import timedelta

from sqlalchemy import func, select

from app.db.base import session_factory
from app.db.models import Session
from app.domain.models import MODULE_LABELS, Module
from app.services import clock


async def counts(user_id: int) -> tuple[int, int]:
    """(усього вправ, за останні 7 днів)."""
    async with session_factory()() as s:
        total = (
            await s.execute(
                select(func.count()).select_from(Session).where(Session.user_id == user_id)
            )
        ).scalar() or 0
        week_ago = clock.now_local() - timedelta(days=7)
        last7 = (
            await s.execute(
                select(func.count())
                .select_from(Session)
                .where(Session.user_id == user_id, Session.created_at >= week_ago)
            )
        ).scalar() or 0
        return int(total), int(last7)


async def recent_scores(user_id: int, module_value: str, limit: int = 5) -> list[int]:
    """Останні бали модуля (найновіші спершу)."""
    async with session_factory()() as s:
        rows = await s.execute(
            select(Session.score)
            .where(Session.user_id == user_id, Session.module == module_value)
            .order_by(Session.created_at.desc())
            .limit(limit)
        )
        return [r[0] for r in rows.all()]


READY_THRESHOLD = 70  # усі 5 модулів ≥ цього → «схоже, готовий до іспиту» (запас над 50%)


def readiness_verdict(readiness: dict[str, int]) -> tuple[str, list[Module]]:
    """Стан підготовки за виміряними модулями:

    ('incomplete', [невиміряні]) — не всі 5 модулів ще перевірені;
    ('gaps', [слабкі <70%]) — усі виміряні, але не всі досягли порогу готовності;
    ('ready', []) — усі 5 модулів ≥ READY_THRESHOLD.
    """
    missing = [m for m in Module if m.value not in readiness]
    if missing:
        return "incomplete", missing
    weak = [m for m in Module if readiness.get(m.value, 0) < READY_THRESHOLD]
    if weak:
        return "gaps", weak
    return "ready", []


def trend(scores: list[int]) -> str:
    """Стрілка тренду за останніми двома балами (найновіші спершу)."""
    if len(scores) < 2:
        return "→"
    if scores[0] > scores[1]:
        return "↑"
    if scores[0] < scores[1]:
        return "↓"
    return "→"


def projection(readiness: dict[str, int], has_date: bool, days_left: int | None) -> str:
    """Чесний якісний прогноз готовності до порога ≥50% у кожному модулі."""
    below = [m for m in Module if readiness.get(m.value, 0) < 50]
    if not below:
        return "✅ Усі модулі ≥50% — тримай темп до іспиту!"
    names = ", ".join(MODULE_LABELS[m] for m in below)
    if has_date and days_left is not None:
        pace = (
            "встигаєш, якщо тримати ~1 год/день"
            if days_left >= len(below) * 14
            else "часу впритул — фокус лише на цих модулях"
        )
        return f"🔸 Нижче порога (50%): {names}.\n📈 Днів до іспиту: {days_left} — {pace}."
    return f"🔸 Нижче порога (50%): {names}. Признач дату іспиту для точнішого прогнозу."
