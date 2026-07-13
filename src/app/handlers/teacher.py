"""Дашборд викладача: прогрес приведених учнів (/uczniowie).

Головна винагорода партнера-викладача — бачити свій клас: готовність до B1,
скільки модулів ≥50%, найслабший модуль, серія й активність. Дані — з тих самих
sessions, що й у учня (progress.compute); учень погодився при вході за посиланням.
Доступно лише роль=teacher.
"""

from __future__ import annotations

import asyncio
import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import cancel_kb, teacher_materials_kb, to_menu_kb
from app.content import all_exams, exam_fill_tasks, exam_open_tasks, exam_sections
from app.domain.models import MODULE_LABELS, Module
from app.services import (
    access,
    assignments,
    billing,
    broadcast,
    clock,
    groups,
    leaderboard,
    progress,
    quest,
    viewas,
)
from app.services import state as user_state

router = Router()


class NotifyClass(StatesGroup):
    waiting = State()  # викладач пише повідомлення класу/групі (gid у data)


class GroupName(StatesGroup):
    waiting = State()  # назва нової/переіменованої групи (mode/gid у data)


class AssignNew(StatesGroup):
    title = State()  # текст завдання (gid у data)
    deadline = State()  # дедлайн (gid, title у data)
    module = State()  # цільовий модуль для авто-заліку (gid, title, deadline у data)


def _activity(days_since: int) -> str:
    if days_since <= 0:
        return " · активн. сьогодні"
    if days_since < 999:
        return f" · {days_since} дн тому"
    return ""


def _row(d: dict, paid: bool = False) -> str:
    """Один рядок класу (чиста функція — тестована)."""
    badge = " 💎" if paid else (" ⚠️ trial завершився" if d["expired"] else "")
    head = f"👤 <b>{html.escape(d['name'])}</b> — 🏁 {d['overall']}% · {d['passed']}/5 ≥50%{badge}"
    if not d["started"]:
        return head + "\n   <i>ще не проходив вправ</i>"
    streak = f" · 🔥 {d['streak']}" if d["streak"] else ""
    return head + f"\n   📉 {d['weak_label']} {d['weak_pct']}%{streak}{_activity(d['days_since'])}"


async def _gather(student_id: int) -> dict:
    inf = await access.info(student_id)
    stats = await progress.compute(student_id)
    pcts = progress.pcts(stats)
    started = any(s.attempts for s in stats.values())
    weak = min(Module, key=lambda m: pcts.get(m.value, 0))
    days_since = min((s.days_since for s in stats.values() if s.attempts), default=999)
    st = await user_state.load(student_id)
    name = f"@{inf.username}" if inf.username else f"id{student_id}"
    return {
        "name": name,
        "overall": quest.overall_pct(pcts),
        "passed": sum(1 for v in pcts.values() if v >= 50),
        "started": started,
        "weak_label": MODULE_LABELS[weak].split()[0] + " " + MODULE_LABELS[weak].split()[1],
        "weak_pct": pcts.get(weak.value, 0),
        "streak": st.streak,
        "days_since": days_since,
        "expired": access.is_expired(inf, clock.today_local()),
    }


async def _guard_teacher(message: Message, user_id: int) -> bool:
    inf = await access.info(user_id)
    if viewas.role_for(await viewas.get(user_id), inf.role) != "teacher":
        await message.answer(
            "👩‍🏫 Цей розділ — для викладачів. Хочеш навчати учнів через бота? "
            "Натисни /start і обери «Я викладач».",
            reply_markup=to_menu_kb(),
        )
        return False
    return True


async def _owns_group(teacher_id: int, gid: int) -> bool:
    """Чи gid — група САМЕ цього викладача (gid=0 — власний бакет «без групи»).
    Захист від IDOR: gid приходить із підроблюваного callback."""
    if not gid:
        return True
    g = await groups.get(gid)
    return bool(g and g["teacher_id"] == teacher_id)


async def _deny_foreign(message: Message) -> None:
    await message.answer("Групу не знайдено.", reply_markup=to_menu_kb())


