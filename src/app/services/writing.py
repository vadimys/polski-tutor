"""Модуль письма (Pisanie): банк завдань B1 + AI-фідбек за критеріями іспиту."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass

from app.integrations import ai


@dataclass
class WritingTask:
    id: str
    genre: str
    prompt: str  # інструкція українською + що написати польською
    min_words: int = 50


# Жанри коротких форм B1 (теми наближені до життя: побут, urząd, резиденція)
TASKS: list[WritingTask] = [
    WritingTask(
        "email_priv", "E-mail prywatny",
        "Напиши приватний e-mail польською до знайомого: запроси його на weekend до себе. "
        "Вкажи: коли, що робитимете, що взяти. (≈ 50–70 слів)",
        50,
    ),
    WritingTask(
        "ogloszenie", "Ogłoszenie",
        "Напиши оголошення польською: ти продаєш rower (велосипед). "
        "Опиши його, вкажи cenę і kontakt. (≈ 40–60 слів)",
        40,
    ),
    WritingTask(
        "zaproszenie", "Zaproszenie",
        "Напиши zaproszenie польською на свої urodziny: kiedy, gdzie, co zabrać. (≈ 40–60 слів)",
        40,
    ),
    WritingTask(
        "email_urzad", "E-mail formalny",
        "Напиши формальний e-mail польською до urzędu: запитай, які dokumenty потрібні "
        "для karty pobytu. Дотримайся ввічливого тону. (≈ 50–70 слів)",
        50,
    ),
    WritingTask(
        "relacja", "Relacja",
        "Опиши польською свій останній weekend: що ти robił(a), де був(ла), як minął. "
        "Минулий час. (≈ 60–80 слів)",
        60,
    ),
    WritingTask(
        "forum", "Wpis na forum",
        "Напиши польською допис на форум: чи краще mieszkać w mieście czy na wsi? "
        "Вислови думку й аргумент. (≈ 60–90 слів)",
        60,
    ),
]


def pick_task() -> WritingTask:
    return random.choice(TASKS)


def task_by_id(task_id: str) -> WritingTask | None:
    return next((t for t in TASKS if t.id == task_id), None)


_SYSTEM = (
    "Ти — доброзичливий екзаменатор державного іспиту B1 з польської ТА репетитор "
    "для україномовного учня. Оцінюєш коротку письмову роботу за критеріями B1: "
    "(1) виконання завдання — чи розкрито всі пункти; (2) poprawność — граматика/орфографія; "
    "(3) структура й звʼязність; (4) багатство мови. "
    "Фідбек давай УКРАЇНСЬКОЮ, конкретно й підбадьорливо. "
    "Формат для Telegram: лише теги <b>...</b> та емодзі, БЕЗ markdown (*, _, #). "
    "Структура відповіді:\n"
    "• <b>Що добре</b> — 1–2 пункти.\n"
    "• <b>Помилки</b> — 3–5 конкретних: «було → стало» + коротке пояснення українською.\n"
    "• <b>Порада</b> — 1 фраза, що підтягнути.\n"
    "• <b>Зразок</b> — як цей текст міг би виглядати правильно (польською).\n"
    "ОСТАННІЙ рядок — строго у форматі: WYNIK: NN  (де NN — оцінка 0–100, орієнтовний % за B1)."
)


def _prompt(task: WritingTask, text: str) -> str:
    return (
        f"Завдання ({task.genre}): {task.prompt}\n\n"
        f"Текст учня:\n«{text}»\n\n"
        "Оціни за критеріями B1 і дай фідбек за вказаною структурою."
    )


SCORE_RE = re.compile(r"WYNIK:\s*(\d{1,3})")


def parse_score(text: str) -> int | None:
    """Витягти оцінку з рядка 'WYNIK: NN'. None, якщо не знайдено."""
    m = SCORE_RE.search(text)
    if not m:
        return None
    return max(0, min(int(m.group(1)), 100))


def strip_score_line(text: str) -> str:
    """Прибрати службовий рядок WYNIK: ... з тексту для показу."""
    return SCORE_RE.sub("", text).strip()


async def feedback(task: WritingTask, text: str) -> tuple[str, int | None]:
    """(відформатований фідбек, оцінка|None). '' якщо AI недоступний."""
    out = await ai.ask(_SYSTEM, _prompt(task, text), strong=True, max_tokens=1600)
    if not out:
        return "", None
    return strip_score_line(out), parse_score(out)
