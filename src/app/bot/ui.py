"""Спільні дрібні рендери для повідомлень."""

from __future__ import annotations


def bar(pct: int) -> str:
    """Візуальний індикатор готовності 0..100 → ▰▰▰▱▱ 60%."""
    pct = max(0, min(pct, 100))
    filled = round(pct / 20)
    return "▰" * filled + "▱" * (5 - filled) + f" {pct}%"
