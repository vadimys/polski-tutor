"""Онбординг + контроль доступу: /start, вибір дати, запит доступу, зв'язок з адміном."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import (
    admin_extend_kb,
    admin_teacher_kb,
    approved_kb,
    contact_admin_kb,
    exam_dates_kb,
    extend_request_kb,
    role_choice_kb,
    send_request_kb,
    to_menu_kb,
)
from app.config import settings
from app.handlers.privacy import PRIVACY_SHORT
from app.services import access, clock, exam_dates, vocab

router = Router()


class Onb(StatesGroup):
    contact = State()
    teacher_app = State()  # очікуємо текст заявки викладача


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


async def _try_referral(message: Message, uid: int, payload: str) -> bool:
    """Учень за посиланням викладача (payload='t<teacher_id>') → авто-trial. True якщо спрацювало."""
    teacher_id = access.parse_referral(payload)
    if teacher_id is None or teacher_id == uid or not await access.is_teacher(teacher_id):
        return False  # не викладач / сам себе — ігноруємо
    until = await access.grant_trial(
        uid, message.from_user.username or "", teacher_id, settings.trial_days
    )
    await vocab.seed_if_empty(uid, clock.today_local())
    await message.answer(
        f"Cześć! 👋 Тебе запросив викладач — тобі відкрито <b>безкоштовний доступ на "
        f"{settings.trial_days} днів</b> (до <b>{until}</b>).\n"
        "<i>Твій викладач бачитиме твій прогрес, щоб допомагати.</i>\n\n"
        "Почнемо зі стартового тесту 👇",
        reply_markup=approved_kb(),
    )
    if teacher_id:  # сповістити викладача про нового учня
        name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
        try:
            await message.bot.send_message(teacher_id, f"🎉 Новий учень долучився за твоїм посиланням: {html.escape(name)}")
        except Exception:  # noqa: BLE001
            pass
    return True


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, command: CommandObject) -> None:
    await state.clear()
    uid = message.from_user.id
    inf = await access.info(uid)
    if uid == settings.admin_id:
        await _approved_welcome(message, uid)
    elif access.is_expired(inf, clock.today_local()):
        await message.answer(
            "⏳ <b>Твій безкоштовний період завершився.</b>\n"
            "Сподіваюсь, бот був корисний! Щоб продовжити підготовку — попроси продовження "
            "доступу (скоро зʼявиться підписка).",
            reply_markup=extend_request_kb(),
        )
    elif inf.status == "approved":
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
    elif await _try_referral(message, uid, (command.args or "").strip()):
        return  # новий учень за реферальним посиланням — доступ уже відкрито
    else:  # новий без реферала → розвилка ролі
        await message.answer(
            "Cześć! 👋 Я тренер польської до державного іспиту <b>B1</b>.\n\n"
            "Хто ти?\n"
            "🎓 <b>Учень</b> — готуєшся до іспиту (персональний план, усі 5 модулів).\n"
            "👩‍🏫 <b>Викладач</b> — навчаєш учнів (безкоштовний доступ + запросиш свій клас).\n\n"
            f"{PRIVACY_SHORT}",
            reply_markup=role_choice_kb(),
        )


@router.callback_query(F.data == "onb:role:student")
async def cb_role_student(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await cb.message.answer(
        "🎓 Чудово! Спершу скажи, <b>коли твій іспит</b> (лише офіційні сесії Держкомісії) — "
        "щоб скласти план і надіслати запит на доступ:",
        reply_markup=_date_kb(),
    )


@router.callback_query(F.data == "onb:role:teacher")
async def cb_role_teacher(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Onb.teacher_app)
    await cb.answer()
    await cb.message.answer(
        "👩‍🏫 <b>Заявка викладача</b>\n\n"
        "Розкажи коротко про себе <b>одним повідомленням</b>:\n"
        "• ім'я;\n"
        "• де навчаєш (школа / платформа, напр. Preply/iTalki, або лінк на профіль);\n"
        "• скількох учнів готуєш до B1.\n\n"
        "Після схвалення відкрию безкоштовний доступ і дам твоє <b>реферальне посилання</b> для учнів.",
    )


@router.message(Onb.teacher_app, F.text, ~F.text.startswith("/"))
async def on_teacher_app(message: Message, state: FSMContext) -> None:
    await state.clear()
    uid = message.from_user.id
    username = message.from_user.username or ""
    await access.request_teacher(uid, username)
    await message.answer(
        "✅ Заявку надіслано! Щойно адмін підтвердить — відкрию доступ і дам твоє "
        "реферальне посилання для учнів.",
        reply_markup=contact_admin_kb(),
    )
    if settings.admin_id:
        name = f"@{username}" if username else (message.from_user.full_name or str(uid))
        await message.bot.send_message(
            settings.admin_id,
            f"👩‍🏫 <b>Заявка ВИКЛАДАЧА</b>\nКористувач: {html.escape(name)} (id <code>{uid}</code>)\n\n"
            f"{html.escape(message.text)}",
            reply_markup=admin_teacher_kb(uid),
        )


@router.callback_query(F.data == "onb:restart")
async def cb_restart(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await cb.message.answer("Коли твій іспит?", reply_markup=_date_kb())


async def _confirm(message: Message, iso: str, confirmed: bool) -> None:
    await message.answer(
        f"📅 Дата іспиту: <b>{_fmt(iso, confirmed)}</b>\n\n"
        f"Відкрию тобі <b>{settings.organic_trial_days} днів безкоштовно</b> — почнемо?",
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
        f"❔ Дату вкажеш пізніше. Відкрию тобі <b>{settings.organic_trial_days} днів "
        "безкоштовно</b> — за цей час зареєструйся на іспит і познач дату "
        "(«📅 Вказати дату іспиту»). Почнемо?",
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
        + (f"\nДоступ активний до <b>{until}</b>." if until else ""),
        reply_markup=to_menu_kb(),
    )


@router.callback_query(F.data == "onb:send")
async def cb_send(cb: CallbackQuery, state: FSMContext) -> None:
    """Органічний учень → авто-trial БЕЗ черги (self-serve freemium). Адмін лише інформується."""
    data = await state.get_data()
    exam_date = data.get("exam_date", "")
    confirmed = bool(data.get("confirmed", False))
    uid = cb.from_user.id
    username = cb.from_user.username or ""
    until = await access.grant_trial(
        uid, username, 0, settings.organic_trial_days, exam_date, confirmed
    )
    await vocab.seed_if_empty(uid, clock.today_local())
    await state.clear()
    await cb.answer()
    await cb.message.answer(
        f"🚀 <b>Доступ відкрито — {settings.organic_trial_days} днів безкоштовно!</b> "
        f"(до <b>{until}</b>)\nПочнемо зі стартового тесту 👇",
        reply_markup=approved_kb(),
    )
    if settings.admin_id:  # інформуємо (без схвалення — доступ уже відкрито)
        name = f"@{username}" if username else (cb.from_user.full_name or str(uid))
        await cb.bot.send_message(
            settings.admin_id,
            f"🆕 <b>Новий учень (self-serve trial)</b>: {html.escape(name)} "
            f"(id <code>{uid}</code>) · дата: <b>{_fmt(exam_date, confirmed)}</b> · до {until}",
        )


@router.callback_query(F.data == "onb:extend")
async def cb_extend(cb: CallbackQuery) -> None:
    """Учень просить продовження після trial → у чергу до адміна (місток до підписки)."""
    await cb.answer()
    uid = cb.from_user.id
    username = cb.from_user.username or ""
    await cb.message.answer("📨 Запит на продовження надіслано. Щойно вирішу — сповіщу 🙂")
    if settings.admin_id:
        name = f"@{username}" if username else (cb.from_user.full_name or str(uid))
        await cb.bot.send_message(
            settings.admin_id,
            f"🔓 <b>Запит на ПРОДОВЖЕННЯ</b> (trial вичерпано)\n{html.escape(name)} "
            f"(id <code>{uid}</code>)",
            reply_markup=admin_extend_kb(uid),
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
