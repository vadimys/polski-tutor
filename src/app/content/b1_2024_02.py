"""РЕАЛЬНИЙ минулий іспит B1 — лютий 2024 (certyfikatpolski.pl, egzamin certyfikatowy).

Джерело: 4-5.02.2024-B1_arkusz_egzaminacyjny.pdf + …_transkrypcja.pdf (містить KLUCZ).
ДОСЛІВНО з arkusz, КОЖЕН ключ звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad):
- Czytanie: Zad I (a/b/c ×5) + Zad II (TAK/NIE ×6) + Zad V (вибір слова ×10) — MCQ;
  Zad III/IV — matching (tasks).
- Gramatyka: I(форми ×10) + II(сполучники ×5) + III(ступ. ×5) + VII(способи ×10)
  + VIII(прийменники ×5) — MCQ; IV(форми ×10) + V(питання ×5) — free-fill; VI(×5) — open.
Далі: Słuchanie (5 Zad).
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

# ── CZYTANIE — Zad I: «Z tego tekstu wynika…» (a/b/c) ────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Dzień kuriera zaczyna się wcześnie rano w magazynie, gdzie odbiera przesyłki, "
            "sprawdza je i aktualizuje ich dane w systemie informatycznym. Praca jest dynamiczna. "
            "Kurierzy muszą być punktualni, mieć dobrą orientację w terenie i nie bać się pracy "
            "fizycznej.",
            "Z tego tekstu wynika, że:",
            ["kurierzy rano przywożą paczki do magazynu",
             "kurierzy muszą obsługiwać programy komputerowe",
             "praca kuriera jest stresująca i niebezpieczna"], 1,
            "«aktualizuje dane w systemie informatycznym» → мусять працювати з програмами. "
            "Вони ЗАБИРАЮТЬ посилки; про стрес/небезпеку не сказано."),
    MCQItem("czytanie",
            "W tureckiej Kapadocji można oglądać piękne krajobrazy. To najpopularniejsze miejsce "
            "na lot balonem. Tysiące balonów lata tam co rano przez około 250 dni w roku – również "
            "zimą. Bilety należy zarezerwować wcześniej, bo chętnych jest dużo.",
            "Z tego tekstu wynika, że:",
            ["Kapadocję można oglądać również z powietrza",
             "od grudnia do marca loty balonem się nie odbywają",
             "zainteresowanie atrakcją jest niewielkie"], 0,
            "лот балоном → огляд з повітря. Літають «również зимою»; охочих багато."),
    MCQItem("czytanie",
            "Rodzice zastanawiają się, kiedy pójść z dzieckiem do teatru. Odpowiedź: jak "
            "najwcześniej, ale repertuar powinien być dostosowany do wieku. W ofercie są spektakle "
            "nawet dla dzieci, które mają dopiero kilka miesięcy.",
            "Z tego tekstu wynika, że:",
            ["rodzice rzadko szukają przedstawień dla dzieci",
             "dzieci najlepiej bawią się na spektaklach porannych",
             "teatry proponują przedstawienia dla różnych grup wiekowych"], 2,
            "«repertuar dostosowany do wieku», спектаклі навіть для кількамісячних → різні вікові групи."),
    MCQItem("czytanie",
            "Od września do szkoły w Kętach codziennie przychodzi pies Wally i towarzyszy uczniom "
            "na lekcjach. Uczniowie byli bardziej zainteresowani tematyką zajęć, kreatywni, "
            "spokojniejsi i szybciej pracowali, gdy Wally był w klasie.",
            "Z tego tekstu wynika, że:",
            ["Wally bawi się z uczniami między lekcjami",
             "pomysł nauczycielki daje dobre efekty",
             "pies Wally przeszkadza dzieciom w nauce"], 1,
            "учні спокійніші, уважніші, швидше працювали → ідея дає добрі результати."),
    MCQItem("czytanie",
            "Najbardziej depresyjny dzień w roku to trzeci poniedziałek stycznia (Blue Monday). "
            "Termin w 2004 roku wymyślił Cliff Arnall. Przeanalizował: niezbyt dobrą pogodę, złą "
            "kondycję finansową po świętach i niską motywację. Wielu naukowców nie akceptuje "
            "jednak jego analiz.",
            "Z tego tekstu wynika, że:",
            ["Blue Monday przypada pod koniec roku",
             "stan konta nie decyduje o naszym samopoczuciu",
             "część badaczy nie zgadza się z teorią Arnalla"], 2,
            "«wielu naukowców nie akceptuje» → частина не згодна. Blue Monday — у січні; "
            "фінанси якраз є чинником."),
    # ── Zad II: TAK/NIE до тексту «Dzień Nauki Polskiej» ────────────────
    MCQItem("czytanie",
            "TEKST «Dzień Nauki Polskiej»: одне з наймолодших держсвят Польщі, вперше святкували "
            "у 2021 році. Мета — вшанувати найвидатніших ПОЛЬСЬКИХ учених і заохотити молодь до "
            "науки. Дата — 19 лютого, день народження Міколая Коперника. Прості дослідження "
            "доступні кожному (телескопи, мікроскопи). Свято варто відзначати в школах і "
            "університетах; долучатися мають і фірми, що використовують наукові відкриття.",
            "TAK/NIE: Dzień Nauki Polskiej świętujemy już od dawna.",
            ["TAK", "NIE"], 1, "НІ — вперше у 2021 р., одне з наймолодших свят."),
    MCQItem("czytanie", "",
            "TAK/NIE: W tym dniu mówi się o naukowcach z całego świata.",
            ["TAK", "NIE"], 1, "НІ — про ПОЛЬСЬКИХ учених."),
    MCQItem("czytanie", "",
            "TAK/NIE: Głównym celem święta jest promocja nauki wśród dzieci i młodzieży.",
            ["TAK", "NIE"], 0, "ТАК — заохотити молодь, змотивувати учнів до наукової кар'єри."),
    MCQItem("czytanie", "",
            "TAK/NIE: Data Dnia Nauki Polskiej jest wyrazem szacunku dla osiągnięć wielkiego Polaka.",
            ["TAK", "NIE"], 0, "ТАК — день народження Коперника."),
    MCQItem("czytanie", "",
            "TAK/NIE: Nieskomplikowaną aparaturę do badań można łatwo kupić.",
            ["TAK", "NIE"], 0, "ТАК — прості дослідження доступні кожному (телескопи, мікроскопи)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Dzień Nauki Polskiej jest okazją do współpracy szkół z biznesem.",
            ["TAK", "NIE"], 0, "ТАК — фірми/підприємства мають долучатися й показувати відкриття молоді."),
    # ── Zad V: обери найкраще слово (текст про комедію «Sami swoi») ──────
    MCQItem("czytanie",
            "Текст про культову польську комедію «Sami swoi». Обери найкраще слово.",
            "Produkcja powstała w 1967 roku, a jej ___ był Sylwester Chęciński.",
            ["dyrektorem", "reżyserem", "aktorem"], 1, "фільм має → <b>reżysera</b> (режисера)."),
    MCQItem("czytanie", "",
            "Jasiek „John” Pawlak dawno temu ___ do Stanów Zjednoczonych.",
            ["wrócił", "wyjechał", "poszedł"], 1, "до США (напрямок, надовго) → <b>wyjechał</b>."),
    MCQItem("czytanie", "",
            "W czasie jego nieobecności w rodzinnej wsi ___ się zmieniło.",
            ["dużo", "nic", "długo"], 0, "багато змінилося → <b>dużo</b>."),
    MCQItem("czytanie", "",
            "Wesoły nastrój ___ się kończy – a wszystko z powodu sąsiada Kargula.",
            ["krótko", "mało", "szybko"], 2, "настрій ШВИДКО закінчується → <b>szybko</b>."),
    MCQItem("czytanie", "",
            "Opisując losy dwóch rodzin, scenarzysta ___ historię swojego wujka.",
            ["zrobił", "wykorzystał", "wymyślił"], 1, "використав історію дядька → <b>wykorzystał</b>."),
    MCQItem("czytanie", "",
            "___ konfliktu między sąsiadami jest w komediach częstym motywem.",
            ["Temat", "Tytuł", "Plan"], 0, "тема конфлікту → <b>Temat</b>."),
    MCQItem("czytanie", "",
            "Bohaterowie „Samych swoich” ___ o wszystko; symbolem niezgody jest płot.",
            ["wołają", "proszą", "kłócą się"], 2, "сваряться за все → <b>kłócą się</b>."),
    MCQItem("czytanie", "",
            "Nawet widzowie, którzy nie są ___ filmu, uważają go za część kultury.",
            ["fanami", "ulubieńcami", "adoratorami"], 0, "не є <b>fanami</b> (фанатами) фільму."),
    MCQItem("czytanie", "",
            "Dużą ___ miały też dwie kontynuacje komedii.",
            ["opinię", "popularność", "sławę"], 1, "мали велику <b>popularność</b> (популярність)."),
    MCQItem("czytanie", "",
            "Festiwal filmów komediowych jest organizowany ___ na Dolnym Śląsku.",
            ["regularnie", "przypadkowo", "czasowo"], 0, "щороку → <b>regularnie</b> (регулярно)."),
]

# ── CZYTANIE — Zad III: вставити фрагменти (A–H) у текст про мікроапартаменти ──
# Приклад = фрагмент C (у пул не входить). Ключ (klucz): E,A,H,B,G,D,F.
_ZAD3 = MatchTask(
    section="czytanie",
    title="2024 Читання Zad III — встав фрагменти (мікроапартаменти)",
    intro=(
        "Прочитай текст про мікроапартаменти (крихітні квартири). Заповни пропуски 1–7 "
        "фрагментами A–G, що логічно й граматично продовжують речення."
    ),
    options=[
        "na przykład przy uniwersytetach",  # A
        "a konkretnie z Nowego Jorku",  # B
        "które planowały kupić mieszkanie",  # D
        "które aktualnie mają młodzi Polacy",  # E
        "gdzie metr kwadratowy kosztuje",  # F
        "a pierwsze mikrokawalerki powstały",  # G
        "więc zawsze będą zainteresowani",  # H
    ],
    prompts=[
        "1. …są odpowiedzią deweloperów na problemy lokalowe, ___",
        "2. …mikroapartamenty powstają w atrakcyjnych lokalizacjach, ___",
        "3. Młodzi chcą żyć szybko, blisko miasta, ___ takimi mieszkaniami.",
        "4. Idea dotarła do Europy i Azji z Ameryki, ___",
        "5. W Polsce moda pojawiła się na początku XX wieku, ___ we Wrocławiu.",
        "6. …ofertę kierowano do osób, ___ dla swojego dziecka – studenta.",
        "7. …oferty lokali blisko centrum Warszawy, ___ nawet 18 000 zł.",
    ],
    key=[3, 0, 6, 1, 5, 2, 4],  # E,A,H,B,G,D,F
    explain=[
        "«problemy lokalowe, ___» → E (які зараз мають молоді поляки).",
        "«atrakcyjnych lokalizacjach, ___» → A (напр. біля університетів).",
        "«blisko miasta, ___ takimi mieszkaniami» → H (тож завжди будуть зацікавлені).",
        "«z Ameryki, ___» → B (а конкретно з Нью-Йорка).",
        "«na początku XX wieku, ___ we Wrocławiu» → G (а перші мікрокавалерки постали).",
        "«do osób, ___ dla dziecka» → D (які планували купити житло).",
        "«blisko centrum Warszawy, ___ 18 000 zł» → F (де квадратний метр коштує).",
    ],
)

# ── CZYTANIE — Zad IV: зіставити заголовки з фрагментами (адопція пса) ──
# Приклад = фрагмент B (у пул не входить). Ключ (klucz): D,H,A,G,C,F,E.
_ZAD4 = MatchTask(
    section="czytanie",
    title="2024 Читання Zad IV — заголовок до тексту (адопція пса)",
    intro=(
        "«Co trzeba wiedzieć przed adopcją psa» — до кожного заголовка (1–7) добери "
        "правильний фрагмент A–G."
    ),
    options=[
        "Dorosłe zwierzę może zostać w mieszkaniu bez opiekuna, jeśli będziemy go tego "
        "systematycznie uczyć.",  # A
        "Opiekunowie psów są często zaskoczeni, że muszą poświęcić więcej czasu na sprzątanie.",  # C
        "Opieka nad zwierzęciem to nie tylko cena karmy, ale i wizyty u weterynarza czy "
        "regularne szczepienia.",  # D
        "Jeśli nie zgadzamy się na spanie w łóżku czy jedzenie przy stole, powinniśmy ustalić "
        "reguły; cała rodzina musi konsekwentnie wychowywać zwierzę.",  # E
        "Coraz więcej jest hoteli i pensjonatów, do których można przyjechać ze zwierzęciem "
        "i spędzić wakacje.",  # F
        "Wyjście na zewnątrz, gdy świeci słońce, to przyjemność; ale pies nie może zostać "
        "w domu tylko dlatego, że jest zimno lub pada deszcz.",  # G
        "Należy przemyśleć, jaki typ psa będzie pasował do rodziny i jej stylu życia.",  # H
    ],
    prompts=[
        "1. Obowiązki i wydatki",
        "2. Dopasowanie charakterów",
        "3. Samotne chwile",
        "4. Spacer również w niepogodę",
        "5. Porządek musi być",
        "6. Wspólny wypoczynek",
        "7. Szkolenie od pierwszych dni",
    ],
    key=[2, 6, 0, 5, 1, 4, 3],  # D,H,A,G,C,F,E
    explain=[
        "обов'язки й витрати → D (корм, ветеринар, щеплення).",
        "збіг характерів → H (обрати тип пса під стиль життя родини).",
        "самотні миті → A (доросле може лишатися саме, якщо привчати).",
        "прогулянка й у негоду → G (пес не лишається вдома через холод/дощ).",
        "порядок мусить бути → C (більше часу на прибирання).",
        "спільний відпочинок → F (готелі, куди можна з твариною).",
        "виховання з перших днів → E (від початку встановити правила)."
    ],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: підкресли форму (відмінювання) — MCQ. Текст про фільм «Chłopi». ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про екранізацію «Chłopi» Реймонта.",
            "Reżyserzy to twórcy animacji ___ „Twój Vincent”.",
            ["malarskiego", "malarskiej", "malarską"], 1, "animacji (якої?) → <b>malarskiej</b>."),
    MCQItem("gramatyka", "", "„Chłopi” nie są ___ filmem.",
            ["typowym", "typowego", "typowemu"], 0, "być + орудний → <b>typowym</b> filmem."),
    MCQItem("gramatyka", "", "W ___ realizacji wzięli udział nie tylko aktorzy…",
            ["jemu", "jego", "go"], 1, "присвійний (у його реалізації) → <b>jego</b>."),
    MCQItem("gramatyka", "", "…wzięli udział nie tylko ___, lecz także ponad 100 malarzy.",
            ["aktorzy", "aktorów", "aktorach"], 0, "підмет (наз. мн., чол.-ос.) → <b>aktorzy</b>."),
    MCQItem("gramatyka", "", "…malarzy, którzy pracowali nad każdym ___.",
            ["kadru", "kadr", "kadrem"], 2, "nad + орудний → <b>kadrem</b>."),
    MCQItem("gramatyka", "", "Całe dzieło składa się z ___ obrazów.",
            ["fascynujących", "fascynującymi", "fascynującym"], 0,
            "z + родовий множини → <b>fascynujących</b>."),
    MCQItem("gramatyka", "", "Fabuła jest podobna do ___ z powieści.",
            ["tą", "tę", "tej"], 2, "podobna do + родовий → <b>tej</b>."),
    MCQItem("gramatyka", "", "…opowiada nam o ___, Macieju Borynie.",
            ["ojca", "ojcu", "ojcem"], 1, "o + місцевий → <b>ojcu</b>."),
    MCQItem("gramatyka", "", "Jagna bardzo podoba się ___ obydwu.",
            ["ich", "im", "nim"], 1, "podobać się + давальний → <b>im</b>."),
    MCQItem("gramatyka", "", "Relacja doprowadza do wielu konfliktów we ___.",
            ["wsie", "wsią", "wsi"], 2, "we + місцевий → <b>wsi</b>."),
    # ── Zad III: ступенювання — MCQ. Текст про зимові види спорту. ──
    MCQItem("gramatyka", "Текст про нетипові зимові види спорту.",
            "Zima to ___ ze wszystkich pora roku (dla sportowców).",
            ["najtrudniej", "trudniejsza", "najtrudniejsza"], 2,
            "«ze wszystkich» → найвищий ступінь → <b>najtrudniejsza</b>."),
    MCQItem("gramatyka", "", "Można uprawiać ___ spotykane aktywności fizyczne.",
            ["rzadziej", "rzadkie", "rzadsze"], 0, "«___ spotykane» (рідше стрічувані) → <b>rzadziej</b>."),
    MCQItem("gramatyka", "", "Snowkiting rozwija się ___ niż myślicie.",
            ["szybsza", "szybciej", "najszybciej"], 1, "порівняння (niż) → <b>szybciej</b>."),
    MCQItem("gramatyka", "", "Snow polo każdego roku zyskuje coraz ___ fanów.",
            ["więcej", "najwięcej", "największych"], 0, "coraz ___ (дедалі більше) → <b>więcej</b>."),
    MCQItem("gramatyka", "", "Biathlon jest sportem ___ w Niemczech, Włoszech i Skandynawii.",
            ["popularnym", "popularniej", "popularnie"], 0, "jest + орудний (яким?) → <b>popularnym</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: dlaczego) → MCQ-per-gap ──
    MCQItem("gramatyka",
            "Текст про проблеми зі сном. Встав сполучник (зайве слово — <b>dlaczego</b>).",
            "Budzisz się często w nocy, ___ rano jesteś zmęczony?",
            ["a", "lecz", "który", "jeśli", "lub", "dlaczego"], 0,
            "зіставлення («а вранці») → <b>a</b>."),
    MCQItem("gramatyka", "", "Nie tylko ty masz taki kłopot, ___ także miliony ludzi.",
            ["a", "lecz", "który", "jeśli", "lub", "dlaczego"], 1, "«nie tylko… ___ także» → <b>lecz</b>."),
    MCQItem("gramatyka", "", "To wina stresu, ___ odczuwasz przez cały dzień.",
            ["a", "lecz", "który", "jeśli", "lub", "dlaczego"], 2, "означальне (який відчуваєш) → <b>który</b>."),
    MCQItem("gramatyka", "", "Nie zaśniesz, ___ wieczorem będziesz myślał o problemach.",
            ["a", "lecz", "który", "jeśli", "lub", "dlaczego"], 3, "умова («якщо») → <b>jeśli</b>."),
    MCQItem("gramatyka", "", "Weź ciepłą kąpiel ___ prysznic.",
            ["a", "lecz", "który", "jeśli", "lub", "dlaczego"], 4, "вибір («або») → <b>lub</b>."),
    # ── Zad VII: підкресли форму (вид і способи) — MCQ. Діалог чоловік/дружина. ──
    MCQItem("gramatyka", "Діалог: чоловікові пропонують підвищення в столиці.",
            "„___ swoją żonę, czy chciałaby zamieszkać w stolicy” – powiedział szef.",
            ["Zapytaj", "Zapytałbym", "Pytajmy"], 0, "наказ до «ty» → <b>Zapytaj</b>."),
    MCQItem("gramatyka", "", "…czy ___ zamieszkać w stolicy?",
            ["chcielibyście", "chciałabyś", "chciałaby"], 2, "умовний, 3 ос. одн. жін. (żona) → <b>chciałaby</b>."),
    MCQItem("gramatyka", "", "Pieniądze oczywiście by się nam ___.",
            ["przydałyby", "przydały", "przydawały"], 1, "«by się ___» — розділений умовний → <b>przydały</b>."),
    MCQItem("gramatyka", "", "Może na razie ___ się do Warszawy sam?",
            ["przeprowadziłby", "przeprowadziłbyś", "przeprowadzałbyś"], 1,
            "умовний, 2 ос. одн. (ty) → <b>przeprowadziłbyś</b>."),
    MCQItem("gramatyka", "", "Sam? Nie ___, proszę!",
            ["zażartuj", "żartowałbyś", "żartuj"], 2, "наказ (недок.) до «ty» → <b>żartuj</b>."),
    MCQItem("gramatyka", "", "Całymi dniami ___ za tobą.",
            ["tęsknij", "tęskniłbym", "zatęskniłbym"], 1, "умовний, 1 ос. одн. → <b>tęskniłbym</b>."),
    MCQItem("gramatyka", "", "Przecież wszystkie weekendy ___ razem.",
            ["spędzalibyśmy", "spędzajmy", "spędzilibyśmy"], 0, "умовний недок., 1 ос. мн. → <b>spędzalibyśmy</b>."),
    MCQItem("gramatyka", "", "Proszę cię, ___ razem!",
            ["pojechalibyśmy", "pojedźmy", "jeździmy"], 1, "спонукання «нумо» (1 ос. мн. наказ) → <b>pojedźmy</b>."),
    MCQItem("gramatyka", "", "Może na razie niech firma ___ ci służbowy pokój.",
            ["dałaby", "da", "dawałaby"], 1, "«niech ___» + докон. → <b>da</b>."),
    MCQItem("gramatyka", "", "___ z nim o tym jutro.",
            ["Porozmawiaj", "Rozmawiaj", "Rozmawiałbyś"], 0, "наказ докон. (одна розмова) → <b>Porozmawiaj</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: bez) → MCQ-per-gap ──
    MCQItem("gramatyka",
            "Текст про проєктування саду. Встав прийменник (зайве слово — <b>bez</b>).",
            "Plany ogrodów to nie tylko rośliny ___ domu.",
            ["wokół", "z", "na", "w", "bez"], 0, "навколо дому → <b>wokół</b> (+ родовий)."),
    MCQItem("gramatyka", "", "Ogrody mają łączyć się ___ budynkiem i otoczeniem.",
            ["wokół", "z", "na", "w", "bez"], 1, "łączyć się z + орудний → <b>z</b>."),
    MCQItem("gramatyka", "", "…służyć wypoczynkowi ___ świeżym powietrzu.",
            ["wokół", "z", "na", "w", "bez"], 2, "стійке «na świeżym powietrzu» → <b>na</b>."),
    MCQItem("gramatyka", "", "…będą się mogły bawić ___ bezpieczny sposób.",
            ["wokół", "z", "na", "w", "bez"], 3, "«w ___ sposób» → <b>w</b> bezpieczny sposób."),
    MCQItem("gramatyka", "", "…zbudujemy im domek ___ drzewie.",
            ["wokół", "z", "na", "w", "bez"], 2, "na + місцевий (на дереві) → <b>na</b>."),
]

# ── Zad IV: вписати форми дієслів (тепер./майб.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2024 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або майб. час). Текст про підготовку "
           "до матури.\n\n<i>Приклад: Egzamin <b>ma</b> (mieć) wpływ na przyszłość.</i>"),
    prompts=[
        "1. Młodzi ludzie intensywnie ___ (zastanawiać się), jak się przygotować.",
        "2. Często oni ___ (prosić) o radę nauczycieli.",
        "3. …albo ___ (kupować) książki z testami.",
        "4. Moja córka ___ (chcieć) zapisać się na kurs.",
        "5. Jednak ja ___ (tłumaczyć) jej i innym uczniom.",
        "6. Przez najbliższe miesiące ___ (wy – móc) dobrze się przygotowywać.",
        "7. Ta strategia na pewno ___ (zmotywować) was.",
        "8. …___ (zapewnić) wam poczucie spokoju.",
        "9. W maju nikt nie ___ (musieć) uczyć się w stresie.",
        "10. Na maturę ___ (wy – przyjść) dobrze przygotowani.",
    ],
    accepted=[
        ["zastanawiają się"], ["proszą"], ["kupują"], ["chce"], ["tłumaczę"],
        ["będziecie mogli"], ["zmotywuje"], ["zapewni"], ["będzie musiał"], ["przyjdziecie"],
    ],
    explain=[
        "тепер., 3 ос. мн. → <b>zastanawiają się</b>.",
        "тепер., 3 ос. мн. (oni) → <b>proszą</b>.",
        "тепер., 3 ос. мн. → <b>kupują</b>.",
        "тепер., 3 ос. одн. (ona) → <b>chce</b>.",
        "тепер., 1 ос. одн. (ja) → <b>tłumaczę</b>.",
        "майб., 2 ос. мн. (wy) → <b>będziecie mogli</b>.",
        "майб. докон., 3 ос. одн. → <b>zmotywuje</b>.",
        "майб. докон., 3 ос. одн. → <b>zapewni</b>.",
        "майб., 3 ос. одн. (nikt) → <b>będzie musiał</b>.",
        "майб. докон., 2 ос. мн. (wy) → <b>przyjdziecie</b>.",
    ],
)

# ── Zad V: постав питання до підкресленого → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2024 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: Staś był u «brata» → U kogo?</i>"),
    prompts=[
        "Robert zaraził się «grypą» od Stefana.",
        "Długo czekałem pod szkołą «na mamę».",
        "Basia studiuje medycynę «piąty» rok.",
        "Babcia cieszy się «z wizyty wnuków».",
        "Nauczyciel sprawdzi testy «na początku przyszłego tygodnia».",
    ],
    accepted=[["czym"], ["na kogo"], ["który"], ["z czego"], ["kiedy"]],
    explain=[
        "grypą — орудний (чим?) → <b>Czym?</b>",
        "na mamę — na + знах. → <b>Na kogo?</b>",
        "piąty (rok) — порядковий → <b>Który?</b>",
        "z wizyty — z + род. → <b>Z czego?</b>",
        "час → <b>Kiedy?</b>",
    ],
)

# ── Zad VI: трансформація речення → open (AI-оцінка) ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2024 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «Mój tata świetnie mówi po francusku.» (zna) → "
           "Mój tata świetnie zna francuski.</i>\n\n📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Mateusz z zainteresowaniem przyglądał się kolorowym wystawom sklepów.",
        "Proszę ustawić ławki wzdłuż tamtej żółtej ściany.",
        "Uczniów z mojej klasy nie stresuje egzamin pisemny.",
        "Kto jest autorem tego opowiadania?",
        "Mój syn jest starszym programistą.",
    ],
    words=["patrzył", "pod", "nie boją się", "napisał", "jako"],
    models=[
        ["Mateusz z zainteresowaniem patrzył na kolorowe wystawy sklepów."],
        ["Proszę ustawić ławki pod tamtą żółtą ścianą."],
        ["Uczniowie z mojej klasy nie boją się egzaminu pisemnego."],
        ["Kto napisał to opowiadanie?"],
        ["Mój syn pracuje jako starszy programista."],
    ],
)

EXAM = Exam(
    id="2024-02",
    label="Реальний іспит лютий-2024 (офіц.)",
    kind="real",
    year=2024,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
