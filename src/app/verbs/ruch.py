"""Група 2 — Рух: іти, їхати, повертатися… (пішки vs транспортом, раз vs регулярно)."""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="ruch",
    icon="🚶",
    title="Рух",
    subtitle="Іти/їхати: пішки чи транспортом, зараз чи регулярно — тут це різні слова.",
    verbs=[
        Verb(
            "iść", "іти (зараз, пішки)", pair="pójść", pair_hint="pójdę, pójdzie",
            group="особливе (-ę, -esz)",
            present=["idę", "idziesz", "idzie", "idziemy", "idziecie", "idą"],
            past="on szedł · ona szła · oni szli",
            rekcja="do + Dopełniacz / na + Biernik: idę do domu, idę na koncert",
            examples=[("Idę do pracy.", "Іду на роботу.")],
        ),
        Verb(
            "chodzić", "ходити (регулярно)", group="-ę, -isz",
            present=["chodzę", "chodzisz", "chodzi", "chodzimy", "chodzicie", "chodzą"],
            past="on chodził · ona chodziła · oni chodzili",
            rekcja="do + Dopełniacz / na + Biernik: chodzę na basen",
            examples=[("Chodzę do szkoły codziennie.", "Ходжу до школи щодня.")],
        ),
        Verb(
            "jechać", "їхати (зараз)", pair="pojechać", pair_hint="pojadę, pojedzie",
            group="особливе (-ę, -esz)",
            present=["jadę", "jedziesz", "jedzie", "jedziemy", "jedziecie", "jadą"],
            past="on jechał · ona jechała · oni jechali",
            rekcja="do + Dopełniacz · чим: autobusem (Narzędnik)",
            examples=[("Jadę do Krakowa pociągiem.", "Їду до Кракова потягом.")],
        ),
        Verb(
            "jeździć", "їздити (регулярно)", group="-ę, -isz (жд/зьдж)",
            present=["jeżdżę", "jeździsz", "jeździ", "jeździmy", "jeździcie", "jeżdżą"],
            past="on jeździł · ona jeździła · oni jeździli",
            rekcja="чим? (Narzędnik): jeżdżę rowerem",
            examples=[("Jeżdżę do pracy autobusem.", "Їжджу на роботу автобусом.")],
        ),
        Verb(
            "wracać", "повертатися", pair="wrócić", pair_hint="wrócę, wróci",
            group="-am, -asz",
            present=["wracam", "wracasz", "wraca", "wracamy", "wracacie", "wracają"],
            past="on wracał · ona wracała · oni wracali",
            rekcja="z + Dopełniacz / do + Dopełniacz: wracam z pracy do domu",
            examples=[("Wracam do domu o piątej.", "Повертаюся додому о пʼятій.")],
        ),
        Verb(
            "wychodzić", "виходити", pair="wyjść", pair_hint="wyjdę, wyjdzie",
            group="-ę, -isz",
            present=["wychodzę", "wychodzisz", "wychodzi", "wychodzimy", "wychodzicie",
                     "wychodzą"],
            past="on wychodził · ona wychodziła · oni wychodzili",
            rekcja="z + Dopełniacz: wychodzę z domu",
            examples=[("Wychodzę z biura o szóstej.", "Виходжу з офісу о шостій.")],
        ),
        Verb(
            "przychodzić", "приходити", pair="przyjść", pair_hint="przyjdę, przyjdzie",
            group="-ę, -isz",
            present=["przychodzę", "przychodzisz", "przychodzi", "przychodzimy",
                     "przychodzicie", "przychodzą"],
            past="on przychodził · ona przychodziła · oni przychodzili",
            rekcja="do + Dopełniacz / na + Biernik: przyjdę na spotkanie",
            examples=[("Przyjdę jutro o dziesiątej.", "Прийду завтра о десятій.")],
        ),
        Verb(
            "zostawać", "залишатися", pair="zostać", pair_hint="zostanę, zostanie",
            group="-ję, -jesz",
            present=["zostaję", "zostajesz", "zostaje", "zostajemy", "zostajecie", "zostają"],
            past="on zostawał · ona zostawała · oni zostawali",
            examples=[("Dziś zostaję w domu.", "Сьогодні залишаюся вдома.")],
        ),
        Verb(
            "biegać", "бігати", group="-am, -asz",
            present=["biegam", "biegasz", "biega", "biegamy", "biegacie", "biegają"],
            past="on biegał · ona biegała · oni biegali",
            examples=[("Biegam rano w parku.", "Бігаю вранці в парку.")],
        ),
        Verb(
            "latać", "літати", group="-am, -asz",
            present=["latam", "latasz", "lata", "latamy", "latacie", "latają"],
            past="on latał · ona latała · oni latali",
            rekcja="czym? (Narzędnik): latam samolotem",
            examples=[("Często latam do Polski.", "Часто літаю до Польщі.")],
        ),
    ],
)
