"""Група 5 — Розум і почуття: думати, розуміти, любити, боятися…"""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="umysl",
    icon="❤️",
    title="Розум і почуття",
    subtitle="Думаю, розумію, люблю, боюся — і несподівані відмінки після них.",
    verbs=[
        Verb(
            "myśleć", "думати", pair="pomyśleć", pair_hint="pomyślę, pomyśli",
            group="-ę, -isz",
            present=["myślę", "myślisz", "myśli", "myślimy", "myślicie", "myślą"],
            past="on myślał · ona myślała · oni myśleli",
            rekcja="o kim? o czym? (o + Miejscownik): myślę o tobie", rekcja_q="o + Miejscownik",
            examples=[("Myślę, że masz rację.", "Думаю, що ти маєш рацію.")],
        ),
        Verb(
            "rozumieć", "розуміти", pair="zrozumieć", pair_hint="zrozumiem, zrozumie",
            group="особливе (-em, -esz)",
            present=["rozumiem", "rozumiesz", "rozumie", "rozumiemy", "rozumiecie",
                     "rozumieją"],
            past="on rozumiał · ona rozumiała · oni rozumieli",
            rekcja="kogo? co? (Biernik): rozumiem cię",
            examples=[("Nie rozumiem tego słowa.", "Не розумію цього слова.")],
        ),
        Verb(
            "pamiętać", "памʼятати", pair="zapamiętać", pair_hint="zapamiętam, zapamięta",
            group="-am, -asz",
            present=["pamiętam", "pamiętasz", "pamięta", "pamiętamy", "pamiętacie",
                     "pamiętają"],
            past="on pamiętał · ona pamiętała · oni pamiętali",
            rekcja="o kim? o czym? (o + Miejscownik) або kogo/co: pamiętam o tobie",
            examples=[("Pamiętam ten dzień.", "Памʼятаю той день.")],
        ),
        Verb(
            "zapominać", "забувати", pair="zapomnieć", pair_hint="zapomnę, zapomni",
            group="-am, -asz",
            present=["zapominam", "zapominasz", "zapomina", "zapominamy", "zapominacie",
                     "zapominają"],
            past="on zapominał · ona zapominała · oni zapominali",
            rekcja="o kim? o czym? (o + Miejscownik): zapominam o spotkaniu", rekcja_q="o + Miejscownik",
            examples=[("Ciągle zapominam słówek.", "Постійно забуваю слова.")],
        ),
        Verb(
            "lubić", "любити, подобатися", pair="polubić", pair_hint="polubię, polubi",
            group="-ę, -isz",
            present=["lubię", "lubisz", "lubi", "lubimy", "lubicie", "lubią"],
            past="on lubił · ona lubiła · oni lubili",
            rekcja="kogo? co? (Biernik): lubię kawę", rekcja_q="Biernik",
            examples=[("Lubię się uczyć języków.", "Люблю вчити мови.")],
        ),
        Verb(
            "kochać", "кохати, любити", group="-am, -asz",
            present=["kocham", "kochasz", "kocha", "kochamy", "kochacie", "kochają"],
            past="on kochał · ona kochała · oni kochali",
            rekcja="kogo? co? (Biernik): kocham cię", rekcja_q="Biernik",
            examples=[("Kocham swoją rodzinę.", "Люблю свою родину.")],
        ),
        Verb(
            "czuć się", "почуватися", pair="poczuć się", pair_hint="poczuję się, poczuje się",
            group="-ję, -jesz",
            present=["czuję się", "czujesz się", "czuje się", "czujemy się", "czujecie się",
                     "czują się"],
            past="on czuł się · ona czuła się · oni czuli się",
            examples=[("Dobrze się czuję.", "Добре почуваюся.")],
        ),
        Verb(
            "bać się", "боятися", group="-ę, -isz (boi-)",
            present=["boję się", "boisz się", "boi się", "boimy się", "boicie się",
                     "boją się"],
            past="on bał się · ona bała się · oni bali się",
            rekcja="kogo? czego? (Dopełniacz!): boję się egzaminu", rekcja_q="Dopełniacz",
            examples=[("Nie bój się błędów.", "Не бійся помилок.")],
        ),
        Verb(
            "cieszyć się", "радіти, тішитися", pair="ucieszyć się",
            pair_hint="ucieszę się, ucieszy się", group="-ę, -ysz",
            present=["cieszę się", "cieszysz się", "cieszy się", "cieszymy się",
                     "cieszycie się", "cieszą się"],
            past="on cieszył się · ona cieszyła się · oni cieszyli się",
            rekcja="z + Dopełniacz: cieszę się z prezentu · що…: cieszę się, że…", rekcja_q="z + Dopełniacz",
            examples=[("Cieszę się, że jesteś.", "Радію, що ти тут.")],
        ),
        Verb(
            "martwić się", "хвилюватися", pair="zmartwić się",
            pair_hint="zmartwię się, zmartwi się", group="-ę, -isz",
            present=["martwię się", "martwisz się", "martwi się", "martwimy się",
                     "martwicie się", "martwią się"],
            past="on martwił się · ona martwiła się · oni martwili się",
            rekcja="o + Biernik: martwię się o ciebie", rekcja_q="o + Biernik",
            examples=[("Nie martw się!", "Не хвилюйся!")],
        ),
    ],
)
