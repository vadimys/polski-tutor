"""Реєстр розділу «Дієслова» — довідник найчастотніших дієслів + тренажер.

Групи впорядковані від найуживаніших. Нові групи/дієслова додаються файлом +
рядком у GROUPS — навігація/пошук/тренажер працюють автоматично.
"""

from __future__ import annotations

from app.verbs.codzienne import GROUP as _CODZIENNE
from app.verbs.core import GROUP as _CORE
from app.verbs.dom import GROUP as _DOM
from app.verbs.komunikacja import GROUP as _KOMUNIKACJA
from app.verbs.praca import GROUP as _PRACA
from app.verbs.ruch import GROUP as _RUCH
from app.verbs.schema import PERSONS, Verb, VerbGroup
from app.verbs.sprawy import GROUP as _SPRAWY
from app.verbs.umysl import GROUP as _UMYSL
from app.verbs.zdrowie import GROUP as _ZDROWIE

__all__ = ["PERSONS", "Verb", "VerbGroup", "GROUPS"]

GROUPS: list[VerbGroup] = [
    _CORE, _RUCH, _CODZIENNE, _KOMUNIKACJA, _UMYSL, _PRACA, _DOM, _ZDROWIE, _SPRAWY,
]


def all_groups() -> list[VerbGroup]:
    return GROUPS


def group_at(gi: int) -> VerbGroup | None:
    return GROUPS[gi] if 0 <= gi < len(GROUPS) else None


def verb_at(gi: int, vi: int) -> Verb | None:
    g = group_at(gi)
    if g is None or not (0 <= vi < len(g.verbs)):
        return None
    return g.verbs[vi]


def all_verbs() -> list[tuple[int, int, Verb]]:
    """Усі дієслова з координатами (gi, vi) — для пошуку й тренажера."""
    return [(gi, vi, v) for gi, g in enumerate(GROUPS) for vi, v in enumerate(g.verbs)]


def search(query: str) -> list[tuple[int, int, Verb]]:
    """Пошук за інфінітивом (початок) або перекладом (входження). До 6 збігів."""
    q = query.strip().lower()
    if not q:
        return []
    hits = [
        (gi, vi, v)
        for gi, vi, v in all_verbs()
        if v.inf.lower().startswith(q) or q in v.uk.lower() or q in v.pair.lower()
    ]
    return hits[:6]
