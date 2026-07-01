"""Middleware: пускає до навчальних розділів лише користувачів із доступом.

Вішається на групу навчальних роутерів. Онбординг/адмін-роутери — поза гейтом.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.config import settings
from app.services import access

_BLOCKED = "🔒 Доступ ще не відкрито. Натисни /start, щоб надіслати запит адміну."


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is not None and await access.is_allowed(user.id, settings.admin_id):
            return await handler(event, data)
        # немає доступу — блокуємо навчальні дії
        if isinstance(event, CallbackQuery):
            await event.answer(_BLOCKED, show_alert=True)
        elif isinstance(event, Message):
            await event.answer(_BLOCKED)
        return None
