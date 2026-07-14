"""Агрегати для адмін-консолі: огляд, список користувачів, картка користувача.

Читає наявні дані (User/Session/Payment). Рендер — чисті функції (тестуються);
збір — async (БД). Для невеликої бази вантажимо користувачів у память і рахуємо
в Python (простіше й портативніше за складні SQL-агрегати по JSON-готовності).
"""

from __future__ import annotations

from datetime import timedelta

from sqlalchemy import func, select

from app.config import settings
from app.db.base import session_factory
from app.db.models import Payment, Session, User
from app.services import clock, quest

PAGE = 8  # користувачів на сторінку списку
_AID = settings.admin_id  # адміна не рахуємо в статистику користувачів
_ROLE = {"teacher": "👩‍🏫 викладач", "student": "🎓 учень", "admin": "🛠 адмін"}
_MOD = {"sluchanie": "🎧", "czytanie": "📖", "gramatyka": "🔤", "pisanie": "✍️", "mowienie": "🗣"}


def role_emoji(role: str) -> str:
    return "👩‍🏫" if role == "teacher" else "🎓"


def _overall(readiness: dict | None) -> int:
    return quest.overall_pct(readiness or {})


def _name(u: User) -> str:
    return f"@{u.username}" if u.username else f"id{u.id}"


async def _paying_ids() -> set[int]:
    async with session_factory()() as s:
        rows = await s.execute(select(func.distinct(Payment.user_id)))
        return {r[0] for r in rows.all()}


async def overview() -> dict:
    today = clock.today_local()
    now = clock.now_local()
    d7 = now - timedelta(days=7)
    d30 = now - timedelta(days=30)
    async with session_factory()() as s:
        allu = list((await s.execute(select(User))).scalars().all())
        active7 = (
            await s.execute(
                select(func.count(func.distinct(Session.user_id)))
                .where(Session.created_at >= d7, Session.user_id != _AID)
            )
        ).scalar() or 0
        active30 = (
            await s.execute(
                select(func.count(func.distinct(Session.user_id)))
                .where(Session.created_at >= d30, Session.user_id != _AID)
            )
        ).scalar() or 0
        payers = (
            await s.execute(select(func.count(func.distinct(Payment.user_id))).where(Payment.user_id != _AID))
        ).scalar() or 0
        revenue = (
            await s.execute(select(func.coalesce(func.sum(Payment.stars), 0)).where(Payment.user_id != _AID))
        ).scalar() or 0

    users = [u for u in allu if u.id != _AID]  # реальні користувачі (без адміна)
    teachers = [u for u in users if u.role == "teacher"]
    students = [u for u in users if u.role == "student"]
    referred = [u for u in students if u.referred_by]
    approved = [u for u in users if u.access_status == "approved"]
    measured = [u for u in students if u.readiness]
    avg_readiness = round(sum(_overall(u.readiness) for u in measured) / len(measured)) if measured else 0
    new7 = sum(1 for u in users if u.created_at and u.created_at >= d7)
    passed = sum(1 for u in students if u.exam_result == "passed")
    failed = sum(1 for u in students if u.exam_result == "failed")
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
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / (passed + failed) * 100) if (passed + failed) else 0,
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
        f"🎓 Іспит: склали <b>{d['passed']}</b> · не склали {d['failed']} · "
        f"pass-rate {d['pass_rate']}%\n"
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


# ── інкремент 2: сегменти + викладачі/групи ─────────────────────────────────
async def segments() -> dict:
    """Самостійні учні vs приведені викладачем + конверсія в оплату кожного сегмента."""
    async with session_factory()() as s:
        users = list((await s.execute(select(User))).scalars().all())
    paying = await _paying_ids()
    students = [u for u in users if u.role == "student" and u.id != _AID]
    organic = [u for u in students if not u.referred_by]
    referred = [u for u in students if u.referred_by]

    def conv(grp: list[User]) -> tuple[int, int, int]:
        pay = sum(1 for u in grp if u.id in paying)
        return len(grp), pay, (round(pay / len(grp) * 100) if grp else 0)

    o_t, o_p, o_c = conv(organic)
    r_t, r_p, r_c = conv(referred)
    return {
        "organic_total": o_t, "organic_paying": o_p, "organic_conv": o_c,
        "referred_total": r_t, "referred_paying": r_p, "referred_conv": r_c,
    }


