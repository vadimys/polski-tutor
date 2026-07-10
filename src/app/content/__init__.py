"""Реєстр офіційних B1-тестів (Держкомісія). Джерела: [[polski-b1-official-sources]].

- all_items(section) — АГРЕГАТ усіх тестів (пул для тренувань/тесту — варіативність);
- exam_items(exam_id, section) — ОДИН тест (для повного моку /egzamin);
- latest() — найновіший тест (дефолт для «сісти за іспит»); порядок EXAMS: старі→нові.
"""

from __future__ import annotations

from app.content import b1_2019, b1_2020, b1_2024_02, b1_2024_04, b1_2024_06
from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

# порядок: найстаріший → найновіший. Реальні іспити додаються в кінець.
EXAMS: list[Exam] = [
    b1_2019.EXAM,
    b1_2020.EXAM,
    b1_2024_02.EXAM,
    b1_2024_04.EXAM,
    b1_2024_06.EXAM,
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


def all_match_tasks(section: str | None = None) -> list[MatchTask]:
    """Агрегат завдань-зіставлень (dopasowanie) по ВСІХ тестах (стабільний порядок)."""
    return [t for e in EXAMS for t in e.match_tasks(section)]


def exam_match_tasks(exam_id: str, section: str | None = None) -> list[MatchTask]:
    e = by_id(exam_id)
    return e.match_tasks(section) if e else []


def all_fill_tasks(section: str | None = None) -> list[FreeFillTask]:
    """Агрегат завдань «вписати форму» (free-fill) по ВСІХ тестах."""
    return [t for e in EXAMS for t in e.fill_tasks(section)]


def exam_fill_tasks(exam_id: str, section: str | None = None) -> list[FreeFillTask]:
    e = by_id(exam_id)
    return e.fill_tasks(section) if e else []


def all_open_tasks(section: str | None = None) -> list[OpenTask]:
    """Агрегат відкритих завдань (питання/трансформація) по ВСІХ тестах."""
    return [t for e in EXAMS for t in e.open_tasks(section)]


def exam_open_tasks(exam_id: str, section: str | None = None) -> list[OpenTask]:
    e = by_id(exam_id)
    return e.open_tasks(section) if e else []


def exam_sections(exam_id: str) -> list[str]:
    e = by_id(exam_id)
    if not e:
        return []
    return [s for s in ("sluchanie", "czytanie", "gramatyka") if e.section(s)]
