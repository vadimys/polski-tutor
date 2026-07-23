"""Модуль 8 — Прикметник (przymiotnik): узгодження + ступенювання."""

from __future__ import annotations

from app.grammar.schema import Card, Lesson, Module, Quiz

MODULE = Module(
    id="przymiotnik",
    icon="🎨",
    title="Прикметник",
    subtitle="Який? яка? яке? Узгодження з іменником і як порівнювати (кращий, найкращий).",
    lessons=[
        # ── Узгодження ──
        Lesson(
            id="prz_zgoda",
            title="Прикметник підлаштовується під іменник",
            cards=[
                Card(
                    "Рід прикметника = рід іменника",
                    "Прикметник змінює закінчення під рід слова:\n• чол. → <code>-y/-i</code>\n"
                    "• жін. → <code>-a</code>\n• сер. → <code>-e</code>",
                    [("ładny dom", "гарний дім (ч.)"), ("ładna kobieta", "гарна жінка (ж.)"),
                     ("ładne okno", "гарне вікно (с.)")],
                ),
                Card(
                    "Місце — зазвичай перед іменником",
                    "Як в українській: <i>duży dom</i> (великий дім). Після іменника — коли це "
                    "тип/класифікація (<i>język polski</i> — польська мова).",
                    [("nowy telefon", "новий телефон"), ("dzień dobry", "добрий день")],
                    tip="Вивчай іменник + прикметник разом — так одразу тренуєш узгодження.",
                ),
            ],
            quiz=[
                Quiz("«гарна жінка»: ładn_ kobieta —", ["ładny", "ładna", "ładne"], 1,
                     "Жін. рід → -a: ładna kobieta."),
                Quiz("«нове вікно»: now_ okno —", ["nowy", "nowa", "nowe"], 2, "Сер. рід → -e: nowe okno."),
            ],
        ),
        # ── Множина ──
        Lesson(
            id="prz_liczba",
            title="Прикметник у множині",
            cards=[
                Card(
                    "Дві форми множини",
                    "Знову важлива група <b>людей-чоловіків</b>:\n• люди-чоловіки → <code>-i/-y</code> "
                    "(зі змʼякшенням)\n• усе інше → <code>-e</code>",
                    [("mili chłopcy", "милі хлопці"), ("miłe dziewczyny", "милі дівчата"),
                     ("nowe domy", "нові будинки")],
                ),
                Card(
                    "Той самий принцип, що й в іменнику",
                    "Прикметник іде за іменником: якщо в групі є чоловік-людина — особлива форма.",
                    tip="Порівняй: dobrzy studenci (студенти-чоловіки) vs dobre koty (коти).",
                ),
            ],
            quiz=[
                Quiz("«милі хлопці»: mil_ chłopcy —", ["miłe", "mili", "miły"], 1,
                     "Люди-чоловіки → -i: mili."),
            ],
        ),
        # ── Ступенювання регулярне ──
        Lesson(
            id="prz_stopniowanie",
            title="Ступенювання: -szy та naj-",
            cards=[
                Card(
                    "Вищий ступінь: -szy / -ejszy",
                    "«Більш…» = основа + <code>-szy</code> (або -ejszy для довших).",
                    [("nowy → nowszy", "новий → новіший"), ("ładny → ładniejszy", "гарний → гарніший"),
                     ("tani → tańszy", "дешевий → дешевший")],
                ),
                Card(
                    "Найвищий ступінь: naj-",
                    "«Най…» = <code>naj-</code> + форма вищого ступеня.",
                    [("najnowszy", "найновіший"), ("najładniejszy", "найгарніший")],
                ),
                Card(
                    "«Ніж» = niż",
                    "Порівнюючи, вживай <code>niż</code> (ніж).",
                    [("Ten dom jest większy niż tamten.", "Цей дім більший, ніж той.")],
                    tip="Довгі прикметники часто беруть -ejszy: ładny→ładniejszy. Коротші — -szy: nowy→nowszy.",
                ),
            ],
            quiz=[
                Quiz("Найвищий ступінь від «nowy» —", ["nowszy", "najnowszy", "nowny"], 1,
                     "naj- + nowszy = najnowszy."),
            ],
        ),
        # ── Ступенювання неправильне ──
        Lesson(
            id="prz_nieregularne",
            title="Неправильне ступенювання (важливе!)",
            cards=[
                Card(
                    "Ці чотири — напамʼять",
                    "Найчастіші прикметники ступенюються неправильно:",
                    [("dobry → lepszy → najlepszy", "добрий → кращий → найкращий"),
                     ("zły → gorszy → najgorszy", "поганий → гірший → найгірший"),
                     ("duży → większy → największy", "великий → більший → найбільший"),
                     ("mały → mniejszy → najmniejszy", "малий → менший → найменший")],
                ),
                Card(
                    "У житті — щодня",
                    "Ці слова всюди: <i>lepszy</i> (кращий), <i>gorszy</i> (гірший)…",
                    [("To lepszy pomysł.", "Це краща ідея."),
                     ("Mam większy problem.", "У мене більша проблема.")],
                    tip="Вивчи ці 4 трійки — і ти покриваєш більшість порівнянь у щоденній мові.",
                ),
            ],
            quiz=[
                Quiz("Вищий ступінь від «dobry» —", ["dobrszy", "lepszy", "najdobry"], 1,
                     "Неправильне: dobry → lepszy."),
                Quiz("«найбільший» —", ["najduży", "największy", "bardziej duży"], 1,
                     "duży → większy → największy."),
            ],
        ),
    ],
)
