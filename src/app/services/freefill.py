"""Перевірка відповідей типу free-fill (учень ВПИСУЄ форму слова).

Чисті функції — нормалізація вводу й звірка зі списком прийнятних варіантів.
Діакритику зберігаємо (pracowali ≠ pracowaly), але ігноруємо регістр, зайві
пробіли й кінцеву пунктуацію.
"""

from __future__ import annotations

_STRIP = " .,;:!?\"'«»„”()"


def normalize(s: str) -> str:
    """Нижній регістр + згорнуті пробіли + зрізана крайова пунктуація."""
    return " ".join(s.lower().split()).strip(_STRIP)


def is_correct(answer: str, accepted: list[str]) -> bool:
    """Чи збігається (нормалізовано) відповідь із будь-яким прийнятним варіантом."""
    a = normalize(answer)
    return bool(a) and any(a == normalize(x) for x in accepted)
