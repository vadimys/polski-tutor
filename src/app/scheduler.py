"""Щоденне нагадування о LESSON_HOUR (локальний пояс) — простий in-process цикл.

Для одного-кількох користувачів цього досить; окремий воркер/cron не потрібен.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import date, timedelta

from aiogram import Bot

from app.bot.keyboards import lesson_kb
from app.config import settings
from app.domain.models import MODULE_LABELS
from app.services import access, clock, state

logger = logging.getLogger(__name__)


async def _seconds_until_next() -> float:
    now = clock.now_local()
    target = now.replace(hour=settings.lesson_hour, minute=0, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


async def _personal_nudge(user_id: int) -> str:
    """Персональне нагадування: фокус на найслабший модуль + днів до іспиту."""
    st = await state.load(user_id)
    weakest = MODULE_LABELS[st.weakest_module()]
    inf = await access.info(user_id)
    tail = ""
    if inf.confirmed and inf.exam_date:
        try:
            days = max(0, (date.fromisoformat(inf.exam_date) - clock.today_local()).days)
            tail = f" До іспиту <b>{days}</b> днів."
        except ValueError:
            tail = ""
    return (
        f"🌅 <b>Dzień dobry!</b> Час для польської.{tail}\n"
        f"Сьогодні підтягнемо: <b>{weakest}</b>. Натисни нижче або /lekcja 👇"
    )


async def daily_nudge_loop(bot: Bot) -> None:
    while True:
        try:
            await asyncio.sleep(await _seconds_until_next())
            user_ids = await state.all_user_ids()
            sent = 0
            for uid in user_ids:
                if not await access.is_allowed(uid, settings.admin_id):
                    continue  # не турбуємо не-схвалених
                try:
                    await bot.send_message(uid, await _personal_nudge(uid), reply_markup=lesson_kb())
                    sent += 1
                except Exception:
                    logger.exception("nudge failed uid=%s", uid)
            logger.info("Daily nudge → %d users", sent)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("nudge loop error; retry in 60s")
            await asyncio.sleep(60)
