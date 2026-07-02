"""Головне меню + дашборд прогресу."""

from __future__ import annotations

import asyncio
from datetime import date

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot import charts
from app.bot.keyboards import menu_kb, start_kb, to_menu_kb
from app.bot.ui import bar
from app.domain.models import MODULE_LABELS, Module
from app.services import access, badges, clock, exam_dates, progress, vocab
from app.services import state as user_state

router = Router()

_MENU_TEXT = "📋 <b>Меню</b> — обери, чим займемось:"


def _user_days_left(inf) -> int | None:
    if not (inf.confirmed and inf.exam_date):
        return None
    try:
        return max(0, (date.fromisoformat(inf.exam_date) - clock.today_local()).days)
    except ValueError:
        return None


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer(_MENU_TEXT, reply_markup=menu_kb())


@router.callback_query(F.data == "menu:home")
async def cb_menu(cb: CallbackQuery) -> None:
    await cb.message.answer(_MENU_TEXT, reply_markup=menu_kb())
    await cb.answer()


async def _render_progress(user_id: int) -> str:
    st = await user_state.load(user_id)
    inf = await access.info(user_id)
    days_left = _user_days_left(inf)
    total_words, due_n = await vocab.counts(user_id, clock.today_local())
    total_sessions, last7 = await progress.counts(user_id)

    exam_line = f"📅 До іспиту: <b>{days_left}</b> днів" if days_left is not None else "📅 Дата іспиту не підтверджена"
    lines = [
        f"📊 <b>Прогрес</b> · рівень <b>{st.level or '—'}</b> · стрік <b>{st.streak}</b> 🔥",
        exam_line,
        f"🏋️ Вправ усього: <b>{total_sessions}</b> · за 7 днів: <b>{last7}</b>",
        f"📚 Слова: <b>{total_words}</b> · на повторення: <b>{due_n}</b>\n",
    ]
    if st.readiness:
        lines.append("<b>Готовність за модулями</b> (мета — 50%, зі стрілкою тренду):")
        for mod in Module:
            pct = st.readiness.get(mod.value, 0)
            mark = "✅" if pct >= 50 else "🔸"
            arrow = progress.trend(await progress.recent_scores(user_id, mod.value))
            lines.append(f"{mark} {MODULE_LABELS[mod]} {arrow}\n  {bar(pct)}")
        lines.append("\n" + progress.projection(st.readiness, days_left is not None, days_left))
    else:
        lines.append("Спершу пройди стартовий тест (/test), щоб я визначив готовність.")

    earned = badges.earned(st.readiness, st.streak, total_sessions)
    if earned:
        lines.append("\n🏅 <b>Бейджі:</b> " + " · ".join(earned))
    return "\n".join(lines)


def _readiness_scene(st, inf) -> tuple[str | None, object | None]:
    """Сцена за станом підготовки: готовий → на іспит (з урахуванням наявної дати);
    incomplete → підказка перевірити решту модулів."""
    status, mods = progress.readiness_verdict(st.readiness)
    note = "\n\n<i>Це наша оцінка за вправами, не офіційна сертифікація.</i>"
    if status == "ready":
        base = "🏆 <b>Схоже, ти на рівні B1!</b>\nЗа нашими вправами всі 5 модулів ≥70%."
        if inf.confirmed and inf.exam_date:
            days = _user_days_left(inf)
            when = exam_dates.label(inf.exam_date) if exam_dates.is_official(inf.exam_date) else inf.exam_date
            tail = f"\n📅 Твій іспит — <b>{when}</b>"
            tail += f" (за <b>{days}</b> дн)" if days is not None else ""
            tail += ". Тримай форму: практикуй і повторюй, щоб прийти впевненим."
            return base + tail + note, None
        upcoming = exam_dates.upcoming(clock.today_local())[:3]
        lst = "\n".join(f"• {exam_dates.label(d)}" for d in upcoming) if upcoming else "—"
        kb = InlineKeyboardBuilder()
        kb.button(text="📅 Вказати дату іспиту", callback_data="onb:setdate")
        kb.adjust(1)
        return (
            base + "\n\n🎯 Час <b>реєструватися на офіційний іспит</b>! Найближчі сесії:\n"
            + lst + "\nКоли зареєструєшся — познач дату 👇" + note,
            kb.as_markup(),
        )
    if status == "incomplete":
        names = ", ".join(MODULE_LABELS[m] for m in mods)
        return f"📋 Щоб побачити повну картину, перевір ще модулі: <b>{names}</b> (по вправі кожного).", None
    return None, None


async def _send_progress(msg: Message, user_id: int) -> None:
    await msg.answer(await _render_progress(user_id), reply_markup=to_menu_kb())
    st = await user_state.load(user_id)
    if st.readiness:  # графік — лише коли є що показати; matplotlib у to_thread (CPU)
        png = await asyncio.to_thread(charts.readiness_bar, st.readiness)
        if png:
            await msg.answer_photo(BufferedInputFile(png, filename="progress.png"))
    inf = await access.info(user_id)
    scene, markup = _readiness_scene(st, inf)
    if scene:
        await msg.answer(scene, reply_markup=markup)


@router.message(Command("postep"))
async def cmd_progress(message: Message) -> None:
    await _send_progress(message, message.from_user.id)


@router.callback_query(F.data == "progress:show")
async def cb_progress(cb: CallbackQuery) -> None:
    await _send_progress(cb.message, cb.from_user.id)
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
