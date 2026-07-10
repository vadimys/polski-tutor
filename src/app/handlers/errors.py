"""Глобальний обробник помилок: лог + алерт адміну + вибачення користувачу."""

from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.types import ErrorEvent

from app.config import settings

logger = logging.getLogger(__name__)


def _uid(event: ErrorEvent) -> int | None:
    """Хто спричинив помилку — для кореляції в логах/алертах."""
    upd = event.update
    if upd.message and upd.message.from_user:
        return upd.message.from_user.id
    if upd.callback_query and upd.callback_query.from_user:
        return upd.callback_query.from_user.id
    return None


async def on_error(event: ErrorEvent, bot: Bot) -> bool:
    exc = event.exception
    uid = _uid(event)
    logger.exception("Unhandled error (uid=%s): %s", uid, exc)

    # алерт адміну (без витоку стектрейсу користувачу)
    if settings.admin_id:
        try:
            await bot.send_message(
                settings.admin_id,
                f"⚠️ <b>Помилка бота</b> (uid=<code>{uid}</code>)\n"
                f"<code>{type(exc).__name__}: {str(exc)[:300]}</code>",
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
