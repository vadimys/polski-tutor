"""Модуль аудіювання (Słuchanie) — на ОФІЦІЙНИХ матеріалах Держкомісії.

Транскрипти записів, питання й КЛЮЧ відповідей — з офіц. збірника ROZUMIENIE ZE
SŁUCHU B1 (розділ «KLUCZ I TRANSKRYPCJA NAGRAŃ», /tmp/b1_sluchanie.txt). Текст
озвучуємо локальним TTS (piper); якщо TTS недоступний — показуємо транскрипт.
Жодних вигаданих відповідей: усе з офіційного ключа.
"""

from __future__ import annotations

import random
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


SOURCE = "офіційний зразок Держкомісії (B1)"

_TAKNIE = ["TAK", "NIE"]

EXERCISES: list[Exercise] = [
    # Zadanie I — короткі висловлювання: «до чого належить фраза» (офіц. ключ I)
    Exercise(
        "u1", "Krótkie wypowiedzi (Zadanie 1)",
        "Прослухай коротку фразу й обери, де/що це. (на іспиті — лунає ОДИН раз)",
        [
            Segment("Czy jest jeszcze świeży chleb?",
                    [LQ("Taką wypowiedź najczęściej słyszymy:",
                        ["w restauracji", "w cukierni", "w sklepie spożywczym"], 2)]),
            Segment("Wszystkiego najlepszego na nowej drodze życia!",
                    [LQ("Taką wypowiedź najczęściej słyszymy:",
                        ["po egzaminie dyplomowym", "po ceremonii ślubnej", "po otrzymaniu awansu"], 1)]),
            Segment("Obiady wydajemy od trzynastej do piętnastej.",
                    [LQ("Ta wypowiedź jest typowa:", ["w barze", "w domu", "w kawiarni"], 0)]),
            Segment("Dałbyś już spokój!",
                    [LQ("Ta wypowiedź znaczy:", ["proszę o spokój", "jesteś niespokojny", "skończ, proszę!"], 2)]),
            Segment("W tym tygodniu Ryby mają szansę na awans.",
                    [LQ("Ta wypowiedź to:", ["reklama sklepu rybnego", "horoskop", "oferta restauracji"], 1)]),
            Segment("Proszę nie wchodzić bez obuwia ochronnego!",
                    [LQ("Ta wypowiedź jest typowa:",
                        ["w szpitalu", "kiedy robimy porządki w domu", "w sklepie z obuwiem"], 0)]),
            Segment("Proszę głęboko oddychać. Nie oddychać.",
                    [LQ("Ta wypowiedź jest typowa:", ["na spacerze", "w perfumerii", "u lekarza"], 2)]),
            Segment("Proszę nie karmić zwierząt!",
                    [LQ("Ta wypowiedź jest typowa:", ["w sklepie", "w ZOO", "w lesie"], 1)]),
            Segment("Do czego to podobne!",
                    [LQ("Ta wypowiedź oznacza:",
                        ["oburzenie", "pytanie o podobieństwo", "pytanie o skojarzenia"], 0)]),
            Segment("Ulgowy proszę!",
                    [LQ("Taką wypowiedź najczęściej słyszymy:", ["w kiosku", "w aptece", "w urzędzie"], 0)]),
        ],
    ),
    # Zadanie III — монолог «willa wśród róż»: TAK/NIE (офіц. ключ III)
    Exercise(
        "willa", "Willa wśród róż (Zadanie — prawda/fałsz)",
        "Прослухай розповідь і познач TAK (правда) / NIE (неправда).",
        [
            Segment(
                "Znajdujemy się na Alei Wielkopolskiej, przy której stoi mój rodzinny dom, "
                "w którym mój dziadek spędził najpiękniejsze lata swojego życia. Według jego pomysłu "
                "został ten dom wybudowany w tysiąc dziewięćset dwudziestym dziewiątym roku, a w "
                "trzydziestym dziewiątym roku rodzina Nowowiejskich musiała opuścić ten dom, przenieść "
                "się do Krakowa i spędzić tam lata okupacji. Powrócili do Poznania na Aleję Wielkopolską "
                "w roku tysiąc dziewięćset czterdziestym piątym, gdzie dziadek Nowowiejski spędził jeszcze "
                "rok swojego życia i tutaj zmarł. Na wprost wejścia frontowego znajduje się salonik, "
                "ulubione instrumenty mojego dziadka, a z okien saloniku ulubiony widok. W tym ogrodzie "
                "hodowane były róże, które uwielbiała moja babcia, dlatego willę nazywano willą wśród róż.",
                [
                    LQ("W tym domu mieszkała rodzina kobiety.", _TAKNIE, 0),
                    LQ("Dom zaprojektował znany architekt.", _TAKNIE, 1,
                       "Дім збудовано за задумом дідуся, не відомого архітектора."),
                    LQ("Dziadek w 1929 roku przeprowadził się do Krakowa.", _TAKNIE, 1,
                       "1929 — збудували дім; до Кракова переїхали 1939."),
                    LQ("Nowowiejscy mieszkali przed wojną na Alei Wielkopolskiej 10 lat.", _TAKNIE, 0,
                       "1929–1939 = 10 років."),
                    LQ("Dziadek zmarł w 1945 roku.", _TAKNIE, 1,
                       "Повернулись 1945 і прожив ще рік → помер близько 1946."),
                    LQ("Instrumenty dziadka stoją przed wejściem do domu.", _TAKNIE, 1,
                       "Інструменти в саліонику навпроти входу, не перед домом."),
                    LQ("Dziadek lubił widok z okna saloniku.", _TAKNIE, 0),
                    LQ("„Willa wśród róż” znajduje się w Poznaniu.", _TAKNIE, 0),
                ],
            )
        ],
    ),
    # Zadanie IV — монолог про музей: a/b/c (офіц. ключ IV)
    Exercise(
        "muzeum", "Muzeum Kultury Łemkowskiej (Zadanie a/b/c)",
        "Прослухай розповідь і обери правильну відповідь.",
        [
            Segment(
                "Jedzie się w kierunku Barwinka – to jest przejście graniczne – i w Tylawie na lewo "
                "skręca się do Zyndranowej; to jest trzy kilometry i od razu na samym początku pod "
                "numerem pierwszym znajduje się Muzeum Kultury Łemkowskiej. Muzeum już istnieje "
                "trzydzieści sześć lat. Jest to taki zestaw budynków łemkowskich: budynek mieszkalny, "
                "koniusznia i taki mniejszy gospodarczy budynek. Myśmy na początku, jeszcze kiedy nie "
                "było tego muzeum, mieszkali w tych budynkach, a obok budowaliśmy nowy dom. Kiedy "
                "zamieszkaliśmy w nowym domu, wtedy powstał pomysł, żeby stworzyć muzeum. Obecnie "
                "można by to nazwać takim małym skansenem.",
                [
                    LQ("Muzeum znajduje się pod numerem:", ["pierwszym", "piętnastym", "piątym"], 0),
                    LQ("Jest to muzeum:",
                       ["literatury łemkowskiej", "muzyki łemkowskiej", "kultury łemkowskiej"], 2),
                    LQ("Muzeum istnieje:", ["46 lat", "36 lat", "6 lat"], 1),
                    LQ("Rodzina kobiety mieszkała:",
                       ["w skansenie", "w bloku", "w budynkach, gdzie dziś jest muzeum"], 2),
                    LQ("Dzisiaj rodzina mieszka:",
                       ["w muzeum", "w domu blisko muzeum", "w małym skansenie"], 1),
                ],
            )
        ],
    ),
]


def by_id(exercise_id: str) -> Exercise | None:
    return next((e for e in EXERCISES if e.id == exercise_id), None)


def pick() -> Exercise:
    return random.choice(EXERCISES)


def total_questions(ex: Exercise) -> int:
    return sum(len(s.questions) for s in ex.segments)
