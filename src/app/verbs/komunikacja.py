"""Група 4 — Спілкування: говорити, питати, просити, дякувати…"""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="komunikacja",
    icon="💬",
    title="Спілкування",
    subtitle="Говорити, питати, дякувати — і з якими відмінками це працює.",
    verbs=[
        Verb(
            "mówić", "говорити, казати", pair="powiedzieć", pair_hint="powiem, powie",
            group="-ę, -isz",
            present=["mówię", "mówisz", "mówi", "mówimy", "mówicie", "mówią"],
            past="on mówił · ona mówiła · oni mówili",
            rekcja="komu? (Celownik) + o czym? (o + Miejscownik): mówię ci o pracy",
            examples=[("Mówię trochę po polsku.", "Трохи говорю польською.")],
        ),
        Verb(
            "rozmawiać", "розмовляти", group="-am, -asz",
            present=["rozmawiam", "rozmawiasz", "rozmawia", "rozmawiamy", "rozmawiacie",
                     "rozmawiają"],
            past="on rozmawiał · ona rozmawiała · oni rozmawiali",
            rekcja="z + Narzędnik · o + Miejscownik: rozmawiam z bratem o pracy", rekcja_q="z + Narzędnik",
            examples=[("Rozmawiamy o planach.", "Розмовляємо про плани.")],
        ),
        Verb(
            "pytać", "питати", pair="zapytać", pair_hint="zapytam, zapyta",
            group="-am, -asz",
            present=["pytam", "pytasz", "pyta", "pytamy", "pytacie", "pytają"],
            past="on pytał · ona pytała · oni pytali",
            rekcja="kogo? (Biernik) + o co? (o + Biernik): pytam go o drogę",
            examples=[("Mogę o coś zapytać?", "Можна щось спитати?")],
        ),
        Verb(
            "odpowiadać", "відповідати", pair="odpowiedzieć", pair_hint="odpowiem, odpowie",
            group="-am, -asz",
            present=["odpowiadam", "odpowiadasz", "odpowiada", "odpowiadamy",
                     "odpowiadacie", "odpowiadają"],
            past="on odpowiadał · ona odpowiadała · oni odpowiadali",
            rekcja="na + Biernik: odpowiadam na pytanie", rekcja_q="na + Biernik",
            examples=[("Odpowiem na twoje pytanie.", "Відповім на твоє питання.")],
        ),
        Verb(
            "prosić", "просити", pair="poprosić", pair_hint="poproszę, poprosi",
            group="-ę, -isz",
            present=["proszę", "prosisz", "prosi", "prosimy", "prosicie", "proszą"],
            past="on prosił · ona prosiła · oni prosili",
            rekcja="kogo? + o co? (o + Biernik): proszę cię o pomoc", rekcja_q="o + Biernik",
            examples=[("Poproszę kawę.", "Будь ласка, каву. (у кавʼярні)")],
        ),
        Verb(
            "dziękować", "дякувати", pair="podziękować", pair_hint="podziękuję, podziękuje",
            group="-uję, -ujesz",
            present=["dziękuję", "dziękujesz", "dziękuje", "dziękujemy", "dziękujecie",
                     "dziękują"],
            past="on dziękował · ona dziękowała · oni dziękowali",
            rekcja="komu? (Celownik!) + za co? (za + Biernik): dziękuję ci za pomoc", rekcja_q="Celownik",
            examples=[("Dziękuję za wszystko.", "Дякую за все.")],
        ),
        Verb(
            "dzwonić", "телефонувати", pair="zadzwonić", pair_hint="zadzwonię, zadzwoni",
            group="-ę, -isz",
            present=["dzwonię", "dzwonisz", "dzwoni", "dzwonimy", "dzwonicie", "dzwonią"],
            past="on dzwonił · ona dzwoniła · oni dzwonili",
            rekcja="do + Dopełniacz!: dzwonię do mamy (не «mamie»)", rekcja_q="do + Dopełniacz",
            examples=[("Zadzwonię do ciebie wieczorem.", "Подзвоню тобі ввечері.")],
        ),
        Verb(
            "pisać", "писати", pair="napisać", pair_hint="napiszę, napisze",
            group="-ę, -esz (pisz-)",
            present=["piszę", "piszesz", "pisze", "piszemy", "piszecie", "piszą"],
            past="on pisał · ona pisała · oni pisali",
            rekcja="co? (Biernik) + do kogo? (do + Dopełniacz): piszę list do babci",
            examples=[("Napiszę do ciebie jutro.", "Напишу тобі завтра.")],
        ),
        Verb(
            "czytać", "читати", pair="przeczytać", pair_hint="przeczytam, przeczyta",
            group="-am, -asz",
            present=["czytam", "czytasz", "czyta", "czytamy", "czytacie", "czytają"],
            past="on czytał · ona czytała · oni czytali",
            rekcja="co? (Biernik): czytam książkę", rekcja_q="Biernik",
            examples=[("Wieczorem czytam książki.", "Увечері читаю книжки.")],
        ),
        Verb(
            "słuchać", "слухати", pair="posłuchać", pair_hint="posłucham, posłucha",
            group="-am, -asz",
            present=["słucham", "słuchasz", "słucha", "słuchamy", "słuchacie", "słuchają"],
            past="on słuchał · ona słuchała · oni słuchali",
            rekcja="kogo? czego? (Dopełniacz!): słucham muzyki (не «muzykę»)", rekcja_q="Dopełniacz",
            examples=[("Słucham polskiej muzyki.", "Слухаю польську музику.")],
        ),
    ],
)
