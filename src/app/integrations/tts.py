"""Локальне озвучення тексту (piper TTS) для модуля Słuchanie.

synthesize() повертає OGG/Opus-байти (для send_voice) або None, якщо TTS
недоступний (тоді хендлер показує текст — деградація, не падіння).
"""

from __future__ import annotations

import asyncio
import logging
import os
import subprocess
import tempfile
import wave

from app.config import settings

logger = logging.getLogger(__name__)

_voice = None


def available() -> bool:
    """Чи встановлено piper і чи є модель голосу."""
    try:
        import piper  # noqa: F401

        return os.path.exists(settings.piper_model)
    except Exception:
        return False


def _v():
    global _voice
    if _voice is None:
        from piper import PiperVoice

        _voice = PiperVoice.load(settings.piper_model, config_path=settings.piper_model + ".json")
    return _voice


def _synth_sync(text: str) -> bytes | None:
    wav_fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(wav_fd)
    ogg_fd, ogg_path = tempfile.mkstemp(suffix=".ogg")
    os.close(ogg_fd)
    try:
        with wave.open(wav_path, "wb") as wf:
            _v().synthesize_wav(text, wf)  # piper >=1.3 — пише заголовок WAV сам
        subprocess.run(
            ["ffmpeg", "-y", "-i", wav_path, "-c:a", "libopus", "-b:a", "32k", ogg_path],
            check=True,
            capture_output=True,
        )
        with open(ogg_path, "rb") as f:
            return f.read()
    except Exception:
        logger.exception("tts synth failed")
        return None
    finally:
        for p in (wav_path, ogg_path):
            try:
                os.remove(p)
            except OSError:
                pass


async def synthesize(text: str) -> bytes | None:
    """OGG/Opus-байти озвученого тексту або None."""
    if not available():
        return None
    return await asyncio.to_thread(_synth_sync, text)