async def _send_overview(message: Message, teacher_id: int, bot_username: str) -> None:
    gs = await groups.list_for(teacher_id)
    ung = await groups.ungrouped(teacher_id)
    link = f"https://t.me/{bot_username}?start=t{teacher_id}"
    kb = InlineKeyboardBuilder()
    for g in gs:
        kb.button(text=f"👥 {g['name']} · {g['n']}", callback_data=f"teacher:grp:{g['id']}")
    if ung:
        kb.button(text=f"👤 Без групи · {len(ung)}", callback_data="teacher:grp:0")
    kb.button(text="➕ Нова група", callback_data="teacher:newgrp")
    kb.button(text="📣 Написати всім", callback_data="teacher:notify")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    total = sum(g["n"] for g in gs) + len(ung)
    await message.answer(
        f"👩‍🏫 <b>Твої класи</b> — груп: {len(gs)} · учнів усього: <b>{total}</b>\n"
        "Обери групу, створи нову або напиши всім. Кожна група має свій join-лінк.\n\n"
        f"🔗 Загальне посилання (без групи): <code>{link}</code>",
        reply_markup=kb.as_markup(),
    )


async def _send_group_roster(message: Message, teacher_id: int, gid: int, bot_username: str) -> None:
    if gid:
        g = await groups.get(gid)
        if not g or g["teacher_id"] != teacher_id:
            await message.answer("Групу не знайдено.")
            return
        ids = await groups.members(gid)
        title = f"👥 <b>{html.escape(g['name'])}</b>"
        link = f"https://t.me/{bot_username}?start=g{gid}"
    else:
        ids = await groups.ungrouped(teacher_id)
        title = "👤 <b>Без групи</b>"
        link = f"https://t.me/{bot_username}?start=t{teacher_id}"
    paying = await billing.paying_student_ids(teacher_id)
    if ids:  # паралельно (уникаємо N+1 послідовних раундтрипів на великому класі)
        gathered = await asyncio.gather(*(_gather(sid) for sid in ids))
        body = "\n\n".join(_row(d, sid in paying) for d, sid in zip(gathered, ids, strict=True))
    else:
        body = "<i>Поки порожньо.</i>"
    kb = InlineKeyboardBuilder()
    kb.button(text="🏆 Лідерборд", callback_data=f"teacher:board:{gid}")
    kb.button(text="📝 Завдання", callback_data=f"teacher:asgn:{gid}")
    kb.button(text="📣 Написати групі", callback_data=f"teacher:gnotify:{gid}")
    if gid:
        kb.button(text="✏️ Перейменувати", callback_data=f"teacher:grename:{gid}")
    kb.button(text="⬅️ Класи", callback_data="teacher:class")
    kb.adjust(1)
    await message.answer(
        f"{title} — учнів: <b>{len(ids)}</b>\n\n{body}\n\n🔗 Приєднатись: <code>{link}</code>",
        reply_markup=kb.as_markup(),
    )


@router.message(Command("uczniowie"))
async def cmd_class(message: Message) -> None:
    if not await _guard_teacher(message, message.from_user.id):
        return
    me = await message.bot.get_me()
    await _send_overview(message, message.from_user.id, me.username or "")


@router.callback_query(F.data == "teacher:class")
async def cb_class(cb: CallbackQuery) -> None:
    await cb.answer()
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    me = await cb.bot.get_me()
    await _send_overview(cb.message, cb.from_user.id, me.username or "")


_SEC_EMOJI = {"sluchanie": "🎧", "czytanie": "📖", "gramatyka": "🔤"}


@router.callback_query(F.data == "teacher:materials")
async def cb_materials(cb: CallbackQuery) -> None:
    await cb.answer()
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    await cb.message.answer(
        "📚 <b>Матеріали та тести</b>\n\n"
        "Тут — увесь контент, який отримують учні. Переглядай будь-яку вправу в режимі "
        "<b>превʼю</b> (не зараховується), щоб знати формат і демонструвати учням.\n"
        "«🎓 Каталог» показує всі офіційні тести — зручно вибрати, що призначити групі.",
        reply_markup=teacher_materials_kb(),
    )


