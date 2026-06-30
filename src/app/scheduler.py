"""Щоденне нагадування о LESSON_HOUR (локальний пояс) — простий in-process цикл.

Для одного-кількох користувачів цього досить; окремий воркер/cron не потрібен.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from aiogram import Bot

from app.bot.keyboards import lesson_kb
from app.config import settings
from app.services import clock, state

logger = logging.getLogger(__name__)

_NUDGE = (
    "🌅 <b>Dzień dobry!</b> Час для польської — 1 урок наближає тебе до B1.\n"
    "Натисни нижче або введи /lekcja 👇"
)


async def _seconds_until_next() -> float:
    now = clock.now_local()
    target = now.replace(hour=settings.lesson_hour, minute=0, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


async def daily_nudge_loop(bot: Bot) -> None:
    while True:
        try:
            await asyncio.sleep(await _seconds_until_next())
            user_ids = await state.all_user_ids()
            logger.info("Daily nudge → %d users", len(user_ids))
            for uid in user_ids:
                try:
                    await bot.send_message(uid, _NUDGE, reply_markup=lesson_kb())
                except Exception:
                    logger.exception("nudge failed uid=%s", uid)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("nudge loop error; retry in 60s")
            await asyncio.sleep(60)
