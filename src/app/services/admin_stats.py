"""Агрегати для адмін-консолі: огляд, список користувачів, картка користувача.

Читає наявні дані (User/Session/Payment). Рендер — чисті функції (тестуються);
збір — async (БД). Для невеликої бази вантажимо користувачів у память і рахуємо
в Python (простіше й портативніше за складні SQL-агрегати по JSON-готовності).
"""

from __future__ import annotations

from datetime import timedelta

from sqlalchemy import func, select

from app.db.base import session_factory
from app.db.models import Payment, Session, User
from app.services import clock, quest

PAGE = 8  # користувачів на сторінку списку
_ROLE = {"teacher": "👩‍🏫 викладач", "student": "🎓 учень", "admin": "🛠 адмін"}
_MOD = {"sluchanie": "🎧", "czytanie": "📖", "gramatyka": "🔤", "pisanie": "✍️", "mowienie": "🗣"}


def role_emoji(role: str) -> str:
    return "👩‍🏫" if role == "teacher" else "🎓"


def _overall(readiness: dict | None) -> int:
    return quest.overall_pct(readiness or {})


async def overview() -> dict:
    today = clock.today_local()
    now = clock.now_local()
    d7 = now - timedelta(days=7)
    d30 = now - timedelta(days=30)
    async with session_factory()() as s:
        users = list((await s.execute(select(User))).scalars().all())
        active7 = (
            await s.execute(select(func.count(func.distinct(Session.user_id))).where(Session.created_at >= d7))
        ).scalar() or 0
        active30 = (
            await s.execute(select(func.count(func.distinct(Session.user_id))).where(Session.created_at >= d30))
        ).scalar() or 0
        payers = (
            await s.execute(select(func.count(func.distinct(Payment.user_id))))
        ).scalar() or 0
        revenue = (await s.execute(select(func.coalesce(func.sum(Payment.stars), 0)))).scalar() or 0

    teachers = [u for u in users if u.role == "teacher"]
    students = [u for u in users if u.role != "teacher"]
    referred = [u for u in students if u.referred_by]
    approved = [u for u in users if u.access_status == "approved"]
    measured = [u for u in students if u.readiness]
    avg_readiness = round(sum(_overall(u.readiness) for u in measured) / len(measured)) if measured else 0
    new7 = sum(1 for u in users if u.created_at and u.created_at >= d7)
    return {
        "total": len(users),
        "teachers": len(teachers),
        "students": len(students),
        "referred": len(referred),
        "organic": len(students) - len(referred),
        "approved": len(approved),
        "pending": sum(1 for u in users if u.access_status == "pending"),
        "active7": active7,
        "active30": active30,
        "new7": new7,
        "payers": payers,
        "revenue": int(revenue),
        "avg_readiness": avg_readiness,
        # конверсія trial→оплата: платних / (схвалених учнів)
        "conv_pct": round(payers / len(students) * 100) if students else 0,
        "today": today.isoformat(),
    }


async def list_users(offset: int = 0) -> tuple[list[dict], int]:
    """Сторінка користувачів (найновіші спершу) + загальна к-сть."""
    async with session_factory()() as s:
        total = (await s.execute(select(func.count()).select_from(User))).scalar() or 0
        rows = list(
            (
                await s.execute(
                    select(User).order_by(User.created_at.desc()).offset(offset).limit(PAGE)
                )
            ).scalars().all()
        )
    out = [
        {
            "id": u.id,
            "name": f"@{u.username}" if u.username else f"id{u.id}",
            "role": u.role,
            "status": u.access_status,
            "until": u.access_until,
            "referred_by": u.referred_by,
            "overall": _overall(u.readiness),
            "streak": u.streak,
        }
        for u in rows
    ]
    return out, int(total)


async def user_detail(user_id: int) -> dict | None:
    async with session_factory()() as s:
        u = await s.get(User, user_id)
        if u is None:
            return None
        n_sessions = (
            await s.execute(select(func.count()).select_from(Session).where(Session.user_id == user_id))
        ).scalar() or 0
        last = list(
            (
                await s.execute(
                    select(Session.module, Session.score, Session.created_at)
                    .where(Session.user_id == user_id)
                    .order_by(Session.created_at.desc())
                    .limit(5)
                )
            ).all()
        )
        pay_n = (
            await s.execute(select(func.count()).select_from(Payment).where(Payment.user_id == user_id))
        ).scalar() or 0
        pay_stars = (
            await s.execute(select(func.coalesce(func.sum(Payment.stars), 0)).where(Payment.user_id == user_id))
        ).scalar() or 0
    return {
        "id": u.id,
        "name": f"@{u.username}" if u.username else f"id{u.id}",
        "role": u.role,
        "status": u.access_status,
        "until": u.access_until,
        "exam_date": u.exam_date,
        "referred_by": u.referred_by,
        "level": u.level,
        "streak": u.streak,
        "placement_done": u.placement_done,
        "readiness": dict(u.readiness or {}),
        "n_sessions": int(n_sessions),
        "last": [(m, sc, ts.isoformat(timespec="minutes") if ts else "") for m, sc, ts in last],
        "pay_n": int(pay_n),
        "pay_stars": int(pay_stars),
        "created_at": u.created_at.isoformat(timespec="minutes") if u.created_at else "",
    }


# ── рендер (чисті функції) ───────────────────────────────────────────────────
def render_overview(d: dict) -> str:
    return (
        f"📊 <b>Огляд</b> · {d['today']}\n\n"
        f"👥 Усього: <b>{d['total']}</b> · активні 7д <b>{d['active7']}</b> / 30д {d['active30']} · "
        f"нових 7д <b>{d['new7']}</b>\n"
        f"🎓 Учні: <b>{d['students']}</b> (самі {d['organic']} · від викладача {d['referred']})\n"
        f"👩‍🏫 Викладачі: <b>{d['teachers']}</b>\n"
        f"🟢 Доступ: схвалено {d['approved']} · очікують {d['pending']}\n"
        f"💎 Платних: <b>{d['payers']}</b> · дохід <b>{d['revenue']}</b>⭐ · "
        f"конверсія {d['conv_pct']}%\n"
        f"📈 Сер. готовність учнів: <b>{d['avg_readiness']}%</b>"
    )


def render_user(d: dict) -> str:
    ready = " ".join(f"{e}{d['readiness'].get(k, 0)}%" for k, e in _MOD.items())
    ref = f"id{d['referred_by']}" if d["referred_by"] else "—"
    exam = f"\n📅 Іспит: {d['exam_date']}" if d["exam_date"] else ""
    last = "\n".join(f"  • {m} {sc}% ({ts})" for m, sc, ts in d["last"]) or "  —"
    return (
        f"👤 <b>{d['name']}</b> · {_ROLE.get(d['role'], d['role'])}\n"
        f"Статус: <b>{d['status']}</b>" + (f" до {d['until']}" if d["until"] else "") + exam + "\n"
        f"Рівень {d['level'] or '—'} · 🔥{d['streak']} · placement {'✅' if d['placement_done'] else '❌'}\n"
        f"Реферер: {ref}\n"
        f"Готовність: {ready}\n"
        f"Вправ усього: <b>{d['n_sessions']}</b>\nОстанні:\n{last}\n"
        f"💎 Оплат: {d['pay_n']} ({d['pay_stars']}⭐)\n"
        f"Створено: {d['created_at']}"
    )
