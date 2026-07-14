"""Глобальний обробник помилок: лог + алерт адміну + вибачення користувачу."""

from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.types import ErrorEvent
from redis.asyncio import Redis

from app.config import settings

logger = logging.getLogger(__name__)

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def _should_alert(kind: str) -> bool:
    """Антиспам: 1 алерт на тип помилки за alert_throttle_secs. Redis лежить → алертимо."""
    try:
        return bool(
            await _r().set(f"alert:err:{kind}", "1", nx=True, ex=settings.alert_throttle_secs)
        )
    except Exception:  # noqa: BLE001
        return True


def _uid(event: ErrorEvent) -> int | None:
    """Хто спричинив помилку — для кореляції в логах/алертах."""
    upd = event.update
    if upd.message and upd.message.from_user:
        return upd.message.from_user.id
    if upd.callback_query and upd.callback_query.from_user:
        return upd.callback_query.from_user.id
    return None


async def on_error(event: ErrorEvent, bot: Bot) -> bool:
    exc = event.exception
    uid = _uid(event)
    logger.exception("Unhandled error (uid=%s): %s", uid, exc)

    # алерт адміну (без витоку стектрейсу користувачу) — з тротлінгом проти спаму під напливом
    if settings.admin_id and await _should_alert(type(exc).__name__):
        try:
            await bot.send_message(
                settings.admin_id,
                f"⚠️ <b>Помилка бота</b> (uid=<code>{uid}</code>)\n"
                f"<code>{type(exc).__name__}: {str(exc)[:300]}</code>",
            )
        except Exception:  # noqa: BLE001
            pass

    # людське вибачення користувачу (якщо є куди відповісти)
    upd = event.update
    target = upd.message or (upd.callback_query.message if upd.callback_query else None)
    if target is not None:
        try:
            await target.answer("Ой, щось пішло не так 😕 Уже розбираюсь. Спробуй ще раз.")
        except Exception:  # noqa: BLE001
            pass
    return True
