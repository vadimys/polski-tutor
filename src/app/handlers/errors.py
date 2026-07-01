"""Глобальний обробник помилок: лог + алерт адміну + вибачення користувачу."""

from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.types import ErrorEvent

from app.config import settings

logger = logging.getLogger(__name__)


async def on_error(event: ErrorEvent, bot: Bot) -> bool:
    exc = event.exception
    logger.exception("Unhandled error: %s", exc)

    # алерт адміну (без витоку стектрейсу користувачу)
    if settings.admin_id:
        try:
            await bot.send_message(
                settings.admin_id,
                f"⚠️ <b>Помилка бота</b>\n<code>{type(exc).__name__}: {str(exc)[:300]}</code>",
            )
        except Exception:  # noqa: BLE001
            pass

    # людське вибачення користувачу (якщо є куди відповісти)
    upd = event.update
    target = upd.message or (upd.callback_query.message if upd.callback_query else None)
    if target is not None:
        try:
            await target.answer("Ой, щось пішло не так 😕 Уже розбираюсь. Спробуй ще раз.")
        except Exception:  # noqa: BLE001
            pass
    return True
