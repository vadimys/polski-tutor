"""Модуль 10 — Числівники (liczebniki): кількісні, порядкові, число + іменник."""

from __future__ import annotations

from app.grammar.schema import Card, Lesson, Module, Quiz

MODULE = Module(
    id="liczebniki",
    icon="🔢",
    title="Числівники",
    subtitle="Рахуємо польською: 1, 2, 3… + хитре правило «число + іменник».",
    lessons=[
        # ── 1-20 ──
        Lesson(
            id="li_glowne",
            title="Числа 1–20 і десятки",
            cards=[
                Card(
                    "1–10",
                    "jeden, dwa, trzy, cztery, pięć, sześć, siedem, osiem, dziewięć, dziesięć.",
                    [("pięć", "пʼять"), ("dziesięć", "десять")],
                ),
                Card(
                    "11–20",
                    "Додаємо <b>-naście</b>: jedenaście, dwanaście, trzynaście… dwadzieścia (20).",
                    [("dwanaście", "дванадцять"), ("piętnaście", "пʼятнадцять")],
                ),
                Card(
                    "Десятки",
                    "dziesięć (10), dwadzieścia (20), trzydzieści (30), czterdzieści (40), "
                    "pięćdziesiąt (50)…",
                    [("dwadzieścia pięć", "двадцять пʼять")],
                    tip="Складаєш як в українській: 25 = dwadzieścia (20) + pięć (5).",
                ),
            ],
            quiz=[
                Quiz("«пʼять» польською —", ["pięć", "sześć", "piąty"], 0, "5 = pięć."),
            ],
        ),
        # ── більші ──
        Lesson(
            id="li_wieksze",
            title="Сотні, тисячі й побудова чисел",
            cards=[
                Card(
                    "100, 1000",
                    "<b>sto</b> (100), <b>tysiąc</b> (1000), <b>milion</b> (мільйон).",
                    [("dwieście", "200"), ("trzysta", "300"), ("pięćset", "500")],
                ),
                Card(
                    "Читаємо великі числа зліва направо",
                    "Як в українській: 253 = dwieście pięćdziesiąt trzy.",
                    [("tysiąc dziewięćset", "1900"), ("dwa tysiące dwadzieścia sześć", "2026")],
                ),
            ],
            quiz=[
                Quiz("«500» —", ["pięćdziesiąt", "pięćset", "pięć sto"], 1, "500 = pięćset."),
            ],
        ),
        # ── порядкові ──
        Lesson(
            id="li_porzadkowe",
            title="Порядкові: перший, другий…",
            cards=[
                Card(
                    "Який за рахунком",
                    "pierwszy (1-й), drugi (2-й), trzeci (3-й), czwarty, piąty, szósty…",
                    [("pierwszy raz", "перший раз"), ("drugie piętro", "другий поверх")],
                ),
                Card(
                    "Поводяться як прикметники",
                    "Узгоджуються за родом: <b>pierwszy</b> (ч.) / <b>pierwsza</b> (ж.) / "
                    "<b>pierwsze</b> (с.).",
                    [("pierwsza klasa", "перший клас"), ("Jest piąta.", "Пʼята година.")],
                    tip="Дати й час — теж порядкові: «pierwszy maja» (перше травня).",
                ),
            ],
            quiz=[
                Quiz("«перший» —", ["jeden", "pierwszy", "raz"], 1,
                     "Порядковий: pierwszy (кількісний jeden = один)."),
            ],
        ),
        # ── число + іменник ──
        Lesson(
            id="li_z_rzeczownikiem",
            title="Хитре правило: число + іменник",
            cards=[
                Card(
                    "Іменник змінюється залежно від числа",
                    "Це відрізняється від української й дуже важливе:",
                    [("1 → jeden kot", "один кіт (однина)"),
                     ("2, 3, 4 → dwa koty", "два/три/чотири коти (множина Nom)"),
                     ("5+ → pięć kotów", "пʼять котів (Dopełniacz мн.!)")],
                ),
                Card(
                    "Логіка правила",
                    "• <b>1</b> → однина\n• <b>2–4</b> → звичайна множина\n"
                    "• <b>5 і більше</b> → Dopełniacz множини (як «багато чогось»)",
                    [("cztery książki", "чотири книжки"), ("pięć książek", "пʼять книжок"),
                     ("dwadzieścia lat", "двадцять років")],
                    tip="Хитрість: 22, 23, 24 поводяться як 2–4 (dwadzieścia dwa koty), а 25 — як 5 (kotów). "
                        "Дивись на ОСТАННЮ цифру.",
                ),
            ],
            quiz=[
                Quiz("«пʼять котів» —", ["pięć koty", "pięć kotów", "pięć kot"], 1,
                     "5+ → Dopełniacz множини: pięć kotów."),
                Quiz("«три книжки» —", ["trzy książek", "trzy książki", "trzy książka"], 1,
                     "2–4 → звичайна множина: trzy książki."),
            ],
        ),
    ],
)
