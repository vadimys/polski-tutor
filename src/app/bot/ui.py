"""Спільні дрібні рендери для повідомлень."""

from __future__ import annotations

import html


def emph(s: str) -> str:
    """Екранує текст, але ЗБЕРІГАЄ авторські теги <i>/<b> (контент навмисно з HTML-акцентами,
    напр. explain «→ <b>przed</b>» чи «зайве слово — <b>z</b>»). Решта символів — екрановані."""
    out = html.escape(s or "")
    for t in ("i", "b"):
        out = out.replace(f"&lt;{t}&gt;", f"<{t}>").replace(f"&lt;/{t}&gt;", f"</{t}>")
    return out


def bar(pct: int) -> str:
    """Візуальний індикатор готовності 0..100 → ▰▰▰▱▱ 60%."""
    pct = max(0, min(pct, 100))
    filled = round(pct / 20)
    return "▰" * filled + "▱" * (5 - filled) + f" {pct}%"