@router.callback_query(F.data == "teacher:catalog")
async def cb_catalog(cb: CallbackQuery) -> None:
    await cb.answer()
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    exams = all_exams()
    lines = [
        f"🎓 <b>Офіційні тести Держкомісії ({len(exams)})</b>",
        "Реальні минулі іспити + пробні. Учням корисно тренуватись на всіх.\n",
    ]
    for e in exams:
        secs = "".join(_SEC_EMOJI[s] for s in exam_sections(e.id)) or "—"
        extra = []
        if exam_fill_tasks(e.id):
            extra.append("форми")
        if exam_open_tasks(e.id):
            extra.append("трансф.")
        tail = (" · " + ", ".join(extra)) if extra else ""
        lines.append(f"• <b>{e.label}</b> · {secs} · {len(e.items)} питань{tail}")
    lines.append(
        "\n💡 Признач групі конкретний тест через «📝 Завдання» (напр. «Пройти мок "
        f"{exams[0].label}»). Сам мок — кнопка «🎓 Повний мок (превʼю)»."
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="🎓 Відкрити повний мок", callback_data="exam:open")
    kb.button(text="⬅️ Матеріали", callback_data="teacher:materials")
    kb.adjust(1)
    await cb.message.answer("\n".join(lines), reply_markup=kb.as_markup())


@router.callback_query(F.data == "teacher:invite")
async def cb_invite(cb: CallbackQuery) -> None:
    await cb.answer()
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    tid = cb.from_user.id
    me = await cb.bot.get_me()
    uname = me.username or ""
    gs = await groups.list_for(tid)
    lines = [
        "🔗 <b>Запросити учнів</b>\n",
        "Учень, що зайде за твоїм посиланням, автоматично закріпиться за тобою: "
        "ти бачиш його прогрес, а він отримує знижку на підписку.\n",
        f"Загальне посилання (без групи):\n<code>https://t.me/{uname}?start=t{tid}</code>",
    ]
    if gs:
        lines.append("\nАбо одразу в групу (join-лінк):")
        for g in gs:
            lines.append(f"• {html.escape(g['name'])}: <code>https://t.me/{uname}?start=g{g['id']}</code>")
    kb = InlineKeyboardBuilder()
    kb.button(text="👥 Керувати групами", callback_data="teacher:class")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    await cb.message.answer("\n".join(lines), reply_markup=kb.as_markup())


@router.callback_query(F.data == "teacher:revenue")
async def cb_revenue(cb: CallbackQuery) -> None:
    await cb.answer()
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    tid = cb.from_user.id
    paying = await billing.paying_student_ids(tid)
    stars = await billing.total_stars_from_referrals(tid)
    total = await groups.total_students(tid)
    kb = InlineKeyboardBuilder()
    kb.button(text="👥 Мій клас", callback_data="teacher:class")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    await cb.message.answer(
        "💎 <b>Оплати твоїх учнів</b>\n\n"
        f"👥 Учнів усього: <b>{total}</b>\n"
        f"💎 З активною підпискою: <b>{len(paying)}</b>\n"
        f"⭐ Сумарно Stars від них: <b>{stars}</b>\n\n"
        "<i>Це основа для revenue-share. Умови й виплати — узгоджуються з адміністратором "
        "(кнопка «🆘 Підтримка / звʼязок»).</i>",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("teacher:grp:"))
async def cb_group(cb: CallbackQuery) -> None:
    await cb.answer()
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    me = await cb.bot.get_me()
    await _send_group_roster(cb.message, cb.from_user.id, int(cb.data.split(":")[2]), me.username or "")


@router.callback_query(F.data.startswith("teacher:board:"))
async def cb_board(cb: CallbackQuery) -> None:
    await cb.answer()
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    tid, gid = cb.from_user.id, int(cb.data.split(":")[2])
    if not await _owns_group(tid, gid):
        await _deny_foreign(cb.message)
        return
    if gid:
        g = await groups.get(gid)
        ids, title = await groups.members(gid), (g["name"] if g else "Група")
    else:
        ids, title = await groups.ungrouped(tid), "Без групи"
    rows = await leaderboard.board(ids)
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Група", callback_data=f"teacher:grp:{gid}")
    await cb.message.answer(leaderboard.render(rows, title), reply_markup=kb.as_markup())


