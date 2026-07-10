"""Головне меню + дашборд прогресу."""

from __future__ import annotations

import asyncio
from contextlib import suppress
from datetime import date

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot import charts
from app.bot.keyboards import cancel_kb, menu_kb, start_kb, to_menu_kb
from app.bot.ui import bar
from app.domain.models import MODULE_LABELS, Module
from app.services import (
    access,
    badges,
    clock,
    coach,
    exam_dates,
    exam_scale,
    goals,
    missions,
    progress,
    quest,
    vocab,
)
from app.services import state as user_state

router = Router()

async def _menu_header(user_id: int) -> str:
    """Жива шапка меню: рівень/XP/серія + ціль дня + похід + місія дня — для мотивації."""
    st = await user_state.load(user_id)
    g = await goals.status(user_id)
    days = _user_days_left(await access.info(user_id))
    qp = quest.overall_pct(st.readiness or {})
    gp = min(100, round(g["today"] / g["goal"] * 100)) if g["goal"] else 0
    dm = missions.daily_mission(user_id, clock.today_local().isoformat())
    m_done = await goals.today_count(user_id, dm["kinds"]) >= dm["n"]

    streak = f"🔥 {g['streak']} дн" if g["streak"] else "🔥 почни серію"
    frz = f" · 🧊{g['freeze']}" if g["freeze"] else ""
    exam = f" · іспит через <b>{days}</b> дн" if days is not None else ""
    mission = f"🎲 Місія дня: {dm['desc']} <b>+{dm['xp']} XP</b>" + (" ✅" if m_done else "")
    return (
        "📋 <b>Меню</b>\n\n"
        f"🏁 <b>Готовність до B1: {qp}%</b>{exam}\n"
        "<i>головна мета — ≥50% у КОЖНОМУ модулі (деталі — /postep)</i>\n\n"
        f"⏱ Ціль дня: {g['today']}/{g['goal']} хв  {bar(gp)}" + (" ✅" if g["done"] else "") + "\n"
        f"⭐ рів. {g['level']} · {g['xp']} XP · {streak}{frz} <i>— для мотивації</i>\n"
        f"{mission}\n\n"
        "Обери дію або тисни <b>⚡ Навчатись зараз</b> 👇"
    )


def _goal_line(g: dict) -> str:
    pct = min(100, round(g["today"] / g["goal"] * 100)) if g["goal"] else 0
    tick = " ✅ виконано!" if g["done"] else ""
    streak = f" · 🔥 <b>{g['streak']}</b> дн поспіль" if g["streak"] else ""
    return f"🎯 <b>Ціль дня:</b> {g['today']}/{g['goal']} хв{tick}\n  {bar(pct)}{streak}"


def _user_days_left(inf) -> int | None:
    if not (inf.confirmed and inf.exam_date):
        return None
    try:
        return max(0, (date.fromisoformat(inf.exam_date) - clock.today_local()).days)
    except ValueError:
        return None


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext) -> None:
    await state.clear()  # вихід із будь-якого активного завдання (без «протікання» стану)
    await message.answer(await _menu_header(message.from_user.id), reply_markup=menu_kb())


