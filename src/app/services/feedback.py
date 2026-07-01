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


# Офіційна шкала Pisanie B1: wykonanie 0-10 · środki językowe 0-10 · poprawność 0-10
_OFFICIAL_RE = re.compile(
    r"wykonanie\D*(\d+).*?(?:środki|srodki)\D*(\d+).*?poprawno\w*\D*(\d+)",
    re.IGNORECASE | re.DOTALL,
)


def parse_official_pisanie(text: str) -> tuple[int, int, int] | None:
    """(wykonanie, środki, poprawność) 0-10 кожен, або None."""
    m = _OFFICIAL_RE.search(text)
    if not m:
        return None

    def clamp(x: str) -> int:
        return max(0, min(int(x), 10))

    return clamp(m.group(1)), clamp(m.group(2)), clamp(m.group(3))


def strip_official_line(text: str) -> str:
    return re.sub(r"WYNIK.*", "", text, flags=re.IGNORECASE | re.DOTALL).strip()


# Офіційна шкала Mówienie B1 (частина, оцінювана з транскрипту): wykonanie (0-max),
# gramatyka 0-8, słownictwo i styl 0-8. Фонетику/плавність із тексту НЕ оцінюємо.
_SPEAK_RE = re.compile(
    r"wykonanie\D*(\d+).*?gramatyka\D*(\d+).*?(?:słownictwo|slownictwo)\D*(\d+)",
    re.IGNORECASE | re.DOTALL,
)


def parse_official_mowienie(text: str) -> tuple[int, int, int] | None:
    """(wykonanie, gramatyka, słownictwo) — сирі числа (клемпінг — на боці викликача)."""
    m = _SPEAK_RE.search(text)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))
