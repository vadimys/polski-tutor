"""РЕАЛЬНИЙ минулий іспит B1 — червень 2022 (certyfikatpolski.pl).

Джерело: 2022.06.25-26_B1_arkusz + _Transkrypcja_nagran.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН
ключ звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad); аудіювання — у listening.py.
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

_ZAD5_BANK = ["robot", "potrafi", "wie", "suficie", "obiekt",
              "drogi", "zajmie", "przyszłości", "kelnerom", "szklanki"]

# ── CZYTANIE — Zad I (6 фрагментів). Ключ: b,c,b,c,b,a. ──────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "„Farma” będzie nowym programem telewizyjnym z udziałem osób, które nigdy nie "
            "mieszkały ani nie pracowały na wsi. Spędzą razem sześć tygodni i wykonają różne "
            "zadania, a wygra ten uczestnik, który najbardziej spodoba się widzom.",
            "Z tego tekstu wynika, że:",
            ["uczestnikami programu „Farma” będą rolnicy",
             "o wygranej będą decydować osoby, które oglądają program",
             "program będzie trwał ponad dwa miesiące"], 1,
            "«spodoba się widzom» → вирішують глядачі. Учасники — НЕ фермери; 6 тижнів < 2 місяців."),
    MCQItem("czytanie",
            "Polski film „Sukienka” (reż. Tadeusz Łysiak) miał szansę na Oscara, ale nagrodę "
            "otrzymał inny film. Głównym tematem jest opowieść o pracownicy hotelu, która z powodu "
            "niskiego wzrostu nie może znaleźć partnera.",
            "Z tego tekstu wynika, że:",
            ["reżyser filmu dostał Oscara", "film Sukienka otrzymał wiele nagród",
             "bohaterka filmu nie jest wysoka"], 2,
            "«z powodu niskiego wzrostu» → героїня невисока. Оскара НЕ отримав."),
    MCQItem("czytanie",
            "Naukowcy z Bergen udowodnili, że dorosły może wydłużyć życie o ponad 10 lat, jeśli "
            "zmieni dietę na taką z większą ilością roślin i orzechów, a mniejszą mięsa. Wyniki "
            "opublikowano w czasopiśmie akademickim „PLOS One”.",
            "Z tego tekstu wynika, że:",
            ["dzięki diecie można wydłużyć życie o niecałe dziesięć lat",
             "rezultaty badań na temat diety zostały opisane w prasie",
             "w diecie dorosłego człowieka nie powinno być posiłków z mięsem"], 1,
            "опубліковано в науковому часописі → описано в пресі. Понад 10 років; менше м'яса (не повна відмова)."),
    MCQItem("czytanie",
            "Latający samochód AirCar przeszedł testy i otrzymał certyfikat bezpieczeństwa. Potrafi "
            "zmieniać się z samochodu w samolot – zajmuje mu to 2 minuty 15 sekund. Do latania "
            "trzeba mieć licencję pilota. Poinformowała o tym słowacka telewizja.",
            "Z tego tekstu wynika, że:",
            ["AirCarem może latać każda osoba", "AirCar zamienia się w samolot w kilka sekund",
             "informacje o AirCarze przekazały media"], 2,
            "«słowacka telewizja poinformowała» → медіа. Треба ліцензія; перетворення 2 хв 15 с."),
    MCQItem("czytanie",
            "W grze „Dying Light 2” jest siedemnaście języków (m.in. czeski, arabski, a także "
            "polski), ale brakuje włoskiego, co skrytykowali gracze z Włoch.",
            "Z tego tekstu wynika, że:",
            ["niedługo w grze będzie można wybrać język polski",
             "w grze już teraz można wybrać język polski",
             "gracze przetłumaczyli grę na język czeski i arabski"], 1,
            "серед 17 мов є польська → вже зараз доступна."),
    MCQItem("czytanie",
            "Zaplanowana na poniedziałek 20 września konferencja „Komunikacja międzynarodowa” "
            "odbędzie się w piątek 24 września. Lokalizacja pozostaje bez zmian – główna aula na "
            "pierwszym piętrze biurowca.",
            "Z tego tekstu wynika, że:",
            ["zmienił się termin konferencji", "planowana jest inna lokalizacja konferencji",
             "konferencja ma zmieniony temat"], 0,
            "з понеділка на п'ятницю → змінився термін. Локація й тема без змін."),
    # ── Zad II: TAK/NIE — «Gwiezdne wojny w Polsce». Ключ: N,T,N,T,N,T. ──
    MCQItem("czytanie",
            "TEKСТ: «Зоряні війни» вперше показали в польських кінотеатрах 30 березня 1979 — за "
            "ДВА РОКИ після світової прем'єри (тоді довго чекали й на інші фільми із Заходу). На "
            "першому Polconі це була тема №1. Але спільнота фанів почала РОЗРОСТАТИСЯ аж у 90-х "
            "(коли з'явилися касети VHS). Тоді ж — ера інтернету, перші сайти від фанів, які "
            "напам'ять знали кожну сцену; згодом автори сайтів познайомилися й заснували фан-клуби. "
            "У 2005 Leszek Budkiewicz із Grabowca попросив ВЛАДУ СЕЛА назвати вулицю іменем Obi-Wana "
            "Kenobiego. Тепер туристи фотографуються біля таблички, дехто — у костюмах героїв.",
            "TAK/NIE: Polscy widzowie mogli obejrzeć pierwszy raz ten film w latach 90. XX wieku.",
            ["TAK", "NIE"], 1, "НІ — вперше в кіно у 1979 р. (у 90-х лише розросталася спільнота)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Podczas pierwszego Polconu dużo rozmawiano o Gwiezdnych wojnach.",
            ["TAK", "NIE"], 0, "ТАК — це була «тема номер один»."),
    MCQItem("czytanie", "",
            "TAK/NIE: Dzięki pierwszym polskim fanom film był sprzedawany na kasetach VHS.",
            ["TAK", "NIE"], 1, "НІ — касети VHS з'явилися незалежно; фани почали множитися завдяки їм."),
    MCQItem("czytanie", "",
            "TAK/NIE: Lokalne fankluby zakładały osoby, które poznały się przez internet.",
            ["TAK", "NIE"], 0, "ТАК — автори сайтів познайомилися й заснували фан-клуби."),
    MCQItem("czytanie", "",
            "TAK/NIE: Władze Grabowca zaproponowały, aby jedną z ulic nazwać imieniem Obi-Wana.",
            ["TAK", "NIE"], 1, "НІ — це запропонував МЕШКАНЕЦЬ (Budkiewicz), не влада."),
    MCQItem("czytanie", "",
            "TAK/NIE: Część fanów przyjeżdża do Grabowca z kostiumami postaci z filmu.",
            ["TAK", "NIE"], 0, "ТАК — дехто привозить костюми улюблених героїв."),
    # ── Zad V: luki z ramki (спільний банк). Текст «Mechaniczny kelner». ──
    MCQItem("czytanie", "Текст про робота-офіціанта. Обери слово з рамки для кожного пропуску.",
            "Jedzenie może przywieźć do stolika ___, który wygląda jak kot.", _ZAD5_BANK, 0,
            "механічний офіціант → <b>robot</b>."),
    MCQItem("czytanie", "", "Dodatkowo ___ zaśpiewać kilka piosenek.", _ZAD5_BANK, 1, "уміє → <b>potrafi</b>."),
    MCQItem("czytanie", "", "Maszyna ___ też, dla kogo przygotowane jest danie.", _ZAD5_BANK, 2, "знає → <b>wie</b>."),
    MCQItem("czytanie", "", "Dzięki kamerom i punktom na ___ restauracji robot wie, gdzie jest.", _ZAD5_BANK, 3,
            "на стелі → <b>suficie</b>."),
    MCQItem("czytanie", "", "Jeśli to będzie jakiś statyczny ___, robot poszuka innej drogi.", _ZAD5_BANK, 4,
            "статичний об'єкт → <b>obiekt</b>."),
    MCQItem("czytanie", "", "…robot poszuka innej ___ do celu.", _ZAD5_BANK, 5, "іншої дороги → <b>drogi</b>."),
    MCQItem("czytanie", "", "Część pracowników boi się, że ___ on miejsce ludzi.", _ZAD5_BANK, 6, "займе → <b>zajmie</b>."),
    MCQItem("czytanie", "", "W ___, gdy w każdym punkcie będą maszyny, goście zechcą znów ludzi.", _ZAD5_BANK, 7,
            "у майбутньому → <b>przyszłości</b>."),
    MCQItem("czytanie", "", "Robot tylko pomaga ___ i nie przyjmie zamówienia.", _ZAD5_BANK, 8, "офіціантам → <b>kelnerom</b>."),
    MCQItem("czytanie", "", "…nie może umyć ___, nalać piwa czy innego napoju.", _ZAD5_BANK, 9, "склянки → <b>szklanki</b>."),
]

# ── Zad III: вставити фрагменти (початок тренувань). Приклад=C. Ключ: G,A,E,H,B,D,F. ──
_ZAD3 = MatchTask(
    section="czytanie",
    title="2022-06 Читання Zad III — встав фрагменти (початок тренувань)",
    intro="Прочитай текст-поради для початківців у спорті. Заповни пропуски 1–7 фрагментами A–H.",
    options=[
        "i zapisać w tradycyjnym lub elektronicznym kalendarzu",  # A
        "szybko ci się znudzą i przestaniesz je lubić",  # B
        "dlatego lepiej zacznij od zestawów ćwiczeń",  # D
        "staraj się ćwiczyć regularnie, najlepiej co drugi dzień",  # E
        "pomogą wzmocnić całe ciało",  # F
        "jak inne obowiązki i aktywności",  # G
        "to nie oczekuj spektakularnych efektów",  # H
    ],
    prompts=[
        "1. Dzięki temu, że potraktujesz trening ___, trudniej będzie ci zrezygnować.",
        "2. Pamiętaj, że ten czas warto zaplanować ___.",
        "3. Jeżeli dopiero zaczynasz, ___ – takie rozwiązanie jest optymalne.",
        "4. Gdy na sport poświęcasz czas raz na siedem dni, ___.",
        "5. Zbyt intensywne ćwiczenia na początek – prawdopodobnie ___.",
        "6. Intensywne ćwiczenia prowadzą do kontuzji, ___, które wymagają precyzji.",
        "7. Takie ćwiczenia ___ i będą doskonałą bazą do dalszej aktywności.",
    ],
    key=[5, 0, 3, 6, 1, 2, 4],  # G,A,E,H,B,D,F
    explain=[
        "«potraktujesz ___» → G (як інші обов'язки).",
        "«zaplanować ___» → A (і записати в календарі).",
        "«dopiero zaczynasz, ___» → E (тренуйся регулярно, через день).",
        "«raz na 7 dni, ___» → H (не чекай видовищних ефектів).",
        "«prawdopodobnie ___» → B (швидко набриднуть).",
        "«do kontuzji, ___» → D (тож краще почни із наборів вправ).",
        "«Takie ćwiczenia ___» → F (допоможуть зміцнити все тіло)."],
)

# ── Zad IV: заголовок↔текст (як навчити дітей заощаджувати). Приклад=C. Ключ: D,G,E,B,A,F. ──
_ZAD4 = MatchTask(
    section="czytanie",
    title="2022-06 Читання Zad IV — заголовок↔текст (заощадження для дітей)",
    intro="«Jak nauczyć dzieci oszczędzania?» — до кожного заголовка (1–6) добери фрагмент A–G.",
    options=[
        "Ile musimy zapłacić za prąd, jedzenie czy ubrania? Już małym dzieciom można tłumaczyć, "
        "jak wygląda budżet rodzinny.",  # A
        "Jesteś wzorem dla dziecka – twoja postawa pomoże lub przeszkodzi; jeśli trzeba, zmień "
        "swoje zwyczaje związane z wydawaniem pieniędzy.",  # B
        "Rysujemy tabelę z obowiązkami i kwotami (np. wyrzucanie śmieci – 3 zł) i liczymy, ile "
        "dziecko może zarobić po wykonaniu zadań.",  # D
        "Część zaoszczędzonych pieniędzy warto przekazać na cel charytatywny – niech dziecko "
        "samo wybierze, komu pomóc.",  # E
        "Wybierz z dzieckiem słoiki do zbierania pieniędzy i podpisz je celami: bilet na koncert "
        "– 150 zł, gra – 85 zł, kieszonkowe na wakacje – 300 zł.",  # F
        "Młodsze dzieci, które nie potrafią liczyć, można nagradzać kuponami – nimi „zapłacą” za "
        "bajkę czy dodatkową przyjemność.",  # G
    ],
    prompts=[
        "1. Miesięczne wynagrodzenie",
        "2. Nie tylko pieniądze za pracę",
        "3. Naucz, jak się dzielić",
        "4. Zacznij od pracy nad sobą",
        "5. Rozmawiaj o wydatkach",
        "6. Naucz oszczędzania na przyjemności",
    ],
    key=[2, 5, 3, 1, 0, 4],  # D,G,E,B,A,F
    explain=[
        "місячна винагорода → D (таблиця обов'язків і сум, скільки дитина заробить).",
        "не тільки гроші за працю → G (молодших нагороджуй купонами).",
        "навчи ділитися → E (частину заощаджень — на благодійність).",
        "почни з роботи над собою → B (ти взірець, зміни свої звички).",
        "розмовляй про витрати → A (пояснюй дітям сімейний бюджет).",
        "навчи заощаджувати на приємності → F (баночки з цілями)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: відмінювання. Текст про журнал «Wiedza i Życie». ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про науково-популярний журнал «Wiedza i Życie».",
            "Łączy długą tradycję z ___.",
            ["nowoczesnością", "nowoczesność", "nowoczesności"], 0, "z + орудний → <b>nowoczesnością</b>."),
    MCQItem("gramatyka", "", "Prostym językiem pisze o ___, co się dzieje w laboratoriach.",
            ["tego", "tych", "tym"], 2, "o + місцевий → <b>tym</b>."),
    MCQItem("gramatyka", "", "Przygląda się ___ rezultatom badań.",
            ["najnowszym", "najnowszą", "najnowszymi"], 0, "przyglądać się + давальний мн. → <b>najnowszym</b>."),
    MCQItem("gramatyka", "", "W każdym numerze jest wiele ___ i tabel.",
            ["ilustracje", "ilustracji", "ilustracjach"], 1, "wiele + родовий мн. → <b>ilustracji</b>."),
    MCQItem("gramatyka", "", "…ilustracji i tabel, ___ ułatwiają zrozumienie.",
            ["które", "którzy", "którymi"], 0, "означальне (наз. мн. неос.) → <b>które</b>."),
    MCQItem("gramatyka", "", "W ___ publikują swoje prace znani badacze.",
            ["miesięcznika", "miesięczniku", "miesięcznikiem"], 1, "w + місцевий → <b>miesięczniku</b>."),
    MCQItem("gramatyka", "", "…publikują prace ___ badacze.",
            ["znane", "znani", "znany"], 1, "наз. мн. чол.-ос. → <b>znani</b>."),
    MCQItem("gramatyka", "", "…znani ___ z różnych stron świata.",
            ["badaczy", "badaczom", "badacze"], 2, "підмет (наз. мн.) → <b>badacze</b>."),
    MCQItem("gramatyka", "", "…z różnych stron ___.",
            ["światów", "światu", "świata"], 2, "stron + родовий → <b>świata</b>."),
    MCQItem("gramatyka", "", "Omawia również ___ książki o nauce.",
            ["ciekawy", "ciekawe", "ciekawi"], 1, "знах. мн. неос. → <b>ciekawe</b>."),
    # ── Zad III: ступенювання. Текст про клімат/катастрофи. ──
    MCQItem("gramatyka", "Текст про кліматичні катастрофи.",
            "Jeżeli temperatura będzie rosła, takie katastrofy będą jeszcze ___.",
            ["najczęściej", "częstsze", "najczęstsze"], 1, "вищий ступ. (частіші) → <b>częstsze</b>."),
    MCQItem("gramatyka", "", "Nigdy wcześniej nie występowały tak ___ temperatury.",
            ["wysokie", "wyższe", "najwyższe"], 0, "«tak ___» + наз. мн. → <b>wysokie</b>."),
    MCQItem("gramatyka", "", "Kilka miesięcy ___ susze stały się przyczyną pożarów.",
            ["późno", "najpóźniej", "później"], 2, "«kilka miesięcy ___» → <b>później</b>."),
    MCQItem("gramatyka", "", "W ciągu 50 lat kataklizmy spowodowały ___ strat materialnych.",
            ["więcej", "najwięcej", "dużo"], 1, "найбільше (за весь час) → <b>najwięcej</b>."),
    MCQItem("gramatyka", "", "Liczba ofiar śmiertelnych jest znacznie ___.",
            ["mniejsza", "mniej", "mało"], 0, "вищий ступ. прикметника (liczba) → <b>mniejsza</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: czyli). ──
    MCQItem("gramatyka", "Текст про Тель-Авів. Встав сполучник (зайве слово — <b>czyli</b>).",
            "Przyjeżdżają nie tylko po to, ___ opalać się na plaży…",
            ["czyli", "żeby", "dlatego", "że", "i", "ale"], 1, "мета → <b>żeby</b>."),
    MCQItem("gramatyka", "", "…opalać się ___ kąpać w morzu…",
            ["czyli", "żeby", "dlatego", "że", "i", "ale"], 4, "перелік → <b>i</b> (та)."),
    MCQItem("gramatyka", "", "…___ także dla wspaniałej kuchni.",
            ["czyli", "żeby", "dlatego", "że", "i", "ale"], 5, "«nie tylko… ___ także» → <b>ale</b>."),
    MCQItem("gramatyka", "", "Podają potrawy warzywne, ___ turyści uważają miasto za stolicę bezmięsnych.",
            ["czyli", "żeby", "dlatego", "że", "i", "ale"], 2, "наслідок → <b>dlatego</b> (тому)."),
    MCQItem("gramatyka", "", "…przyjaznymi dla wegan, co oznacza, ___ 25% dań jest roślinnych.",
            ["czyli", "żeby", "dlatego", "że", "i", "ale"], 3, "«oznacza, ___» → <b>że</b>."),
    # ── Zad VII: вид/способи. Текст про подарунки/мрії. ──
    MCQItem("gramatyka", "Текст-заклик про подарунки й мрії.",
            "…i ___ o nich otwarcie (o swoich marzeniach).",
            ["powiedzielibyście", "mówcie", "mówilibyście"], 1, "наказ до «wy» → <b>mówcie</b>."),
    MCQItem("gramatyka", "", "Gdybyście ___ ze znajomymi, że każdy zrobi listę prezentów…",
            ["umówili się", "umawialibyście się", "umówilibyście się"], 0, "«gdybyście ___» → <b>umówili się</b>."),
    MCQItem("gramatyka", "", "…wtedy wybieranie podarunku ___ łatwiejsze.",
            ["byłby", "byłoby", "bądź"], 1, "умовний, ніяк. → <b>byłoby</b>."),
    MCQItem("gramatyka", "", "Vouchery, które różne osoby ___ od bliskich.",
            ["otrzymaliby", "otrzymywałoby", "otrzymałyby"], 2, "умовний, 3 ос. мн. (osoby) → <b>otrzymałyby</b>."),
    MCQItem("gramatyka", "", "Badani internauci często ___ dostać voucher niż rzecz.",
            ["wolałaby", "woleliby", "wolałyby"], 1, "умовний, 3 ос. мн. чол.-ос. → <b>woleliby</b>."),
    MCQItem("gramatyka", "", "Jeśli masz kupić prezent, ___ lot balonem lub skok ze spadochronem.",
            ["niech wybiera", "wybierałbyś", "wybierz"], 2, "наказ до «ty» → <b>wybierz</b>."),
    MCQItem("gramatyka", "", "…i nie ___ o to, że prezent się nie spodoba.",
            ["martwiłbyś się", "martw się", "zmartwiłbyś się"], 1, "наказ до «ty» → <b>martw się</b>."),
    MCQItem("gramatyka", "", "Znajomy bardziej ___ z takiej niespodzianki niż ze skarpetek.",
            ["ucieszyłby się", "ucieszyłaby się", "niech się cieszy"], 0, "умовний, 3 ос. одн. чол. → <b>ucieszyłby się</b>."),
    MCQItem("gramatyka", "", "___ podarować komuś spełnienie chociaż jednego marzenia.",
            ["Próbowalibyśmy", "Spróbowalibyśmy", "Spróbujmy"], 2, "«нумо» докон., 1 ос. мн. → <b>Spróbujmy</b>."),
    MCQItem("gramatyka", "", "Niech nasz przyjaciel ___ szczęśliwy!",
            ["poczuje się", "poczułby się", "czułby się"], 0, "«niech ___» докон. → <b>poczuje się</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: między). Текст про кам'яниці. ──
    MCQItem("gramatyka", "Текст про квартири в кам'яницях. Встав прийменник (зайве слово — <b>między</b>).",
            "Wielu kolegów zdecydowało się na kupno mieszkania ___ kamienicy.",
            ["dla", "w", "przed", "z", "do", "między"], 1, "w + місцевий → <b>w</b> kamienicy."),
    MCQItem("gramatyka", "", "Często są to lokale ___ ciekawą historią.",
            ["dla", "w", "przed", "z", "do", "między"], 3, "lokale z + орудний → <b>z</b>."),
    MCQItem("gramatyka", "", "Każdy próbuje wrócić ___ dawnego stylu mieszkania.",
            ["dla", "w", "przed", "z", "do", "między"], 4, "wrócić do + родовий → <b>do</b>."),
    MCQItem("gramatyka", "", "To wyraz szacunku ___ ludzi, którzy tu żyli.",
            ["dla", "w", "przed", "z", "do", "między"], 0, "szacunek dla + родовий → <b>dla</b>."),
    MCQItem("gramatyka", "", "…ludzi, którzy żyli tu wiele lat ___ nimi.",
            ["dla", "w", "przed", "z", "do", "między"], 2, "przed + орудний (перед ними) → <b>przed</b>."),
]

# ── Zad IV: вписати форми (тепер./мин.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2022-06 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або минулий час). Текст про родинний "
           "дім Anny.\n\n<i>Приклад: często <b>wspomina</b> (wspominać), gdy <b>była</b> (być) mała.</i>"),
    prompts=[
        "1. Jej rodzice ___ (uczyć) w szkole,",
        "2. …a nią i siostrą ___ (opiekować się) babcia Wanda.",
        "3. Dom ___ (dawać) Annie poczucie bezpieczeństwa.",
        "4. Magdalena z dzieciństwa ___ (pamiętać) tylko samotne wieczory.",
        "5. …zwłaszcza gdy Magda ___ (chcieć) się pobawić z ojcem.",
        "6. Dziewczyna szybko ___ (wyjść) za mąż i wyprowadziła się.",
        "7. Mąż i ja ___ (tęsknić) za dużą, wielopokoleniową rodziną,",
        "8. …i właśnie ___ (rozglądać się) za wspólnym mieszkaniem.",
        "9. Ten pomysł bardzo mi się ___ (podobać).",
        "10. Ja nadal ___ (marzyć) o domu dla całej rodziny.",
    ],
    accepted=[
        ["uczyli"], ["opiekowała się"], ["dawał"], ["pamięta"], ["chciała"],
        ["wyszła"], ["tęsknimy"], ["rozglądamy się"], ["podoba"], ["marzę"],
    ],
    explain=[
        "минулий, 3 ос. мн. чол.-ос. (rodzice) → <b>uczyli</b>.",
        "минулий, 3 ос. одн. жін. (babcia) → <b>opiekowała się</b>.",
        "минулий, 3 ос. одн. чол. (dom) → <b>dawał</b>.",
        "тепер., 3 ос. одн. (Magdalena) → <b>pamięta</b>.",
        "минулий, 3 ос. одн. жін. (Magda) → <b>chciała</b>.",
        "минулий, 3 ос. одн. жін. → <b>wyszła</b>.",
        "тепер., 1 ос. мн. → <b>tęsknimy</b>.",
        "тепер., 1 ос. мн. → <b>rozglądamy się</b>.",
        "тепер., 3 ос. одн. → <b>podoba</b>.",
        "тепер., 1 ос. одн. → <b>marzę</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2022-06 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: program «o podróżach» → O czym?</i>"),
    prompts=[
        "Michał smaruje chleb «dżemem».",
        "Weronika zapytała starszego pana «o drogę».",
        "Marcin «codziennie» używa laptopa.",
        "Karol zabrał dzieci «siostry» do muzeum.",
        "Monika mieszkała w Australii «dwa lata».",
    ],
    accepted=[["czym"], ["o co"], ["jak często"], ["czyje"], ["jak długo"]],
    explain=[
        "smarować чим? орудний → <b>Czym?</b>",
        "zapytać o + знах. → <b>O co?</b>",
        "частота → <b>Jak często?</b>",
        "«czyje dzieci» → <b>Czyje?</b>",
        "тривалість → <b>Jak długo?</b>",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2022-06 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «dała jeść kotom» (nakarmiła) → nakarmiła koty.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "W lipcu planujemy wyjazd do Hiszpanii.",
        "Mojej koleżance ładnie jest w kolorze zielonym.",
        "Dorota przeprowadziła się do Krakowa już rok temu.",
        "W jakim wieku jest ich córka?",
        "Wczoraj był słoneczny, ale chłodny dzień.",
    ],
    words=["zamiar", "wygląda", "mieszka", "lat", "było"],
    models=[
        ["W lipcu mamy zamiar wyjechać do Hiszpanii."],
        ["Moja koleżanka ładnie wygląda w kolorze zielonym."],
        ["Dorota mieszka w Krakowie już rok.", "Dorota mieszka w Krakowie od roku."],
        ["Ile lat ma ich córka?"],
        ["Wczoraj było słonecznie, ale chłodno."],
    ],
)

EXAM = Exam(
    id="2022-06",
    label="Реальний іспит червень-2022 (офіц.)",
    kind="real",
    year=2022,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
