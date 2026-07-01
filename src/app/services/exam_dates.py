"""Офіційні дати сесій іспиту B1 (дорослі) — джерело: certyfikatpolski.pl.

Куровано з офіційного розкладу Держкомісії. ОНОВЛЮВАТИ раз на рік, коли комісія
публікує новий розклад (і коли зʼявляться дати 2027). Користувач обирає ЛИШЕ з
цього списку → неможливо ввести неіснуючу дату.
"""

from __future__ import annotations

from datetime import date

SOURCE = "certyfikatpolski.pl (Держкомісія)"

# ISO-дати субот (перший день сесії — письмова частина). Сесії B1 2026.
OFFICIAL_SESSIONS: list[str] = [
    "2026-02-14",
    "2026-04-25",
    "2026-06-27",
    "2026-10-17",
    "2026-12-05",
]

_MONTHS_UK = {
    1: "січня", 2: "лютого", 3: "березня", 4: "квітня", 5: "травня", 6: "червня",
    7: "липня", 8: "серпня", 9: "вересня", 10: "жовтня", 11: "листопада", 12: "грудня",
}


def label(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.day} {_MONTHS_UK[d.month]} {d.year}"


def upcoming(today: date) -> list[str]:
    """Майбутні офіційні сесії (від сьогодні)."""
    ref = today.isoformat()
    return [d for d in OFFICIAL_SESSIONS if d >= ref]


def is_official(iso: str) -> bool:
    return iso in OFFICIAL_SESSIONS
