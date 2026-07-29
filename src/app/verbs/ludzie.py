"""Група 12 — Люди й дозвілля: зустрічатися, відвідувати, сміятися, грати…"""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="ludzie",
    icon="🤝",
    title="Люди й дозвілля",
    subtitle="Зустрітися, відвідати, посміятися — і чому «śmiać się Z czegoś».",
    verbs=[
        Verb(
            "spotykać się", "зустрічатися", pair="spotkać się",
            pair_hint="spotkam się, spotka się", group="-am, -asz",
            present=["spotykam się", "spotykasz się", "spotyka się", "spotykamy się",
                     "spotykacie się", "spotykają się"],
            past="on spotykał się · ona spotykała się · oni spotykali się",
            rekcja="z + Narzędnik: spotykam się z przyjaciółmi", rekcja_q="z + Narzędnik",
            examples=[("Spotkajmy się w sobotę!", "Зустріньмося в суботу!")],
        ),
        Verb(
            "poznawać", "знайомитися; пізнавати", pair="poznać", pair_hint="poznam, pozna",
            group="-ję, -jesz",
            present=["poznaję", "poznajesz", "poznaje", "poznajemy", "poznajecie",
                     "poznają"],
            past="on poznawał · ona poznawała · oni poznawali",
            rekcja="kogo? co? (Biernik): poznaję nowych ludzi", rekcja_q="Biernik",
            examples=[("Miło cię poznać!", "Приємно познайомитися!")],
        ),
        Verb(
            "odwiedzać", "відвідувати", pair="odwiedzić", pair_hint="odwiedzę, odwiedzi",
            group="-am, -asz",
            present=["odwiedzam", "odwiedzasz", "odwiedza", "odwiedzamy", "odwiedzacie",
                     "odwiedzają"],
            past="on odwiedzał · ona odwiedzała · oni odwiedzali",
            rekcja="kogo? (Biernik): odwiedzam babcię", rekcja_q="Biernik",
            examples=[("W niedzielę odwiedzam rodziców.", "У неділю відвідую батьків.")],
        ),
        Verb(
            "witać", "вітати (при зустрічі)", pair="przywitać", pair_hint="przywitam, przywita",
            group="-am, -asz",
            present=["witam", "witasz", "wita", "witamy", "witacie", "witają"],
            past="on witał · ona witała · oni witali",
            rekcja="kogo? (Biernik): witam gości",
            examples=[("Witamy w Polsce!", "Вітаємо в Польщі!")],
        ),
        Verb(
            "żegnać się", "прощатися", pair="pożegnać się",
            pair_hint="pożegnam się, pożegna się", group="-am, -asz",
            present=["żegnam się", "żegnasz się", "żegna się", "żegnamy się",
                     "żegnacie się", "żegnają się"],
            past="on żegnał się · ona żegnała się · oni żegnali się",
            rekcja="z + Narzędnik: żegnam się z gośćmi",
            examples=[("Muszę się już pożegnać.", "Мушу вже прощатися.")],
        ),
        Verb(
            "śmiać się", "сміятися", group="-ję, -jesz (śmiej-)",
            present=["śmieję się", "śmiejesz się", "śmieje się", "śmiejemy się",
                     "śmiejecie się", "śmieją się"],
            past="on śmiał się · ona śmiała się · oni śmiali się",
            rekcja="z + Dopełniacz!: śmieję się z żartu (не «над жартом»)",
            rekcja_q="z + Dopełniacz",
            examples=[("Śmiejemy się z tego do dziś.", "Сміємося з цього досі.")],
        ),
        Verb(
            "płakać", "плакати", pair="zapłakać", pair_hint="zapłaczę, zapłacze",
            group="-ę, -esz (płacz-)",
            present=["płaczę", "płaczesz", "płacze", "płaczemy", "płaczecie", "płaczą"],
            past="on płakał · ona płakała · oni płakali",
            examples=[("Dziecko płacze w nocy.", "Дитина плаче вночі.")],
        ),
        Verb(
            "tańczyć", "танцювати", pair="zatańczyć", pair_hint="zatańczę, zatańczy",
            group="-ę, -ysz",
            present=["tańczę", "tańczysz", "tańczy", "tańczymy", "tańczycie", "tańczą"],
            past="on tańczył · ona tańczyła · oni tańczyli",
            rekcja="z + Narzędnik: tańczę z tobą",
            examples=[("Zatańczysz ze mną?", "Потанцюєш зі мною?")],
        ),
        Verb(
            "śpiewać", "співати", pair="zaśpiewać", pair_hint="zaśpiewam, zaśpiewa",
            group="-am, -asz",
            present=["śpiewam", "śpiewasz", "śpiewa", "śpiewamy", "śpiewacie", "śpiewają"],
            past="on śpiewał · ona śpiewała · oni śpiewali",
            examples=[("Ona pięknie śpiewa.", "Вона гарно співає.")],
        ),
        Verb(
            "grać", "грати", pair="zagrać", pair_hint="zagram, zagra",
            group="-am, -asz",
            present=["gram", "grasz", "gra", "gramy", "gracie", "grają"],
            past="on grał · ona grała · oni grali",
            rekcja="w + Biernik (гра/спорт): gram w piłkę · na + Miejscownik (інструмент): "
                   "gram na gitarze",
            examples=[("Gramy w piłkę w parku.", "Граємо у футбол у парку.")],
        ),
    ],
)
