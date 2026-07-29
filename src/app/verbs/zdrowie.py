"""Група 8 — Здоровʼя і самопочуття: хворіти, відпочивати, прокидатися…"""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="zdrowie",
    icon="🩺",
    title="Здоровʼя і самопочуття",
    subtitle="Хворію, відпочиваю, прокидаюся — і чому «chorować NA grypę».",
    verbs=[
        Verb(
            "chorować", "хворіти", pair="zachorować", pair_hint="zachoruję, zachoruje",
            group="-uję, -ujesz",
            present=["choruję", "chorujesz", "choruje", "chorujemy", "chorujecie",
                     "chorują"],
            past="on chorował · ona chorowała · oni chorowali",
            rekcja="na + Biernik!: choruję na grypę (не «grypą»)", rekcja_q="na + Biernik",
            examples=[("Zachorowałem na grypę.", "Я захворів на грип.")],
        ),
        Verb(
            "leczyć się", "лікуватися", pair="wyleczyć się",
            pair_hint="wyleczę się, wyleczy się", group="-ę, -ysz",
            present=["leczę się", "leczysz się", "leczy się", "leczymy się", "leczycie się",
                     "leczą się"],
            past="on leczył się · ona leczyła się · oni leczyli się",
            rekcja="u + Dopełniacz: leczę się u dobrego lekarza",
            examples=[("Leczę się u tego lekarza.", "Лікуюся в цього лікаря.")],
        ),
        Verb(
            "odpoczywać", "відпочивати", pair="odpocząć", pair_hint="odpocznę, odpocznie",
            group="-am, -asz",
            present=["odpoczywam", "odpoczywasz", "odpoczywa", "odpoczywamy",
                     "odpoczywacie", "odpoczywają"],
            past="on odpoczywał · ona odpoczywała · oni odpoczywali",
            examples=[("W weekend odpoczywam nad jeziorem.", "У вихідні відпочиваю біля озера.")],
        ),
        Verb(
            "męczyć się", "втомлюватися", pair="zmęczyć się",
            pair_hint="zmęczę się, zmęczy się", group="-ę, -ysz",
            present=["męczę się", "męczysz się", "męczy się", "męczymy się", "męczycie się",
                     "męczą się"],
            past="on męczył się · ona męczyła się · oni męczyli się",
            examples=[("Szybko się męczę.", "Швидко втомлююся.")],
        ),
        Verb(
            "budzić się", "прокидатися", pair="obudzić się",
            pair_hint="obudzę się, obudzi się", group="-ę, -isz",
            present=["budzę się", "budzisz się", "budzi się", "budzimy się", "budzicie się",
                     "budzą się"],
            past="on budził się · ona budziła się · oni budzili się",
            examples=[("Budzę się o szóstej.", "Прокидаюся о шостій.")],
        ),
        Verb(
            "zasypiać", "засинати", pair="zasnąć", pair_hint="zasnę, zaśnie",
            group="-am, -asz",
            present=["zasypiam", "zasypiasz", "zasypia", "zasypiamy", "zasypiacie",
                     "zasypiają"],
            past="on zasypiał · ona zasypiała · oni zasypiali (zasnąć: zasnął/zasnęła/zasnęli)",
            examples=[("Nie mogę zasnąć.", "Не можу заснути.")],
        ),
        Verb(
            "ćwiczyć", "тренуватися, вправлятися", group="-ę, -ysz",
            present=["ćwiczę", "ćwiczysz", "ćwiczy", "ćwiczymy", "ćwiczycie", "ćwiczą"],
            past="on ćwiczył · ona ćwiczyła · oni ćwiczyli",
            examples=[("Ćwiczę trzy razy w tygodniu.", "Тренуюся тричі на тиждень.")],
        ),
        Verb(
            "spacerować", "гуляти, прогулюватися", group="-uję, -ujesz",
            present=["spaceruję", "spacerujesz", "spaceruje", "spacerujemy", "spacerujecie",
                     "spacerują"],
            past="on spacerował · ona spacerowała · oni spacerowali",
            rekcja="po + Miejscownik: spaceruję po parku", rekcja_q="po + Miejscownik",
            examples=[("Wieczorem spaceruję po parku.", "Увечері гуляю парком.")],
        ),
        Verb(
            "dbać", "дбати", group="-am, -asz",
            present=["dbam", "dbasz", "dba", "dbamy", "dbacie", "dbają"],
            past="on dbał · ona dbała · oni dbali",
            rekcja="o + Biernik!: dbam o zdrowie", rekcja_q="o + Biernik",
            examples=[("Dbam o swoje zdrowie.", "Дбаю про своє здоровʼя.")],
        ),
        Verb(
            "uśmiechać się", "усміхатися", pair="uśmiechnąć się",
            pair_hint="uśmiechnę się, uśmiechnie się", group="-am, -asz",
            present=["uśmiecham się", "uśmiechasz się", "uśmiecha się", "uśmiechamy się",
                     "uśmiechacie się", "uśmiechają się"],
            past="on uśmiechał się · ona uśmiechała się · oni uśmiechali się",
            rekcja="do + Dopełniacz: uśmiecham się do ciebie", rekcja_q="do + Dopełniacz",
            examples=[("Ona zawsze się uśmiecha.", "Вона завжди усміхається.")],
        ),
    ],
)
