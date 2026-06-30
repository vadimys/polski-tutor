"""Точка входу: aiogram-бот (long polling) + щоденне нагадування."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand

from app.config import settings
from app.handlers import (
    drills,
    lesson,
    listening,
    menu,
    placement,
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
    BotCommand(command="sluchanie", description="Аудіювання (запис + питання)"),
    BotCommand(command="trening", description="Тренування (граматика/читання)"),
    BotCommand(command="powtorki", description="Повторення слів (SRS)"),
    BotCommand(command="postep", description="Мій прогрес"),
    BotCommand(command="test", description="Стартовий тест"),
    BotCommand(command="pomoc", description="Довідка"),
]


async def main() -> None:
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=RedisStorage.from_url(settings.redis_url))
    dp.include_router(start.router)
    dp.include_router(placement.router)
    dp.include_router(lesson.router)
    dp.include_router(writing.router)
    dp.include_router(drills.router)
    dp.include_router(review.router)
    dp.include_router(speaking.router)
    dp.include_router(listening.router)
    dp.include_router(menu.router)

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
