"""Група 6 — Робота і справи: працювати, вчитися, шукати, брати, допомагати…"""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="praca",
    icon="💼",
    title="Робота і справи",
    subtitle="Праця, навчання, пошук — і найпідступніші rekcje (szukać/pomagać).",
    verbs=[
        Verb(
            "pracować", "працювати", group="-uję, -ujesz",
            present=["pracuję", "pracujesz", "pracuje", "pracujemy", "pracujecie",
                     "pracują"],
            past="on pracował · ona pracowała · oni pracowali",
            rekcja="w + Miejscownik / jako + Mianownik: pracuję w biurze jako grafik",
            examples=[("Pracuję zdalnie.", "Працюю віддалено.")],
        ),
        Verb(
            "uczyć się", "вчитися", pair="nauczyć się", pair_hint="nauczę się, nauczy się",
            group="-ę, -ysz",
            present=["uczę się", "uczysz się", "uczy się", "uczymy się", "uczycie się",
                     "uczą się"],
            past="on uczył się · ona uczyła się · oni uczyli się",
            rekcja="czego? (Dopełniacz!): uczę się polskiego (не «polski»)", rekcja_q="Dopełniacz",
            examples=[("Uczę się polskiego codziennie.", "Вчу польську щодня.")],
        ),
        Verb(
            "mieszkać", "мешкати, жити", group="-am, -asz",
            present=["mieszkam", "mieszkasz", "mieszka", "mieszkamy", "mieszkacie",
                     "mieszkają"],
            past="on mieszkał · ona mieszkała · oni mieszkali",
            rekcja="w + Miejscownik: mieszkam w Warszawie",
            examples=[("Mieszkam w Polsce od roku.", "Живу в Польщі рік.")],
        ),
        Verb(
            "szukać", "шукати", pair="poszukać", pair_hint="poszukam, poszuka",
            group="-am, -asz",
            present=["szukam", "szukasz", "szuka", "szukamy", "szukacie", "szukają"],
            past="on szukał · ona szukała · oni szukali",
            rekcja="kogo? czego? (Dopełniacz!): szukam pracy (не «pracę»)", rekcja_q="Dopełniacz",
            examples=[("Szukam mieszkania w centrum.", "Шукаю квартиру в центрі.")],
        ),
        Verb(
            "znajdować", "знаходити", pair="znaleźć", pair_hint="znajdę, znajdzie",
            group="-uję, -ujesz",
            present=["znajduję", "znajdujesz", "znajduje", "znajdujemy", "znajdujecie",
                     "znajdują"],
            past="on znajdował · ona znajdowała · oni znajdowali (znaleźć: znalazł/znalazła/znaleźli)",
            rekcja="kogo? co? (Biernik): znalazłem pracę",
            examples=[("W końcu znalazłem klucze!", "Нарешті знайшов ключі!")],
        ),
        Verb(
            "dawać", "давати", pair="dać", pair_hint="dam, da (oni dadzą!)",
            group="-ję, -jesz",
            present=["daję", "dajesz", "daje", "dajemy", "dajecie", "dają"],
            past="on dawał · ona dawała · oni dawali",
            rekcja="komu? (Celownik) + co? (Biernik): daję mamie kwiaty",
            examples=[("Dam ci znać jutro.", "Дам тобі знати завтра.")],
        ),
        Verb(
            "brać", "брати", pair="wziąć", pair_hint="wezmę, weźmie",
            group="особливе (-ę, -esz)",
            present=["biorę", "bierzesz", "bierze", "bierzemy", "bierzecie", "biorą"],
            past="on brał · ona brała · oni brali (wziąć: wziął/wzięła/wzięli)",
            rekcja="co? (Biernik): biorę parasol",
            examples=[("Wezmę taksówkę.", "Візьму таксі.")],
        ),
        Verb(
            "czekać", "чекати", pair="poczekać", pair_hint="poczekam, poczeka",
            group="-am, -asz",
            present=["czekam", "czekasz", "czeka", "czekamy", "czekacie", "czekają"],
            past="on czekał · ona czekała · oni czekali",
            rekcja="na + Biernik!: czekam na autobus, czekam na ciebie", rekcja_q="na + Biernik",
            examples=[("Czekam na odpowiedź.", "Чекаю на відповідь.")],
        ),
        Verb(
            "pomagać", "допомагати", pair="pomóc", pair_hint="pomogę, pomoże",
            group="-am, -asz",
            present=["pomagam", "pomagasz", "pomaga", "pomagamy", "pomagacie", "pomagają"],
            past="on pomagał · ona pomagała · oni pomagali (pomóc: pomógł/pomogła/pomogli)",
            rekcja="komu? (Celownik!): pomagam bratu (не «brata»)", rekcja_q="Celownik",
            examples=[("Mogę ci pomóc?", "Можу тобі допомогти?")],
        ),
        Verb(
            "kończyć", "закінчувати", pair="skończyć", pair_hint="skończę, skończy",
            group="-ę, -ysz",
            present=["kończę", "kończysz", "kończy", "kończymy", "kończycie", "kończą"],
            past="on kończył · ona kończyła · oni kończyli",
            rekcja="co? (Biernik): kończę pracę o piątej",
            examples=[("Kiedy kończysz pracę?", "Коли закінчуєш роботу?")],
        ),
    ],
)
