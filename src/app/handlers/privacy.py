"""GDPR: /moidane (експорт) + /zapomnij (видалення з підтвердженням). Поза гейтом."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.services import gdpr

router = Router()


def _confirm_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🗑 Так, видалити все", callback_data="gdpr:del")
    kb.button(text="↩️ Скасувати", callback_data="gdpr:cancel")
    kb.adjust(1)
    return kb.as_markup()


@router.message(Command("moidane"))
async def cmd_export(message: Message) -> None:
    await message.answer(await gdpr.export_data(message.from_user.id))


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
    await cb.message.answer("Ок, нічого не видалено 🙂")
