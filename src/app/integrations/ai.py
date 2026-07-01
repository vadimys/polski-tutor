"""Anthropic API — тіровано: дешева модель для дрилів, сильна для письма/фідбеку.

Без ключа повертає "" — виклик-сайти показують статичний фолбек.
"""

from __future__ import annotations

import asyncio
import logging

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


async def ask(system: str, user: str, *, strong: bool = False, max_tokens: int = 1200) -> str:
    """Один запит до Claude. strong=True → сильна модель (письмо/фідбек).

    Транзієнтні помилки (429/5xx/timeout/конект) — до _MAX_ATTEMPTS спроб з
    експоненційним backoff. Постійні помилки або вичерпані спроби → "" (фолбек).
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
    for attempt in range(_MAX_ATTEMPTS):
        try:
            resp = await _c().messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
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
