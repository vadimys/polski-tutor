"""Точка входу: aiogram-бот (long polling) + щоденне нагадування."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand

from app.bot.access_mw import AccessMiddleware
from app.config import settings
from app.db.migrate_legacy import migrate_from_redis
from app.handlers import (
    admin,
    drills,
    errors,
    lesson,
    listening,
    menu,
    mock,
    onboarding,
    placement,
    plan,
    review,
    speaking,
    start,
    writing,
)
from app.scheduler import daily_nudge_loop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

COMMANDS = [
    BotCommand(command="start", description="Головна + рівень"),
    BotCommand(command="menu", description="Меню"),
    BotCommand(command="lekcja", description="Почати урок"),
    BotCommand(command="pisanie", description="Письмо (з фідбеком)"),
    BotCommand(command="mowienie", description="Мовлення (голосове + фідбек)"),
    BotCommand(command="opis", description="Опис фотографії (Zadanie 1)"),
    BotCommand(command="sluchanie", description="Аудіювання (запис + питання)"),
    BotCommand(command="mok", description="Офіційний МОК (читання/граматика)"),
    BotCommand(command="trening", description="Тренування (граматика/читання)"),
    BotCommand(command="powtorki", description="Повторення слів (SRS)"),
    BotCommand(command="postep", description="Мій прогрес"),
    BotCommand(command="plan", description="Мій план підготовки"),
    BotCommand(command="test", description="Стартовий тест"),
    BotCommand(command="pomoc", description="Довідка"),
]


async def main() -> None:
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=RedisStorage.from_url(settings.redis_url))
    dp.errors.register(errors.on_error)  # глобальний обробник помилок → алерт адміну

    # Поза гейтом: онбординг (/start, запит доступу), адмін (схвалення), довідка
    dp.include_router(onboarding.router)
    dp.include_router(admin.router)
    dp.include_router(start.router)

    # Навчальні розділи — під access-гейтом (лише схвалені; адмін завжди)
    learning = Router()
    for r in (placement, lesson, writing, drills, review, speaking, listening, mock, plan, menu):
        learning.include_router(r.router)
    learning.message.middleware(AccessMiddleware())
    learning.callback_query.middleware(AccessMiddleware())
    dp.include_router(learning)

    migrated = await migrate_from_redis()
    if migrated:
        logger.info("Мігровано %d користувачів Redis→Postgres", migrated)

    await bot.set_my_commands(COMMANDS)
    logger.info(
        "Polski B1 Coach запущено. Нагадування о %02d:00 %s",
        settings.lesson_hour,
        settings.timezone,
    )

    nudge_task = asyncio.create_task(daily_nudge_loop(bot))
    try:
        await dp.start_polling(bot)
    finally:
        nudge_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
