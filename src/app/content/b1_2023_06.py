"""РЕАЛЬНИЙ минулий іспит B1 — червень 2023 (certyfikatpolski.pl).

Джерело: 2023_06_24_25_B1_arkusz + …_transkrypcja.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН ключ
звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad); аудіювання — у listening.py.
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

# ── CZYTANIE — Zad I. Ключ: b,c,c,a,b. ──────────────────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Ta popularna linia lotnicza zarabia głównie na dodatkowych opcjach: przed podróżą "
            "można zapłacić za szybsze wejście na pokład, rezerwację miejsca, a nawet za posiłek "
            "w czasie lotu. Chcąc podróżować ekonomicznie, warto przemyśleć swoje potrzeby.",
            "Z tego tekstu wynika, że:",
            ["dodatkowe usługi to dla linii lotniczej sposób na promocję",
             "cena biletu lotniczego nie zawiera usługi gastronomicznej",
             "pasażerowie najwięcej pieniędzy wydają w czasie lotu"], 1,
            "«za posiłek… zapłacić» → ціна квитка не включає харчування."),
    MCQItem("czytanie",
            "Ponad 8 tys. osób z 60 krajów wzięło udział w Maratonie Warszawskim. Pierwszy na "
            "mecie był Kenijczyk, rywalizację kobiet wygrała Etiopka (rekord imprezy). Najszybszy "
            "z Polaków, Dariusz Nożyński, zajął 8. miejsce.",
            "Z tego tekstu możemy się dowiedzieć, że:",
            ["zawodnikami byli przede wszystkim warszawiacy",
             "żadna kobieta nie wygrała warszawskiego biegu",
             "żaden z Polaków nie zdobył w tych zawodach medalu"], 2,
            "найшвидший поляк — 8 місце → без медалі. Учасники з 60 країн; жінку-переможницю було."),
    MCQItem("czytanie",
            "„Żywioły” to nietypowa piekarnia – idealna na śniadanie, wieczornego drinka czy "
            "posiłek. To pierwszy w Warszawie punkt łączący piekarnię z bistro. Chleby, bułki, "
            "kanapki, ciasta i przekąski można zjeść na miejscu lub wziąć na wynos.",
            "Z tego tekstu wynika, że w piekarni „Żywioły” można:",
            ["spróbować lokalnych i nietypowych deserów",
             "zarezerwować stolik na romantyczne spotkanie",
             "zjeść posiłek w bistro lub zabrać jedzenie ze sobą"], 2,
            "«na miejscu lub na wynos» → з'їсти в бістро або взяти із собою."),
    MCQItem("czytanie",
            "POLIN Music Festival wraca do Warszawy po ponad dwóch latach. W najbliższy piątek "
            "rozpocznie się trzydniowy koncert – pięć występów polskich i zagranicznych artystów. "
            "Uczestnicy poznają też kilka zupełnie nowych utworów.",
            "Z tego tekstu wynika, że:",
            ["POLIN Music Festival odbędzie się pierwszy raz po przerwie",
             "podczas imprezy można kupić płyty znanych zespołów",
             "tym razem na festiwalu wystąpią tylko polskie zespoły"], 0,
            "«wraca po ponad dwóch latach» → перший раз після перерви. Артисти й закордонні."),
    MCQItem("czytanie",
            "Ponad połowa Polaków nie wyobraża sobie początku dnia bez kawy. Pijemy ją, bo lubimy "
            "i dodaje energii. Ma też pozytywny wpływ na zdrowie – tak uważają naukowcy: „Pijcie "
            "kawę na zdrowie!”.",
            "Z tego tekstu wynika, że:",
            ["prawie 50% Polaków pije kawę każdego dnia rano",
             "picie tego napoju pomaga ludziom dbać o zdrowie",
             "badacze uważają, że kawa jest lepsza niż lekarstwa"], 1,
            "«pozytywny wpływ na zdrowie» → допомагає дбати про здоров'я. Понад половина (не «майже 50%»)."),
    # ── Zad II: TAK/NIE — «Ekspres Lodowcowy». Ключ: N,T,N,T,N,N. ────────
    MCQItem("czytanie",
            "TEKСТ «Glacier Express» (Ekspres Lodowcowy): одна з найцікавіших атракцій "
            "Швейцарії, з'єднує Zermatt і Sankt Moritz. Вагони з вікнами від підлоги до стелі "
            "(але дах звичайний). «Найповільніший експрес світу»: 291 км за 8 год; комфортні "
            "купе, зручні крісла. Невдовзі після старту — 6 великих мостів; ЦЯ ЧАСТИНА траси "
            "внесена в UNESCO (не вся). Відходить раз на день, дуже пунктуально (вагони стоять "
            "за 15 хв). Уся траса дорога, але можна вийти раніше — тоді дешевше. КОЖЕН (і з "
            "картою Swiss Travel Pass, і з разовим квитком) мусить доплатити за резервацію місця.",
            "TAK/NIE: Pojazd ma ogromne okna i dach ze szkła.",
            ["TAK", "NIE"], 1, "НІ — великі вікна є, але про скляний дах не сказано."),
    MCQItem("czytanie", "",
            "TAK/NIE: Dobre warunki w Ekspresie Lodowcowym ułatwiają turystom długą podróż.",
            ["TAK", "NIE"], 0, "ТАК — комфортні купе, зручні крісла на довгу дорогу."),
    MCQItem("czytanie", "",
            "TAK/NIE: Cała trasa Ekspresu Lodowcowego znajduje się na liście UNESCO.",
            ["TAK", "NIE"], 1, "НІ — лише ЧАСТИНА (з мостами) в UNESCO."),
    MCQItem("czytanie", "",
            "TAK/NIE: Ekspres rusza ze stacji początkowej zawsze zgodnie z rozkładem.",
            ["TAK", "NIE"], 0, "ТАК — «bardzo punktualnie»."),
    MCQItem("czytanie", "",
            "TAK/NIE: Wszystkie bilety na Ekspres Lodowcowy są w jednej cenie.",
            ["TAK", "NIE"], 1, "НІ — можна вийти раніше → дешевше (ціни різні)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Posiadacze karty Swiss Travel Pass mają zagwarantowane miejsca siedzące.",
            ["TAK", "NIE"], 1, "НІ — КОЖЕН мусить доплатити за резервацію місця."),
    # ── Zad V: обери найкраще слово («Pokolenie Alfa»). ─────────────────
    MCQItem("czytanie", "Текст про покоління Альфа (сучасні учні). Обери найкраще слово.",
            "Specjaliści próbują ___ wzorce zachowania młodzieży.",
            ["opisywać", "opowiadać", "odmieniać"], 0, "описувати зразки → <b>opisywać</b>."),
    MCQItem("czytanie", "", "Co jeszcze warto ___ o dzisiejszych uczniach?",
            ["znać", "wiedzieć", "myśleć"], 1, "«wiedzieć o» → <b>wiedzieć</b>."),
    MCQItem("czytanie", "", "___ „pokolenie Alfa” wymyślił badacz Mark McCrindle.",
            ["Imię", "Nazwę", "Tytuł"], 1, "назву терміна → <b>Nazwę</b>."),
    MCQItem("czytanie", "", "Czas ___ głównie w portalach społecznościowych.",
            ["wykorzystują", "prowadzą", "spędzają"], 2, "проводять час → <b>spędzają</b>."),
    MCQItem("czytanie", "", "Świetnie poruszają się w internecie i nie ___ nudy.",
            ["czują", "mają", "trzymają"], 0, "не відчувають нудьги → <b>czują</b>."),
    MCQItem("czytanie", "", "Oto kilka ___, które je wyróżnia.",
            ["wad", "zalet", "cech"], 2, "кілька рис → <b>cech</b>."),
    MCQItem("czytanie", "", "Dlatego tak ___ jest komunikacja między pokoleniami.",
            ["poważna", "ważna", "miła"], 1, "така важлива → <b>ważna</b>."),
    MCQItem("czytanie", "", "Starsi mogą ___ dzieciom świat bez technologii.",
            ["podawać", "poznawać", "pokazywać"], 2, "показувати світ → <b>pokazywać</b>."),
    MCQItem("czytanie", "", "…radość z ___ spędzania czasu na świeżym powietrzu.",
            ["mobilnego", "aktywnego", "energicznego"], 1, "активне проведення часу → <b>aktywnego</b>."),
    MCQItem("czytanie", "", "…jak być ludźmi ___ tolerancyjnymi i otwartymi na nowości.",
            ["bardziej", "więcej", "lepiej"], 0, "бути більш толерантними → <b>bardziej</b>."),
]

# ── Zad III: вставити фрагменти («Funkcjonalna kuchnia»). Приклад=C. Ключ: E,B,G,A,H,D,F. ──
_ZAD3 = MatchTask(
    section="czytanie",
    title="2023-06 Читання Zad III — встав фрагменти (функціональна кухня)",
    intro="Прочитай текст про облаштування кухні. Заповни пропуски 1–7 фрагментами A–G.",
    options=[
        "krojenia, zmywania, gotowania i pieczenia",  # A
        "najważniejszych sprzętów",  # B
        "powinien stanowić element dekoracyjny",  # D
        "mniej niż 10 metrów kwadratowych",  # E
        "najważniejszy mebel w całym domu",  # F
        "od półtora do dwóch i pół metra",  # G
        "wykonywać niepotrzebnych ruchów",  # H
    ],
    prompts=[
        "1. Gdy powierzchnia kuchni jest mała i wynosi ___, dobre planowanie jest ważne.",
        "2. Najbardziej istotny jest odpowiedni układ ___: lodówki, zlewu i kuchenki.",
        "3. Najlepsza odległość między głównymi urządzeniami to ___.",
        "4. Reguła „trójkąta” pozwoli wyróżnić strefy: ___.",
        "5. Dzięki takiej aranżacji nie będziemy ___, a tym samym zaoszczędzimy czas.",
        "6. Szczególną rolę odgrywa stół, który z jednej strony ___, a z drugiej jest funkcjonalny.",
        "7. Według wielu osób jest to ___ i nie wyobrażają sobie, aby go zabrakło.",
    ],
    key=[3, 1, 5, 0, 6, 2, 4],  # E,B,G,A,H,D,F
    explain=[
        "«wynosi ___» → E (менш ніж 10 м²).",
        "«układ ___» → B (найважливіших приладів).",
        "«odległość to ___» → G (від 1,5 до 2,5 м).",
        "«strefy: ___» → A (нарізання, миття, готування, випікання).",
        "«nie będziemy ___» → H (робити зайвих рухів).",
        "«stół, który ___» → D (має бути елементом декору).",
        "«jest to ___» → F (найважливіший меблевий предмет у домі)."],
)

# ── Zad IV: заголовки↔тексти («Jak oszczędzać na zakupach»). Приклад=B. Ключ: E,H,A,G,C,F,D. ──
_ZAD4 = MatchTask(
    section="czytanie",
    title="2023-06 Читання Zad IV — заголовок↔порада (економія на покупках)",
    intro="«Jak oszczędzać na zakupach?» — до кожного заголовка (1–7) добери фрагмент A–G.",
    options=[
        "Są produkty, których ceny zmieniają się z tygodnia na tydzień – jeśli możesz, zrób "
        "zapasy tych o długim terminie ważności.",  # A
        "Kupuj z głową! Kup kurczaka, bo możesz zrobić z niego kotlety, rosół i pieczone udka.",  # C
        "Otwórz lodówkę i sprawdź, co może być dodatkiem do zupy, pasztetu lub omleta – trochę "
        "kreatywności i powstanie nowe danie.",  # D
        "Nawet gdy zapiszesz produkty, zastanów się, czy na pewno są niezbędne. W sklepie bądź "
        "konsekwentny, nie kupuj nic dodatkowego.",  # E
        "Sposobów na wykorzystanie pieczywa jest wiele – tosty, bułka tarta, a nawet zupa; "
        "w internecie znajdziesz mnóstwo przepisów.",  # F
        "Możesz zainstalować aplikacje Foodsi lub Too Good To Go, dzięki którym zamówisz "
        "potrawy w dużo niższych cenach.",  # G
        "Określ tygodniowy budżet na produkty spożywcze i zawsze płać gotówką – nie wydasz "
        "wtedy więcej, niż zaplanowałeś.",  # H
    ],
    prompts=[
        "1. Zrób dokładną listę zakupów",
        "2. Nie płać kartą, jeśli chcesz kontrolować wydatki",
        "3. Czasami więcej oznacza też taniej",
        "4. Nowe technologie – korzystne promocje",
        "5. Postaw na produkty, z których przygotujesz kilka obiadów",
        "6. Zrób użytek ze starego chleba",
        "7. Wykorzystaj resztki",
    ],
    key=[3, 6, 0, 5, 1, 4, 2],  # E,H,A,G,C,F,D
    explain=[
        "точний список → E (перевір, чи все справді потрібне).",
        "не плати карткою → H (тижневий бюджет, плати готівкою).",
        "більше = дешевше → A (роби запаси товарів тривалого зберігання).",
        "нові технології → G (застосунки Foodsi/Too Good To Go).",
        "продукти на кілька обідів → C (курка: котлети, росіл, ніжки).",
        "старий хліб → F (тости, панірувальні сухарі, суп).",
        "використай рештки → D (додай до супу/омлета)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: відмінювання. Текст про Dzień Krajobrazu. ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про Міжнародний день ландшафту.",
            "Warto pomyśleć, w jakich ___ czujemy się dobrze.",
            ["miejsca", "miejscach", "miejscu"], 1, "w jakich + місцевий мн. → <b>miejscach</b>."),
    MCQItem("gramatyka", "", "Niektóre okolice działają na ___ pozytywnie.",
            ["nas", "nam", "nami"], 0, "działać na + знах. → <b>nas</b>."),
    MCQItem("gramatyka", "", "Chcemy, aby w ___ miejscowości było dużo dobrych terenów.",
            ["naszą", "nasza", "naszej"], 2, "w + місцевий → <b>naszej</b>."),
    MCQItem("gramatyka", "", "Warto rozmawiać z ___ o tym, że każdy może zmieniać otoczenie.",
            ["ludzie", "ludzi", "ludźmi"], 2, "z + орудний → <b>ludźmi</b>."),
    MCQItem("gramatyka", "", "…każdy może zmieniać ___, w którym żyje.",
            ["miastu", "miasto", "mieście"], 1, "zmieniać + знах. → <b>miasto</b>."),
    MCQItem("gramatyka", "", "Wystarczy uwierzyć w ___ kreatywność.",
            ["swojego", "swojej", "swoją"], 2, "uwierzyć w + знах. → <b>swoją</b>."),
    MCQItem("gramatyka", "", "…i nie bać się ___.",
            ["pomysłami", "pomysłów", "pomysły"], 1, "bać się + родовий → <b>pomysłów</b>."),
    MCQItem("gramatyka", "", "Mieszkańcy powinni tworzyć ___ projekty.",
            ["nowi", "nowy", "nowe"], 2, "знах. множини (проєкти) → <b>nowe</b>."),
    MCQItem("gramatyka", "", "Konsultacje pozwalają każdemu ___ wypowiedzieć się.",
            ["mieszkańcu", "mieszkańcowi", "mieszkańcem"], 1, "pozwalać + давальний → <b>mieszkańcowi</b>."),
    MCQItem("gramatyka", "", "…na temat jego ___ okolicy.",
            ["najbliższej", "najbliższych", "najbliższą"], 0, "родовий одн. жін. → <b>najbliższej</b>."),
    # ── Zad III: ступенювання. Текст про читалки e-book. ──
    MCQItem("gramatyka", "Текст про читалки e-book.",
            "Bateria e-booka funkcjonuje ___ od baterii tabletu.",
            ["dłużej", "dłuższa", "najdłużej"], 0, "порівняння (od) → <b>dłużej</b>."),
    MCQItem("gramatyka", "", "Ekran e-ink jest ___ tradycyjnej książce niż ekran cyfrowy.",
            ["najbliższy", "bliższy", "bliski"], 1, "вищий ступ. (niż) → <b>bliższy</b>."),
    MCQItem("gramatyka", "", "E-book oferuje coraz ___ opcji czytania.",
            ["większą", "najwięcej", "więcej"], 2, "coraz ___ (дедалі більше) → <b>więcej</b>."),
    MCQItem("gramatyka", "", "Jakość ekranu jest ___ w jasnym świetle.",
            ["najwyższa", "wyżej", "najwyżej"], 0, "найвища (у яскравому світлі) → <b>najwyższa</b>."),
    MCQItem("gramatyka", "", "Czytniki ważą ___ od tabletów.",
            ["mniejsze", "mniej", "najmniejsze"], 1, "важать менше (od) → <b>mniej</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: więc). ──
    MCQItem("gramatyka", "Текст про екологію. Встав сполучник (зайве слово — <b>więc</b>).",
            "Nie kupujmy produktów w promocji, ___ ich aktualnie nie potrzebujemy.",
            ["lub", "jeśli", "ponieważ", "więc", "a", "żeby"], 1, "умова → <b>jeśli</b>."),
    MCQItem("gramatyka", "", "Do pracy możemy jeździć komunikacją miejską ___ rowerem.",
            ["lub", "jeśli", "ponieważ", "więc", "a", "żeby"], 0, "вибір → <b>lub</b>."),
    MCQItem("gramatyka", "", "Rower nie emituje spalin, ___ jednocześnie zapewni nam ruch.",
            ["lub", "jeśli", "ponieważ", "więc", "a", "żeby"], 4, "зіставлення → <b>a</b> (а водночас)."),
    MCQItem("gramatyka", "", "Wyłączajmy urządzenia, ___ zaoszczędzić prąd.",
            ["lub", "jeśli", "ponieważ", "więc", "a", "żeby"], 5, "мета → <b>żeby</b>."),
    MCQItem("gramatyka", "", "Wybierajmy prysznic, ___ wtedy zużywamy mniej wody.",
            ["lub", "jeśli", "ponieważ", "więc", "a", "żeby"], 2, "причина → <b>ponieważ</b>."),
    # ── Zad VII: вид/способи. Діалог студентів + професор. ──
    MCQItem("gramatyka", "Діалог: студенти не готові до тесту, просять професора.",
            "Janku, ___ z profesorem – on bardzo cię lubi.",
            ["porozmawiałby", "porozmawiaj", "niech rozmawia"], 1, "наказ до «ty» → <b>porozmawiaj</b>."),
    MCQItem("gramatyka", "", "…ale ___ potem, jeśli się nie uda!",
            ["nie narzekaliby", "niech nie narzeka", "nie narzekajcie"], 2, "наказ до «wy» → <b>nie narzekajcie</b>."),
    MCQItem("gramatyka", "", "A teraz ___, bo zaczyna się lekcja!",
            ["chodźmy", "niech chodzą", "chodzilibyście"], 0, "«нумо» 1 ос. мн. → <b>chodźmy</b>."),
    MCQItem("gramatyka", "", "Profesor: Czy ___ nie rozmawiać?",
            ["mogliby", "moglibyście", "mogłybyście"], 1, "ввічливе 2 ос. мн. (uczniowie) → <b>moglibyście</b>."),
    MCQItem("gramatyka", "", "___ już zacząć lekcję.",
            ["Chciałbym", "Chciałby", "Chciej"], 0, "умовний, 1 ос. одн. (professor) → <b>Chciałbym</b>."),
    MCQItem("gramatyka", "", "Dlaczego ___ go dzisiaj nie pisać, Janku?",
            ["wolałby", "wolałybyście", "wolałbyś"], 2, "умовний, 2 ос. одн. (ty) → <b>wolałbyś</b>."),
    MCQItem("gramatyka", "", "Czy ___ pan przełożyć test na przyszły tydzień?",
            ["zgodziłby się", "zgadzałby się", "niech się zgodzi"], 0, "ввічливе прохання → <b>zgodziłby się</b> pan."),
    MCQItem("gramatyka", "", "___ panu bardzo wdzięczni!",
            ["Byliby", "Byłyby", "Bylibyśmy"], 2, "умовний, 1 ос. мн. (my) → <b>Bylibyśmy</b>."),
    MCQItem("gramatyka", "", "Osoby nieprzygotowane ___ test za tydzień.",
            ["napisałby", "pisaliby", "niech napiszą"], 2, "спонукання 3 ос. мн. → <b>niech napiszą</b>."),
    MCQItem("gramatyka", "", "Niech Paweł ___ nam, o czym mówiliśmy na lekcji.",
            ["przypomniałby", "przypomina", "przypomni"], 2, "«niech ___» докон. → <b>przypomni</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: przez). Текст про Італію. ──
    MCQItem("gramatyka", "Текст про італійський клімат у Польщі. Встав прийменник (зайве — <b>przez</b>).",
            "Planowałam, że za tydzień będę ___ rodziny w Neapolu.",
            ["dla", "z", "przez", "u", "o", "na"], 3, "u + родовий (у родини) → <b>u</b>."),
    MCQItem("gramatyka", "", "Spędzam czas ___ książką.",
            ["dla", "z", "przez", "u", "o", "na"], 1, "z + орудний → <b>z</b> książką."),
    MCQItem("gramatyka", "", "Poprosiłam koleżanki ___ polecenie mi miejsc.",
            ["dla", "z", "przez", "u", "o", "na"], 4, "poprosić o + знах. → <b>o</b>."),
    MCQItem("gramatyka", "", "Marta, gdy ma ochotę ___ włoski klimat, idzie do restauracji.",
            ["dla", "z", "przez", "u", "o", "na"], 5, "ochota na + знах. → <b>na</b>."),
    MCQItem("gramatyka", "", "…oferują to, co typowe ___ Włoch.",
            ["dla", "z", "przez", "u", "o", "na"], 0, "typowe dla + родовий → <b>dla</b>."),
]

# ── Zad IV: вписати форми (тепер./мин.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2023-06 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або минулий час). Текст про переїзд на "
           "село.\n\n<i>Приклад: rodzina <b>przeprowadziła się</b> (przeprowadzić się).</i>"),
    prompts=[
        "1. Uważamy, że ___ (my – podjąć) najlepszą decyzję w życiu.",
        "2. Dawniej, gdy ___ (ja – mieszkać) w mieście, przeszkadzał mi hałas.",
        "3. …to bardzo ___ (przeszkadzać) mi hałas uliczny.",
        "4. Dzieci ___ (musieć) czekać na nas w przedszkolu do późna.",
        "5. …bo mąż i ja często ___ (stać) w korkach.",
        "6. Teraz oboje ___ (cieszyć się) ciszą i spokojem.",
        "7. Obecnie mąż ___ (prowadzić) gospodarstwo,",
        "8. …a ja ___ (pracować) na pół etatu.",
        "9. Dzieci do przedszkola ___ (iść) tylko 5 minut spacerem.",
        "10. Jesteśmy szczęśliwi, że ___ (żyć) w zgodzie z naturą.",
    ],
    accepted=[
        ["podjęliśmy"], ["mieszkałam"], ["przeszkadzał"], ["musiały"], ["staliśmy"],
        ["cieszymy się"], ["prowadzi"], ["pracuję"], ["idą"], ["żyjemy"],
    ],
    explain=[
        "минулий, 1 ос. мн. чол.-ос. → <b>podjęliśmy</b>.",
        "минулий, 1 ос. одн. жін. → <b>mieszkałam</b>.",
        "минулий, 3 ос. одн. чол. (hałas) → <b>przeszkadzał</b>.",
        "минулий, 3 ос. мн. не-чол.-ос. (dzieci) → <b>musiały</b>.",
        "минулий, 1 ос. мн. → <b>staliśmy</b>.",
        "тепер., 1 ос. мн. → <b>cieszymy się</b>.",
        "тепер., 3 ос. одн. → <b>prowadzi</b>.",
        "тепер., 1 ос. одн. → <b>pracuję</b>.",
        "тепер., 3 ос. мн. (dzieci) → <b>idą</b>.",
        "тепер., 1 ос. мн. → <b>żyjemy</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2023-06 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: czekała «na przystanku» → Gdzie?</i>"),
    prompts=[
        "Adam poszedł na spacer «z całą swoją rodziną».",
        "Państwo Sikorscy obchodzą «dziesiątą» rocznicę ślubu.",
        "Igor mieszka w Warszawie «już prawie dwa lata».",
        "Przed domem stoi samochód «mojego brata».",
        "Michał podarował kwiaty «swojej nauczycielce matematyki».",
    ],
    accepted=[
        ["z kim"], ["którą"], ["jak długo", "ile czasu", "ile lat"], ["czyj"], ["komu"],
    ],
    explain=[
        "з людьми → <b>Z kim?</b>",
        "«którą rocznicę» → <b>Którą?</b>",
        "тривалість → <b>Jak długo?</b> (Ile czasu? / Ile lat?)",
        "«czyj samochód» → <b>Czyj?</b>",
        "podarować + давальний → <b>Komu?</b>",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2023-06 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «planujemy urlop» (myślimy) → myślimy o urlopie.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Mąż Anny jest technikiem dentystycznym.",
        "Brak mi długich rozmów z przyjaciółką.",
        "Jerzy często wspomina swoją pierwszą wycieczkę rowerową.",
        "Jestem trochę wyższa niż moja siostra.",
        "W grupie astronautów są kobiety i mężczyźni.",
    ],
    words=["pracuje jako", "Tęsknię za", "opowiada o", "od", "składa się z"],
    models=[
        ["Mąż Anny pracuje jako technik dentystyczny."],
        ["Tęsknię za długimi rozmowami z przyjaciółką."],
        ["Jerzy często opowiada o swojej pierwszej wycieczce rowerowej."],
        ["Jestem trochę wyższa od mojej siostry."],
        ["Grupa astronautów składa się z kobiet i mężczyzn."],
    ],
)

EXAM = Exam(
    id="2023-06",
    label="Реальний іспит червень-2023 (офіц.)",
    kind="real",
    year=2023,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
