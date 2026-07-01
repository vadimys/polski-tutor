"""Онбординг + контроль доступу: /start, вибір дати, запит доступу, зв'язок з адміном."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import (
    admin_decision_kb,
    approved_kb,
    contact_admin_kb,
    exam_dates_kb,
    send_request_kb,
)
from app.config import settings
from app.handlers.privacy import PRIVACY_SHORT
from app.services import access, clock, exam_dates, vocab

router = Router()


class Onb(StatesGroup):
    contact = State()


def _fmt(iso: str, confirmed: bool) -> str:
    return exam_dates.label(iso) if (confirmed and iso) else "ще не підтверджена"


def _date_kb():
    return exam_dates_kb(exam_dates.upcoming(clock.today_local()), "onb:date", with_unconfirmed=True)


async def _approved_welcome(message: Message, user_id: int) -> None:
    await vocab.seed_if_empty(user_id, clock.today_local())
    await message.answer(
        f"Cześć! 👋 Доступ активний. До іспиту <b>{clock.days_to_exam()}</b> днів.\n"
        "Почнемо зі стартового тесту або обери в меню 👇",
        reply_markup=approved_kb(),
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    uid = message.from_user.id
    inf = await access.info(uid)
    if uid == settings.admin_id or inf.status == "approved":
        await _approved_welcome(message, uid)
    elif inf.status == "pending":
        await message.answer(
            "⏳ Твій запит на розгляді. Щойно адмін вирішить — сповіщу.",
            reply_markup=contact_admin_kb(),
        )
    elif inf.status == "denied":
        await message.answer(
            "🚫 На жаль, доступ відхилено. Можеш написати адміну.",
            reply_markup=contact_admin_kb(),
        )
    else:  # новий
        await message.answer(
            "Cześć! 👋 Я твій тренер польської до державного іспиту <b>B1</b>.\n\n"
            "Спершу скажи, <b>коли твій іспит</b> (лише офіційні сесії Держкомісії) — "
            "щоб скласти план і надіслати запит на доступ:\n\n"
            f"{PRIVACY_SHORT}",
            reply_markup=_date_kb(),
        )


@router.callback_query(F.data == "onb:restart")
async def cb_restart(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await cb.message.answer("Коли твій іспит?", reply_markup=_date_kb())


async def _confirm(message: Message, iso: str, confirmed: bool) -> None:
    await message.answer(
        f"📅 Дата іспиту: <b>{_fmt(iso, confirmed)}</b>\n\nНадіслати запит на доступ адміну?",
        reply_markup=send_request_kb(),
    )


@router.callback_query(F.data.startswith("onb:date:"))
async def cb_date(cb: CallbackQuery, state: FSMContext) -> None:
    iso = cb.data.split(":", 2)[2]
    if not exam_dates.is_official(iso):  # захист: лише офіційні дати
        await cb.answer("Оберіть офіційну дату зі списку.", show_alert=True)
        return
    await state.update_data(exam_date=iso, confirmed=True)
    await cb.answer()
    await _confirm(cb.message, iso, True)


@router.callback_query(F.data == "onb:unconfirmed")
async def cb_unconfirmed(cb: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(exam_date="", confirmed=False)
    await cb.answer()
    await cb.message.answer(
        "❔ Дата ще не підтверджена → доступ на <b>6 місяців</b>. За цей час зареєструйся "
        "на іспит і познач дату («📅 Вказати дату іспиту») — якщо вона далі, доступ подовжимо.\n\n"
        "Надіслати запит адміну?",
        reply_markup=send_request_kb(),
    )


# --- Оновлення/підтвердження дати іспиту (для схвалених) ---
@router.callback_query(F.data == "onb:setdate")
async def cb_setdate(cb: CallbackQuery) -> None:
    await cb.answer()
    await cb.message.answer(
        "Обери офіційну дату свого іспиту:",
        reply_markup=exam_dates_kb(exam_dates.upcoming(clock.today_local()), "onb:exam"),
    )


@router.callback_query(F.data.startswith("onb:exam:"))
async def cb_examdate(cb: CallbackQuery) -> None:
    iso = cb.data.split(":", 2)[2]
    if not exam_dates.is_official(iso):
        await cb.answer("Оберіть офіційну дату зі списку.", show_alert=True)
        return
    until = await access.set_exam_date(cb.from_user.id, iso)
    await cb.answer()
    await cb.message.answer(
        f"✅ Дату іспиту збережено: <b>{exam_dates.label(iso)}</b>."
        + (f"\nДоступ активний до <b>{until}</b>." if until else "")
    )


@router.callback_query(F.data == "onb:send")
async def cb_send(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    exam_date = data.get("exam_date", "")
    confirmed = bool(data.get("confirmed", False))
    uid = cb.from_user.id
    username = cb.from_user.username or ""
    await access.request_access(uid, username, exam_date, confirmed)
    await state.clear()
    await cb.answer()
    await cb.message.answer(
        "✅ Запит надіслано! Щойно адмін вирішить — сповіщу. Можеш поки написати йому.",
        reply_markup=contact_admin_kb(),
    )
    if settings.admin_id:
        name = f"@{username}" if username else (cb.from_user.full_name or str(uid))
        await cb.bot.send_message(
            settings.admin_id,
            f"📨 <b>Запит на доступ</b>\nКористувач: {html.escape(name)} (id <code>{uid}</code>)\n"
            f"Дата іспиту: <b>{_fmt(exam_date, confirmed)}</b>",
            reply_markup=admin_decision_kb(uid),
        )


@router.callback_query(F.data == "onb:contact")
async def cb_contact(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Onb.contact)
    await cb.answer()
    await cb.message.answer("✍️ Напиши повідомлення для адміна одним повідомленням:")


@router.message(Onb.contact, F.text, ~F.text.startswith("/"))
async def on_contact(message: Message, state: FSMContext) -> None:
    await state.clear()
    uid = message.from_user.id
    username = message.from_user.username or ""
    name = f"@{username}" if username else (message.from_user.full_name or str(uid))
    if settings.admin_id:
        await message.bot.send_message(
            settings.admin_id,
            f"✉️ <b>Повідомлення від</b> {html.escape(name)} (id <code>{uid}</code>):\n"
            f"{html.escape(message.text)}\n\n<i>Відповісти: /reply {uid} текст</i>",
        )
    await message.answer("📨 Надіслано адміну. Дякую!")