async def teachers() -> list[dict]:
    """Викладачі з к-стю учнів і платних (для списку груп)."""
    async with session_factory()() as s:
        users = list((await s.execute(select(User))).scalars().all())
    paying = await _paying_ids()
    tmap = {u.id: u for u in users if u.role == "teacher"}
    groups: dict[int, list[User]] = {}
    for u in users:
        if u.referred_by in tmap:
            groups.setdefault(u.referred_by, []).append(u)
    out = [
        {
            "id": tid,
            "name": _name(t),
            "n_students": len(groups.get(tid, [])),
            "n_paying": sum(1 for x in groups.get(tid, []) if x.id in paying),
        }
        for tid, t in tmap.items()
    ]
    return sorted(out, key=lambda d: d["n_students"], reverse=True)


async def teacher_group(teacher_id: int) -> dict | None:
    async with session_factory()() as s:
        t = await s.get(User, teacher_id)
        if t is None or t.role != "teacher":
            return None
        studs = list(
            (await s.execute(select(User).where(User.referred_by == teacher_id))).scalars().all()
        )
    paying = await _paying_ids()
    students = [
        {
            "id": u.id, "name": _name(u), "overall": _overall(u.readiness),
            "status": u.access_status, "streak": u.streak, "paying": u.id in paying,
        }
        for u in sorted(studs, key=lambda x: _overall(x.readiness), reverse=True)
    ]
    return {"id": teacher_id, "name": _name(t), "students": students}


def render_segments(d: dict) -> str:
    return (
        "🧑‍🎓 <b>Сегменти учнів</b>\n\n"
        f"🙋 <b>Самостійні:</b> {d['organic_total']} · платних {d['organic_paying']} "
        f"(конверсія <b>{d['organic_conv']}%</b>)\n"
        f"👩‍🏫 <b>Від викладача:</b> {d['referred_total']} · платних {d['referred_paying']} "
        f"(конверсія <b>{d['referred_conv']}%</b>)\n\n"
        "<i>Порівняй конверсію: який канал ефективніший.</i>"
    )


def render_group(d: dict) -> str:
    if not d["students"]:
        return f"👩‍🏫 <b>{d['name']}</b>\nУ групі поки немає учнів."
    lines = [f"👩‍🏫 <b>{d['name']}</b> — учнів: <b>{len(d['students'])}</b>\n"]
    for st in d["students"]:
        badge = " 💎" if st["paying"] else ""
        lines.append(f"{'✅' if st['status'] == 'approved' else '⏳'} {st['name']} · 🏁{st['overall']}% · 🔥{st['streak']}{badge}")
    return "\n".join(lines)


# ── інкремент 3: воронка + складність модулів + топ/анти-топ фіч ─────────────
async def funnel() -> dict:
    """Воронка активації: старт → доступ → placement → ≥1 вправа → оплата."""
    async with session_factory()() as s:
        total = (
            await s.execute(select(func.count()).select_from(User).where(User.id != _AID))
        ).scalar() or 0
        approved = (
            await s.execute(
                select(func.count()).select_from(User).where(User.access_status == "approved", User.id != _AID)
            )
        ).scalar() or 0
        placement = (
            await s.execute(
                select(func.count()).select_from(User).where(User.placement_done.is_(True), User.id != _AID)
            )
        ).scalar() or 0
        did_ex = (
            await s.execute(select(func.count(func.distinct(Session.user_id))).where(Session.user_id != _AID))
        ).scalar() or 0
        paid = (
            await s.execute(select(func.count(func.distinct(Payment.user_id))).where(Payment.user_id != _AID))
        ).scalar() or 0
    return {
        "total": int(total), "approved": int(approved), "placement": int(placement),
        "did_ex": int(did_ex), "paid": int(paid),
    }


async def module_difficulty() -> list[tuple[str, int, int]]:
    """[(module, n_sessions, avg_score)] — сортовано за avg зростанням (найважче спершу)."""
    async with session_factory()() as s:
        rows = list(
            (
                await s.execute(
                    select(Session.module, func.count(), func.avg(Session.score))
                    .where(Session.user_id != _AID)
                    .group_by(Session.module)
                )
            ).all()
        )
    out = [(m, int(n), round(float(avg or 0))) for m, n, avg in rows]
    return sorted(out, key=lambda x: x[2])


