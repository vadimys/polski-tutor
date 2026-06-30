"""Тренування у форматі екзамену: банк питань (граматика + читання/лексика).

Окремий від placement банк (більше варіативності й не «зливає» відповіді тесту).
Миттєвий фідбек на кожну відповідь, оновлення готовності модуля.
"""

from __future__ import annotations

import random

from app.domain.models import Module
from app.services.placement import Question  # переюзаємо форму питання

DRILLS: list[Question] = [
    # --- Gramatyka ---
    Question("dg1", Module.GRAMATYKA, "A2", "Nie lubię ___ (kawa).",
             ["kawa", "kawy", "kawę", "kawą"], 1,
             "Заперечення «nie» + перехідне дієслово → РОДОВИЙ, не знахідний: kawę → kawy."),
    Question("dg2", Module.GRAMATYKA, "B1", "Czytam książkę, ___ jest bardzo ciekawa.",
             ["który", "która", "które", "którzy"], 1,
             "«książka» — ж.р. → który → która (узгодження займенника)."),
    Question("dg3", Module.GRAMATYKA, "A2", "Wczoraj ___ w kinie. (ja, m.)",
             ["byłem", "byłam", "jestem", "będę"], 0,
             "Минулий час «być», чоловік: byłem. (жінка — byłam)."),
    Question("dg4", Module.GRAMATYKA, "B1", "Gdyby ___ więcej czasu, odpoczęlibyśmy.",
             ["mamy", "mieliśmy", "mielibyśmy", "będziemy mieć"], 2,
             "Умовний спосіб (gdyby + …libyśmy): mielibyśmy («якби ми мали»)."),
    Question("dg5", Module.GRAMATYKA, "A2", "Codziennie idę ___ pracy.",
             ["do", "na", "w", "z"], 0,
             "«iść do pracy» — прийменник «do» + родовий."),
    Question("dg6", Module.GRAMATYKA, "B1", "On jest ___ od brata. (wysoki)",
             ["wysoki", "wyższy", "najwyższy", "wysoko"], 1,
             "Вищий ступінь + «od»: wyższy od brata («вищий за брата»)."),
    Question("dg7", Module.GRAMATYKA, "A2", "Mam dwa ___ . (kot)",
             ["kot", "koty", "kotów", "kota"], 1,
             "Після 2/3/4 — називний множини: dwa koty."),
    Question("dg8", Module.GRAMATYKA, "B1", "Musisz ___ do lekarza.",
             ["pójść", "pójdziesz", "poszedł", "idź"], 0,
             "Після «musisz» — інфінітив: pójść."),
    # --- Czytanie / słownictwo ---
    Question("dc1", Module.CZYTANIE, "A2",
             "Sklep jest czynny od 8 do 20. — O której się zamyka?",
             ["o 8", "o 20", "o 12", "jest nieczynny"], 1,
             "«czynny do 20» = зачиняється о 20."),
    Question("dc2", Module.CZYTANIE, "B1",
             "Pociąg jest opóźniony o 30 minut. — Co z pociągiem?",
             ["przyjechał wcześniej", "jest spóźniony", "odwołany", "wszystko ok"], 1,
             "«opóźniony» = запізнюється."),
    Question("dc3", Module.CZYTANIE, "A2", "«mieszkanie» to po ukraińsku...",
             ["квартира", "місто", "лікарня", "робота"], 0,
             "mieszkanie = квартира (важливо для wynajem/meldunek)."),
    Question("dc4", Module.CZYTANIE, "B1", "Fałszywy przyjaciel: «owoce» znaczy...",
             ["овочі", "фрукти", "ягоди", "гриби"], 1,
             "Пастка! owoce = ФРУКТИ, а овочі — warzywa."),
    Question("dc5", Module.CZYTANIE, "A2", "Dziś poniedziałek. Jutro będzie...",
             ["niedziela", "wtorek", "sobota", "piątek"], 1,
             "Після poniedziałek — wtorek (вівторок)."),
    Question("dc6", Module.CZYTANIE, "B1", "«cudzoziemiec» to...",
             ["іноземець", "громадянин", "турист", "сусід"], 0,
             "cudzoziemiec = іноземець (ключове слово для karty pobytu)."),
]


def by_id(qid: str) -> Question | None:
    return next((q for q in DRILLS if q.id == qid), None)


def session(module: Module | None = None, n: int = 5) -> list[Question]:
    """Випадкові n питань (опційно лише з одного модуля)."""
    pool = [q for q in DRILLS if module is None or q.module == module]
    if len(pool) < n:
        pool = DRILLS
    return random.sample(pool, min(n, len(pool)))
