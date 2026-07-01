"""Спільні хелпери MCQ-вікторин (placement/drills/mock/listening).

Прибирає дублювання: парсинг callback-відповіді (з guard за індексом) і формування
«картки розбору» після відповіді. Control-flow лишається в кожному хендлері.
Callback формат: '<prefix>:ans:<qidx>:<option>'.
"""

from __future__ import annotations

import html


def parse_answer(data: str) -> tuple[int, int] | None:
    """'<prefix>:ans:<qidx>:<opt>' → (qidx, opt); None, якщо формат не той (стара кнопка)."""
    parts = data.split(":")
    if len(parts) != 4:
        return None
    try:
        return int(parts[2]), int(parts[3])
    except ValueError:
        return None


def verdict_card(question: str, chosen: int, correct: int, options: list[str], explain: str) -> str:
    """Текст питання, що перетворюється на «розібрану картку» після відповіді."""
    if chosen == correct:
        verdict = "✔️ <b>Dobrze!</b>"
    else:
        verdict = f"❌ Poprawnie: <b>{html.escape(options[correct])}</b>"
    exp = f"\n💡 {html.escape(explain)}" if explain else ""
    return f"{html.escape(question)}\n\n{verdict}{exp}"
