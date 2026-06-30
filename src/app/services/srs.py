"""SRS — інтервальне повторення за системою Leitner.

Чисті функції (легко тестувати). Стан слів зберігає окремо vocab-стор.
Інтервали за коробкою: 1→1д, 2→3, 3→7, 4→16, 5→35.
Вгадав → box+1 (до 5). Помилився → box=1.
"""

from __future__ import annotations

from datetime import date, timedelta

INTERVALS: dict[int, int] = {1: 1, 2: 3, 3: 7, 4: 16, 5: 35}
MAX_BOX = 5


def clamp_box(box: int) -> int:
    return max(1, min(box, MAX_BOX))


def next_due(box: int, today: date) -> str:
    """Дата наступного повторення (YYYY-MM-DD) для коробки box."""
    box = clamp_box(box)
    return (today + timedelta(days=INTERVALS[box])).isoformat()


def on_correct(box: int) -> int:
    """Правильна відповідь → підняти коробку (до MAX_BOX)."""
    return clamp_box(box + 1)


def on_wrong(_box: int) -> int:
    """Помилка → повернути в першу коробку."""
    return 1


def is_due(due: str, today: date) -> bool:
    """Чи слово «доспіло» до повторення (порожнє due = так)."""
    if not due:
        return True
    return due <= today.isoformat()
