"""Схема розділу «Граматика» — окремого від B1 курсу вивчення польської з нуля.

Педагогіка: мікроуроки-картки (одна ідея = одна картка, без «полотна»), пояснення
українською ПРОСТО + приклади польською з перекладом, наприкінці — коротка міні-практика.
Спіральна прогресія: алфавіт → базові речення → відмінки → дієслова → … (нарощуємо).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Card:
    """Одна картка уроку — ОДНА думка. Показується сама в повідомленні (◀️ ▶️)."""

    title: str  # короткий заголовок картки
    body: str  # просте пояснення українською (HTML: <b>, <i>)
    examples: list[tuple[str, str]] = field(default_factory=list)  # (польською, переклад)
    tip: str = ""  # опційна «фішка / запамʼятай» (виділяється 💡)


@dataclass
class Quiz:
    """Міні-практика в кінці уроку — закріпити (без впливу на готовність до B1)."""

    q: str
    options: list[str]
    correct: int  # індекс правильної
    explain: str = ""


@dataclass
class Lesson:
    id: str  # унікальний (напр. "alf_samogloski")
    title: str  # напр. "Голосні: a e i o u y"
    cards: list[Card]
    quiz: list[Quiz] = field(default_factory=list)


@dataclass
class Module:
    id: str  # унікальний (напр. "alfabet")
    icon: str  # емодзі модуля
    title: str  # "Алфавіт і вимова"
    subtitle: str  # короткий опис (одне речення)
    lessons: list[Lesson]
