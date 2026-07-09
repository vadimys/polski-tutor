"""Сумісний фасад над реєстром офіційного контенту (app.content).

Історично тут жив god-module з питаннями. Тепер контент — у пакеті `app.content`
(реєстр тестів). Цей модуль лишає стабільний API для drills/placement/mock-хендлера:
section_items(section) — АГРЕГАТ усіх офіційних тестів (пул варіативності).
Повний мок /egzamin бере ОДИН тест напряму з app.content.
"""

from __future__ import annotations

from app import content
from app.content.schema import MCQItem

MockItem = MCQItem  # зворотна сумісність (старий тип)


def section_items(section: str) -> list[MCQItem]:
    return content.all_items(section)


# лишаємо для тестів/статистики — усі питання всіх тестів
ITEMS: list[MCQItem] = content.all_items_flat()
