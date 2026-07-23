"""Модуль 11 — Прийменники (przyimki): який відмінок вимагають, місце/рух/час."""

from __future__ import annotations

from app.grammar.schema import Card, Lesson, Module, Quiz

MODULE = Module(
    id="przyimki",
    icon="🧭",
    title="Прийменники",
    subtitle="w, na, do, z, o… — і який відмінок кожен «вмикає».",
    lessons=[
        # ── Вступ ──
        Lesson(
            id="pi_wstep",
            title="Прийменник керує відмінком",
            cards=[
                Card(
                    "Головна ідея",
                    "Кожен прийменник «вмикає» певний відмінок наступного слова. Вивчати "
                    "прийменник варто <b>разом із відмінком</b>, який він вимагає.",
                    [("do domu", "додому (do + Dopełniacz)"),
                     ("z bratem", "з братом (z + Narzędnik)")],
                ),
                Card(
                    "Ти вже знаєш багато",
                    "З модуля «Відмінки»: <b>do, od, bez, dla</b> → Dopełniacz · <b>z</b> (разом) → "
                    "Narzędnik · <b>w, na, o</b> (місце) → Miejscownik. Тепер упорядкуємо.",
                    tip="Один прийменник іноді керує різними відмінками — залежно від значення (див. далі).",
                ),
            ],
            quiz=[
                Quiz("«do domu»: який відмінок після do?", ["Biernik", "Dopełniacz", "Narzędnik"], 1,
                     "do + Dopełniacz: do domu."),
            ],
        ),
        # ── Місце ──
        Lesson(
            id="pi_miejsce",
            title="Де? — місце (w, na, przy, obok)",
            cards=[
                Card(
                    "w / na + Miejscownik",
                    "«У/на» для місця → Miejscownik.",
                    [("w domu", "вдома"), ("na stole", "на столі"), ("w Polsce", "у Польщі")],
                ),
                Card(
                    "w чи na?",
                    "• <b>w</b> — усередині (w domu, w szkole)\n• <b>na</b> — на поверхні або з подіями/"
                    "відкритими місцями (na stole, na uniwersytecie, na koncercie)",
                    [("na poczcie", "на пошті"), ("na wsi", "у селі")],
                    tip="w/na — питання звички. Запамʼятовуй у фразах: «w pracy», але «na uczelni».",
                ),
                Card(
                    "Поруч: przy, obok, koło",
                    "<b>przy</b> (біля) → Miejscownik · <b>obok / koło</b> (поруч/біля) → Dopełniacz.",
                    [("przy stole", "за столом"), ("obok domu", "поруч із домом")],
                ),
            ],
            quiz=[
                Quiz("«на столі» —", ["na stole", "na stół", "na stołem"], 0,
                     "na + Miejscownik: na stole."),
            ],
        ),
        # ── Рух ──
        Lesson(
            id="pi_ruch",
            title="Куди / звідки? — рух (do, na, z, od)",
            cards=[
                Card(
                    "Куди",
                    "• <b>do</b> + Dopełniacz — до/в (місця): do domu, do szkoły\n"
                    "• <b>na</b> + Biernik — на (подію/відкрите): na koncert, na pocztę",
                    [("Idę do sklepu.", "Іду в магазин."), ("Idę na koncert.", "Іду на концерт.")],
                ),
                Card(
                    "Звідки",
                    "• <b>z</b> + Dopełniacz — з (місця): z domu, z Polski\n"
                    "• <b>od</b> + Dopełniacz — від (людини): od mamy",
                    [("Wracam z pracy.", "Повертаюся з роботи."),
                     ("List od babci.", "Лист від бабусі.")],
                    tip="Пара «куди↔звідки»: do↔z (do domu / z domu), na↔z (na pocztę / z poczty).",
                ),
            ],
            quiz=[
                Quiz("«Іду в магазин»: do sklep_ —", ["sklep", "sklepu", "sklepem"], 1,
                     "do + Dopełniacz: do sklepu."),
            ],
        ),
        # ── Час ──
        Lesson(
            id="pi_czas",
            title="Коли? — час (w, o, za, przez)",
            cards=[
                Card(
                    "Дні й години",
                    "• <b>w</b> + день (Biernik): w poniedziałek (у понеділок)\n"
                    "• <b>o</b> + година (Miejscownik): o piątej (о пʼятій)",
                    [("w sobotę", "у суботу"), ("o dziesiątej", "о десятій")],
                ),
                Card(
                    "Тривалість і «через»",
                    "• <b>przez</b> + Biernik — протягом: przez godzinę (годину)\n"
                    "• <b>za</b> + Biernik — через (у майбутньому): za godzinę (за годину)",
                    [("Uczę się przez godzinę.", "Вчуся годину."),
                     ("Wrócę za tydzień.", "Повернуся за тиждень.")],
                    tip="«za» тут = «через стільки-то часу», а не «за» у просторі.",
                ),
            ],
            quiz=[
                Quiz("«у понеділок» —", ["w poniedziałek", "o poniedziałku", "za poniedziałek"], 0,
                     "День → w + Biernik: w poniedziałek."),
            ],
        ),
    ],
)
