"""Anthropic API — тіровано: дешева модель для дрилів, сильна для письма/фідбеку.

Без ключа повертає "" — виклик-сайти показують статичний фолбек.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)

_client = None
_MAX_ATTEMPTS = 3  # 1 спроба + 2 повтори на транзієнтних помилках (429/5xx/timeout)


def enabled() -> bool:
    return bool(settings.anthropic_api_key)


def _c():
    global _client
    if _client is None:
        from anthropic import AsyncAnthropic

        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


async def ask(
    system: str,
    user: str,
    *,
    strong: bool = False,
    max_tokens: int = 1200,
    cache: bool = False,
    label: str = "",
) -> str:
    """Один запит до Claude. strong=True → сильна модель (письмо/фідбек).

    cache=True → системний промпт кешується (prompt caching) — вигідно, коли `system`
    СТАТИЧНИЙ і достатньо великий (мін. ~2048/4096 ток); дає ефект при повторах у вікні 5 хв.
    label → фіча для обліку витрат (services.aicost). Транзієнтні помилки (429/5xx/timeout/
    конект) — до _MAX_ATTEMPTS спроб з backoff. Постійні помилки/вичерпані спроби → "".
    """
    if not enabled():
        return ""
    from anthropic import (
        APIConnectionError,
        APITimeoutError,
        InternalServerError,
        RateLimitError,
    )

    retryable = (RateLimitError, InternalServerError, APITimeoutError, APIConnectionError)
    model = settings.strong_model if strong else settings.cheap_model
    # статичний системний промпт → кешований блок (решта префікса стабільна: без дат/ID)
    system_param = (
        [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        if cache
        else system
    )
    for attempt in range(_MAX_ATTEMPTS):
        try:
            resp = await _c().messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_param,
                messages=[{"role": "user", "content": user}],
            )
            if label:  # облік витрат — best-effort, не валимо основний потік
                try:
                    from app.services import aicost

                    await aicost.record(label, "strong" if strong else "cheap", resp.usage)
                except Exception:  # noqa: BLE001
                    logger.debug("aicost record failed", exc_info=True)
            parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
            return "\n".join(parts).strip()
        except retryable as e:
            if attempt + 1 >= _MAX_ATTEMPTS:
                logger.warning("AI ask вичерпав спроби (model=%s): %s", model, e)
                return ""
            await asyncio.sleep(0.5 * (2**attempt))  # 0.5с, 1с
        except Exception:
            logger.exception("AI ask failed (model=%s)", model)
            return ""
    return ""


async def ask_json(
    system: str,
    user: str,
    schema: dict,
    *,
    strong: bool = False,
    max_tokens: int = 1200,
    cache: bool = False,
    label: str = "",
) -> Any | None:
    """Запит зі structured output (json_schema) — API гарантує валідний JSON за схемою.
    Надійніше за регекс-парсинг «десь у тексті». Повертає розпарсений обʼєкт або None
    (AI вимкнено / збій / неповна відповідь). Модель має підтримувати structured outputs
    (Sonnet 4.6 / Haiku 4.5)."""
    if not enabled():
        return None
    from anthropic import (
        APIConnectionError,
        APITimeoutError,
        InternalServerError,
        RateLimitError,
    )

    retryable = (RateLimitError, InternalServerError, APITimeoutError, APIConnectionError)
    model = settings.strong_model if strong else settings.cheap_model
    system_param: Any = (
        [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        if cache
        else system
    )
    for attempt in range(_MAX_ATTEMPTS):
        try:
            resp = await _c().messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_param,
                messages=[{"role": "user", "content": user}],
                output_config={"format": {"type": "json_schema", "schema": schema}},
            )
            if label:
                try:
                    from app.services import aicost

                    await aicost.record(label, "strong" if strong else "cheap", resp.usage)
                except Exception:  # noqa: BLE001
                    logger.debug("aicost record failed", exc_info=True)
            text = next((b.text for b in resp.content if getattr(b, "type", None) == "text"), "")
            return json.loads(text) if text else None
        except retryable as e:
            if attempt + 1 >= _MAX_ATTEMPTS:
                logger.warning("AI ask_json вичерпав спроби (model=%s): %s", model, e)
                return None
            await asyncio.sleep(0.5 * (2**attempt))
        except Exception:
            logger.exception("AI ask_json failed (model=%s)", model)
            return None
    return None
