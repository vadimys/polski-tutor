"""Модуль аудіювання (Słuchanie): банк коротких текстів + питання формату іспиту.

Текст озвучується локальним TTS (piper). Якщо TTS недоступний — показуємо текст
(деградація замість падіння). Питання — MCQ, як у тренуванні.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class LQuestion:
    id: str
    text: str
    options: list[str]
    correct: int
    explain: str


@dataclass
class ListeningItem:
    id: str
    title: str
    text: str  # польський текст для озвучення (4–6 речень, B1)
    questions: list[LQuestion]


def _q(qid: str, text: str, options: list[str], correct: int, explain: str) -> LQuestion:
    return LQuestion(qid, text, options, correct, explain)


ITEMS: list[ListeningItem] = [
    ListeningItem(
        "komunikat_pociag", "Komunikat na dworcu",
        "Uwaga, uwaga. Pociąg do Warszawy planowo o godzinie czternastej trzydzieści "
        "jest opóźniony o dwadzieścia minut. Odjazd z peronu drugiego. Przepraszamy za utrudnienia.",
        [
            _q("lk1", "O której miał odjechać pociąg?", ["14:30", "14:20", "20:00", "13:14"], 0,
               "«czternasta trzydzieści» = 14:30."),
            _q("lk2", "Z którego peronu odjedzie pociąg?", ["pierwszego", "drugiego", "trzeciego", "czwartego"], 1,
               "«z peronu drugiego» = з другої платформи."),
        ],
    ),
    ListeningItem(
        "poczta", "W urzędzie",
        "Dzień dobry. Chciałbym złożyć wniosek o kartę pobytu. Czy potrzebuję umówić wizytę? "
        "Tak, proszę zarezerwować termin przez internet. Proszę też przynieść paszport i dwa zdjęcia.",
        [
            _q("lp1", "Po co przyszedł klient?", ["po paszport", "złożyć wniosek o kartę pobytu", "zapłacić podatek", "po zdjęcia"], 1,
               "«wniosek o kartę pobytu» = заява на карту перебування."),
            _q("lp2", "Co trzeba przynieść?", ["tylko paszport", "paszport i dwa zdjęcia", "tylko zdjęcia", "nic"], 1,
               "«paszport i dwa zdjęcia»."),
        ],
    ),
    ListeningItem(
        "pogoda", "Prognoza pogody",
        "Na jutro synoptycy zapowiadają deszcz i silny wiatr. Temperatura wyniesie tylko "
        "dziesięć stopni. Radzimy zabrać parasol i ciepłą kurtkę.",
        [
            _q("lw1", "Jaka będzie jutro pogoda?", ["słonecznie", "deszcz i wiatr", "śnieg", "upał"], 1,
               "«deszcz i silny wiatr» = дощ і сильний вітер."),
            _q("lw2", "Co radzą zabrać?", ["okulary", "parasol i kurtkę", "krem", "rower"], 1,
               "«parasol i ciepłą kurtkę» = парасолю й теплу куртку."),
        ],
    ),
    ListeningItem(
        "sklep", "Zakupy",
        "Przepraszam, szukam mleka i chleba. Mleko jest na końcu, przy lodówkach, "
        "a chleb zaraz przy wejściu. Dziękuję. Czy płaci pan kartą czy gotówką? Kartą.",
        [
            _q("ls1", "Gdzie jest mleko?", ["przy wejściu", "przy lodówkach", "przy kasie", "na zewnątrz"], 1,
               "«przy lodówkach» = біля холодильників."),
            _q("ls2", "Jak klient zapłaci?", ["gotówką", "kartą", "czekiem", "telefonem"], 1,
               "«Kartą» = карткою."),
        ],
    ),
    ListeningItem(
        "lekarz", "U lekarza",
        "Dzień dobry, co panią boli? Od wczoraj boli mnie gardło i mam gorączkę. "
        "Proszę otworzyć usta. Przepiszę pani syrop. Proszę dużo pić i odpoczywać.",
        [
            _q("ld1", "Co boli pacjentkę?", ["głowa", "gardło", "noga", "ząb"], 1,
               "«boli mnie gardło» = болить горло."),
            _q("ld2", "Co przepisał lekarz?", ["tabletki", "syrop", "zastrzyk", "nic"], 1,
               "«Przepiszę pani syrop» = випишу сироп."),
        ],
    ),
]


def by_id(item_id: str) -> ListeningItem | None:
    return next((it for it in ITEMS if it.id == item_id), None)


def pick() -> ListeningItem:
    return random.choice(ITEMS)
