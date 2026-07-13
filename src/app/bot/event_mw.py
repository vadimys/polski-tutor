"""Middleware: трекінг використання фіч (для адмін-аналітики).

Вішається на dp (усі повідомлення/callback). Записує лише НАЗВУ фічі; ніколи не
ламає обробку (усе в suppress). Адміна пропускаємо (не спотворюємо статистику).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from contextlib import suppress
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.config import settings
from app.services import events


class EventMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is not None and user.id != settings.admin_id:
            raw = None
            if isinstance(event, Message):
                raw = event.text
            elif isinstance(event, CallbackQuery):
                raw = event.data
            if raw:
                with suppress(Exception):
                    await events.track(user.id, raw)
        return await handler(event, data)
