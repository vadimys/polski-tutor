"""Схема розділу «Дієслова» — довідник + тренажер найчастотніших польських дієслів.

Кожне дієслово: повна таблиця теперішнього часу, минулий (готовим рядком — без
генерації, щоб жодна форма не була вигадана), видова пара з ключовими формами,
керування відмінком (rekcja — унікальна фішка) і приклад у контексті.
"""

from __future__ import annotations

from dataclasses import dataclass, field

PERSONS = ["ja", "ty", "on/ona", "my", "wy", "oni/one"]  # порядок форм у present


@dataclass
class Verb:
    inf: str  # інфінітив (недоконаний, база словника)
    uk: str  # переклад українською
    pair: str = ""  # інфінітив видової пари (доконаний), "" якщо нема
    pair_hint: str = ""  # ключові майбутні форми пари: "zrobię, zrobi"
    group: str = ""  # модель відмінювання: "-am, -asz" / "-ę, -isz" / "-ę, -esz" / "особливе"
    present: list[str] = field(default_factory=list)  # 6 форм: ja/ty/on/my/wy/oni
    past: str = ""  # готовий рядок: "on robił · ona robiła · oni robili"
    rekcja: str = ""  # керування: "kogo? co? (Biernik)" або з прийменником
    rekcja_q: str = ""  # канонічна коротка відповідь для тренажера rekcji ("na + Biernik");
    # ставиться ЛИШЕ коли керування однозначне (одна модель) — інакше лишити ""
    examples: list[tuple[str, str]] = field(default_factory=list)  # (pl, uk)


@dataclass
class VerbGroup:
    id: str
    icon: str
    title: str
    subtitle: str
    verbs: list[Verb]