async def _send_assignments(message: Message, teacher_id: int, gid: int) -> None:
    if gid:
        g = await groups.get(gid)
        title = g["name"] if g and g["teacher_id"] == teacher_id else "Група"
    else:
        title = "Без групи"
    rows = await assignments.for_group(teacher_id, gid)
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Нове завдання", callback_data=f"teacher:asgnnew:{gid}")
    for r in rows:
        kb.button(text=f"🗑 {r['title'][:24]}", callback_data=f"teacher:asgndel:{gid}:{r['id']}")
    kb.button(text="⬅️ Група", callback_data=f"teacher:grp:{gid}")
    kb.adjust(1)
    await message.answer(
        assignments.render_teacher(rows, title, clock.today_local()), reply_markup=kb.as_markup()
    )


@router.callback_query(F.data.startswith("teacher:asgn:"))
async def cb_assignments(cb: CallbackQuery) -> None:
    await cb.answer()
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    gid = int(cb.data.split(":")[2])
    if not await _owns_group(cb.from_user.id, gid):
        await _deny_foreign(cb.message)
        return
    await _send_assignments(cb.message, cb.from_user.id, gid)


@router.callback_query(F.data.startswith("teacher:asgnnew:"))
async def cb_assign_new(cb: CallbackQuery, state: FSMContext) -> None:
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    gid = int(cb.data.split(":")[2])
    if not await _owns_group(cb.from_user.id, gid):
        await _deny_foreign(cb.message)
        return
    await state.set_state(AssignNew.title)
    await state.update_data(gid=gid)
    await cb.answer()
    await cb.message.answer(
        "📝 Опиши завдання одним повідомленням (напр. «Пройти /sluchanie 2 рази»):",
        reply_markup=cancel_kb(),
    )


@router.message(AssignNew.title, F.text, ~F.text.startswith("/"))
async def on_assign_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=(message.text or "").strip()[:200])
    await state.set_state(AssignNew.deadline)
    await message.answer(
        "📅 Дедлайн: дата у форматі <b>ДД.ММ</b> (напр. 20.11) або <b>РРРР-ММ-ДД</b>.",
        reply_markup=cancel_kb(),
    )


