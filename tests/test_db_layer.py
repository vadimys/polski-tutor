"""Тести async/persistence-шару на in-memory БД (фікстура `db`).

Покривають критичні шляхи, які раніше були без тестів: авто-залік завдань,
ідемпотентність оплат, атрибуція revenue-share, сегменти розсилки, групи+лідерборд,
X/N виконання, FK-каскади (Хвиля 2 аудиту).
"""

from datetime import datetime

from sqlalchemy import delete, func, select, update

from app.db.models import Assignment, AssignmentDone, Group, Payment, Session, User
from app.services import assignments, billing, broadcast, groups, leaderboard

# фіксовані дати (SQLite зберігає CURRENT_TIMESTAMP як рядок без мікросекунд → щоб
# порівняння created_at було детермінованим, задаємо явні наивні datetime у тестах)
_EARLY = datetime(2026, 1, 1)
_LATER = datetime(2026, 6, 1)
_OLD = datetime(2020, 1, 1)


async def _add(maker, obj):
    async with maker() as s:
        s.add(obj)
        await s.commit()


async def _set_created(maker, model, obj_id, dt):
    async with maker() as s:
        await s.execute(update(model).where(model.id == obj_id).values(created_at=dt))
        await s.commit()


async def _count(maker, model, **where):
    async with maker() as s:
        q = select(func.count()).select_from(model)
        for k, v in where.items():
            q = q.where(getattr(model, k) == v)
        return int((await s.execute(q)).scalar() or 0)


# ---------- авто-залік завдань ----------


async def test_on_session_auto_completes(db):
    await _add(db, User(id=10, role="teacher", access_status="approved"))
    await _add(db, User(id=11, role="student", referred_by=10, group_id=0, access_status="approved"))
    aid = await assignments.create(10, 0, "Аудіо", "2026-12-01", module="sluchanie", target=1)
    await _set_created(db, Assignment, aid, _EARLY)

    # до вправи — не виконано
    assert [r["done"] for r in await assignments.for_student(11)] == [False]

    # вправа ІНШОГО модуля не зараховує
    await _add(db, Session(user_id=11, module="czytanie", score=80, created_at=_LATER))
    assert await assignments.on_session(11) == []

    # вправа цільового модуля — авто-залік (повертає назву)
    await _add(db, Session(user_id=11, module="sluchanie", score=70, created_at=_LATER))
    assert await assignments.on_session(11) == ["Аудіо"]
    assert [r["done"] for r in await assignments.for_student(11)] == [True]
    # повторний виклик не дублює
    assert await assignments.on_session(11) == []
    assert await _count(db, AssignmentDone, assignment_id=aid, user_id=11) == 1


async def test_on_session_respects_target_and_created_at(db):
    await _add(db, User(id=20, role="teacher", access_status="approved"))
    await _add(db, User(id=21, role="student", referred_by=20, access_status="approved"))
    # сесія ДО створення завдання не має рахуватись
    await _add(db, Session(user_id=21, module="gramatyka", score=90, created_at=_OLD))
    aid = await assignments.create(20, 0, "Граматика x2", "2026-12-01", module="gramatyka", target=2)
    await _set_created(db, Assignment, aid, _EARLY)

    await _add(db, Session(user_id=21, module="gramatyka", score=50, created_at=_LATER))
    assert await assignments.on_session(21) == []  # лише 1 після створення < target 2
    await _add(db, Session(user_id=21, module="gramatyka", score=60, created_at=_LATER))
    assert await assignments.on_session(21) == ["Граматика x2"]


async def test_on_session_none_for_selfstudy(db):
    await _add(db, User(id=99, role="teacher", access_status="approved"))  # FK для завдання
    await _add(db, User(id=30, role="student", referred_by=0, group_id=0, access_status="approved"))
    await assignments.create(99, 0, "X", "2026-12-01", module="pisanie")
    await _add(db, Session(user_id=30, module="pisanie", score=80, created_at=_LATER))
    assert await assignments.on_session(30) == []  # без викладача — жодних завдань


# ---------- оплати ----------


async def test_apply_subscription_idempotent_and_attributed(db):
    await _add(db, User(id=41, role="student", referred_by=7, access_status="approved"))
    u1 = await billing.apply_subscription(41, 30, 300, "charge-A")
    u2 = await billing.apply_subscription(41, 30, 300, "charge-A")  # ретрай
    assert u1 == u2  # доступ не подовжено вдруге
    assert await _count(db, Payment, charge_id="charge-A") == 1  # рівно один запис
    # атрибуція зафіксована на момент оплати
    async with db() as s:
        p = (await s.execute(select(Payment).where(Payment.charge_id == "charge-A"))).scalar_one()
    assert p.teacher_id == 7
    assert 41 in await billing.paying_student_ids(7)
    assert await billing.total_stars_from_referrals(7) == 300


async def test_payment_attribution_frozen_on_teacher_switch(db):
    await _add(db, User(id=51, role="student", referred_by=1, access_status="approved"))
    await billing.apply_subscription(51, 30, 300, "charge-B")
    # учень переходить до викладача 2 (оновлення referred_by, не видалення)
    async with db() as s:
        await s.execute(update(User).where(User.id == 51).values(referred_by=2))
        await s.commit()
    # історична оплата лишається за викладачем 1, НЕ переноситься до 2
    assert await billing.total_stars_from_referrals(1) == 300
    assert await billing.total_stars_from_referrals(2) == 0