@router.callback_query(F.data == "menu:home")
async def cb_menu(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.message.answer(await _menu_header(cb.from_user.id), reply_markup=menu_kb())
    await cb.answer()


# --- ⚡ Навчатись зараз (розумний автопідбір найкориснішої дії) ---


async def _send_coach(msg: Message, user_id: int) -> None:
    st = await user_state.load(user_id)
    stats = await progress.compute(user_id)
    attempts = {k: v.attempts for k, v in stats.items()}
    _, due_n = await vocab.counts(user_id, clock.today_local())
    act = coach.choose(st.placement_done, progress.pcts(stats), attempts, due_n)
    kb = InlineKeyboardBuilder()
    kb.button(text=f"▶️ Почати: {act.label}", callback_data=act.cb)
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    await msg.answer(
        f"⚡ <b>Навчатись зараз</b>\n\nНайкорисніше зараз: <b>{act.label}</b>\n💡 {act.reason}",
        reply_markup=kb.as_markup(),
    )


@router.message(Command("zaraz"))
async def cmd_coach(message: Message, state: FSMContext) -> None:
    await state.clear()
    await _send_coach(message, message.from_user.id)


@router.callback_query(F.data == "coach:now")
async def cb_coach(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await _send_coach(cb.message, cb.from_user.id)


@router.message(Command("anuluj", "cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """Глобальне скасування — виходить із будь-якого стану (тест/письмо/мовлення)."""
    await state.clear()
    await message.answer("🚫 Скасовано. Повертаю в меню 👇", reply_markup=menu_kb())


@router.callback_query(F.data == "nav:cancel")
async def cb_cancel(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Скасовано")
    await cb.message.answer("🚫 Скасовано. Повертаю в меню 👇", reply_markup=menu_kb())


async def _render_progress(user_id: int, stats: dict) -> str:
    st = await user_state.load(user_id)
    inf = await access.info(user_id)
    days_left = _user_days_left(inf)
    total_words, due_n = await vocab.counts(user_id, clock.today_local())
    total_sessions, last7 = await progress.counts(user_id)
    r = progress.pcts(stats)

    exam_line = f"📅 До іспиту: <b>{days_left}</b> днів" if days_left is not None else "📅 Дата іспиту не підтверджена"
    g = await goals.status(user_id)
    xp_line = f"⭐ Рівень <b>{g['level']}</b> · {g['xp']} XP (до наступного {g['to_next']})"
    if g["freeze"]:
        xp_line += f" · 🧊 заморозки: <b>{g['freeze']}</b>"
    lines = [
        f"📊 <b>Прогрес</b> · CEFR <b>{st.level or '—'}</b> · стрік <b>{st.streak}</b> 🔥",
        exam_line,
        _goal_line(g),
        xp_line,
        f"🏋️ Вправ усього: <b>{total_sessions}</b> · за 7 днів: <b>{last7}</b>",
        f"📚 Слова: <b>{total_words}</b> · на повторення: <b>{due_n}</b>\n",
    ]
    if any(s.attempts for s in stats.values()):
        lines.append("<b>Готовність за модулями</b> (≈ орієнтовні бали іспиту):")
        for mod in Module:
            s = stats[mod.value]
            if s.attempts == 0:
                lines.append(f"❔ {MODULE_LABELS[mod]} — ще не виміряно")
                continue
            mark = "✅" if s.mastered else "🔸"
            hint = "  <i>мало практики</i>" if not (s.attempts >= 8 and s.days >= 3) else ""
            lines.append(
                f"{mark} {MODULE_LABELS[mod]} — {exam_scale.module_line(mod.value, s.pct)}\n"
                f"  {bar(s.pct)}{hint}"
            )
        got, mx = exam_scale.total_points(r)
        lines.append(f"\n📊 Орієнтовно <b>≈{got}/{mx}</b> балів (але поріг — у КОЖНОМУ окремо!)")
        lines.append(progress.projection(r, days_left is not None, days_left))
        lines.append(
            "<i>ℹ️ Готовність росте від СТАБІЛЬНОЇ практики (багато вправ, різні дні) "
            "і тане без повторення — щоб оцінка була чесною.</i>"
        )
    else:
        lines.append("Спершу пройди стартовий тест (/test), щоб я визначив готовність.")

    earned = badges.earned(r, st.streak, total_sessions, level=g["level"])
    if earned:
        lines.append("\n🏅 <b>Бейджі:</b> " + " · ".join(earned))
    return "\n".join(lines)


def _readiness_scene(inf, status: str, mods: list) -> tuple[str | None, object | None]:
    """Сцена за станом підготовки (incomplete/gaps/almost/ready)."""
    note = "\n\n<i>Це наша оцінка за вправами, не офіційна сертифікація.</i>"
    if status == "almost":
        return (
            "🔥 <b>Майже готовий!</b> Усі 5 модулів на впевненому рівні.\n"
            "Лишилось <b>скласти повний мок</b> обох секцій (/mok) на ≥60% — це доказ, "
            "що тримаєш рівень «під іспитом». Тоді підтверджу готовність 🏁" + note,
            to_menu_kb(),
        )
    if status == "ready":
        base = "🏆 <b>Схоже, ти на рівні B1!</b>\nЗа нашими вправами всі 5 модулів ≥70%."
        if inf.confirmed and inf.exam_date:
            days = _user_days_left(inf)
            when = exam_dates.label(inf.exam_date) if exam_dates.is_official(inf.exam_date) else inf.exam_date
            tail = f"\n📅 Твій іспит — <b>{when}</b>"
            tail += f" (за <b>{days}</b> дн)" if days is not None else ""
            tail += ". Тримай форму: практикуй і повторюй, щоб прийти впевненим."
            return base + tail + note, to_menu_kb()
        upcoming = exam_dates.upcoming(clock.today_local())[:3]
        lst = "\n".join(f"• {exam_dates.label(d)}" for d in upcoming) if upcoming else "—"
        kb = InlineKeyboardBuilder()
        kb.button(text="📅 Вказати дату іспиту", callback_data="onb:setdate")
        kb.button(text="⬅️ Меню", callback_data="menu:home")
        kb.adjust(1)
        return (
            base + "\n\n🎯 Час <b>реєструватися на офіційний іспит</b>! Найближчі сесії:\n"
            + lst + "\nКоли зареєструєшся — познач дату 👇" + note,
            kb.as_markup(),
        )
    if status == "incomplete":
        names = ", ".join(MODULE_LABELS[m] for m in mods)
        return (
            f"📋 Щоб побачити повну картину, перевір ще модулі: <b>{names}</b> (по вправі кожного).",
            to_menu_kb(),
        )
    if status == "gaps":
        names = ", ".join(MODULE_LABELS[m] for m in mods)
        return (
            f"🔸 <b>Майже там!</b> Усі модулі виміряні, лишилось підтягнути до впевненого рівня: "
            f"<b>{names}</b>.\nРоби вправи саме цих модулів — і побачиш, як стрілка йде вгору ▲." + note,
            to_menu_kb(),
        )
    return None, None


async def _send_progress(msg: Message, user_id: int) -> None:
    stats = await progress.compute(user_id)  # свіжо (з урахуванням спаду)
    r = progress.pcts(stats)
    st = await user_state.load(user_id)
    st.readiness = r  # оновлюємо кеш (для меню/квесту/плану/нагадування)
    await user_state.save(st)

    await msg.answer(await _render_progress(user_id, stats), reply_markup=to_menu_kb())
    if any(s.attempts for s in stats.values()):  # графік — лише коли є що показати
        png = await asyncio.to_thread(charts.readiness_bar, r)
        if png:
            await msg.answer_photo(BufferedInputFile(png, filename="progress.png"))
    inf = await access.info(user_id)
    status, mods = progress.verdict(stats, await progress.mock_ok(user_id))
    scene, markup = _readiness_scene(inf, status, mods)
    if scene:
        await msg.answer(scene, reply_markup=markup)


@router.message(Command("postep"))
async def cmd_progress(message: Message) -> None:
    await _send_progress(message, message.from_user.id)


@router.callback_query(F.data == "progress:show")
async def cb_progress(cb: CallbackQuery) -> None:
    await _send_progress(cb.message, cb.from_user.id)
    await cb.answer()


# --- Денна ціль (хвилини навчання на день) ---


def _goal_text(g: dict) -> str:
    return (
        "🎯 <b>Денна ціль навчання</b>\n\n"
        f"{_goal_line(g)}\n\n"
        "Скільки хвилин польської на день тобі комфортно? Обери — я рахуватиму прогрес "
        "щодня й нагадуватиму. Регулярність важливіша за обсяг 🙂"
    )


class GoalInput(StatesGroup):
    waiting = State()  # очікуємо власне число хвилин


def _goal_kb(current: int) -> object:
    kb = InlineKeyboardBuilder()
    labels = {10: "🟢 10 хв — легко", 20: "🟡 20 хв — норма", 30: "🔴 30 хв — інтенсив"}
    for m in goals.GOAL_CHOICES:
        mark = "✅ " if m == current else ""
        kb.button(text=mark + labels.get(m, f"{m} хв"), callback_data=f"goal:set:{m}")
    star = "✅ " if current not in goals.GOAL_CHOICES else ""
    kb.button(text=f"{star}✏️ Своя кількість", callback_data="goal:custom")
    kb.button(text="⏰ Час нагадувань", callback_data="reminder:show")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


@router.message(Command("cel"))
async def cmd_goal(message: Message) -> None:
    g = await goals.status(message.from_user.id)
    await message.answer(_goal_text(g), reply_markup=_goal_kb(g["goal"]))


@router.callback_query(F.data.startswith("goal:set:"))
async def cb_goal_set(cb: CallbackQuery) -> None:
    minutes = int(cb.data.split(":")[2])
    await goals.set_goal(cb.from_user.id, minutes)
    await cb.answer(f"Ціль: {minutes} хв/день 🎯")
    g = await goals.status(cb.from_user.id)
    with suppress(Exception):
        await cb.message.edit_text(_goal_text(g), reply_markup=_goal_kb(g["goal"]))


@router.callback_query(F.data == "goal:custom")
async def cb_goal_custom(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(GoalInput.waiting)
    await cb.answer()
    await cb.message.answer(
        "✏️ Скільки хвилин на день ставимо за ціль? Надішли <b>число</b> (5–180).",
        reply_markup=cancel_kb(),
    )


@router.message(GoalInput.waiting, F.text, ~F.text.startswith("/"))
async def on_goal_input(message: Message, state: FSMContext) -> None:
    txt = (message.text or "").strip()
    if not txt.isdigit() or not (5 <= int(txt) <= 180):
        await message.answer("Введи, будь ласка, число від 5 до 180 🙂", reply_markup=cancel_kb())
        return
    await goals.set_goal(message.from_user.id, int(txt))
    await state.clear()
    g = await goals.status(message.from_user.id)
    await message.answer(
        f"🎯 Ціль встановлено: <b>{int(txt)}</b> хв/день. Погнали!", reply_markup=_goal_kb(g["goal"])
    )


# --- Час щоденного нагадування (персональна година) ---

_HOUR_CHOICES = (6, 7, 8, 9, 12, 18, 19, 20, 21, 22)


def _reminder_text(hour: int) -> str:
    return (
        "⏰ <b>Час щоденного нагадування</b>\n\n"
        f"Зараз нагадую щодня о <b>{hour:02d}:00</b> (твій пояс).\n\n"
        "Обери зручну годину — щодня в цей час надішлю поштовх до заняття "
        "(фокус на найслабшому модулі + серія). Регулярність — головне 🙂"
    )


class HourInput(StatesGroup):
    waiting = State()  # очікуємо власну годину (0–23)


def _reminder_kb(current: int) -> object:
    kb = InlineKeyboardBuilder()
    btns = []
    for h in _HOUR_CHOICES:
        mark = "✅ " if h == current else ""
        btns.append(InlineKeyboardButton(text=f"{mark}{h:02d}:00", callback_data=f"reminder:set:{h}"))
    for i in range(0, len(btns), 3):  # по 3 у рядок
        kb.row(*btns[i : i + 3])
    star = "✅ " if current not in _HOUR_CHOICES else ""
    kb.row(InlineKeyboardButton(text=f"{star}✏️ Інша година", callback_data="reminder:custom"))
    kb.row(InlineKeyboardButton(text="⬅️ Меню", callback_data="menu:home"))
    return kb.as_markup()


async def _send_reminder(msg: Message, user_id: int) -> None:
    st = await user_state.load(user_id)
    await msg.answer(_reminder_text(st.lesson_hour), reply_markup=_reminder_kb(st.lesson_hour))


@router.message(Command("przypomnienie"))
async def cmd_reminder(message: Message) -> None:
    await _send_reminder(message, message.from_user.id)


@router.callback_query(F.data == "reminder:show")
async def cb_reminder(cb: CallbackQuery) -> None:
    await cb.answer()
    await _send_reminder(cb.message, cb.from_user.id)


@router.callback_query(F.data.startswith("reminder:set:"))
async def cb_reminder_set(cb: CallbackQuery) -> None:
    hour = int(cb.data.split(":")[2])
    await user_state.set_lesson_hour(cb.from_user.id, hour)
    await cb.answer(f"Нагадуватиму о {hour:02d}:00 ⏰")
    with suppress(Exception):
        await cb.message.edit_text(_reminder_text(hour), reply_markup=_reminder_kb(hour))


@router.callback_query(F.data == "reminder:custom")
async def cb_reminder_custom(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(HourInput.waiting)
    await cb.answer()
    await cb.message.answer(
        "✏️ О котрій годині нагадувати? Надішли <b>число</b> 0–23 (напр. <code>7</code> — це 07:00).",
        reply_markup=cancel_kb(),
    )


@router.message(HourInput.waiting, F.text, ~F.text.startswith("/"))
async def on_hour_input(message: Message, state: FSMContext) -> None:
    txt = (message.text or "").strip()
    if not txt.isdigit() or not (0 <= int(txt) <= 23):
        await message.answer("Введи, будь ласка, число від 0 до 23 🙂", reply_markup=cancel_kb())
        return
    hour = int(txt)
    await user_state.set_lesson_hour(message.from_user.id, hour)
    await state.clear()
    await message.answer(
        f"⏰ Готово: нагадуватиму щодня о <b>{hour:02d}:00</b>.", reply_markup=_reminder_kb(hour)
    )


# --- Місії (щоденний виклик + тижнева ціль) ---


def _mission_line(m: dict, unit: str, target: int) -> str:
    if m["done"]:
        return f"✅ <s>{m['desc']}</s> — виконано! <b>+{m['xp']} XP</b>"
    return f"▫️ {m['desc']}\n  {m['progress']}/{target} {unit} · нагорода <b>+{m['xp']} XP</b>"


async def _send_missions(msg: Message, user_id: int) -> None:
    st = await missions.status(user_id)
    d, w = st["daily"], st["weekly"]
    lines = [
        "🎲 <b>Місії</b> — виконуй, щоб заробити бонусний XP.\n",
        "<b>Сьогодні:</b>",
        _mission_line(d, "", d["n"]),
        "\n<b>Цей тиждень:</b>",
        _mission_line(w, "дн", w["days"]),
    ]
    if d["claimed_now"] or w["claimed_now"]:
        lines.append("\n🎉 <b>Нагороду зараховано!</b>")
    await msg.answer("\n".join(lines), reply_markup=to_menu_kb())


@router.message(Command("misje"))
async def cmd_missions(message: Message) -> None:
    await _send_missions(message, message.from_user.id)


@router.callback_query(F.data == "missions:show")
async def cb_missions(cb: CallbackQuery) -> None:
    await _send_missions(cb.message, cb.from_user.id)
    await cb.answer()


# --- Квест-мапа (похід до B1) ---


async def _send_quest(msg: Message, user_id: int) -> None:
    r = progress.pcts(await progress.compute(user_id))  # свіжо (з урахуванням спаду)
    inf = await access.info(user_id)
    g = await goals.status(user_id)
    text = quest.render(r, _user_days_left(inf), g["level"], g["streak"])
    await msg.answer(text, reply_markup=to_menu_kb())


@router.message(Command("quest", "pohid"))
async def cmd_quest(message: Message) -> None:
    await _send_quest(message, message.from_user.id)


@router.callback_query(F.data == "quest:show")
async def cb_quest(cb: CallbackQuery) -> None:
    await _send_quest(cb.message, cb.from_user.id)
    await cb.answer()


# --- Ресет прогресу (почати навчання заново; акаунт і доступ лишаються) ---


@router.message(Command("reset"))
async def cmd_reset(message: Message) -> None:
    kb = InlineKeyboardBuilder()
    kb.button(text="♻️ Так, почати заново", callback_data="reset:do")
    kb.button(text="↩️ Скасувати", callback_data="reset:cancel")
    kb.adjust(1)
    await message.answer(
        "♻️ <b>Почати навчання заново?</b>\n\n"
        "Обнуляться: рівень, готовність усіх модулів, стрік, історія вправ і повторення слів.\n"
        "✅ Доступ і дата іспиту <b>залишаться</b> (онбординг проходити не треба).\n\n"
        "Це незворотно.",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data == "reset:do")
async def cb_reset_do(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await user_state.reset_progress(cb.from_user.id)
    await vocab.reset(cb.from_user.id)
    await cb.answer("Готово")
    await cb.message.answer(
        "♻️ <b>Прогрес обнулено.</b> Починаємо з чистого аркуша!\n"
        "Найкраще стартувати зі стартового тесту 👇",
        reply_markup=start_kb(),
    )


@router.callback_query(F.data == "reset:cancel")
async def cb_reset_cancel(cb: CallbackQuery) -> None:
    await cb.answer("Скасовано")
    await cb.message.answer("Ок, нічого не змінено 🙂", reply_markup=to_menu_kb())
