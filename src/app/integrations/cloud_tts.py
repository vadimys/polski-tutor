"""Хмарний нейро-TTS (Azure Speech) — чиста вимова ОДИНОЧНИХ слів.

piper-VITS ламає одиночні слова (навчений на реченнях); Azure neural вимовляє їх
коректно «з коробки». Використовуємо для вимови слів у словнику; piper лишається
фолбеком (лексикон/аудіювання не падають без ключа/інтернету).

Azure REST v1 віддає одразу OGG/Opus (X-Microsoft-OutputFormat) — годиться для
send_voice без перекодування. Порожній ключ/регіон → available()=False → фолбек.
"""

from __future__ import annotations

import logging

import aiohttp

from app.config import settings

logger = logging.getLogger(__name__)

_SSML = "<speak version='1.0' xml:lang='pl-PL'><voice name='{voice}'>{text}</voice></speak>"


def available() -> bool:
    return bool(settings.azure_tts_key and settings.azure_tts_region)


def _escape(text: str) -> str:
    """XML-екранування для вмісту SSML."""
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


async def synthesize(text: str) -> bytes | None:
    """OGG/Opus-байти вимови (Azure neural) або None (не налаштовано/збій → фолбек на piper)."""
    if not available():
        return None
    url = f"https://{settings.azure_tts_region}.tts.speech.microsoft.com/cognitiveservices/v1"
    ssml = _SSML.format(voice=settings.azure_tts_voice, text=_escape(text.strip()))
    headers = {
        "Ocp-Apim-Subscription-Key": settings.azure_tts_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "ogg-48khz-16bit-mono-opus",
        "User-Agent": "polski-b1-coach",
    }
    try:
        async with aiohttp.ClientSession() as s, s.post(
            url, data=ssml.encode("utf-8"), headers=headers,
            timeout=aiohttp.ClientTimeout(total=15),
        ) as r:
            if r.status != 200:
                logger.warning("azure tts HTTP %s: %s", r.status, (await r.text())[:200])
                return None
            return await r.read()
    except Exception:
        logger.exception("azure tts failed")
        return None
