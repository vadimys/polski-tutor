"""Схема аудіювання: типи завдань + спільні константи (дані офіційні)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LQ:
    text: str
    options: list[str]
    correct: int  # з офіційного ключа
    explain: str = ""


@dataclass
class Segment:
    audio: str  # текст запису для озвучення (verbatim з транскрипту)
    questions: list[LQ] = field(default_factory=list)


@dataclass
class Exercise:
    id: str
    title: str
    intro: str
    segments: list[Segment]


@dataclass
class MatchAudio:
    """Аудіо-зіставлення (Słuch «przyporządkowanie») — офіц. тип, який НЕ лягає в
    single-choice: чуємо N мовців, кожен опис (A–E) стосується МНОЖИНИ мовців
    (одна особа може мати кілька описів). Тому multi-select + звірка множин.

    `speakers[i]` — транскрипт мовця i (для TTS, verbatim). `prompts[j]` — опис j.
    `key[j]` — множина 0-based індексів мовців, яких стосується опис j.
    """

    id: str
    title: str
    intro: str
    speakers: list[str]  # транскрипти мовців 1..N (verbatim, для озвучення)
    prompts: list[str]  # описи A–E (те, що зіставляємо з мовцями)
    key: list[list[int]]  # key[j] = 0-based індекси мовців для опису j (порядок довільний)
    explain: list[str]


SOURCE = "офіційний зразок Держкомісії (B1)"

_TAKNIE = ["TAK", "NIE"]

# спільні описи-опції для Zad V тесту 2020 (порядок A-F; C — дистрактор із прикладу)
_ZAD5_OPTS = [
    "sport, który nie wymagał specjalnego stroju",  # A
    "dyscyplina, w której Polacy odnosili sukcesy",  # B
    "sport tak samo popularny jak jazda na nartach",  # C (przykład: hokej)
    "aktywność związana też z turystyką",  # D
    "sport stosunkowo niedrogi",  # E
    "dyscyplina związana z modą sportową",  # F
]

# спільні описи-опції (кол. II) для single-choice matching Zad V іспитів 2022 (порядок A–F)
_P2202 = [  # парки: przykład Białowieski→B
    "jest dopiero planowany.",  # A
    "jest jednym z pierwszych parków narodowych w Polsce.",  # B (przykład)
    "oferuje turystom różne zabytki.",  # C
    "to miejsce, w którym są nietypowe kształty skał.",  # D
    "ma dobrą ofertę dla osób aktywnych fizycznie.",  # E
    "to miejsce, w którym woda zajmuje największy teren.",  # F
]
_P2203 = [  # студенти: przykład Ania→B
    "mieszka w akademiku.",  # A
    "mieszka z rodzicami.",  # B (przykład)
    "ma własne mieszkanie.",  # C
    "wynajmuje mieszkanie z kolegą.",  # D
    "mieszka z bliskimi.",  # E
    "samodzielnie wynajmuje mieszkanie.",  # F
]
_P2206 = [  # молоко: przykład krowie→E
    "nie jest dobre dla osób na diecie.",  # A
    "jest odpowiednie dla alergików.",  # B
    "dobrze pasuje do różnych rodzajów kaw.",  # C
    "jest chętnie kupowane przez Polaków.",  # D
    "może powodować alergię.",  # E (przykład)
    "można zrobić samodzielnie.",  # F
]

