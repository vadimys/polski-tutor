"""Підписка через Telegram Stars (XTR).

Флоу: /subskrypcja або кнопка → send_invoice(XTR) → pre_checkout(ok) →
successful_payment → продовжуємо доступ (billing.apply_subscription) + сповіщаємо
учня й (якщо приведений) викладача. Хендлери — ПОЗА access-гейтом (платити може
й той, у кого trial завершився).
"""

from __future__ import annotations

import logging
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

from app.bot.keyboards import approved_kb
from app.config import settings
from app.services import billing

router = Router()
logger = logging.getLogger(__name__)

_PAYLOAD = "sub"  # ідентифікатор інвойсу підписки


async def _send_invoice(message: Message) -> None:
    await message.answer_invoice(
        title="Підписка Polski B1 Coach",
        description=(
            f"Повний доступ до всіх 5 модулів на {settings.sub_days} днів: "
            "аудіо, читання, граматика, письмо й мовлення з фідбеком."
        ),
        payload=_PAYLOAD,
        currency="XTR",  # Telegram Stars
        prices=[LabeledPrice(label=f"{settings.sub_days} днів доступу", amount=settings.sub_stars)],
    )


async def _offer(message: Message) -> None:
    await message.answer(
        f"💎 <b>Підписка</b> — {settings.sub_stars} ⭐ за {settings.sub_days} днів повного доступу.\n"
        "Оплата через Telegram Stars (⭐). Тисни кнопку оплати нижче 👇"
    )
    await _send_invoice(message)


@router.message(Command("subskrypcja"))
async def cmd_subscribe(message: Message) -> None:
    await _offer(message)


@router.callback_query(F.data == "pay:start")
async def cb_subscribe(cb: CallbackQuery) -> None:
    await cb.answer()
    await _offer(cb.message)


@router.pre_checkout_query()
async def on_pre_checkout(pcq: PreCheckoutQuery) -> None:
    # для Stars-товару просто підтверджуємо; валідних сценаріїв відмови нема
    await pcq.answer(ok=True)


@router.message(F.successful_payment)
async def on_paid(message: Message) -> None:
    sp = message.successful_payment
    uid = message.from_user.id
    stars = sp.total_amount  # у Stars = кількість ⭐
    charge = sp.telegram_payment_charge_id
    try:
        until = await billing.apply_subscription(uid, settings.sub_days, stars, charge)
    except Exception:
        # оплату отримано, але доступ не продовжився — НЕ брешемо про успіх, кличемо адміна
        logger.exception("payment grant FAILED uid=%s stars=%s charge=%s", uid, stars, charge)
        await message.answer(
            "✅ Оплату отримано, але сталася технічна затримка з активацією. "
            "Уже розбираюсь — доступ відкрию найближчим часом 🙏"
        )
        if settings.admin_id:
            with suppress(Exception):
                await message.bot.send_message(
                    settings.admin_id,
                    f"🆘 <b>ОПЛАТА БЕЗ АКТИВАЦІЇ</b> uid <code>{uid}</code> · {stars}⭐ · "
                    f"charge <code>{charge}</code> — активувати вручну!",
                )
        return
    await message.answer(
        f"✅ <b>Дякуємо! Підписку активовано</b> до <b>{until}</b>.\n"
        "Повний доступ відкрито — продовжуймо підготовку 👇",
        reply_markup=approved_kb(),
    )
    logger.info("payment ok uid=%s stars=%s until=%s", uid, stars, until)
    # сповістити викладача, якщо учень приведений (референс-бонус/атрибуція)
    teacher_id = await billing.referrer_of(uid)
    if teacher_id:
        name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
        try:
            await message.bot.send_message(
                teacher_id,
                f"🎉 Твій учень {name} оформив підписку — дякуємо, що приводиш клас! "
                "Деталі — у /uczniowie.",
            )
        except Exception:  # noqa: BLE001
            pass
    # сповістити адміна (облік)
    if settings.admin_id:
        try:
            await message.bot.send_message(
                settings.admin_id, f"💰 Оплата: uid <code>{uid}</code> · {stars} ⭐ · до {until}"
            )
        except Exception:  # noqa: BLE001
            pass
