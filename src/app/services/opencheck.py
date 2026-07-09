"""AI-оцінка відкритих завдань (трансформація/питання) — заземлена офіц. зразком.

ОДИН виклик Claude на все завдання (щоб не палити AI-ліміт: 1 таск = 1 запит).
Повертає вердикт+фідбек на кожен пункт або None (AI вимкнено/збій/невалідний JSON →
хендлер робить self-check fallback: показ зразка, готовність НЕ рухаємо).
"""

from __future__ import annotations

import json
import logging

from app.integrations import ai

logger = logging.getLogger(__name__)

_SYSTEM = (
    "Ти екзаменатор іспиту B1 з польської. Оцінюєш відкрите граматичне завдання: "
    "студент перетворює речення, ЗБЕРІГАЮЧИ той самий сенс і ВЖИВАЮЧИ задане слово "
    "(у правильній формі). Тобі дано офіційний зразок(и) як еталон — можливі й інші "
    "правильні варіанти. Признач ok=true, якщо відповідь студента: (1) містить форму "
    "заданого слова, (2) зберігає сенс оригіналу, (3) граматично коректна. Дрібні "
    "одруки й брак діакритики пробач. Поверни СУВОРО JSON-масив об'єктів "
    '{"ok": true/false, "feedback": "коротко українською: що добре або що виправити"} '
    "у ТОМУ Ж порядку, що й пункти. Нічого поза JSON."
)


def _build_prompt(items: list[dict]) -> str:
    blocks = []
    for it in items:
        models = " / ".join(it["models"])
        blocks.append(
            f"#{it['n']}\n"
            f"Оригінал: {it['original']}\n"
            f"Обов'язкове слово: {it['word']}\n"
            f"Офіційний зразок: {models}\n"
            f"Відповідь студента: {it['answer'] or '(порожньо)'}"
        )
    return "Оціни кожен пункт:\n\n" + "\n\n".join(blocks)


def _parse(raw: str, n: int) -> list[dict] | None:
    s = raw.strip()
    try:
        start, end = s.index("["), s.rindex("]") + 1
        data = json.loads(s[start:end])
    except (ValueError, json.JSONDecodeError):
        return None
    if not isinstance(data, list) or len(data) != n:
        return None
    out: list[dict] = []
    for d in data:
        if not isinstance(d, dict):
            return None
        out.append({"ok": bool(d.get("ok")), "feedback": str(d.get("feedback", ""))[:300]})
    return out


async def grade(items: list[dict]) -> list[dict] | None:
    """items: [{n, original, word, models, answer}]. → [{ok, feedback}] або None.

    None → AI недоступний або відповідь невалідна (хендлер: self-check fallback +
    refund AI-квоти).
    """
    if not ai.enabled() or not items:
        return None
    raw = await ai.ask(_SYSTEM, _build_prompt(items), strong=True, max_tokens=1000)
    if not raw:
        return None
    parsed = _parse(raw, len(items))
    if parsed is None:
        logger.warning("opencheck: AI відповів (%d симв.), але JSON не розпарсився", len(raw))
    return parsed
