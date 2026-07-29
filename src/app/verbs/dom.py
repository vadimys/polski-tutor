"""Група 7 — Дім і побут: відчиняти, вмикати, сідати, лежати, губити…"""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="dom",
    icon="🏠",
    title="Дім і побут",
    subtitle="Відчинити, увімкнути, сісти, лягти — дієслова навколо дому.",
    verbs=[
        Verb(
            "otwierać", "відчиняти", pair="otworzyć", pair_hint="otworzę, otworzy",
            group="-am, -asz",
            present=["otwieram", "otwierasz", "otwiera", "otwieramy", "otwieracie",
                     "otwierają"],
            past="on otwierał · ona otwierała · oni otwierali",
            rekcja="co? (Biernik): otwieram okno", rekcja_q="Biernik",
            examples=[("Otwórz okno, proszę.", "Відчини вікно, будь ласка.")],
        ),
        Verb(
            "zamykać", "зачиняти", pair="zamknąć", pair_hint="zamknę, zamknie",
            group="-am, -asz",
            present=["zamykam", "zamykasz", "zamyka", "zamykamy", "zamykacie", "zamykają"],
            past="on zamykał · ona zamykała · oni zamykali",
            rekcja="co? (Biernik): zamykam drzwi", rekcja_q="Biernik",
            examples=[("Zamknij drzwi na klucz.", "Зачини двері на ключ.")],
        ),
        Verb(
            "włączać", "вмикати", pair="włączyć", pair_hint="włączę, włączy",
            group="-am, -asz",
            present=["włączam", "włączasz", "włącza", "włączamy", "włączacie", "włączają"],
            past="on włączał · ona włączała · oni włączali",
            rekcja="co? (Biernik): włączam światło", rekcja_q="Biernik",
            examples=[("Włącz światło.", "Увімкни світло.")],
        ),
        Verb(
            "wyłączać", "вимикати", pair="wyłączyć", pair_hint="wyłączę, wyłączy",
            group="-am, -asz",
            present=["wyłączam", "wyłączasz", "wyłącza", "wyłączamy", "wyłączacie",
                     "wyłączają"],
            past="on wyłączał · ona wyłączała · oni wyłączali",
            rekcja="co? (Biernik): wyłączam telewizor", rekcja_q="Biernik",
            examples=[("Wyłącz telefon na noc.", "Вимкни телефон на ніч.")],
        ),
        Verb(
            "siadać", "сідати", pair="usiąść", pair_hint="usiądę, usiądzie",
            group="-am, -asz",
            present=["siadam", "siadasz", "siada", "siadamy", "siadacie", "siadają"],
            past="on siadał · ona siadała · oni siadali (usiąść: usiadł/usiadła/usiedli)",
            examples=[("Usiądź, proszę.", "Сідай, будь ласка.")],
        ),
        Verb(
            "stać", "стояти", group="-ę, -isz (stoi-)",
            present=["stoję", "stoisz", "stoi", "stoimy", "stoicie", "stoją"],
            past="on stał · ona stała · oni stali",
            examples=[("Autobus już stoi na przystanku.", "Автобус уже стоїть на зупинці.")],
        ),
        Verb(
            "leżeć", "лежати", group="-ę, -ysz",
            present=["leżę", "leżysz", "leży", "leżymy", "leżycie", "leżą"],
            past="on leżał · ona leżała · oni leżeli",
            examples=[("Klucze leżą na stole.", "Ключі лежать на столі.")],
        ),
        Verb(
            "kłaść się", "лягати", pair="położyć się", pair_hint="położę się, położy się",
            group="особливе (-ę, -esz)",
            present=["kładę się", "kładziesz się", "kładzie się", "kładziemy się",
                     "kładziecie się", "kładą się"],
            past="on kładł się · ona kładła się · oni kładli się",
            examples=[("Kładę się spać o północy.", "Лягаю спати опівночі.")],
        ),
        Verb(
            "gubić", "губити", pair="zgubić", pair_hint="zgubię, zgubi",
            group="-ę, -isz",
            present=["gubię", "gubisz", "gubi", "gubimy", "gubicie", "gubią"],
            past="on gubił · ona gubiła · oni gubili",
            rekcja="co? (Biernik): zgubiłem klucze", rekcja_q="Biernik",
            examples=[("Zgubiłem telefon.", "Я загубив телефон.")],
        ),
        Verb(
            "naprawiać", "лагодити", pair="naprawić", pair_hint="naprawię, naprawi",
            group="-am, -asz",
            present=["naprawiam", "naprawiasz", "naprawia", "naprawiamy", "naprawiacie",
                     "naprawiają"],
            past="on naprawiał · ona naprawiała · oni naprawiali",
            rekcja="co? (Biernik): naprawiam rower", rekcja_q="Biernik",
            examples=[("Muszę naprawić pralkę.", "Мушу полагодити пральну машину.")],
        ),
    ],
)
