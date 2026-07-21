"""Модуль аудіювання (Słuchanie) — на ОФІЦІЙНИХ матеріалах Держкомісії.

Транскрипти записів, питання й КЛЮЧ відповідей — з офіц. збірника ROZUMIENIE ZE
SŁUCHU B1 (розділ «KLUCZ I TRANSKRYPCJA NAGRAŃ»). Текст озвучуємо локальним TTS
(piper); якщо TTS недоступний — показуємо транскрипт. Жодних вигаданих відповідей.

Пакет: `schema` (типи + спільні константи) · `exercises` (EXERCISES) ·
`match_audio` (MATCH_AUDIO). Публічний API незмінний — `from app.services import listening`.
"""

from __future__ import annotations

import random

from app.services.listening.exercises import EXERCISES
from app.services.listening.match_audio import MATCH_AUDIO
from app.services.listening.schema import LQ, SOURCE, Exercise, MatchAudio, Segment

__all__ = [
    "EXERCISES",
    "MATCH_AUDIO",
    "SOURCE",
    "LQ",
    "Exercise",
    "MatchAudio",
    "Segment",
    "by_id",
    "match_audio_by_id",
    "match_audio_correct",
    "pick",
    "toggle_selection",
    "total_questions",
]


def by_id(exercise_id: str) -> Exercise | None:
    return next((e for e in EXERCISES if e.id == exercise_id), None)


def pick() -> Exercise:
    return random.choice(EXERCISES)


def total_questions(ex: Exercise) -> int:
    return sum(len(s.questions) for s in ex.segments)


def match_audio_by_id(mid: str) -> MatchAudio | None:
    return next((m for m in MATCH_AUDIO if m.id == mid), None)


def toggle_selection(selected: list[int], i: int) -> list[int]:
    """Перемкнути особу i у виборі (для multi-select). Повертає відсортований список."""
    s = set(selected)
    s ^= {i}
    return sorted(s)


def match_audio_correct(selected: list[int] | set[int], key_row: list[int]) -> bool:
    """Опис зараховано ⇔ обрана множина осіб точно дорівнює ключу (порядок не важить)."""
    return set(selected) == set(key_row)
