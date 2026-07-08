"""GDPR: /moidane (експорт) + /zapomnij (видалення з підтвердженням). Поза гейтом."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import to_menu_kb
from app.services import gdpr

router = Router()

# Коротке повідомлення при онбордингу (ст. 13 GDPR — прозорість у момент збору даних)
PRIVACY_SHORT = (
    "ℹ️ <i>Зберігаю лише твій ID, дату іспиту та прогрес. Тексти письма й голосові "
    "йдуть на AI-оцінку в Anthropic (США) і не зберігаються. Деталі — /prywatnosc, "
    "видалити свої дані будь-коли — /zapomnij.</i>"
)

# Повне повідомлення про приватність
PRIVACY_NOTICE = (
    "🔐 <b>Приватність і твої дані (GDPR)</b>\n\n"
    "<b>Що зберігаю:</b> Telegram ID та @username, обрану дату іспиту, статус доступу, "
    "прогрес (бали й готовність по модулях) і набір слів для повторень.\n\n"
    "<b>Чого НЕ зберігаю:</b> тексти письма та голосові повідомлення. Вони надсилаються на "
    "оцінку в сервіс <b>Anthropic (США)</b> і одразу відкидаються; голосове видаляється "
    "з сервера відразу після розпізнавання.\n\n"
    "<b>Кому передаю:</b> лише Anthropic — для AI-оцінки твоїх відповідей (США; за умовами "
    "Anthropic дані не використовуються для тренування моделей). Більше нікому.\n\n"
    "<b>Де зберігається:</b> на приватному self-hosted сервері власника бота (він же — "
    "контролер даних).\n\n"
    "<b>Твої права:</b>\n"
    "• /moidane — переглянути всі свої дані\n"
    "• /zapomnij — видалити все безповоротно"
)


def _confirm_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🗑 Так, видалити все", callback_data="gdpr:del")
    kb.button(text="↩️ Скасувати", callback_data="gdpr:cancel")
    kb.adjust(1)
    return kb.as_markup()


@router.message(Command("prywatnosc"))
async def cmd_privacy(message: Message) -> None:
    await message.answer(PRIVACY_NOTICE, reply_markup=to_menu_kb())


@router.message(Command("moidane"))
async def cmd_export(message: Message) -> None:
    await message.answer(await gdpr.export_data(message.from_user.id), reply_markup=to_menu_kb())


@router.message(Command("zapomnij"))
async def cmd_forget(message: Message) -> None:
    await message.answer(
        "⚠️ Видалити <b>ВСІ</b> твої дані (прогрес, доступ, історія вправ)? Це незворотно.",
        reply_markup=_confirm_kb(),
    )


@router.callback_query(F.data == "gdpr:del")
async def cb_delete(cb: CallbackQuery) -> None:
    await gdpr.delete_data(cb.from_user.id)
    await cb.answer("Видалено")
    await cb.message.answer("🗑 Усі твої дані видалено. Щоб почати знову — /start.")


@router.callback_query(F.data == "gdpr:cancel")
async def cb_cancel(cb: CallbackQuery) -> None:
    await cb.answer("Скасовано")
    await cb.message.answer("Ок, нічого не видалено 🙂", reply_markup=to_menu_kb())
