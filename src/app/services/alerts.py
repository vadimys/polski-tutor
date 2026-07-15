"""Централізований канал інфра-алертів.

Усі технічні алерти (помилки бота, бюджет AI, тощо) йдуть в ОДИН приватний Telegram-канал
через ОКРЕМИЙ alerts-бот — НІКОЛИ в чат продукт-бота й тим паче не користувачам.
Кожне повідомлення тегнуте проєктом. Порожні alert_bot_token/alert_chat_id → фолбек на
DM адміну через продукт-бота (перехідний період, поки канал не налаштовано)."""

from __future__ import annotations

import logging
from contextlib import suppress

import aiohttp
from aiogram import Bot

from app.config import settings

logger = logging.getLogger(__name__)

PROJECT = "polski-b1"  # тег проєкту в кожному алерті (спільний канал на кілька проєктів)


async def send(text: str, *, fallback_bot: Bot | None = None) -> None:
    """Надіслати інфра-алерт у спільний канал (окремий бот). Фолбек — DM адміну."""
    body = f"🔧 <b>[{PROJECT}]</b>\n{text}"
    if settings.alert_bot_token and settings.alert_chat_id:
        url = f"https://api.telegram.org/bot{settings.alert_bot_token}/sendMessage"
        payload = {"chat_id": settings.alert_chat_id, "text": body, "parse_mode": "HTML"}
        try:
            async with aiohttp.ClientSession() as s, s.post(
                url, json=payload, timeout=aiohttp.ClientTimeout(total=10)
            ) as r:
                if r.status == 200:
                    return
                logger.warning("alert send HTTP %s: %s", r.status, (await r.text())[:200])
        except Exception:
            logger.exception("alert send failed")
    # фолбек: продукт-бот → адмін (лише якщо канал ще не налаштовано або збій)
    if fallback_bot is not None and settings.admin_id:
        with suppress(Exception):
            await fallback_bot.send_message(settings.admin_id, body)
