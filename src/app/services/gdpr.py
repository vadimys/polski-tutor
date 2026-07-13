"""GDPR: експорт і видалення персональних даних користувача.

Дані користувача: рядок users + історія sessions (Postgres) + словник/лічильники
та FSM-стан (Redis). Право на доступ і видалення — обов'язкове для EU-сервісу.
"""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import delete, select, update

from app.config import settings
from app.db.base import session_factory
from app.db.models import Assignment, AssignmentDone, Group, Session, User


async def export_data(user_id: int) -> str:
    """Читабельний дамп усіх даних користувача (право на доступ, ст. 15)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        rows = (
            await s.execute(
                select(Session.module, Session.score, Session.created_at)
                .where(Session.user_id == user_id)
                .order_by(Session.created_at.desc())
                .limit(50)
            )
        ).all()
    if u is None:
        return "У нас немає збережених даних про тебе."

    from app.services import vocab

    words = await vocab.count(user_id)
    lines = [
        "🗂 <b>Твої дані</b>",
        f"• ID: <code>{u.id}</code>" + (f" · @{u.username}" if u.username else ""),
        f"• Рівень: {u.level} · стрік: {u.streak}",
        f"• Готовність: {u.readiness or {}}",
        f"• Дата іспиту: {u.exam_date or '—'} (підтв.: {'так' if u.exam_date_confirmed else 'ні'})",
        f"• Доступ: {u.access_status}" + (f" до {u.access_until}" if u.access_until else ""),
        f"• Слів у повтореннях (SRS): {words}",
        f"• Створено: {u.created_at}",
    ]
    if rows:
        lines.append(f"\n<b>Останні вправи ({len(rows)}):</b>")
        lines += [f"• {m} — {sc}% ({ts})" for m, sc, ts in rows]
    lines.append("\nВидалити всі дані: /zapomnij")
    return "\n".join(lines)


async def _delete_redis(user_id: int) -> None:
    """Прибрати Redis-сліди користувача: словник/AI/нудж/FSM + гейміфікація + тікети."""
    from app.services import goals, support

    await goals.reset(user_id)  # polski:min/act/goalmet/celeb/xp/goal/freeze/streak
    await support.delete_user_tickets(user_id)

    from redis.asyncio import Redis

    r = Redis.from_url(settings.redis_url, decode_responses=True)
    try:
        await r.delete(f"polski:vocab:{user_id}")
        await r.srem("polski:users", user_id)
        for pattern in (f"polski:ai:{user_id}:*", f"polski:nudge:{user_id}:*", f"fsm:*:{user_id}:*"):
            async for key in r.scan_iter(pattern):
                await r.delete(key)
    finally:
        await r.aclose()


async def _delete_pg(s, user_id: int) -> None:
    """Повне PG-видалення сутностей користувача. Якщо це викладач — прибрати його
    групи/завдання й від'єднати його учнів (осиротіння зв'язків неприпустиме)."""
    u = await s.get(User, user_id)
    if u is not None and u.role == "teacher":
        gids = (
            await s.execute(select(Group.id).where(Group.teacher_id == user_id))
        ).scalars().all()
        aids = (
            await s.execute(select(Assignment.id).where(Assignment.teacher_id == user_id))
        ).scalars().all()
        if aids:
            await s.execute(delete(AssignmentDone).where(AssignmentDone.assignment_id.in_(aids)))
        await s.execute(delete(Assignment).where(Assignment.teacher_id == user_id))
        if gids:
            await s.execute(delete(Group).where(Group.id.in_(gids)))
        # від'єднати учнів цього викладача (щоб не лишалися биті referred_by/group_id)
        await s.execute(
            update(User).where(User.referred_by == user_id).values(referred_by=0, group_id=0)
        )
    # власні виконання завдань учня (нема FK на users → чистимо явно)
    await s.execute(delete(AssignmentDone).where(AssignmentDone.user_id == user_id))
    await s.execute(delete(Session).where(Session.user_id == user_id))
    if u is not None:
        await s.delete(u)  # payments підуть каскадом (FK ondelete=CASCADE)


async def delete_data(user_id: int) -> None:
    """Повне видалення даних користувача (право на забуття, ст. 17)."""
    async with session_factory()() as s:
        await _delete_pg(s, user_id)
        await s.commit()
    await _delete_redis(user_id)


async def purge_stale(today: date, denied_days: int = 30) -> int:
    """Storage limitation (ст. 5 GDPR): видаляє denied-користувачів, рішення по яких
    старше denied_days. Повертає к-сть видалених. Викликається щодня зі scheduler.

    PG-видалення — ОДНИМ bulk-запитом (не N раундтрипів → не блокує цикл надовго),
    Redis-прибирання — по кожному (denied-юзери майже не мають Redis-слідів)."""
    cutoff = (today - timedelta(days=denied_days)).isoformat()
    async with session_factory()() as s:
        ids = (
            await s.execute(
                select(User.id).where(
                    User.access_status == "denied",
                    User.decided_at != "",
                    User.decided_at < cutoff,
                )
            )
        ).scalars().all()
        if ids:
            await s.execute(delete(AssignmentDone).where(AssignmentDone.user_id.in_(ids)))
            await s.execute(delete(Session).where(Session.user_id.in_(ids)))
            await s.execute(delete(User).where(User.id.in_(ids)))
            await s.commit()
    for uid in ids:
        await _delete_redis(uid)
    return len(ids)
