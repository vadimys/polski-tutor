"""Реєстр розділу «Граматика» — окремий курс вивчення польської з нуля.

Модулі впорядковані як навчальний шлях (алфавіт → базові речення → …). Нові модулі
(відмінки, дієслова, прикметники) додаються сюди в MODULES — движок і навігація
працюють автоматично.
"""

from __future__ import annotations

from app.grammar.alfabet import MODULE as _ALFABET
from app.grammar.aspekt import MODULE as _ASPEKT
from app.grammar.czasownik_czas import MODULE as _CZAS_PP
from app.grammar.czasownik_teraz import MODULE as _CZAS_TER
from app.grammar.liczebniki import MODULE as _LICZEBNIKI
from app.grammar.podstawy import MODULE as _PODSTAWY
from app.grammar.przymiotnik import MODULE as _PRZYMIOTNIK
from app.grammar.przypadki import MODULE as _PRZYPADKI
from app.grammar.rzeczownik import MODULE as _RZECZOWNIK
from app.grammar.schema import Card, Lesson, Module, Quiz
from app.grammar.zaimki import MODULE as _ZAIMKI

__all__ = ["Card", "Lesson", "Module", "Quiz", "MODULES"]

# Порядок = навчальний шлях (від легкого до найважчого). Далі: przyimki, składnia…
MODULES: list[Module] = [
    _ALFABET, _PODSTAWY, _RZECZOWNIK, _PRZYPADKI, _CZAS_TER, _CZAS_PP, _ASPEKT,
    _PRZYMIOTNIK, _ZAIMKI, _LICZEBNIKI,
]


def all_modules() -> list[Module]:
    return MODULES


def module_by_id(mid: str) -> Module | None:
    return next((m for m in MODULES if m.id == mid), None)


def lesson_by_id(lid: str) -> Lesson | None:
    return next((ls for m in MODULES for ls in m.lessons if ls.id == lid), None)


def module_of(lid: str) -> Module | None:
    return next((m for m in MODULES for ls in m.lessons if ls.id == lid), None)


def all_lesson_ids() -> list[str]:
    return [ls.id for m in MODULES for ls in m.lessons]


def next_lesson(lid: str) -> Lesson | None:
    """Наступний урок у навчальному шляху (у тому ж модулі або перший наступного). None — кінець."""
    seq = [ls for m in MODULES for ls in m.lessons]
    for i, ls in enumerate(seq):
        if ls.id == lid:
            return seq[i + 1] if i + 1 < len(seq) else None
    return None
