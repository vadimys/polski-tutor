"""Anthropic API — тіровано: дешева модель для дрилів, сильна для письма/фідбеку.

Без ключа повертає "" — виклик-сайти показують статичний фолбек.
"""

from __future__ import annotations

import logging

from app.config import settings

logger = logging.getLogger(__name__)

_client = None


def enabled() -> bool:
    return bool(settings.anthropic_api_key)


def _c():
    global _client
    if _client is None:
        from anthropic import AsyncAnthropic

        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


async def ask(system: str, user: str, *, strong: bool = False, max_tokens: int = 1200) -> str:
    """Один запит до Claude. strong=True → сильна модель (письмо/фідбек)."""
    if not enabled():
        return ""
    model = settings.strong_model if strong else settings.cheap_model
    try:
        resp = await _c().messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
        return "\n".join(parts).strip()
    except Exception:
        logger.exception("AI ask failed (model=%s)", model)
        return ""
