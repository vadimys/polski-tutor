"""Зовнішній dead-man's-switch: періодичний пінг healthchecks.io.

Внутрішній /health бачить лише коли бот живий. Якщо ляже ВЕСЬ хост (або бот
зависне) — нікому сказати. Тому бот сам пінгує зовнішній сервіс що `heartbeat_secs`:
пінги припинились > періоду → сервіс алертить (email/Telegram/пуш). При degraded
(db/redis лежить) шлемо `/fail` — алерт навіть коли процес ще живий.
"""

from __future__ import annotations

import asyncio
import logging

import aiohttp

from app.config import settings
from app.health import check

logger = logging.getLogger(__name__)


def _fail_url(url: str) -> str:
    """healthchecks.io: сигнал провалу — суфікс /fail до ping-URL."""
    return url.rstrip("/") + "/fail"


async def _ping(session: aiohttp.ClientSession, url: str) -> None:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            await resp.read()
    except Exception:  # noqa: BLE001 — heartbeat не має валити бота
        logger.debug("heartbeat ping failed", exc_info=True)


async def loop() -> None:
    """Пінгувати healthchecks.io що heartbeat_secs (success або /fail за станом)."""
    if not settings.healthcheck_url:
        return  # вимкнено — не запускаємо
    ok_url = settings.healthcheck_url
    fail_url = _fail_url(ok_url)
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                ok, _ = await check()
                await _ping(session, ok_url if ok else fail_url)
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001
                logger.exception("heartbeat loop error")
            await asyncio.sleep(settings.heartbeat_secs)