# ---------- групи + лідерборд ----------


async def test_groups_members_and_counts(db):
    await _add(db, User(id=60, role="teacher", access_status="approved"))
    gid = await groups.create(60, "Ранкова B1")
    await _add(db, User(id=61, role="student", referred_by=60, group_id=gid, streak=10, access_status="approved"))
    await _add(db, User(id=62, role="student", referred_by=60, group_id=gid, streak=5, access_status="approved"))
    await _add(db, User(id=63, role="student", referred_by=60, group_id=0, access_status="approved"))

    assert set(await groups.members(gid)) == {61, 62}
    assert await groups.ungrouped(60) == [63]
    assert [g["n"] for g in await groups.list_for(60)] == [2]  # лічильник == members


async def test_leaderboard_sorted_and_ranked(db):
    await _add(db, User(id=71, username="a", streak=5, access_status="approved"))
    await _add(db, User(id=72, username="b", streak=12, access_status="approved"))
    rows = await leaderboard.board([71, 72])
    assert [r["id"] for r in rows] == [72, 71]  # більший стрік — вище
    assert rows[0]["rank"] == 1 and rows[1]["rank"] == 2


async def test_leaderboard_deterministic_ties(db):
    # рівні стрік і готовність → стабільний порядок (менший id вище), без «стрибків»
    await _add(db, User(id=74, streak=5, access_status="approved"))
    await _add(db, User(id=73, streak=5, access_status="approved"))
    assert [r["id"] for r in await leaderboard.board([74, 73])] == [73, 74]
    assert [r["id"] for r in await leaderboard.board([73, 74])] == [73, 74]


async def test_total_students_helper(db):
    await _add(db, User(id=200, role="teacher", access_status="approved"))
    gid = await groups.create(200, "G")
    await _add(db, User(id=201, role="student", referred_by=200, group_id=gid, access_status="approved"))
    await _add(db, User(id=202, role="student", referred_by=200, group_id=0, access_status="approved"))
    assert await groups.total_students(200) == 2


# ---------- X/N виконання ----------


async def test_for_group_xn_and_pending(db):
    await _add(db, User(id=80, role="teacher", access_status="approved"))
    gid = await groups.create(80, "Клас")
    await _add(db, User(id=81, role="student", referred_by=80, group_id=gid, access_status="approved"))
    await _add(db, User(id=82, role="student", referred_by=80, group_id=gid, access_status="approved"))
    aid = await assignments.create(80, gid, "Есе", "2026-12-01")

    await assignments.mark_done(aid, 81)
    await assignments.mark_done(aid, 81)  # подвійний клік — без дубля
    assert await _count(db, AssignmentDone, assignment_id=aid) == 1

    row = (await assignments.for_group(80, gid))[0]
    assert row["done"] == 1 and row["total"] == 2
    assert await assignments.pending_students(await assignments.get(aid)) == [82]


# ---------- сегменти розсилки ----------


async def test_broadcast_segments(db):
    await _add(db, User(id=90, role="teacher", access_status="approved"))
    await _add(db, User(id=91, role="student", access_status="approved"))
    await _add(db, User(id=92, role="student", access_status="approved"))
    await _add(db, User(id=93, role="student", access_status="pending"))  # не схвалений
    await billing.apply_subscription(91, 30, 300, "c1")  # 91 — платний

    assert set(await broadcast.recipients("teachers")) == {90}
    assert set(await broadcast.recipients("students")) == {91, 92}  # 93 не схвалений — поза
    assert set(await broadcast.recipients("paying")) == {91}
    assert set(await broadcast.recipients("trial")) == {92}  # student без оплати
    assert 93 not in await broadcast.recipients("all")


# ---------- FK-каскади (Хвиля 2) ----------


async def test_cascade_delete_user_removes_done_and_payments(db):
    await _add(db, User(id=100, role="teacher", access_status="approved"))
    await _add(db, User(id=101, role="student", referred_by=100, access_status="approved"))
    aid = await assignments.create(100, 0, "T", "2026-12-01")
    await assignments.mark_done(aid, 101)
    await billing.apply_subscription(101, 30, 300, "c-casc")

    async with db() as s:
        await s.execute(delete(User).where(User.id == 101))
        await s.commit()
    assert await _count(db, AssignmentDone, user_id=101) == 0  # FK CASCADE
    assert await _count(db, Payment, user_id=101) == 0


async def test_cascade_delete_teacher_removes_groups_and_assignments(db):
    await _add(db, User(id=110, role="teacher", access_status="approved"))
    gid = await groups.create(110, "G")
    await assignments.create(110, gid, "A", "2026-12-01")
    async with db() as s:
        await s.execute(delete(User).where(User.id == 110))
        await s.commit()
    assert await _count(db, Group, teacher_id=110) == 0
    assert await _count(db, Assignment, teacher_id=110) == 0
