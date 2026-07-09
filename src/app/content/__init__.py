"""Реєстр офіційних B1-тестів (Держкомісія). Джерела: [[polski-b1-official-sources]].

- all_items(section) — АГРЕГАТ усіх тестів (пул для тренувань/тесту — варіативність);
- exam_items(exam_id, section) — ОДИН тест (для повного моку /egzamin);
- latest() — найновіший тест (дефолт для «сісти за іспит»); порядок EXAMS: старі→нові.
"""

from __future__ import annotations

from app.content import b1_2019, b1_2020
from app.content.schema import Exam, MCQItem

# порядок: найстаріший → найновіший. Реальні іспити додаються в кінець.
EXAMS: list[Exam] = [
    b1_2019.EXAM,
    b1_2020.EXAM,
]

_COMPLETE_MIN_SECTIONS = 2  # «повний» тест = має ≥2 секції (щоб не стати дефолтом частковим)


def all_exams() -> list[Exam]:
    """Уся база (найновіші спершу — для показу вибору)."""
    return list(reversed(EXAMS))


def latest() -> Exam:
    """Найновіший ПОВНИЙ тест (дефолт /egzamin). Частковий (напр. лише читання) — не дефолт."""
    complete = [e for e in EXAMS if len({it.section for it in e.items}) >= _COMPLETE_MIN_SECTIONS]
    return complete[-1] if complete else EXAMS[-1]


def by_id(exam_id: str) -> Exam | None:
    return next((e for e in EXAMS if e.id == exam_id), None)


def all_items(section: str) -> list[MCQItem]:
    """Агрегат секції по ВСІХ тестах (детермінований порядок → стабільні індекси)."""
    return [it for e in EXAMS for it in e.items if it.section == section]


def all_items_flat() -> list[MCQItem]:
    return [it for e in EXAMS for it in e.items]


def exam_items(exam_id: str, section: str) -> list[MCQItem]:
    e = by_id(exam_id)
    return e.section(section) if e else []


def exam_sections(exam_id: str) -> list[str]:
    e = by_id(exam_id)
    if not e:
        return []
    return [s for s in ("sluchanie", "czytanie", "gramatyka") if e.section(s)]
