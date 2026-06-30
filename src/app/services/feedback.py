"""Спільний парсинг оцінки з AI-фідбеку (письмо/мовлення).

Модель завершує відповідь рядком 'WYNIK: NN' (0–100).
"""

from __future__ import annotations

import re

SCORE_RE = re.compile(r"WYNIK:\s*(\d{1,3})")


def parse_score(text: str) -> int | None:
    """Витягти оцінку з рядка 'WYNIK: NN'. None, якщо не знайдено."""
    m = SCORE_RE.search(text)
    if not m:
        return None
    return max(0, min(int(m.group(1)), 100))


def strip_score_line(text: str) -> str:
    """Прибрати службовий рядок WYNIK: ... для показу користувачу."""
    return SCORE_RE.sub("", text).strip()
