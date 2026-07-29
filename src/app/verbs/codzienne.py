"""Група 3 — Щоденні дії: їсти, пити, спати, купувати…"""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="codzienne",
    icon="🍽",
    title="Щоденні дії",
    subtitle="Їжа, сон, покупки — лексика кожного дня.",
    verbs=[
        Verb(
            "jeść", "їсти", pair="zjeść", pair_hint="zjem, zje",
            group="особливе",
            present=["jem", "jesz", "je", "jemy", "jecie", "jedzą"],
            past="on jadł · ona jadła · oni jedli",
            rekcja="co? (Biernik): jem śniadanie",
            examples=[("Co jesz na śniadanie?", "Що їси на сніданок?")],
        ),
        Verb(
            "pić", "пити", pair="wypić", pair_hint="wypiję, wypije",
            group="-ję, -jesz",
            present=["piję", "pijesz", "pije", "pijemy", "pijecie", "piją"],
            past="on pił · ona piła · oni pili",
            rekcja="co? (Biernik): piję kawę",
            examples=[("Piję kawę z mlekiem.", "Пʼю каву з молоком.")],
        ),
        Verb(
            "spać", "спати", group="-ę, -isz (śpi-)",
            present=["śpię", "śpisz", "śpi", "śpimy", "śpicie", "śpią"],
            past="on spał · ona spała · oni spali",
            examples=[("W weekend długo śpię.", "У вихідні довго сплю.")],
        ),
        Verb(
            "wstawać", "вставати", pair="wstać", pair_hint="wstanę, wstanie",
            group="-ję, -jesz",
            present=["wstaję", "wstajesz", "wstaje", "wstajemy", "wstajecie", "wstają"],
            past="on wstawał · ona wstawała · oni wstawali",
            examples=[("Wstaję o siódmej rano.", "Встаю о сьомій ранку.")],
        ),
        Verb(
            "kupować", "купувати", pair="kupić", pair_hint="kupię, kupi",
            group="-uję, -ujesz",
            present=["kupuję", "kupujesz", "kupuje", "kupujemy", "kupujecie", "kupują"],
            past="on kupował · ona kupowała · oni kupowali",
            rekcja="co? (Biernik): kupuję chleb", rekcja_q="Biernik",
            examples=[("Kupuję warzywa na targu.", "Купую овочі на базарі.")],
        ),
        Verb(
            "płacić", "платити", pair="zapłacić", pair_hint="zapłacę, zapłaci",
            group="-ę, -isz",
            present=["płacę", "płacisz", "płaci", "płacimy", "płacicie", "płacą"],
            past="on płacił · ona płaciła · oni płacili",
            rekcja="za + Biernik: płacę za obiad · чим: kartą (Narzędnik)", rekcja_q="za + Biernik",
            examples=[("Płacę kartą.", "Плачу карткою.")],
        ),
        Verb(
            "gotować", "готувати (їжу)", pair="ugotować", pair_hint="ugotuję, ugotuje",
            group="-uję, -ujesz",
            present=["gotuję", "gotujesz", "gotuje", "gotujemy", "gotujecie", "gotują"],
            past="on gotował · ona gotowała · oni gotowali",
            rekcja="co? (Biernik): gotuję obiad", rekcja_q="Biernik",
            examples=[("Dziś gotuję pierogi.", "Сьогодні готую вареники.")],
        ),
        Verb(
            "sprzątać", "прибирати", pair="posprzątać", pair_hint="posprzątam, posprząta",
            group="-am, -asz",
            present=["sprzątam", "sprzątasz", "sprząta", "sprzątamy", "sprzątacie",
                     "sprzątają"],
            past="on sprzątał · ona sprzątała · oni sprzątali",
            rekcja="co? (Biernik): sprzątam mieszkanie",
            examples=[("W sobotę sprzątam mieszkanie.", "У суботу прибираю квартиру.")],
        ),
        Verb(
            "myć się", "митися", pair="umyć się", pair_hint="umyję się, umyje się",
            group="-ję, -jesz",
            present=["myję się", "myjesz się", "myje się", "myjemy się", "myjecie się",
                     "myją się"],
            past="on mył się · ona myła się · oni myli się",
            examples=[("Myję się rano i wieczorem.", "Миюся вранці й увечері.")],
        ),
        Verb(
            "ubierać się", "одягатися", pair="ubrać się", pair_hint="ubiorę się, ubierze się",
            group="-am, -asz",
            present=["ubieram się", "ubierasz się", "ubiera się", "ubieramy się",
                     "ubieracie się", "ubierają się"],
            past="on ubierał się · ona ubierała się · oni ubierali się",
            examples=[("Szybko się ubieram.", "Швидко одягаюся.")],
        ),
    ],
)
