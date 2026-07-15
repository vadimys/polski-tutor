"""Локальне озвучення тексту (piper TTS) для модуля Słuchanie.

synthesize() повертає OGG/Opus-байти (для send_voice) або None, якщо TTS
недоступний (тоді хендлер показує текст — деградація, не падіння).
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import subprocess
import tempfile
import wave
from contextlib import suppress

from app.config import settings

logger = logging.getLogger(__name__)

# Одиночне слово (без пробілів) piper-VITS вимовляє нестабільно (навчений на реченнях).
# Тому слово синтезуємо В КОНТЕКСТІ речення, а тоді вирізаємо саме його за
# word-timestamps від Whisper (форс-аляйнмент) → чиста вимова слова, без «милиць».
_WORD_CARRIER = "To jest {}."


def _is_single_word(text: str) -> bool:
    return bool(text.strip()) and not re.search(r"\s", text.strip())


def _norm(s: str) -> str:
    return re.sub(r"\W", "", s.strip().lower(), flags=re.UNICODE)

_voice = None


def _piper_ok() -> bool:
    """Чи встановлено piper і чи є модель голосу."""
    try:
        import piper  # noqa: F401

        return os.path.exists(settings.piper_model)
    except Exception:
        return False


def available() -> bool:
    """Чи можемо озвучувати взагалі (piper АБО хмарний Azure)."""
    from app.integrations import cloud_tts

    return _piper_ok() or cloud_tts.available()


def _v():
    global _voice
    if _voice is None:
        from piper import PiperVoice

        _voice = PiperVoice.load(settings.piper_model, config_path=settings.piper_model + ".json")
    return _voice


def _prep(text: str) -> str:
    """Голе слово/фраза без кінцевої пунктуації → piper кліпить хвіст і говорить куце
    (напр. «skóra» звучить обрубком). Додаємо крапку для повного закриття синтезу."""
    t = text.strip()
    if t and t[-1] not in ".?!…":
        t += "."
    return t


def _synth_sync(text: str) -> bytes | None:
    wav_fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(wav_fd)
    ogg_fd, ogg_path = tempfile.mkstemp(suffix=".ogg")
    os.close(ogg_fd)
    try:
        with wave.open(wav_path, "wb") as wf:
            _v().synthesize_wav(_prep(text), wf)  # piper >=1.3 — пише заголовок WAV сам
        # фіксовані аргументи, без shell і без вводу користувача — безпечно; apad — хвіст-тиша,
        # щоб останній звук не «зʼїдався» кодеком/плеєром
        cmd = ["ffmpeg", "-y", "-i", wav_path, "-af", "apad=pad_dur=0.25",
               "-c:a", "libopus", "-b:a", "32k", ogg_path]
        subprocess.run(cmd, check=True, capture_output=True)  # noqa: S603 — фікс.аргументи, без shell
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


def _synth_word_sync(word: str) -> bytes | None:
    """Чиста вимова ОДНОГО слова: синтез у реченні-носії + виріз слова за
    Whisper word-timestamps. Фолбек на простий синтез, якщо аляйнмент не вдався."""
    from app.integrations import speech

    word = word.strip()
    wav_fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(wav_fd)
    ogg_fd, ogg_path = tempfile.mkstemp(suffix=".ogg")
    os.close(ogg_fd)
    try:
        with wave.open(wav_path, "wb") as wf:
            _v().synthesize_wav(_WORD_CARRIER.format(word), wf)
        words = speech.transcribe_words_sync(wav_path)
        tgt = _norm(word)
        hits = [w for w in words if _norm(w["word"]) == tgt]
        span = hits[-1] if hits else (words[-1] if words else None)
        if span is None:  # без аляйнменту чисто не виріжемо → простий синтез слова
            return _synth_sync(word)
        start = max(0.0, span["start"] - 0.06)
        end = span["end"] + 0.12
        cmd = ["ffmpeg", "-y", "-i", wav_path, "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
               "-af", "apad=pad_dur=0.15", "-c:a", "libopus", "-b:a", "32k", ogg_path]
        subprocess.run(cmd, check=True, capture_output=True)  # noqa: S603 — фікс.аргументи, без shell
        with open(ogg_path, "rb") as f:
            return f.read()
    except Exception:
        logger.exception("word synth failed")
        return None
    finally:
        for p in (wav_path, ogg_path):
            with suppress(OSError):
                os.remove(p)


async def synthesize(text: str) -> bytes | None:
    """OGG/Opus-байти озвученого тексту або None.

    Одиночне слово: спершу хмарний Azure (чиста вимова), фолбек — piper у контексті+виріз.
    Фрази/речення: piper (локально, безкоштовно; аудіювання й так якісне)."""
    single = _is_single_word(text)
    if single:
        from app.integrations import cloud_tts

        data = await cloud_tts.synthesize(text)  # None, якщо ключа нема/збій → фолбек
        if data:
            return data
    if not _piper_ok():
        return None
    return await asyncio.to_thread(_synth_word_sync if single else _synth_sync, text)