def render_funnel(d: dict) -> str:
    total = max(1, d["total"])
    steps = [
        ("🚀 Старт (усього)", d["total"]),
        ("🟢 Отримали доступ", d["approved"]),
        ("📝 Пройшли placement", d["placement"]),
        ("🏋️ Зробили ≥1 вправу", d["did_ex"]),
        ("💎 Оплатили", d["paid"]),
    ]
    lines = ["🔻 <b>Воронка активації</b>\n"]
    drops: list[tuple[int, str, str]] = []  # (конв%, звідки, куди) — для пошуку діри
    prev_n: int | None = None
    prev_label = ""
    for label, n in steps:
        pct = round(n / total * 100)
        if prev_n is None:
            lines.append(f"{label}: <b>{n}</b> · {pct}%")
        else:
            conv = round(n / max(1, prev_n) * 100)
            lost = max(0, prev_n - n)
            tail = f" <i>(конв. {conv}% від пункту вище" + (f", −{lost})</i>" if lost else ")</i>")
            lines.append(f"{label}: <b>{n}</b> · {pct}%{tail}")
            if prev_n > 0:
                drops.append((conv, prev_label, label))
        prev_n, prev_label = n, label
    _FUNNEL_MIN = 20  # не робимо висновків про «діру» на малій вибірці (шум)
    if d["total"] < _FUNNEL_MIN:
        lines.append(f"\n<i>Замало даних (потрібно ≥{_FUNNEL_MIN} стартів) для висновку про діру.</i>")
    elif drops and min(x[0] for x in drops) < 100:
        conv, frm, to = min(drops, key=lambda x: x[0])
        lines.append(f"\n👉 <b>Головна діра:</b> {frm} → {to} (конв. лише <b>{conv}%</b>). Дій тут першим.")
    else:
        lines.append("\n<i>Воронка без явної діри.</i>")
    return "\n".join(lines)


def render_churn(report: dict[str, int]) -> str:
    """Розподіл причин відмови (exit-survey) — куди бити оффером/ціною."""
    from app.services.churn import reason_label

    if not report:
        return "🙅 <b>Причини відмов</b>\nПоки немає даних (ніхто не проходив exit-survey)."
    total = sum(report.values())
    lines = [f"🙅 <b>Причини відмов</b> (усього {total})\n"]
    for k, n in sorted(report.items(), key=lambda x: x[1], reverse=True):
        pct = round(n / max(1, total) * 100)
        lines.append(f"{reason_label(k)}: <b>{n}</b> · {pct}%")
    lines.append("\n<i>Найчастіша причина підказує, який save-offer/ціну підсилити.</i>")
    return "\n".join(lines)


def render_mods(rows: list[tuple[str, int, int]]) -> str:
    if not rows:
        return "📉 Даних по модулях ще немає."
    lines = ["📉 <b>Складність модулів</b> (сер. бал; найважче спершу)\n"]
    for m, n, avg in rows:
        e = _MOD.get(m, "•")
        lines.append(f"{e} {m}: <b>{avg}%</b> · {n} вправ")
    lines.append("\n<i>Низький бал = де учні провалюються найчастіше.</i>")
    return "\n".join(lines)


def render_features(rows: list[tuple[str, int, int]]) -> str:
    if not rows:
        return "📈 Ще немає даних про використання (трекінг щойно ввімкнено)."
    top = rows[:8]
    bottom = rows[8:][-5:] if len(rows) > 8 else []
    lines = ["📈 <b>Використання фіч</b> (звернень · унікальних)\n", "<b>Найпопулярніші:</b>"]
    for feat, hits, uniq in top:
        lines.append(f"• {feat}: <b>{hits}</b> · 👤{uniq}")
    if bottom:
        lines.append("\n<b>Найрідше вживані:</b>")
        for feat, hits, uniq in bottom:
            lines.append(f"• {feat}: {hits} · 👤{uniq}")
    lines.append("\n<i>На що звертають увагу більше/менше.</i>")
    return "\n".join(lines)
