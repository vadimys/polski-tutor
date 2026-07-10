"""РЕАЛЬНИЙ минулий іспит B1 — квітень 2023 (certyfikatpolski.pl).

Джерело: 2023_04_15_16_B1_arkusz + …_transkrypcja.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН ключ
звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad); аудіювання — у listening.py.
- Czytanie: Zad I(×5)+II(TAK/NIE ×6)+V(×10) MCQ; Zad III/IV matching.
- Gramatyka: I(×10)+II(×5)+III(×5)+VII(×10)+VIII(×5) MCQ; IV(×10)+V(×5) free-fill; VI(×5) open.
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

# ── CZYTANIE — Zad I (a/b/c). Ключ: c,b,b,a,a. ───────────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Najnowsze badania japońskich naukowców po raz pierwszy potwierdzają, że picie kawy "
            "poprawia wyniki sportowców w bieganiu. Czy w przyszłości kawa trafi na listę "
            "substancji zakazanych przed zawodami?",
            "Z tego tekstu wynika, że:",
            ["sportowcy już teraz nie powinni pić kawy przed treningiem",
             "wypicie kawy nie wpływa na rezultat biegu",
             "wcześniej nikt nie zajmował się takimi badaniami"], 2,
            "«po raz pierwszy potwierdzają» → раніше таких досліджень не було."),
    MCQItem("czytanie",
            "W amerykańskich i brytyjskich sklepach zaczyna brakować jajek. Polscy producenci "
            "informują, że w Polsce ich nie zabraknie, ale zapłacimy więcej. Droższe będą też "
            "makaron, majonez i ciasta.",
            "Z tego tekstu wynika, że:",
            ["Polska jest największym na świecie producentem jajek",
             "cena jajek w Polsce będzie wyższa",
             "niedługo w Polsce będzie problem z kupieniem jajek"], 1,
            "«zapłacimy za nie więcej» → ціна вища. В Польщі яєць НЕ забракне."),
    MCQItem("czytanie",
            "Michał znalazł nad morzem w Dziwnowie bardzo stare narzędzie – ma ponad 7 tys. lat. "
            "Prezes lokalnego muzeum podziękował Michałowi za podarowanie tak cennego przedmiotu.",
            "Z tego tekstu wynika, że:",
            ["Michał nadal jest właścicielem narzędzia, które znalazł",
             "Michał oddał do muzeum przedmiot, który znalazł",
             "za znaleziony przedmiot chłopak otrzymał nagrodę od prezesa"], 1,
            "«podarowanie» → віддав до музею. Про нагороду не сказано."),
    MCQItem("czytanie",
            "Z czeskiego zoo przy polskiej granicy uciekł kangur. Szuka go policja. Pracownik zoo "
            "poinformował, że zwierzę nie jest agresywne, jest nieśmiałe i na pewno bardzo głodne.",
            "Z tego tekstu wynika, że:",
            ["zwierzę od dawna nie jadło", "kangur jest niebezpieczny i może zaatakować ludzi",
             "w poszukiwaniach pomagają pracownicy zoo"], 0,
            "«bardzo głodne» → давно не їло. Не агресивний; шукає поліція."),
    MCQItem("czytanie",
            "Marta dowiaduje się od Adama, że będzie miał dziecko z jej byłą koleżanką Niną. Jest "
            "bardzo zdenerwowana. Kocha go, ale nie wie, czy będzie mogła dalej z nim być. Tak "
            "zaczyna się kolejny sezon serialu „Papiery na szczęście”.",
            "Z tego tekstu wynika, że:",
            ["Nina nie powiedziała Marcie, że spodziewa się dziecka Adama",
             "wiadomość o dziecku pozytywnie zaskoczyła Martę",
             "Adam i Marta planują wziąć ślub"], 0,
            "Marta дізнається від Адама (не від Ніни) → Ніна не сказала. Вона zdenerwowana (не рада)."),
    # ── Zad II: TAK/NIE — «Przyszłość pszczół». Ключ: T,N,T,N,T,N. ──────
    MCQItem("czytanie",
            "TEKСТ «Przyszłość pszczół»: у майбутньому бджіл може не бути (стаття в «Nature»). "
            "Аналізи ТРИВАЮТЬ, але вже підтверджено: бджоли живуть коротше через зміни клімату. "
            "Після холодів раптове потепління → квіти цвітуть навіть у грудні. Людина легко "
            "приймає аномалії, а бджоли — ні: узимку сплять, навесні/влітку працюють; коли рано "
            "тепліє — прокидаються, а раптовий холод їх убиває. Довга посуха = нема квітів = нема "
            "їжі. На тривалість життя впливають і віруси: змінюють запах бджоли, тож вона не "
            "впізнає сестер і не вертається додому — це смерть.",
            "TAK/NIE: Badania nad pszczołami jeszcze się nie zakończyły.",
            ["TAK", "NIE"], 0, "ТАК — «Analizy ciągle trwają»."),
    MCQItem("czytanie", "",
            "TAK/NIE: Naukowcy nadal nie wiedzą, dlaczego te owady coraz wcześniej umierają.",
            ["TAK", "NIE"], 1, "НІ — відомо: винен клімат (раптові зміни погоди)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Pszczoły gorzej niż ludzie radzą sobie ze zmianą klimatu.",
            ["TAK", "NIE"], 0, "ТАК — людина легко приймає аномалії, бджоли мають проблему."),
    MCQItem("czytanie", "",
            "TAK/NIE: Brak deszczu pozytywnie wpływa na produkcję miodu.",
            ["TAK", "NIE"], 1, "НІ — без дощу нема квітів → бджолам бракує їжі."),
    MCQItem("czytanie", "",
            "TAK/NIE: Wirusy atakują również pszczoły.",
            ["TAK", "NIE"], 0, "ТАК — віруси змінюють запах бджіл."),
    MCQItem("czytanie", "",
            "TAK/NIE: Zmiany klimatu powodują u owadów problemy z identyfikacją członków rodziny.",
            ["TAK", "NIE"], 0, "ТАК — через зміну запаху не впізнають сестер."),
    # ── Zad V: обери найкраще слово («Higiena snu»). ────────────────────
    MCQItem("czytanie", "Текст про гігієну сну. Обери найкраще слово.",
            "Dzięki temu w ciągu dnia nie poczujemy się ___.",
            ["zmęczeni", "wypoczęci", "zrelaksowani"], 0, "не почуватися ___ → <b>zmęczeni</b> (втомленими)."),
    MCQItem("czytanie", "", "Gdy jesteśmy mali, rodzice ___, żebyśmy dobrze spali.",
            ["opiekują się", "próbują", "dbają"], 2, "«dbają, żeby» → <b>dbają</b>."),
    MCQItem("czytanie", "", "…rytuały, które uczą organizm, że nadchodzi czas ___.",
            ["wakacji", "odpoczynku", "urlopu"], 1, "час відпочинку (сну) → <b>odpoczynku</b>."),
    MCQItem("czytanie", "", "Regularne godziny to także ___ nawyk.",
            ["łatwy", "ogromny", "ważny"], 2, "важлива звичка → <b>ważny</b>."),
    MCQItem("czytanie", "", "Problemami, których ___ doświadczamy, są trudności z zasypianiem.",
            ["najczęściej", "najgłębiej", "najbardziej"], 0, "яких найчастіше зазнаємо → <b>najczęściej</b>."),
    MCQItem("czytanie", "", "Jeśli te sytuacje występują rzadko, nie powinny nas ___.",
            ["boleć", "martwić", "nudzić"], 1, "не мають нас турбувати → <b>martwić</b>."),
    MCQItem("czytanie", "", "Jest kilka reguł, o których trzeba ___.",
            ["zapominać", "pamiętać", "troszczyć się"], 1, "треба пам'ятати → <b>pamiętać</b>."),
    MCQItem("czytanie", "", "___ zasadą zdrowego snu jest zachowanie spokoju.",
            ["Centralną", "Podstawową", "Regularną"], 1, "основне правило → <b>Podstawową</b>."),
    MCQItem("czytanie", "", "Pomocne są ___ relaksacyjne i oddechowe.",
            ["ćwiczenia", "szkolenia", "zadania"], 0, "релаксаційні вправи → <b>ćwiczenia</b>."),
    MCQItem("czytanie", "", "Jeśli nadal nie możemy spać, warto umówić się na ___ u specjalisty.",
            ["przyjęcie", "radę", "wizytę"], 2, "записатися на візит → <b>wizytę</b>."),
]

# ── Zad III: вставити фрагменти («Niezła sztuka»). Приклад=C. Ключ: G,B,A,E,H,F,D. ──
_ZAD3 = MatchTask(
    section="czytanie",
    title="2023-04 Читання Zad III — встав фрагменти (Niezła sztuka)",
    intro="Прочитай текст про фонд «Niezła sztuka». Заповни пропуски 1–7 фрагментами A–G.",
    options=[
        "bez tych wszystkich skomplikowanych terminów naukowych",  # A
        "można również posłuchać w formie audio",  # B
        "ponieważ są ukryte w muzealnych magazynach",  # D
        "informacje o aktualnych wydarzeniach ze świata sztuki",  # E
        "będzie dostępny dla każdego i o każdej porze",  # F
        "„sztuka dla każdego – od amatora do konesera”",  # G
        "ale wszyscy mają jedną cechę, która ich łączy",  # H
    ],
    prompts=[
        "1. …chcą zainteresować jak najszerszą publiczność według zasady ___",
        "2. …a niektórych materiałów ___.",
        "3. Chcemy pokazać, że sztukę warto prezentować inaczej, ___.",
        "4. …galerie prac artystów oraz ___.",
        "5. Piszą przedstawiciele różnych zawodów – wykładowcy, pracownicy muzeów, pisarze, ___",
        "6. …wirtualny katalog dzieł, który ___.",
        "7. Również te dzieła, których nie można obejrzeć na co dzień, ___.",
    ],
    key=[5, 1, 0, 3, 6, 4, 2],  # G,B,A,E,H,F,D
    explain=[
        "«według zasady ___» → G (мистецтво для кожного).",
        "«niektórych materiałów ___» → B (можна й послухати в аудіо).",
        "«prezentować inaczej, ___» → A (без складних наукових термінів).",
        "«oraz ___» → E (інформація про події зі світу мистецтва).",
        "«pisarze, ___» → H (але всіх єднає одна риса).",
        "«katalog, który ___» → F (буде доступний кожному й будь-коли).",
        "«nie można obejrzeć, ___» → D (бо сховані в музейних сховищах)."],
)

# ── Zad IV: заголовки↔тексти («Jak pomagać bez pieniędzy»). Приклад=B. Ключ: E,H,A,G,C,F,D. ──
_ZAD4 = MatchTask(
    section="czytanie",
    title="2023-04 Читання Zad IV — заголовок↔текст (як допомагати без грошей)",
    intro="«Jak pomagać bez pieniędzy?» — до кожного заголовка (1–7) добери фрагмент A–G.",
    options=[
        "Zaproponuj kolegom w firmie, aby przekazać potrzebującym podstawowe produkty "
        "spożywcze i wspólnie zawieźć je do organizacji charytatywnej.",  # A
        "Jeżeli jesteś zdrowy i masz więcej niż 18 lat, zastanów się nad oddaniem krwi – "
        "nie da się jej wyprodukować w laboratorium.",  # C
        "Możesz oferować swój czas i zaangażowanie, nic nie zarabiając – pomagasz seniorom, "
        "samotnym matkom czy osobom chorym.",  # D
        "Ktoś na ulicy źle się poczuł albo nie radzi sobie z ciężkimi zakupami? Nie zastanawiaj "
        "się, tylko zaproponuj pomoc.",  # E
        "Zbliżają się twoje urodziny lub ślub? Poproś, aby bliscy zamiast prezentów wpłacili "
        "pieniądze na konto organizacji charytatywnej.",  # F
        "Na stronie domydziecka.org są informacje o tym, czego potrzebują mali mieszkańcy – "
        "zabawki, buty, książki czy ubrania.",  # G
        "Podczas sprzątania znalazłeś rzeczy, których nie używasz? Koce i miski możesz oddać "
        "do schroniska dla zwierząt.",  # H
    ],
    prompts=[
        "1. Nie bądź bierny w codziennych sytuacjach",
        "2. Podaruj drugie życie niepotrzebnym przedmiotom",
        "3. Zorganizuj zbiórkę w pracy",
        "4. Przygotuj paczkę dla najmłodszych",
        "5. Przekaż to, co najcenniejsze",
        "6. Zrezygnuj z prezentów",
        "7. Zostań wolontariuszem",
    ],
    key=[3, 6, 0, 5, 1, 4, 2],  # E,H,A,G,C,F,D
    explain=[
        "не будь пасивним → E (запропонуй допомогу на вулиці).",
        "друге життя речам → H (ковдри/миски — до притулку).",
        "збірка в праці → A (колеги збирають продукти).",
        "пакунок для дітей → G (домдитини: іграшки, книжки).",
        "передай найцінніше → C (здай кров).",
        "відмовся від подарунків → F (нехай перекажуть на благодійність).",
        "стань волонтером → D (даруй свій час і залучення)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: підкресли форму (відмінювання). Текст про виставку Canaletta. ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про виставку картин Каналетто в Королівському замку.",
            "Pierwsza część ___ kolekcji to prace związane z Wenecją.",
            ["tej", "te", "tę"], 0, "перша частина (чого?) родовий → <b>tej</b> kolekcji."),
    MCQItem("gramatyka", "", "…a także z ___ młodego malarza do włoskich miast.",
            ["podróżach", "podróżom", "podróżami"], 2, "związane z + орудний → <b>podróżami</b>."),
    MCQItem("gramatyka", "", "…do innych włoskich ___.",
            ["miastach", "miast", "miasta"], 1, "do + родовий множини → <b>miast</b>."),
    MCQItem("gramatyka", "", "To był kraj, w ___ mieszkał ponad dwadzieścia lat.",
            ["którego", "które", "którym"], 2, "w + місцевий → <b>którym</b>."),
    MCQItem("gramatyka", "", "Tutaj malował dla ___ króla, Stanisława Augusta.",
            ["polskiego", "polskiemu", "polska"], 0, "dla + родовий → <b>polskiego</b>."),
    MCQItem("gramatyka", "", "W ___ Zamku Królewskiego ludzie przyglądają się obrazom.",
            ["salę", "sale", "sali"], 2, "w + місцевий → <b>sali</b>."),
    MCQItem("gramatyka", "", "…przyglądają się ___ z XVIII wieku.",
            ["obrazom", "obrazy", "obrazami"], 0, "przyglądać się + давальний → <b>obrazom</b>."),
    MCQItem("gramatyka", "", "Eksperci przygotowali ___ katalog wystawy.",
            ["specjalnego", "specjalne", "specjalny"], 2, "знах. (яку каталог?) → <b>specjalny</b>."),
    MCQItem("gramatyka", "", "…napisany w wersji ___.",
            ["angielskie", "angielskiej", "angielską"], 1, "w wersji (якій?) місц./род. → <b>angielskiej</b>."),
    MCQItem("gramatyka", "", "Można ___ kupić w zamkowym sklepie.",
            ["go", "ich", "niego"], 0, "kupić + знах. (katalog→його) → <b>go</b>."),
    # ── Zad III: ступенювання. Текст про ціни на житло. ──
    MCQItem("gramatyka", "Текст про ринок житла.",
            "Liczba kupionych mieszkań jest obecnie ___.",
            ["niżej", "niższą", "najniższa"], 2, "найнижча (за всі) → <b>najniższa</b>."),
    MCQItem("gramatyka", "", "Coraz ___ młodych ludzi decyduje się na wynajem.",
            ["większy", "więcej", "najwięcej"], 1, "coraz ___ (дедалі більше) → <b>więcej</b>."),
    MCQItem("gramatyka", "", "…wynajem małego, a tym samym ___ lokalu.",
            ["taniej", "tańszego", "tańszy"], 1, "родовий (дешевшого приміщення) → <b>tańszego</b>."),
    MCQItem("gramatyka", "", "Przyszły rok może być dla branży budowlanej ___ w historii.",
            ["gorzej", "gorszy", "najgorszy"], 2, "найгірший (в історії) → <b>najgorszy</b>."),
    MCQItem("gramatyka", "", "Zainteresowanie może być o 40 procent ___ niż w 2022 roku.",
            ["mniej", "mniejsze", "mniejsi"], 1, "вищий ступ. прикметника (zainteresowanie) → <b>mniejsze</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: chociaż). ──
    MCQItem("gramatyka", "Текст про навчання. Встав сполучник (зайве слово — <i>chociaż</i>).",
            "Lekcji jest niemało i są za krótkie, ___ wszystkiego nauczyć się w szkole.",
            ["żeby", "chociaż", "oraz", "więc", "który", "gdy"], 0, "«za krótkie, ___» → <b>żeby</b> (замало, щоб)."),
    MCQItem("gramatyka", "", "Zadania są ważne, ___ uczniowie całe popołudnia spędzają nad książkami.",
            ["żeby", "chociaż", "oraz", "więc", "który", "gdy"], 3, "наслідок → <b>więc</b> (тому)."),
    MCQItem("gramatyka", "", "…treningi sportowe ___ warsztaty artystyczne.",
            ["żeby", "chociaż", "oraz", "więc", "który", "gdy"], 2, "перелік → <b>oraz</b> (та)."),
    MCQItem("gramatyka", "", "Wszyscy mają dostęp do internetu, ___ także zabiera czas.",
            ["żeby", "chociaż", "oraz", "więc", "który", "gdy"], 4, "означальне → <b>który</b> (який)."),
    MCQItem("gramatyka", "", "Nawet prostych rzeczy trudno się nauczyć, ___ człowiek jest zmęczony.",
            ["żeby", "chociaż", "oraz", "więc", "który", "gdy"], 5, "час/умова → <b>gdy</b> (коли)."),
    # ── Zad VII: підкресли форму (вид/способи). Діалог про дієту. ──
    MCQItem("gramatyka", "Діалог: Anna хоче схуднути до весілля, радиться з Pawłem (дієтологом).",
            "Nie ma diety cud, dzięki której ___ schudnąć w kilkanaście dni.",
            ["mogłaby", "mogłabyś", "mogłoby"], 1, "умовний, 2 ос. одн. жін. (ty) → <b>mogłabyś</b>."),
    MCQItem("gramatyka", "", "To nie ___ też zdrowe dla twojego organizmu.",
            ["byłoby", "byłyby", "bądź"], 0, "умовний, ніяк. рід → <b>byłoby</b>."),
    MCQItem("gramatyka", "", "___ rozsądnie!",
            ["Odchudziłabyś się", "Odchudzałyby się", "Odchudzaj się"], 2, "наказ до «ty» → <b>Odchudzaj się</b>."),
    MCQItem("gramatyka", "", "A co ty ___ na moim miejscu?",
            ["zrobiłby", "zrób", "zrobiłbyś"], 2, "умовний, 2 ос. одн. → <b>zrobiłbyś</b>."),
    MCQItem("gramatyka", "", "Gdybym ___ wyglądać lepiej, starałbym się jeść zdrowo.",
            ["chciałbym", "chciał", "chciałem"], 1, "«Gdybym ___» — форма на -ł → <b>chciał</b>."),
    MCQItem("gramatyka", "", "…owoce i warzywa, które ___ mi dawkę witamin.",
            ["niech zapewni", "zapewniłyby", "zapewniłoby"], 1, "умовний, 3 ос. мн. (owoce i warzywa) → <b>zapewniłyby</b>."),
    MCQItem("gramatyka", "", "Jeśli możesz, ___ ze swojej diety tłuste mięso.",
            ["wyrzucałaby", "wyrzuciłabyś", "wyrzuć"], 2, "наказ докон. до «ty» → <b>wyrzuć</b>."),
    MCQItem("gramatyka", "", "Po południu ___ pełnoziarnisty makaron lub ryż.",
            ["niech wybierze", "niech wybiera", "wybieraj"], 2, "наказ до «ty» → <b>wybieraj</b>."),
    MCQItem("gramatyka", "", "Idę z synem na basen. Proponuję, ___ tam razem.",
            ["chodźmy", "chodź", "chodziliby"], 0, "«нумо» 1 ос. мн. → <b>chodźmy</b>."),
    MCQItem("gramatyka", "", "Dzisiaj nie mogę. ___ sami.",
            ["Idźmy", "Idźcie", "Poszlibyście"], 1, "наказ до «wy» → <b>Idźcie</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: na). Текст про котів. ──
    MCQItem("gramatyka", "Текст про котів. Встав прийменник (зайве слово — <i>na</i>).",
            "Koty ciągle chodzą ___ człowiekiem, chcą się bawić.",
            ["z", "dla", "na", "w", "za", "u"], 4, "chodzić za + орудний (ходять за) → <b>za</b>."),
    MCQItem("gramatyka", "", "Starajmy się, by zwierzę miało ___ domu wszystko, czego potrzebuje.",
            ["z", "dla", "na", "w", "za", "u"], 3, "w + місцевий (удома) → <b>w</b>."),
    MCQItem("gramatyka", "", "Ważne, żeby często się ___ nim bawić.",
            ["z", "dla", "na", "w", "za", "u"], 0, "bawić się z + орудний → <b>z</b> nim."),
    MCQItem("gramatyka", "", "Pamiętajmy o regularnych wizytach ___ weterynarza.",
            ["z", "dla", "na", "w", "za", "u"], 5, "u + родовий (у ветеринара) → <b>u</b>."),
    MCQItem("gramatyka", "", "Wszystko to jest ważne ___ zdrowia małego przyjaciela.",
            ["z", "dla", "na", "w", "za", "u"], 1, "dla + родовий (для здоров'я) → <b>dla</b>."),
]

# ── Zad IV: вписати форми (тепер./мин.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2023-04 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або минулий час). Текст про нарікання "
           "бабусі й дідуся.\n\n<i>Приклад: <b>było</b> (być) lepiej, <b>powtarzają</b> (powtarzać).</i>"),
    prompts=[
        "1. Teraz młodzież ___ (patrzyć) tylko na ekrany.",
        "2. Chłopcy nie ___ (widzieć) świata poza internetem.",
        "3. …dziewczyny ___ (ubierać się) w za krótkie bluzki.",
        "4. Ja w młodości nigdy takich nie ___ (nosić)!",
        "5. …te słowa często ___ (ja – słyszeć) dziś od babci.",
        "6. Kiedyś chętnie ze sobą ___ (my – rozmawiać),",
        "7. …a młodzież bardziej ___ (szanować) stare tradycje.",
        "8. Dawniej dorośli także ___ (skarżyć się) na swoje dzieci,",
        "9. …a starsze panie ___ (krytykować) zachowanie młodych.",
        "10. Współcześni dziadkowie ___ (narzekać) tak samo jak przodkowie.",
    ],
    accepted=[
        ["patrzy"], ["widzą"], ["ubierają się"], ["nosiłam"], ["słyszę"],
        ["rozmawialiśmy"], ["szanowała"], ["skarżyli się"], ["krytykowały"], ["narzekają"],
    ],
    explain=[
        "тепер., 3 ос. одн. (młodzież) → <b>patrzy</b>.",
        "тепер., 3 ос. мн. (chłopcy) → <b>widzą</b>.",
        "тепер., 3 ос. мн. (dziewczyny) → <b>ubierają się</b>.",
        "минулий, 1 ос. одн. жін. → <b>nosiłam</b>.",
        "тепер., 1 ос. одн. → <b>słyszę</b>.",
        "минулий, 1 ос. мн. чол.-ос. → <b>rozmawialiśmy</b>.",
        "минулий, 3 ос. одн. (młodzież) → <b>szanowała</b>.",
        "минулий, 3 ос. мн. чол.-ос. (dorośli) → <b>skarżyli się</b>.",
        "минулий, 3 ос. мн. жін. (panie) → <b>krytykowały</b>.",
        "тепер., 3 ос. мн. → <b>narzekają</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2023-04 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: słucha «radia» → Czego?</i>"),
    prompts=[
        "Zosia «trzy razy w tygodniu» chodzi na basen.",
        "Poinformowaliśmy «ciocię Basię», że przyjdziemy jutro.",
        "Janek kupił tort z owocami «egzotycznymi».",
        "Matka nie wyprała ubrania «syna».",
        "Marysia przyszła do szkoły na «drugą» lekcję.",
    ],
    accepted=[
        ["jak często", "ile razy w tygodniu", "ile razy na tydzień"],
        ["kogo"], ["z jakimi"], ["czyjego"], ["na którą"],
    ],
    explain=[
        "частота → <b>Jak często?</b> (Ile razy w tygodniu?)",
        "poinformować + знах. → <b>Kogo?</b>",
        "«z jakimi owocami» → <b>Z jakimi?</b>",
        "«ubrania syna» (чиє?) → <b>Czyjego?</b>",
        "«na którą lekcję» → <b>Na którą?</b>",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2023-04 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «zna angielski» (mówi) → mówi po angielsku.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Mojej siostrze smakuje zupa pomidorowa.",
        "Wszyscy pracowici ludzie szanują czas.",
        "W weekend byliśmy w kinie na fascynującym filmie.",
        "Wiem, jak ma na nazwisko ten pan.",
        "Dlaczego nigdy nie ubierasz się w ten ciepły płaszcz?",
    ],
    words=["lubi", "osoby", "poszliśmy", "znam", "nosisz"],
    models=[
        ["Moja siostra lubi zupę pomidorową."],
        ["Wszystkie pracowite osoby szanują czas."],
        ["W weekend poszliśmy do kina na fascynujący film."],
        ["Znam nazwisko tego pana."],
        ["Dlaczego nigdy nie nosisz tego ciepłego płaszcza?"],
    ],
)

EXAM = Exam(
    id="2023-04",
    label="Реальний іспит квітень-2023 (офіц.)",
    kind="real",
    year=2023,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
