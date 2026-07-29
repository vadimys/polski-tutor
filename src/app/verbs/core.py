"""Група 1 — Базові дієслова: бути, мати, могти, хотіти… (без них — нікуди)."""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="core",
    icon="⭐",
    title="Базові",
    subtitle="10 дієслів, без яких не буває жодної розмови.",
    verbs=[
        Verb(
            "być", "бути", group="особливе",
            present=["jestem", "jesteś", "jest", "jesteśmy", "jesteście", "są"],
            past="on był · ona była · oni byli",
            examples=[("Jestem z Ukrainy.", "Я з України.")],
        ),
        Verb(
            "mieć", "мати", group="-am, -asz",
            present=["mam", "masz", "ma", "mamy", "macie", "mają"],
            past="on miał · ona miała · oni mieli",
            rekcja="kogo? co? (Biernik): mam kota, mam czas",
            examples=[("Nie mam czasu.", "Не маю часу.")],
        ),
        Verb(
            "robić", "робити", pair="zrobić", pair_hint="zrobię, zrobi",
            group="-ę, -isz",
            present=["robię", "robisz", "robi", "robimy", "robicie", "robią"],
            past="on robił · ona robiła · oni robili",
            rekcja="co? (Biernik): robię zakupy",
            examples=[("Co robisz wieczorem?", "Що робиш увечері?")],
        ),
        Verb(
            "móc", "могти", group="особливе (-ę, -esz)",
            present=["mogę", "możesz", "może", "możemy", "możecie", "mogą"],
            past="on mógł · ona mogła · oni mogli",
            examples=[("Czy mogę wejść?", "Можна увійти?")],
        ),
        Verb(
            "chcieć", "хотіти", group="особливе (-ę, -esz)",
            present=["chcę", "chcesz", "chce", "chcemy", "chcecie", "chcą"],
            past="on chciał · ona chciała · oni chcieli",
            examples=[("Chcę się uczyć polskiego.", "Хочу вчити польську.")],
        ),
        Verb(
            "musieć", "мусити", group="-ę, -isz",
            present=["muszę", "musisz", "musi", "musimy", "musicie", "muszą"],
            past="on musiał · ona musiała · oni musieli",
            examples=[("Muszę już iść.", "Мушу вже йти.")],
        ),
        Verb(
            "wiedzieć", "знати (факт)", group="особливе",
            present=["wiem", "wiesz", "wie", "wiemy", "wiecie", "wiedzą"],
            past="on wiedział · ona wiedziała · oni wiedzieli",
            rekcja="o kim? o czym? (o + Miejscownik) або що…: wiem, że…",
            examples=[("Nie wiem, gdzie to jest.", "Не знаю, де це.")],
        ),
        Verb(
            "znać", "знати (когось/щось)", pair="poznać", pair_hint="poznam, pozna",
            group="-am, -asz",
            present=["znam", "znasz", "zna", "znamy", "znacie", "znają"],
            past="on znał · ona znała · oni znali",
            rekcja="kogo? co? (Biernik): znam Annę, znam to miasto",
            examples=[("Znasz ten film?", "Знаєш цей фільм?")],
        ),
        Verb(
            "umieć", "уміти", group="особливе (-em, -esz)",
            present=["umiem", "umiesz", "umie", "umiemy", "umiecie", "umieją"],
            past="on umiał · ona umiała · oni umieli",
            examples=[("Umiem pływać.", "Умію плавати.")],
        ),
        Verb(
            "potrzebować", "потребувати", group="-uję, -ujesz",
            present=["potrzebuję", "potrzebujesz", "potrzebuje", "potrzebujemy",
                     "potrzebujecie", "potrzebują"],
            past="on potrzebował · ona potrzebowała · oni potrzebowali",
            rekcja="kogo? czego? (Dopełniacz!): potrzebuję pomocy",
            examples=[("Potrzebuję twojej pomocy.", "Мені потрібна твоя допомога.")],
        ),
    ],
)
