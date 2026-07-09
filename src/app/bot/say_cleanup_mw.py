"""Прибирання «застарілого» голосового вимови (🔊) при навігації.

Голосове, надіслане кнопкою 🔊 (say:*), лишалось у чаті, коли користувач рухався
далі (урок → завдання → вправа). Цей middleware на будь-який callback, ОКРІМ самого
say:*, видаляє останнє надіслане голосове — щоб історія не засмічувалась. Дешево:
1 Redis GET (+ рідкісний delete). Bot береться з data (aiogram передає його туди).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.services import tts_say


class SayCleanupMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        cbdata = getattr(event, "data", None)
        msg = getattr(event, "message", None)
        bot = data.get("bot")
        if cbdata and msg is not None and bot is not None and not cbdata.startswith("say:"):
            await tts_say.forget_voice(bot, msg.chat.id)  # рушив далі → прибрати вимову
        return await handler(event, data)
