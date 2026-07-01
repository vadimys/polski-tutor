"""Стартовий placement-тест — на ОФІЦІЙНОМУ банку (services/mock).

За правилом «тільки офіційне»: діагностика бере реальні питання з офіційного
пробного тесту (граматика + читання), лише коротшою вибіркою. Вимірює ЛИШЕ ці
два модулі (об'єктивні MCQ); продуктивні (Pisanie/Mówienie) і Słuchanie тут НЕ
оцінюються — їхня готовність зʼявляється у відповідних вправах.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from app.services import mock


@dataclass
class PlacementResult:
    overall_pct: int
    level: str
    per_module: dict[str, int]  # лише виміряні (gramatyka/czytanie)
    correct: int
    total: int


def _standalone_indices(section: str) -> list[int]:
    items = mock.section_items(section)
    return [i for i, it in enumerate(items) if it.context]


def build_test(n_grammar: int = 8, n_reading: int = 4) -> list[tuple[str, int]]:
    """Випадковий збалансований набір пар (секція, індекс) з офіц. банку."""
    pairs: list[tuple[str, int]] = []
    for section, n in (("gramatyka", n_grammar), ("czytanie", n_reading)):
        idxs = _standalone_indices(section)
        random.shuffle(idxs)
        pairs += [(section, i) for i in idxs[: min(n, len(idxs))]]
    random.shuffle(pairs)
    return pairs


def _level_from_pct(pct: int) -> str:
    if pct < 40:
        return "A1"
    if pct < 65:
        return "A2"
    if pct < 85:
        return "B1 (низький)"
    return "B1+"


def score(pairs: list[tuple[str, int]], chosen: list[int]) -> PlacementResult:
    """Порахувати результат: pairs = (секція, індекс), chosen = обрані опції (паралельно)."""
    by_section: dict[str, list[bool]] = {}
    correct = 0
    for (section, idx), ch in zip(pairs, chosen, strict=False):
        it = mock.section_items(section)[idx]
        ok = ch == it.correct
        correct += int(ok)
        by_section.setdefault(section, []).append(ok)
    total = len(pairs)
    overall = round(correct / total * 100) if total else 0
    per_module = {sec: round(sum(r) / len(r) * 100) for sec, r in by_section.items()}
    return PlacementResult(overall, _level_from_pct(overall), per_module, correct, total)
