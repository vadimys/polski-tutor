"""Глобальний обробник помилок: лог + алерт адміну + вибачення користувачу."""

from __future__ import annotations

import html
import logging

from aiogram import Bot
from aiogram.types import ErrorEvent
from redis.asyncio import Redis

from app.config import settings
from app.services import alerts

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


def _where(event: ErrorEvent) -> str:
    """Контекст тригера (що саме викликало) — для деталізації алерту."""
    upd = event.update
    if upd.message:
        return f'повідомлення "{(upd.message.text or upd.message.content_type or "?")[:60]}"'
    if upd.callback_query:
        return f'кнопка "{(upd.callback_query.data or "?")[:60]}"'
    return "update"


async def on_error(event: ErrorEvent, bot: Bot) -> bool:
    exc = event.exception
    uid = _uid(event)
    logger.exception("Unhandled error (uid=%s): %s", uid, exc)

    # детальний алерт у спільний канал (окремий бот) — НЕ користувачу; з тротлінгом
    if await _should_alert(type(exc).__name__):
        detail = (
            "⚠️ <b>Помилка бота</b>\n"
            f"Тип: <code>{type(exc).__name__}</code>\n"
            f"Опис: <code>{html.escape(str(exc)[:300])}</code>\n"
            f"Хто: uid <code>{uid}</code>\n"
            f"Де: {html.escape(_where(event))}"
        )
        await alerts.send(detail, fallback_bot=bot)

    # людське вибачення користувачу (якщо є куди відповісти)
    upd = event.update
    target = upd.message or (upd.callback_query.message if upd.callback_query else None)
    if target is not None:
        try:
            await target.answer("Ой, щось пішло не так 😕 Уже розбираюсь. Спробуй ще раз.")
        except Exception:  # noqa: BLE001
            pass
    return True
