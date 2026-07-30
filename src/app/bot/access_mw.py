"""Middleware: пускає до навчальних розділів лише користувачів із доступом.

Вішається на групу навчальних роутерів. Онбординг/адмін/оплата — поза гейтом.
Той, у кого закінчився trial/підписка, бачить ЧЕСНИЙ текст із кнопкою оплати
(а не «надішли запит адміну»); повне повідомлення тротлиться 1/хв (анти-спам).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from redis.asyncio import Redis

from app.config import settings
from app.services import access, clock

_BLOCKED = "🔒 Доступ ще не відкрито. Натисни /start, щоб надіслати запит адміну."
_EXPIRED = (
    "⏳ Безкоштовний період завершився, тому вправи зараз закриті.\n"
    "Твій прогрес збережено!"
)
_EXPIRED_ALERT = "⏳ Доступ завершився. Прогрес збережено — дивись повідомлення нижче 👇"

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def _once_per_minute(uid: int) -> bool:
    """Анти-спам: повне повідомлення з кнопками — не частіше 1/хв на користувача."""
    return bool(await _r().set(f"blockedmsg:{uid}", "1", nx=True, ex=60))


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

        # немає доступу — розрізняємо «закінчився» (був approved) від «ще не відкрито»
        expired = False
        if user is not None:
            inf = await access.info(user.id)
            expired = access.is_expired(inf, clock.today_local())

        if expired:
            from app.bot.keyboards import extend_request_kb  # ліниво — без циклів імпорту

            msg = event.message if isinstance(event, CallbackQuery) else event
            if isinstance(event, CallbackQuery):
                await event.answer(_EXPIRED_ALERT)
            if isinstance(msg, Message) and await _once_per_minute(user.id):
                await msg.answer(_EXPIRED, reply_markup=extend_request_kb())
            return None

        if isinstance(event, CallbackQuery):
            await event.answer(_BLOCKED, show_alert=True)
        elif isinstance(event, Message):
            await event.answer(_BLOCKED)
        return None