@router.message(AssignNew.deadline, F.text, ~F.text.startswith("/"))
async def on_assign_deadline(message: Message, state: FSMContext) -> None:
    today = clock.today_local()
    deadline = assignments.parse_deadline(message.text or "", today)
    if deadline is None:
        await message.answer(
            "🤔 Не зрозумів дату або вона в минулому. Приклад: <b>20.11</b> або <b>2026-11-20</b>.",
            reply_markup=cancel_kb(),
        )
        return
    await state.update_data(deadline=deadline)
    await state.set_state(AssignNew.module)
    kb = InlineKeyboardBuilder()
    for m in Module:
        kb.button(text=MODULE_LABELS[m], callback_data=f"teacher:asgnmod:{m.value}")
    kb.button(text="✋ Без авто-заліку (учень позначить сам)", callback_data="teacher:asgnmod:none")
    kb.adjust(1)
    await message.answer(
        "🤖 <b>Авто-залік:</b> обери модуль — завдання зарахується САМО, щойно учень "
        "виконає вправу цього модуля. Або без авто (учень позначить вручну).",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(AssignNew.module, F.data.startswith("teacher:asgnmod:"))
async def cb_assign_module(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    raw = cb.data.split(":")[2]
    module = "" if raw == "none" else raw
    data = await state.get_data()
    await state.clear()
    gid, title = int(data.get("gid", 0)), str(data.get("title", ""))
    deadline, tid = str(data.get("deadline", "")), cb.from_user.id
    await assignments.create(tid, gid, title, deadline, module=module)
    today = clock.today_local()
    auto = (
        f"🤖 Зарахується авто, щойно учень виконає: <b>{assignments.module_short(module)}</b>."
        if module
        else "✋ Учень позначить виконаним вручну."
    )
    await cb.message.answer(
        f"✅ Завдання створено!\n<b>{html.escape(title)}</b>\n"
        f"{assignments.deadline_label(deadline, today)}\n{auto}\n\n"
        "Учні побачать його в меню «📝 Завдання» й отримають нагадування напередодні.",
        reply_markup=to_menu_kb(),
    )
    await _send_assignments(cb.message, tid, gid)


@router.callback_query(F.data.startswith("teacher:asgndel:"))
async def cb_assign_del(cb: CallbackQuery) -> None:
    await cb.answer("Видалено")
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    _, _, gid, aid = cb.data.split(":")
    if not await _owns_group(cb.from_user.id, int(gid)):
        await _deny_foreign(cb.message)
        return
    a = await assignments.get(int(aid))
    if a and a["teacher_id"] == cb.from_user.id:
        await assignments.delete_one(int(aid))
    await _send_assignments(cb.message, cb.from_user.id, int(gid))


@router.callback_query(F.data == "teacher:newgrp")
async def cb_newgroup(cb: CallbackQuery, state: FSMContext) -> None:
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    await state.set_state(GroupName.waiting)
    await state.update_data(mode="create", gid=0)
    await cb.answer()
    await cb.message.answer("➕ Назва нової групи (напр. «Ранкова B1»):", reply_markup=cancel_kb())


@router.callback_query(F.data.startswith("teacher:grename:"))
async def cb_rename(cb: CallbackQuery, state: FSMContext) -> None:
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    gid = int(cb.data.split(":")[2])
    if not await _owns_group(cb.from_user.id, gid):
        await _deny_foreign(cb.message)
        return
    await state.set_state(GroupName.waiting)
    await state.update_data(mode="rename", gid=gid)
    await cb.answer()
    await cb.message.answer("✏️ Нова назва групи:", reply_markup=cancel_kb())


@router.message(GroupName.waiting, F.text, ~F.text.startswith("/"))
async def on_group_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    name = (message.text or "").strip()[:64]
    tid = message.from_user.id
    if data.get("mode") == "rename":
        gid = int(data.get("gid", 0))
        if not await _owns_group(tid, gid):
            await _deny_foreign(message)
            return
        await groups.rename(gid, name)
        await message.answer(f"✏️ Групу перейменовано на «{html.escape(name)}».", reply_markup=to_menu_kb())
        return
    gid = await groups.create(tid, name)
    me = await message.bot.get_me()
    link = f"https://t.me/{me.username}?start=g{gid}"
    await message.answer(
        f"✅ Групу «<b>{html.escape(name)}</b>» створено!\n\n"
        f"🔗 Join-лінк для учнів цієї групи:\n<code>{link}</code>\n\n"
        "Учень, який зайде за ним, потрапить саме в цю групу.",
        reply_markup=to_menu_kb(),
    )


@router.callback_query(F.data == "teacher:notify")
async def cb_notify(cb: CallbackQuery, state: FSMContext) -> None:
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    await state.set_state(NotifyClass.waiting)
    await state.update_data(gid=0)
    await cb.answer()
    await cb.message.answer(
        "📣 Повідомлення для ВСІХ учнів одним повідомленням — надішлю від твого імені.",
        reply_markup=cancel_kb(),
    )


@router.callback_query(F.data.startswith("teacher:gnotify:"))
async def cb_gnotify(cb: CallbackQuery, state: FSMContext) -> None:
    if not await _guard_teacher(cb.message, cb.from_user.id):
        return
    gid = int(cb.data.split(":")[2])
    if not await _owns_group(cb.from_user.id, gid):
        await _deny_foreign(cb.message)
        return
    await state.set_state(NotifyClass.waiting)
    await state.update_data(gid=gid)
    await cb.answer()
    await cb.message.answer(
        "📣 Повідомлення для цієї групи одним повідомленням — надішлю від твого імені.",
        reply_markup=cancel_kb(),
    )


@router.message(NotifyClass.waiting, F.text, ~F.text.startswith("/"))
async def on_notify(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    tid = message.from_user.id
    gid = int(data.get("gid", 0))
    if not await _owns_group(tid, gid):
        await _deny_foreign(message)
        return
    ids = await groups.members(gid) if gid else await access.students_of(tid)
    if not ids:
        await message.answer("У цій вибірці поки немає учнів.", reply_markup=to_menu_kb())
        return
    uname = message.from_user.username
    who = f"@{uname}" if uname else "твій викладач"
    text = f"📣 <b>Повідомлення від викладача</b> ({html.escape(who)}):\n{html.escape(message.text or '')}"
    sent, failed = await broadcast.send(message.bot, ids, text)
    await message.answer(
        f"✅ Надіслано: доставлено <b>{sent}</b>" + (f" · не вдалося {failed}" if failed else ""),
        reply_markup=to_menu_kb(),
    )
