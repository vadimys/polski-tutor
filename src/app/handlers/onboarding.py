"""Онбординг + контроль доступу: /start, вибір дати, запит доступу, зв'язок з адміном."""

from __future__ import annotations

import html
from datetime import date

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import (
    admin_decision_kb,
    approved_kb,
    contact_admin_kb,
    onboarding_date_kb,
    send_request_kb,
)
from app.config import settings
from app.services import access, clock, vocab

router = Router()


class Onb(StatesGroup):
    other_date = State()
    contact = State()


def _fmt(iso: str, confirmed: bool) -> str:
    return iso if (confirmed and iso) else "ще не підтверджена"


def _parse_date(text: str) -> str:
    """Приймає РРРР-ММ-ДД або ДД.ММ.РРРР → ISO або '' якщо не розпізнано/не майбутнє."""
    t = text.strip()
    parsed: date | None = None
    try:
        parsed = date.fromisoformat(t)
    except ValueError:
        parts = t.replace("/", ".").split(".")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            d, m, y = parts
            try:
                parsed = date(int(y), int(m), int(d))
            except ValueError:
                parsed = None
    if parsed is None or parsed <= clock.today_local():
        return ""
    return parsed.isoformat()


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
            "Спершу скажи, <b>коли твій іспит</b> — щоб скласти план і надіслати запит на доступ:",
            reply_markup=onboarding_date_kb(),
        )


@router.callback_query(F.data == "onb:restart")
async def cb_restart(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await cb.message.answer("Коли твій іспит?", reply_markup=onboarding_date_kb())


async def _confirm(message: Message, iso: str, confirmed: bool) -> None:
    await message.answer(
        f"📅 Дата іспиту: <b>{_fmt(iso, confirmed)}</b>\n\nНадіслати запит на доступ адміну?",
        reply_markup=send_request_kb(),
    )


@router.callback_query(F.data.startswith("onb:date:"))
async def cb_date(cb: CallbackQuery, state: FSMContext) -> None:
    iso = cb.data.split(":", 2)[2]
    await state.update_data(exam_date=iso, confirmed=True)
    await cb.answer()
    await _confirm(cb.message, iso, True)


@router.callback_query(F.data == "onb:unconfirmed")
async def cb_unconfirmed(cb: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(exam_date="", confirmed=False)
    await cb.answer()
    await _confirm(cb.message, "", False)


@router.callback_query(F.data == "onb:other")
async def cb_other(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Onb.other_date)
    await cb.answer()
    await cb.message.answer("Введи дату іспиту: <b>РРРР-ММ-ДД</b> (напр. 2026-12-05) або ДД.ММ.РРРР:")


@router.message(Onb.other_date, F.text)
async def on_other_date(message: Message, state: FSMContext) -> None:
    iso = _parse_date(message.text)
    if not iso:
        await message.answer("Не зрозумів дату 😕 Формат: 2026-12-05 (майбутня). Спробуй ще:")
        return
    await state.set_state(None)
    await state.update_data(exam_date=iso, confirmed=True)
    await _confirm(message, iso, True)


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
