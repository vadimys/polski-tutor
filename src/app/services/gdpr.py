"""GDPR: експорт і видалення персональних даних користувача.

Дані користувача: рядок users + історія sessions (Postgres) + словник/лічильники
(Redis). Право на доступ і видалення — обов'язкове для EU-сервісу.
"""

from __future__ import annotations

from sqlalchemy import delete, func, select

from app.config import settings
from app.db.base import session_factory
from app.db.models import Session, User


async def export_data(user_id: int) -> str:
    """Читабельний дамп усіх даних користувача (для права на доступ)."""
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        sessions = (
            await s.execute(
                select(func.count()).select_from(Session).where(Session.user_id == user_id)
            )
        ).scalar() or 0
    if u is None:
        return "У нас немає збережених даних про тебе."
    lines = [
        "🗂 <b>Твої дані</b>",
        f"• ID: <code>{u.id}</code>" + (f" · @{u.username}" if u.username else ""),
        f"• Рівень: {u.level} · стрік: {u.streak}",
        f"• Готовність: {u.readiness or {}}",
        f"• Дата іспиту: {u.exam_date or '—'} (підтв.: {'так' if u.exam_date_confirmed else 'ні'})",
        f"• Доступ: {u.access_status}" + (f" до {u.access_until}" if u.access_until else ""),
        f"• Виконано вправ: {sessions}",
        f"• Створено: {u.created_at}",
        "\nВидалити всі дані: /zapomnij",
    ]
    return "\n".join(lines)


async def delete_data(user_id: int) -> None:
    """Повне видалення даних користувача (право на забуття)."""
    async with session_factory()() as s:
        await s.execute(delete(Session).where(Session.user_id == user_id))
        u = await s.get(User, user_id)
        if u is not None:
            await s.delete(u)
        await s.commit()

    from redis.asyncio import Redis

    r = Redis.from_url(settings.redis_url, decode_responses=True)
    try:
        await r.delete(f"polski:vocab:{user_id}")
        await r.srem("polski:users", user_id)
        async for key in r.scan_iter(f"polski:ai:{user_id}:*"):
            await r.delete(key)
    finally:
        await r.aclose()
