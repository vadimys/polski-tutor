"""Група 9 — Справи в місті: залагодити, заповнити, підписати, замовити…

Найпрактичніша група для життя в Польщі: urząd, пошта, ресторан, бронювання.
"""

from __future__ import annotations

from app.verbs.schema import Verb, VerbGroup

GROUP = VerbGroup(
    id="sprawy",
    icon="🏙",
    title="Справи в місті",
    subtitle="Urząd, пошта, ресторан: залагодити, заповнити, замовити, забронювати.",
    verbs=[
        Verb(
            "załatwiać", "залагоджувати (справи)", pair="załatwić",
            pair_hint="załatwię, załatwi", group="-am, -asz",
            present=["załatwiam", "załatwiasz", "załatwia", "załatwiamy", "załatwiacie",
                     "załatwiają"],
            past="on załatwiał · ona załatwiała · oni załatwiali",
            rekcja="co? (Biernik): załatwiam sprawę w urzędzie", rekcja_q="Biernik",
            examples=[("Muszę załatwić sprawę w urzędzie.", "Мушу залагодити справу в управлінні.")],
        ),
        Verb(
            "wypełniać", "заповнювати", pair="wypełnić", pair_hint="wypełnię, wypełni",
            group="-am, -asz",
            present=["wypełniam", "wypełniasz", "wypełnia", "wypełniamy", "wypełniacie",
                     "wypełniają"],
            past="on wypełniał · ona wypełniała · oni wypełniali",
            rekcja="co? (Biernik): wypełniam formularz", rekcja_q="Biernik",
            examples=[("Proszę wypełnić ten formularz.", "Будь ласка, заповніть цей формуляр.")],
        ),
        Verb(
            "podpisywać", "підписувати", pair="podpisać", pair_hint="podpiszę, podpisze",
            group="-uję, -ujesz",
            present=["podpisuję", "podpisujesz", "podpisuje", "podpisujemy", "podpisujecie",
                     "podpisują"],
            past="on podpisywał · ona podpisywała · oni podpisywali",
            rekcja="co? (Biernik): podpisuję umowę", rekcja_q="Biernik",
            examples=[("Gdzie mam podpisać?", "Де мені підписати?")],
        ),
        Verb(
            "wysyłać", "надсилати", pair="wysłać", pair_hint="wyślę, wyśle",
            group="-am, -asz",
            present=["wysyłam", "wysyłasz", "wysyła", "wysyłamy", "wysyłacie", "wysyłają"],
            past="on wysyłał · ona wysyłała · oni wysyłali",
            rekcja="co? + do kogo? (do + Dopełniacz): wysyłam paczkę do mamy",
            examples=[("Wyślę ci dokumenty mailem.", "Надішлю тобі документи мейлом.")],
        ),
        Verb(
            "odbierać", "забирати; відповідати (на дзвінок)", pair="odebrać",
            pair_hint="odbiorę, odbierze", group="-am, -asz",
            present=["odbieram", "odbierasz", "odbiera", "odbieramy", "odbieracie",
                     "odbierają"],
            past="on odbierał · ona odbierała · oni odbierali",
            rekcja="co? (Biernik): odbieram paczkę / odbieram telefon", rekcja_q="Biernik",
            examples=[("Odbiorę paczkę z paczkomatu.", "Заберу посилку з пачкомата.")],
        ),
        Verb(
            "zwiedzać", "оглядати (місто, музей)", pair="zwiedzić",
            pair_hint="zwiedzę, zwiedzi", group="-am, -asz",
            present=["zwiedzam", "zwiedzasz", "zwiedza", "zwiedzamy", "zwiedzacie",
                     "zwiedzają"],
            past="on zwiedzał · ona zwiedzała · oni zwiedzali",
            rekcja="co? (Biernik): zwiedzam Kraków", rekcja_q="Biernik",
            examples=[("W niedzielę zwiedzamy stare miasto.", "У неділю оглядаємо старе місто.")],
        ),
        Verb(
            "zamawiać", "замовляти", pair="zamówić", pair_hint="zamówię, zamówi",
            group="-am, -asz",
            present=["zamawiam", "zamawiasz", "zamawia", "zamawiamy", "zamawiacie",
                     "zamawiają"],
            past="on zamawiał · ona zamawiała · oni zamawiali",
            rekcja="co? (Biernik): zamawiam pizzę", rekcja_q="Biernik",
            examples=[("Zamówimy coś do jedzenia?", "Замовимо щось поїсти?")],
        ),
        Verb(
            "rezerwować", "бронювати", pair="zarezerwować",
            pair_hint="zarezerwuję, zarezerwuje", group="-uję, -ujesz",
            present=["rezerwuję", "rezerwujesz", "rezerwuje", "rezerwujemy", "rezerwujecie",
                     "rezerwują"],
            past="on rezerwował · ona rezerwowała · oni rezerwowali",
            rekcja="co? (Biernik): rezerwuję stolik", rekcja_q="Biernik",
            examples=[("Chciałbym zarezerwować stolik na dwie osoby.",
                       "Хотів би забронювати столик на двох.")],
        ),
        Verb(
            "zgadzać się", "погоджуватися", pair="zgodzić się",
            pair_hint="zgodzę się, zgodzi się", group="-am, -asz",
            present=["zgadzam się", "zgadzasz się", "zgadza się", "zgadzamy się",
                     "zgadzacie się", "zgadzają się"],
            past="on zgadzał się · ona zgadzała się · oni zgadzali się",
            rekcja="z + Narzędnik (з ким) / na + Biernik (на що): zgadzam się z tobą",
            examples=[("Zgadzam się z tobą.", "Погоджуюся з тобою.")],
        ),
        Verb(
            "zapraszać", "запрошувати", pair="zaprosić", pair_hint="zaproszę, zaprosi",
            group="-am, -asz",
            present=["zapraszam", "zapraszasz", "zaprasza", "zapraszamy", "zapraszacie",
                     "zapraszają"],
            past="on zapraszał · ona zapraszała · oni zapraszali",
            rekcja="kogo? + na co? (na + Biernik): zapraszam cię na kawę",
            examples=[("Zapraszam cię na urodziny.", "Запрошую тебе на день народження.")],
        ),
    ],
)
