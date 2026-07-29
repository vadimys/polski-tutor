"""Реєстр розділу «Дієслова» — довідник найчастотніших дієслів + тренажер.

Групи впорядковані від найуживаніших. Нові групи/дієслова додаються файлом +
рядком у GROUPS — навігація/пошук/тренажер працюють автоматично.
"""

from __future__ import annotations

import re

from app.verbs.codzienne import GROUP as _CODZIENNE
from app.verbs.core import GROUP as _CORE
from app.verbs.dom import GROUP as _DOM
from app.verbs.komunikacja import GROUP as _KOMUNIKACJA
from app.verbs.ludzie import GROUP as _LUDZIE
from app.verbs.nauka import GROUP as _NAUKA
from app.verbs.pieniadze import GROUP as _PIENIADZE
from app.verbs.praca import GROUP as _PRACA
from app.verbs.ruch import GROUP as _RUCH
from app.verbs.schema import PERSONS, Verb, VerbGroup
from app.verbs.sprawy import GROUP as _SPRAWY
from app.verbs.umysl import GROUP as _UMYSL
from app.verbs.zdrowie import GROUP as _ZDROWIE

__all__ = ["PERSONS", "Verb", "VerbGroup", "GROUPS"]

GROUPS: list[VerbGroup] = [
    _CORE, _RUCH, _CODZIENNE, _KOMUNIKACJA, _UMYSL, _PRACA, _DOM, _ZDROWIE, _SPRAWY,
    _NAUKA, _PIENIADZE, _LUDZIE,
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


# мітки слотів минулого часу (рід — головна складність минулого для українців)
PAST_PERSONS = ["ja (чол.)", "ja (жін.)", "on", "ona", "oni", "one"]

# майбутній складений (недоконаний): форма być-майбутнього + інфінітив — 100% регулярний
_BEDE = ["będę", "będziesz", "będzie", "będziemy", "będziecie", "będą"]


def future_paradigm(inf: str) -> list[str]:
    """6 форм майбутнього складеного: będę robić… (zwrotne: będę się myć).

    Регулярне правило без винятків → генерація безпечна (жодних вигаданих форм).
    """
    if inf.endswith(" się"):
        base = inf.removesuffix(" się")
        return [f"{b} się {base}" for b in _BEDE]
    return [f"{b} {inf}" for b in _BEDE]

_PAST_RE = re.compile(r"on (.+?) · ona (.+?) · oni (.+?)(?:\s*\(|$)")


def past_paradigm(past: str) -> list[str] | None:
    """6 форм минулого [ja(ч), ja(ж), on, ona, oni, one] з рядка «on X · ona Y · oni Z».

    Польський минулий регулярний від 3-ї особи; єдиний підступ — чергування ó→o
    (mógł → mogłem): якщо чол. форма з «ó» відповідає жін. стему з «o» — 1-ша особа
    йде від жіночого стему. НЕ вигадує форм: усе виводиться з виписаних вручну past.
    None — якщо рядок нестандартний (тренажер тоді питає лише теперішній).
    """
    m = _PAST_RE.search(past)
    if not m:
        return None
    on, ona, oni = (s.strip() for s in m.groups())
    refl = " się" if on.endswith(" się") else ""
    m3 = on.removesuffix(" się")
    f3 = ona.removesuffix(" się")
    if not f3.endswith("a"):
        return None
    f_stem = f3[:-1]  # mogła → mogł, robiła → robił
    # стем 1-ї особи чол.: зазвичай = m3 (szedł→szedłem), але mógł→mogłem (ó→o)
    ja_stem = f_stem if (m3 != f_stem and m3.replace("ó", "o") == f_stem) else m3
    return [
        ja_stem + "em" + refl,  # ja (чол.)
        f3 + "m" + refl,  # ja (жін.)
        on, ona, oni,
        f_stem + "y" + refl,  # one (robiły)
    ]


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
