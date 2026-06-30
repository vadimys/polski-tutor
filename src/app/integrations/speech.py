"""Локальне розпізнавання голосу (faster-whisper) для модуля Mówienie.

Модель завантажується раз (lazy) і кешується. Транскрипція — у потоці
(блокуючий CPU-виклик), щоб не блокувати event loop бота.
"""

from __future__ import annotations

import asyncio
import logging

from app.config import settings

logger = logging.getLogger(__name__)

_model = None


def available() -> bool:
    """Чи встановлено faster-whisper (у тестах/CI може бути відсутній)."""
    try:
        import faster_whisper  # noqa: F401

        return True
    except Exception:
        return False


def _m():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel

        _model = WhisperModel(
            settings.whisper_model,
            device="cpu",
            compute_type="int8",
            download_root=settings.whisper_dir,
        )
        logger.info("Whisper model '%s' loaded", settings.whisper_model)
    return _model


def _transcribe_sync(path: str) -> str:
    segments, _info = _m().transcribe(path, language="pl", vad_filter=True)
    return " ".join(s.text.strip() for s in segments).strip()


async def transcribe(path: str) -> str:
    """Транскрибувати аудіофайл (польська). '' якщо порожньо/помилка."""
    if not available():
        return ""
    try:
        return await asyncio.to_thread(_transcribe_sync, path)
    except Exception:
        logger.exception("transcribe failed")
        return ""
