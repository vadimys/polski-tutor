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


def transcribe_words_sync(path: str) -> list[dict]:
    """Слова з таймкодами [{word,start,end}] (для форс-аляйнменту вирізання слова).
    Синхронно — виклик уже з робочого потоку (напр. синтез вимови). [] якщо недоступно."""
    if not available():
        return []
    try:
        segments, _info = _m().transcribe(path, language="pl", word_timestamps=True)
        out: list[dict] = []
        for seg in segments:
            for w in seg.words or []:
                out.append({"word": w.word.strip(), "start": float(w.start), "end": float(w.end)})
        return out
    except Exception:
        logger.exception("transcribe_words failed")
        return []


async def _transcribe_groq(path: str) -> str | None:
    """Groq Whisper large-v3 (PRIMARY, якщо є ключ) — кращий польський WER на акценті.
    None → нема ключа/збій → викликач падає на локальний faster-whisper."""
    if not settings.groq_api_key:
        return None
    try:
        import aiohttp

        with open(path, "rb") as fh:
            data = aiohttp.FormData()
            # Telegram voice = OGG/Opus; Groq визначає формат за розширенням у filename і
            # приймає 'ogg' (не 'oga') — тож маркуємо .ogg, вміст той самий OGG-контейнер
            data.add_field("file", fh, filename="audio.ogg", content_type="audio/ogg")
            data.add_field("model", settings.groq_stt_model)
            data.add_field("language", "pl")
            data.add_field("response_format", "text")
            async with aiohttp.ClientSession() as s, s.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                data=data,
                headers={"Authorization": f"Bearer {settings.groq_api_key}"},
                timeout=aiohttp.ClientTimeout(total=30),
            ) as r:
                if r.status != 200:
                    logger.warning("groq STT HTTP %s: %s", r.status, (await r.text())[:200])
                    return None
                return (await r.text()).strip()
    except Exception:
        logger.exception("groq STT failed — фолбек на локальний whisper")
        return None


async def transcribe(path: str) -> str:
    """Транскрибувати аудіофайл (польська). Groq (якщо ключ) → локальний whisper. '' на збій."""
    groq = await _transcribe_groq(path)
    if groq is not None:
        return groq
    if not available():
        return ""
    try:
        return await asyncio.to_thread(_transcribe_sync, path)
    except Exception:
        logger.exception("transcribe failed")
        return ""
