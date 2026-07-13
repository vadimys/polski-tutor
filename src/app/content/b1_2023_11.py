"""РЕАЛЬНИЙ минулий іспит B1 — листопад 2023 (certyfikatpolski.pl).

Джерело: 2023_11_18_19_B1_arkusz + …_transkrypcja.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН ключ
звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad); аудіювання — у listening.py.
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

# ── CZYTANIE — Zad I. Ключ: a,c,c,b,b. ──────────────────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Na zagraniczne wakacje planuje wyjechać tego lata tylko 18 proc. Polaków. Wypoczynek "
            "z biurami podróży kosztuje średnio 3,5 tys. zł za osobę – rok temu podobne oferty "
            "były ponad 500 zł tańsze, a biura oferowały wiele promocji.",
            "Z tego tekstu wynika, że w tym roku:",
            ["wakacje poza Polską nie są popularne",
             "ponad połowa Polaków skorzysta z ofert biura podróży",
             "biura podróży obniżyły ceny wyjazdów za granicę"], 0,
            "лише 18% планують закордон → непопулярні. Ціни зросли (не знизились)."),
    MCQItem("czytanie",
            "W Gdyni mieszkańcy cieszą się ścieżkami rowerowymi, czystym powietrzem i "
            "nowoczesnością. Dobra komunikacja miejska ułatwia życie. Jest wiele sklepów, punktów "
            "usługowych, zakładów pracy, a także najlepsze w regionie szkoły podstawowe.",
            "Z tego tekstu wynika, że w Gdyni:",
            ["mieszkańcy wolą jeździć do pracy rowerami",
             "potrzebne są inwestycje w komunikację miejską",
             "dzieci mają szansę na dobre wykształcenie"], 2,
            "«najlepsze w regionie szkoły» → діти можуть добре навчатися."),
    MCQItem("czytanie",
            "Catering dietetyczny to najlepszy wybór dla ludzi zapracowanych, którzy chcą jeść "
            "zdrowo, ale nie mogą spędzać wielu godzin w kuchni. Zestawy posiłków przygotowują "
            "dietetycy.",
            "Z tego tekstu wynika, że:",
            ["firmy płacą pracownikom za catering", "w cateringu dietetycznym nie ma śniadania",
             "niektórym brakuje czasu na gotowanie w domu"], 2,
            "«nie mogą spędzać godzin w kuchni» → декому бракує часу на готування."),
    MCQItem("czytanie",
            "Zbliża się 16. edycja Nocy Teatrów – wydarzenie, podczas którego mieszkańcy Krakowa "
            "i turyści mogą zupełnie za darmo zobaczyć przedstawienia krakowskich teatrów. "
            "Odbywają się też spotkania z aktorami i prezentacje multimedialne.",
            "Z tego tekstu wynika, że:",
            ["aktorzy będą udzielać wywiadów krakowskim mediom",
             "nie trzeba płacić za oglądanie przedstawień teatralnych",
             "spektakle są prezentowane przez teatry z całej Polski"], 1,
            "«zupełnie za darmo» → не треба платити. Театри — краківські."),
    MCQItem("czytanie",
            "Firma „Sokołów” zaprasza rodziców i dzieci do Akademii Sokolika, w której maluchy "
            "poprzez zabawę odkrywają zasady zdrowego stylu życia, poznają przepisy na nowe dania "
            "i samodzielnie je gotują.",
            "Z tego tekstu wynika, że:",
            ["dzieci będą przygotowywać dania, które dobrze znają i lubią",
             "firma „Sokołów” proponuje zajęcia edukacyjne połączone z zabawą",
             "opiekunowie dzieci nie mogą uczestniczyć w zajęciach"], 1,
            "«poprzez zabawę odkrywać zasady» → навчання + гра. Страви НОВІ; батьки залучені."),
    # ── Zad II: TAK/NIE — «Projekt RESQL». Ключ: N,T,T,N,T,N. ────────────
    MCQItem("czytanie",
            "TEKСТ «RESQL»: у школах дедалі частіше агресія й кібербулінг (який важче помітити). "
            "Раніше учні легко знаходили безпечне місце (вийшов зі школи — зачинив двері), тепер "
            "ні — багато часу в соцмережах. Лише ~20% молоді шукає допомоги. Науковці зі "
            "столичного ВНЗ створили проєкт RESQL, працюючи з гімназистами, ліцеїстами й "
            "вчителями. RESQL дозволяє учневі АНОНІМНО повідомити школу, що він жертва чи свідок "
            "насильства (спілкування з педагогом — у застосунку). Автори також дають набори "
            "інтервенцій і СЦЕНАРІЇ УРОКІВ для вчителів; матеріали протестовані. Роботу завершено, "
            "від червня застосунок доступний усім.",
            "TAK/NIE: Cyberprzemoc jest rodzajem agresji najłatwiejszym do rozpoznania.",
            ["TAK", "NIE"], 1, "НІ — кібербулінг ВАЖЧЕ помітити."),
    MCQItem("czytanie", "",
            "TAK/NIE: Obecnie jest coraz mniej miejsc, w których uczniowie czują się bezpieczni.",
            ["TAK", "NIE"], 0, "ТАК — раніше зачиняли двері школи; тепер соцмережі скрізь."),
    MCQItem("czytanie", "",
            "TAK/NIE: W powstaniu programu RESQL brali udział wykładowcy, nauczyciele i uczniowie.",
            ["TAK", "NIE"], 0, "ТАК — науковці працювали з учнями й учителями."),
    MCQItem("czytanie", "",
            "TAK/NIE: Aplikacja RESQL automatycznie informuje nauczycieli i rodziców o problemach.",
            ["TAK", "NIE"], 1, "НІ — учень САМ анонімно повідомляє (не автоматично; батьків не згадано)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Program RESQL oferuje także gotowe propozycje lekcji dla nauczycieli.",
            ["TAK", "NIE"], 0, "ТАК — сценарії уроків про агресію."),
    MCQItem("czytanie", "",
            "TAK/NIE: Aplikacja jest jeszcze testowana na polskich uniwersytetach.",
            ["TAK", "NIE"], 1, "НІ — роботу завершено, від червня доступна всім."),
    # ── Zad V: обери найкраще слово («Ile jest pór roku»). ──────────────
    MCQItem("czytanie", "Текст про пори року. Обери найкраще слово.",
            "Wiele osób uważa, że w Polsce ___ cztery podstawowe pory roku.",
            ["są", "znajdują się", "pokazują się"], 0, "є чотири пори → <b>są</b>."),
    MCQItem("czytanie", "", "Skąd ta ___? Można ich wymienić aż sześć lub osiem!",
            ["błąd", "różnica", "opinia"], 1, "звідки ця різниця → <b>różnica</b>."),
    MCQItem("czytanie", "", "Standardowy podział nie opisuje wszystkich zmian w ___.",
            ["miesiącu", "kalendarzu", "pogodzie"], 2, "зміни в погоді → <b>pogodzie</b>."),
    MCQItem("czytanie", "", "…przedwiośnie, czyli ___ między końcem zimy i początkiem wiosny.",
            ["data", "czas", "wiek"], 1, "час між → <b>czas</b>."),
    MCQItem("czytanie", "", "…co razem ___ aż osiem pór roku!",
            ["dodaje", "daje", "pokazuje"], 1, "разом дає → <b>daje</b>."),
    MCQItem("czytanie", "", "Zima zaczyna się, gdy temperatura jest równa zeru lub ___ poniżej 0°C.",
            ["pada", "spada", "rośnie"], 1, "спадає нижче → <b>spada</b>."),
    MCQItem("czytanie", "", "Dzięki ___ od pogody mówimy o meteorologicznych porach roku.",
            ["specjalistom", "pracownikom", "prezenterom"], 0, "завдяки фахівцям → <b>specjalistom</b>."),
    MCQItem("czytanie", "", "…czy już mamy wiosnę, czy jeszcze ___ trwa przedwiośnie.",
            ["długo", "ciągle", "potem"], 1, "чи все ще триває → <b>ciągle</b>."),
    MCQItem("czytanie", "", "Początek wiosny bywa w lutym lub marcu, ale ___ w kwietniu.",
            ["nigdy", "zawsze", "regularnie"], 0, "але ніколи в квітні → <b>nigdy</b>."),
    MCQItem("czytanie", "", "Pory roku mogą zaniknąć ze względu na ___ klimatu.",
            ["rodzaje", "typy", "zmiany"], 2, "зміни клімату → <b>zmiany</b>."),
]

# ── Zad III: вставити фрагменти (скорочення тижня праці). Приклад=C. Ключ: A,E,B,F,D,G,H. ──
_ZAD3 = MatchTask(
    section="czytanie",
    title="2023-11 Читання Zad III — встав фрагменти (чотириденний тиждень)",
    intro="Прочитай текст про скорочення робочого тижня. Заповни пропуски 1–7 фрагментами A–H.",
    options=[
        "takie rozwiązanie było nierealne",  # A
        "jak ludzie zareagują",  # B
        "że skrócenie tygodnia pracy",  # D
        "testuje się możliwości wykonywania pracy",  # E
        "ale też zdrowie badanych",  # F
        "że mieli większą ochotę",  # G
        "bo wcześniej w wielu miejscach",  # H
    ],
    prompts=[
        "1. Jeszcze kilkanaście lat temu ___, ale ostatnio coraz więcej krajów chce to przetestować.",
        "2. To największy eksperyment, w którym ___ w czterodniowym tygodniu.",
        "3. Przeanalizujemy, ___ na dodatkowy dzień wolny.",
        "4. Naukowcy skontrolują nie tylko zadowolenie z pracy, ___, stres i inne aspekty.",
        "5. Wyniki pokazały, ___ było korzystne dla pracowników.",
        "6. Czuli się lepiej. To spowodowało, ___ na inne czynności: ćwiczenia, hobby.",
        "7. Wydłużenie weekendu to nic nowego, ___ jedynym dniem wolnym była niedziela.",
    ],
    key=[0, 3, 1, 4, 2, 5, 6],  # A,E,B,F,D,G,H
    explain=[
        "«kilkanaście lat temu ___» → A (таке рішення було нереальним).",
        "«w którym ___» → E (випробовують можливості роботи).",
        "«Przeanalizujemy, ___» → B (як люди відреагують).",
        "«nie tylko zadowolenie, ___» → F (але й здоров'я досліджуваних).",
        "«pokazały, ___ było korzystne» → D (що скорочення тижня).",
        "«spowodowało, ___» → G (що мали більше охоти).",
        "«nic nowego, ___» → H (бо раніше в багатьох місцях)."],
)

# ── Zad IV: заголовки↔тексти (нетипові ресторани). Приклад=B. Ключ: G,E,A,H,C,D,F. ──
_ZAD4 = MatchTask(
    section="czytanie",
    title="2023-11 Читання Zad IV — заголовок↔ресторан (нетипові ресторани)",
    intro="«Nietypowe restauracje w Warszawie» — до кожного заголовка (1–7) добери фрагмент A–H.",
    options=[
        "Jack's przypomina rockowy klub z oglądaniem filmu w fotelach samochodowych – przyjdź "
        "na burgera i obejrzyj dobry film.",  # A
        "Restauracja Shabu-shabu: częścią stołu jest garnek, do którego goście wlewają bulion "
        "i dodają mięso, warzywa czy grzyby.",  # C
        "Masz dość czekania na piwo? W The Alchemist nalej je sobie sam – dzięki specjalnej "
        "ścianie z 8 kranami.",  # D
        "Pizza, pasta, wino: pierwsza w Polsce restauracja z pizzą, którą sami komponujemy "
        "i zamawiamy za pomocą tabletu.",  # E
        "W M. Cafe mieszkają koty; w ich towarzystwie wypijemy kawę i zjemy wegetariańską "
        "kanapkę lub wegańskie potrawy.",  # F
        "Dobro & Dobro Cafe to najmniejsza kawiarnia w Polsce, założona przez małżeństwo "
        "z Ukrainy – smaczna kawa i rozmowa z właścicielami.",  # G
        "W Dine in dominują węgierskie potrawy, ale goście nie widzą, co jedzą – jest bardzo "
        "mało światła, a szef nie zdradza menu.",  # H
    ],
    prompts=[
        "1. Niewiele miejsca, dużo serdeczności",
        "2. Technologia i kuchnia",
        "3. Sala kinowa w środku restauracji",
        "4. Kolacja w ciemności",
        "5. Ugotuj to sam",
        "6. Tu szklanki zawsze są pełne",
        "7. W nietypowym towarzystwie i bez mięsa",
    ],
    key=[5, 3, 0, 6, 1, 2, 4],  # G,E,A,H,C,D,F
    explain=[
        "мало місця, багато сердечності → G (найменша кав'ярня, подружжя з України).",
        "технологія і кухня → E (замовляєш піцу через планшет).",
        "кінозал у ресторані → A (Jack's — фільм у авто-кріслах).",
        "вечеря в темряві → H (Dine in — майже нема світла).",
        "приготуй сам → C (Shabu-shabu — казанок на столі).",
        "тут склянки завжди повні → D (The Alchemist — стіна з кранами).",
        "у нетиповому товаристві й без м'яса → F (M. Cafe — коти, вегетаріанське)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: відмінювання. Текст про «U króla Maciusia» (POLIN). ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про дитячий простір «U króla Maciusia» в музеї POLIN.",
            "Tolerancja i odpowiedzialność to w ___ miejscu najważniejsze wartości.",
            ["tym", "tego", "temu"], 0, "w + місцевий → <b>tym</b> miejscu."),
    MCQItem("gramatyka", "", "…więc ___ będą się tu czuć komfortowo.",
            ["rodzinie", "rodziną", "rodziny"], 2, "підмет (наз. мн.) → <b>rodziny</b>."),
    MCQItem("gramatyka", "", "___ słowa – „Ważne, co myślisz” – są główną zasadą.",
            ["Go", "Niego", "Jego"], 2, "присвійний (його слова) → <b>Jego</b>."),
    MCQItem("gramatyka", "", "…są główną ___ „U króla Maciusia”.",
            ["zasadą", "zasadę", "zasady"], 0, "być + орудний (є головним принципом) → <b>zasadą</b>."),
    MCQItem("gramatyka", "", "Zajęcia prowadzą nauczyciele oraz ___.",
            ["artyści", "artysty", "artyście"], 0, "наз. мн. (та митці) → <b>artyści</b>."),
    MCQItem("gramatyka", "", "Chętnie spędzają z ___ czas.",
            ["nich", "nim", "nimi"], 2, "z + орудний (з ними) → <b>nimi</b>."),
    MCQItem("gramatyka", "", "Za pomocą specjalnych ___ maluchy odkrywają świat.",
            ["materiały", "materiałów", "materiałach"], 1, "za pomocą + родовий мн. → <b>materiałów</b>."),
    MCQItem("gramatyka", "", "…odkrywają świat ___ kultury i tradycji.",
            ["żydowskiej", "żydowskiego", "żydowską"], 0, "родовий одн. жін. (єврейської культури) → <b>żydowskiej</b>."),
    MCQItem("gramatyka", "", "Zapraszamy do ___ „U króla Maciusia” w weekendy.",
            ["zabawy", "zabawą", "zabawie"], 0, "do + родовий → <b>zabawy</b>."),
    MCQItem("gramatyka", "", "Wejście jest całkowicie ___.",
            ["bezpłatne", "bezpłatnym", "bezpłatny"], 0, "wejście jest ___ (наз. ніяк.) → <b>bezpłatne</b>."),
    # ── Zad III: ступенювання. Текст про подорож авто vs літак. ──
    MCQItem("gramatyka", "Текст: чому подорожувати авто, а не літаком.",
            "Gdy jedziesz samochodem, masz ___ wolności niż podczas lotu.",
            ["dużo", "najwięcej", "więcej"], 2, "порівняння (niż) → <b>więcej</b>."),
    MCQItem("gramatyka", "", "Przejazd samochodem może okazać się ___, jeśli jedziemy w grupie.",
            ["tańszy", "tańsze", "taniej"], 0, "вищий ступ. (przejazd — чол. рід) → <b>tańszy</b>."),
    MCQItem("gramatyka", "", "Coraz ___ staje się obecnie nocowanie w aucie.",
            ["modniejsze", "modne", "modniej"], 0, "coraz + вищий ступ. (nocowanie — ніяк.) → <b>modniejsze</b>."),
    MCQItem("gramatyka", "", "___ samochodem osobowym jest w tym wypadku camper.",
            ["Najwygodniej", "Najwygodniejszym", "Najwygodniejszy"], 1, "орудний (яким авто?) → <b>Najwygodniejszym</b>."),
    MCQItem("gramatyka", "", "Warto jak ___ zaplanować trasę.",
            ["dokładniej", "dokładnie", "najdokładniej"], 2, "«jak ___» → найвищий ступ. → <b>najdokładniej</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: dlaczego). ──
    MCQItem("gramatyka", "Текст про планування майбутнього. Встав сполучник (зайве слово — <b>dlaczego</b>).",
            "Nie umiem zaplanować przyszłości, ___ nikt nas w szkole nie uczył organizacji.",
            ["więc", "bo", "dlaczego", "ale", "że", "które"], 1, "причина → <b>bo</b>."),
    MCQItem("gramatyka", "", "Zajmuję się mnóstwem spraw, ___ nie zawsze są tego warte.",
            ["więc", "bo", "dlaczego", "ale", "że", "które"], 5, "означальне → <b>które</b> (які)."),
    MCQItem("gramatyka", "", "Wiem, ___ praca jest ważna,",
            ["więc", "bo", "dlaczego", "ale", "że", "które"], 4, "«wiem, ___» → <b>że</b>."),
    MCQItem("gramatyka", "", "…praca jest ważna, ___ chciałabym realizować też marzenia.",
            ["więc", "bo", "dlaczego", "ale", "że", "które"], 3, "протиставлення → <b>ale</b>."),
    MCQItem("gramatyka", "", "Uwielbiam gotować, ___ zapiszę się na kurs kulinarny.",
            ["więc", "bo", "dlaczego", "ale", "że", "które"], 0, "наслідок → <b>więc</b> (тому)."),
    # ── Zad VII: вид/способи. Діалог бабусі з Krzysztofem про вакації. ──
    MCQItem("gramatyka", "Діалог: бабуся радить Krzysztofowi щодо сімейних вакацій.",
            "Halinka powiedziała, żebym ich już nie ___.",
            ["obudziłbym", "budził", "budziliby"], 1, "«żebym nie ___» недок. → <b>budził</b>."),
    MCQItem("gramatyka", "", "Nie wiem, ___ się głębiej nad tym zastanowić.",
            ["musiałbym", "musiałaby", "musielibyście"], 0, "умовний, 1 ос. одн. → <b>musiałbym</b>."),
    MCQItem("gramatyka", "", "Kasia pewnie ___ wakacje nad morzem.",
            ["proponowałabym", "zaproponuj", "zaproponowałaby"], 2, "умовний, 3 ос. одн. жін. → <b>zaproponowałaby</b>."),
    MCQItem("gramatyka", "", "Jaś chyba by ___ jakąś wyprawę rowerową.",
            ["wolałby", "wolał", "woli"], 1, "«by ___» + -ł → <b>wolał</b> (розділений умовний)."),
    MCQItem("gramatyka", "", "„___ w tym roku sami. Ja zostanę w domu” – mówi Halinka.",
            ["Jedźcie", "Jechalibyście", "Pojechaliby"], 0, "наказ до «wy» → <b>Jedźcie</b>."),
    MCQItem("gramatyka", "", "Gdybyście częściej ___ jej wybrać miejsce…",
            ["pozwoli", "pozwalali", "pozwalalibyście"], 1, "«gdybyście ___» форма на -li → <b>pozwalali</b>."),
    MCQItem("gramatyka", "", "…to ___ inaczej.",
            ["byłaby", "byliby", "byłoby"], 2, "умовний, ніяк. → <b>byłoby</b>."),
    MCQItem("gramatyka", "", "Może w tym roku niech ona sama ___, gdzie spędzicie wakacje.",
            ["zdecyduje", "zdecyduj", "zdecydowałaby"], 0, "«niech ___» докон. → <b>zdecyduje</b>."),
    MCQItem("gramatyka", "", "Nie ___! Halinka dobrze cię zna.",
            ["zmartwiłby się", "zmartwi się", "martw się"], 2, "наказ до «ty» → <b>martw się</b> (Nie martw się!)."),
    MCQItem("gramatyka", "", "___ jej tylko trochę czasu do namysłu!",
            ["Dałbyś", "Daj", "Dawaj"], 1, "наказ докон. до «ty» → <b>Daj</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: przy). Текст про Targi Książki. ──
    MCQItem("gramatyka", "Текст про Ярмарок книги. Встав прийменник (зайве слово — <b>przy</b>).",
            "___ półkach stały poradniki, albumy i powieści po ukraińsku.",
            ["dla", "przed", "na", "przy", "wśród", "przez"], 2, "na + місцевий (на полицях) → <b>Na</b>."),
    MCQItem("gramatyka", "", "___ cztery dni odbywały się spotkania z autorami.",
            ["dla", "przed", "na", "przy", "wśród", "przez"], 5, "тривалість → <b>przez</b> cztery dni."),
    MCQItem("gramatyka", "", "…był też kącik gier i zabaw ___ dzieci.",
            ["dla", "przed", "na", "przy", "wśród", "przez"], 0, "dla + родовий (для дітей) → <b>dla</b>."),
    MCQItem("gramatyka", "", "Przyjechało ponad 20 osób z Ukrainy, ___ nich Jurij Andruchowycz.",
            ["dla", "przed", "na", "przy", "wśród", "przez"], 4, "wśród + родовий (серед них) → <b>wśród</b>."),
    MCQItem("gramatyka", "", "___ publicznością wystąpił młodzieżowy zespół z Charkowa.",
            ["dla", "przed", "na", "przy", "wśród", "przez"], 1, "przed + орудний (перед публікою) → <b>Przed</b>."),
]

# ── Zad IV: вписати форми (тепер./майб.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2023-11 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або майбутній час). Текст про зміну "
           "клімату.\n\n<i>Приклад: <b>zgadzają się</b> (zgadzać się) wszystkie organizacje.</i>"),
    prompts=[
        "1. Jaki świat ___ (my – zostawić) za jakiś czas naszym dzieciom?",
        "2. Już dziś tempo zmian ___ (decydować) o naszym życiu.",
        "3. W przyszłości coraz częściej ___ (zdarzać się): huragany, burze, śnieżyce.",
        "4. Nie wiemy, jak różne państwa wtedy ___ (zareagować).",
        "5. Czy politycy wreszcie ___ (zrozumieć), że konieczne są działania?",
        "6. Może już wkrótce ___ (my – musieć) bardzo oszczędzać elektryczność.",
        "7. Już teraz fale upałów i susze ___ (niszczyć) rolnictwo.",
        "8. Poziom wody w rzekach cały czas ___ (spadać).",
        "9. W wielu miejscach ___ (brakować) wody do picia.",
        "10. Wciąż za mało ___ (my – myśleć) o tym, jak dbać o środowisko.",
    ],
    accepted=[
        ["zostawimy"], ["decyduje"], ["będą się zdarzały", "będą się zdarzać"], ["zareagują"],
        ["zrozumieją"], ["będziemy musieli"], ["niszczą"], ["spada"], ["brakuje"], ["myślimy"],
    ],
    explain=[
        "майб., 1 ос. мн. → <b>zostawimy</b>.",
        "тепер., 3 ос. одн. → <b>decyduje</b>.",
        "майб., 3 ос. мн. → <b>będą się zdarzały</b> (або будуть się zdarzać).",
        "майб. докон., 3 ос. мн. → <b>zareagują</b>.",
        "майб. докон., 3 ос. мн. → <b>zrozumieją</b>.",
        "майб., 1 ос. мн. → <b>będziemy musieli</b>.",
        "тепер., 3 ос. мн. → <b>niszczą</b>.",
        "тепер., 3 ос. одн. → <b>spada</b>.",
        "тепер., 3 ос. одн. (безос.) → <b>brakuje</b>.",
        "тепер., 1 ос. мн. → <b>myślimy</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2023-11 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: pracuje «w szpitalu» → Gdzie?</i>"),
    prompts=[
        "Magda najbardziej lubi «mleczną» czekoladę.",
        "Byłam wczoraj w kinie «z siostrą Adama».",
        "Anna spotkała na spacerze «swoją nauczycielkę».",
        "Chłopcy marzą «o nocnej wyprawie do lasu».",
        "«Za dwa tygodnie» zaczynają się egzaminy maturalne.",
    ],
    accepted=[
        ["jaką"], ["z kim"], ["kogo"], ["o czym"], ["kiedy", "za ile tygodni", "za ile czasu"],
    ],
    explain=[
        "«jaką czekoladę» → <b>Jaką?</b>",
        "з людьми → <b>Z kim?</b>",
        "spotkać + знах. → <b>Kogo?</b>",
        "marzyć o + місц. → <b>O czym?</b>",
        "час → <b>Kiedy?</b> (Za ile tygodni?)",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2023-11 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «ładniejsza niż tamta» (od) → ładniejsza od tamtej.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Anna ma na sobie strój kąpielowy.",
        "Wczoraj pojechaliśmy na wycieczkę rowerową do lasu.",
        "Hobby Dawida to gry komputerowe.",
        "Jej mąż jest dyrektorem w dużej firmie energetycznej.",
        "Czy masz jeszcze stary adres mailowy?",
    ],
    words=["ubrana", "byliśmy", "interesuje się", "kieruje", "korzystać"],
    models=[
        ["Anna jest ubrana w strój kąpielowy."],
        ["Wczoraj byliśmy na wycieczce rowerowej w lesie."],
        ["Dawid interesuje się grami komputerowymi."],
        ["Jej mąż kieruje dużą firmą energetyczną."],
        ["Czy korzystasz jeszcze ze starego adresu mailowego?"],
    ],
)

EXAM = Exam(
    id="2023-11",
    label="Реальний іспит листопад-2023 (офіц.)",
    kind="real",
    year=2023,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
