"""Захист від випадкового подвійного тапу по одній кнопці.

Якщо той самий користувач тисне ту саму кнопку (callback_data) двічі за коротке
вікно — другий тап тихо гаситься (частий кейс: фет-фінгер / лаг мережі → подвійна
дія/повідомлення). Вікно мале (0.4с), щоб не заважати швидкій навігації (Далі-Далі).
Стан у пам'яті (бот — один процес); періодичне прибирання старих ключів.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

_WINDOW = 0.4  # с — коротке вікно дедуплікації подвійного тапу
_MAX = 2000  # поріг очищення словника


class DebounceMiddleware(BaseMiddleware):
    """Реєструється на callback_query; качино читає from_user/data (легко тестувати)."""

    def __init__(self) -> None:
        self._seen: dict[tuple[int, str], float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        uid = getattr(getattr(event, "from_user", None), "id", None)
        cbdata = getattr(event, "data", None)
        if uid is None or cbdata is None:  # не callback — не чіпаємо
            return await handler(event, data)
        key = (uid, cbdata)
        now = time.monotonic()
        if now - self._seen.get(key, 0.0) < _WINDOW:
            answer = getattr(event, "answer", None)
            if answer:
                await answer()  # тихо ковтаємо дубль
            return None
        self._seen[key] = now
        if len(self._seen) > _MAX:  # прибрати старі записи
            cutoff = now - _WINDOW * 5
            self._seen = {k: v for k, v in self._seen.items() if v > cutoff}
        return await handler(event, data)
