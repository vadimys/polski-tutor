"""РЕАЛЬНИЙ минулий іспит B1 — квітень 2024 (certyfikatpolski.pl).

Джерело: 20-21.04.2024-B1_arkusz + …_transkrypcja.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН
ключ звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad):
- Czytanie: Zad I (a/b/c ×5) + Zad II (TAK/NIE ×6) + Zad V (вибір слова ×10) — MCQ;
  Zad III/IV — matching.
- Gramatyka: I(×10)+II(×5)+III(×5)+VII(×10)+VIII(×5) MCQ; IV(×10)+V(×5) free-fill; VI(×5) open.
Далі: Słuchanie (5 Zad).
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

# ── CZYTANIE — Zad I (a/b/c) ─────────────────────────────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "W kursie surfowania mogą uczestniczyć dorośli, młodzież i dzieci. Najpierw trzeba "
            "poznać teorię związaną m.in. z bezpieczeństwem w wodzie. To nie sport dla bogatych – "
            "na początku można wypożyczyć deskę surfingową.",
            "Z tego tekstu wynika, że:",
            ["trzeba zainwestować dużo pieniędzy, żeby uprawiać surfing",
             "na kursie dowiemy się również, jak chronić swoje życie i zdrowie",
             "osoby zainteresowane muszą najpierw kupić specjalny sprzęt"], 1,
            "«teorię… z bezpieczeństwem w wodzie» → як убезпечити життя/здоров'я. Дошку можна "
            "ВЗЯТИ НАПРОКАТ (не купувати); не для багатих."),
    MCQItem("czytanie",
            "Trnawa – jedno z najważniejszych miast Słowacji, ok. 56 km od Bratysławy. Jest tam "
            "wiele zabytków przyrodniczych i kulturowych; największa atrakcja to park Dolna Krupa. "
            "Według legendy mieszkał tam Beethoven i prawdopodobnie napisał sonatę Księżycową.",
            "Z tego tekstu wynika, że:",
            ["Trnawa jest największym – po Bratysławie – słowackim miastem",
             "turyści, którzy lubią naturę, nie będą się nudzili w Trnawie",
             "słynna sonata Beethovena powstała w Bratysławie"], 1,
            "«wiele zabytków przyrodniczych, park» → любителям природи не буде нудно. Соната — "
            "у Тнаві (за легендою), не в Братиславі."),
    MCQItem("czytanie",
            "Dzieła Banksy'ego można zobaczyć od 14 grudnia na krakowskim Kazimierzu, gdzie Hazis "
            "Vardar, dyrektor europejskich teatrów, otworzył muzeum. Słynny grafficiarz jest "
            "z Wielkiej Brytanii – tam w latach 90. pojawiły się jego prace.",
            "Z tego tekstu wynika, że:",
            ["pierwsze graffiti Banksy'ego powstały w Krakowie",
             "nową wystawę artysty można oglądać w Anglii",
             "Hazis Vardar kieruje instytucjami kulturalnymi w Europie"], 2,
            "«dyrektor europejskich teatrów» → керує культурними закладами. Перші графіті — "
            "у Британії; виставка — у Кракові."),
    MCQItem("czytanie",
            "Sprzedam willę pod Warszawą, przypominającą rezydencje z Hollywood. Ma dwa baseny, "
            "lądowisko dla helikopterów, prywatną ścieżkę do biegania i duży taras. Dom jest "
            "komfortowy i wyposażony w najnowsze technologie.",
            "Z tego tekstu wynika, że:",
            ["rezydencja jest zlokalizowana w centrum Hollywood",
             "do willi można dostać się tylko helikopterem",
             "dom znajduje się niedaleko Warszawy"], 2,
            "«willa pod Warszawą» → недалеко від Варшави. Схожа на Голлівуд (не в ньому); "
            "гелікоптер — не єдиний спосіб."),
    MCQItem("czytanie",
            "Andrea Camastra z wykształcenia jest muzykiem, ale wybrał zawód kucharza. Urodził się "
            "we Włoszech, pracował w całej Europie. Prawdziwą karierę zrobił w Polsce: jego "
            "pierwsza restauracja Nuta dostała gwiazdkę Michelin.",
            "Z tego tekstu wynika, że:",
            ["Andrea Camastra został kucharzem, gdy przyjechał do Polski",
             "kucharz największy sukces odniósł w znanej włoskiej restauracji",
             "lokal Camastry w Warszawie otrzymał gastronomiczne wyróżnienie"], 2,
            "«Nuta dostała gwiazdkę Michelin» → відзнака. Кухарем став раніше; успіх — у Польщі."),
    # ── Zad II: TAK/NIE — застосунок «Pan Paragon» ──────────────────────
    MCQItem("czytanie",
            "TEKST «Pan Paragon»: безкоштовний застосунок для контролю витрат родини. Робиш фото "
            "чека — програма АВТОМАТИЧНО розпізнає назву магазину, дату й суму. Покупки додаєш до "
            "категорій (можна створювати власні групи). Зберігає всі чеки — електронний чек = таке "
            "саме підтвердження, як паперовий (для повернення/рекламації). Тримає картки клієнта, "
            "купони-знижки, актуальні газетки з промоціями; можна додавати товари до списку "
            "покупок, зокрема вставивши посилання на рецепт із інтернету.",
            "TAK/NIE: Pan Paragon ma pomóc w zarządzaniu domowym budżetem.",
            ["TAK", "NIE"], 0, "ТАК — допомагає контролювати витрати родини."),
    MCQItem("czytanie", "",
            "TAK/NIE: W aplikacji trzeba wpisać, kiedy i gdzie robiliśmy zakupy.",
            ["TAK", "NIE"], 1, "НІ — програма АВТОМАТИЧНО розпізнає магазин, дату й суму з фото."),
    MCQItem("czytanie", "",
            "TAK/NIE: Użytkownik może samodzielnie zmieniać kategorie zakupów.",
            ["TAK", "NIE"], 0, "ТАК — можна створювати власні групи витрат."),
    MCQItem("czytanie", "",
            "TAK/NIE: Gdy klient chce złożyć reklamację, musi pokazać w sklepie tradycyjny paragon.",
            ["TAK", "NIE"], 1, "НІ — електронний чек = таке саме підтвердження, як паперовий."),
    MCQItem("czytanie", "",
            "TAK/NIE: Pan Paragon umożliwia przeglądanie ofert promocyjnych w wielu sklepach.",
            ["TAK", "NIE"], 0, "ТАК — газетки з промоціями, оферти супермаркетів."),
    MCQItem("czytanie", "",
            "TAK/NIE: Aplikacja samodzielnie wybiera w internecie najlepsze przepisy.",
            ["TAK", "NIE"], 1, "НІ — користувач вставляє посилання, застосунок лише зчитує продукти."),
    # ── Zad V: обери найкраще слово (текст «Najstarsza didżejka») ────────
    MCQItem("czytanie", "Текст про найстаршу діджейку Польщі (DJ Wika). Обери найкраще слово.",
            "W Polsce starość zwykle ___ z czymś smutnym.",
            ["pamięta się", "zna się", "łączy się"], 2, "«___ z czymś» (асоціюється) → <b>łączy się</b>."),
    MCQItem("czytanie", "", "Energii mogą jej pozazdrościć ___ dużo młodszych pokoleń.",
            ["uczestnicy", "przedstawiciele", "prezenterzy"], 1, "представники поколінь → <b>przedstawiciele</b>."),
    MCQItem("czytanie", "", "Z wykształcenia jest pedagogiem i ___ dzieci z niepełnosprawnościami.",
            ["uczyła", "bawiła się", "uczyła się"], 0, "навчала дітей → <b>uczyła</b> (а не uczyła się = вчилася)."),
    MCQItem("czytanie", "", "Po przejściu na emeryturę ___ działać na rzecz seniorów.",
            ["zaczęła", "skończyła", "kontynuowała"], 0, "почала діяти → <b>zaczęła</b>."),
    MCQItem("czytanie", "", "…poznawała sztukę miksowania i ___ docenili ją nawet młodzi.",
            ["tylko", "wreszcie", "wolno"], 1, "нарешті → <b>wreszcie</b>."),
    MCQItem("czytanie", "", "Ma 86 lat i cały czas jest ___ zawodowo.",
            ["aktywna", "energiczna", "doświadczona"], 0, "активна професійно → <b>aktywna</b>."),
    MCQItem("czytanie", "", "Z jej inicjatywy od kilku lat ___ Parada Seniorów w Warszawie.",
            ["prowadzi się", "odbywa się", "występuje"], 1, "парад ВІДБУВАЄТЬСЯ → <b>odbywa się</b>."),
    MCQItem("czytanie", "", "Starsi powinni uczestniczyć w życiu ___.",
            ["publicznym", "narodowym", "ogólnym"], 0, "громадське життя → życie <b>publicznym</b>."),
    MCQItem("czytanie", "", "___ na film wziął się ze strachu reżyserki przed przemijaniem.",
            ["cel", "program", "pomysł"], 2, "задум фільму → <b>pomysł</b>."),
    MCQItem("czytanie", "", "Chciała przekonać ___ i samą siebie, że można się pięknie starzeć.",
            ["czytelników", "widzów", "obserwatorów"], 1, "глядачів (фільму) → <b>widzów</b>."),
]

# ── CZYTANIE — Zad III: вставити фрагменти (навчання за кордоном) ──
# Приклад = C. Ключ (klucz): A,H,F,E,D,B,G.
_ZAD3 = MatchTask(
    section="czytanie",
    title="2024-04 Читання Zad III — встав фрагменти (навчання за кордоном)",
    intro="Прочитай текст про Міхала, який навчався за кордоном. Заповни пропуски 1–7 фрагментами A–G.",
    options=[
        "gdzie poznawał kulturę kraju i język mandaryński",  # A
        "żeby zbudować jego precyzyjny profil",  # B
        "że im wcześniej zaplanujemy studia za granicą",  # D
        "która chce pomagać przyszłym studentom",  # E
        "który zrobił na nim ogromne wrażenie",  # F
        "lecz ważniejsze są rzeczy pozaakademickie",  # G
        "ale studia magisterskie odbył już na uniwersytecie",  # H
    ],
    prompts=[
        "1. Wyjechał do Azji, ___ oraz zarabiał na edukację.",
        "2. Naukę zaczął w Glasgow, ___ w Cambridge.",
        "3. Realizował praktyki w Parlamencie Europejskim, ___",
        "4. Otworzył firmę doradztwa akademickiego, ___ w wyborze kierunku studiów.",
        "5. Okazuje się, ___, tym łatwiej będzie nam się dostać.",
        "6. Pracujemy indywidualnie z każdym kandydatem, ___ i zasugerować wybór uczelni.",
        "7. Wyniki z egzaminów mają znaczenie, ___: staże, wolontariaty, sport.",
    ],
    key=[0, 6, 4, 3, 2, 1, 5],  # A,H,F,E,D,B,G
    explain=[
        "«do Azji, ___» → A (де пізнавав культуру й мандаринську).",
        "«zaczął w Glasgow, ___ w Cambridge» → H (але магістратуру — в університеті).",
        "«praktyki…, ___» → F (які справили величезне враження).",
        "«firmę…, ___» → E (яка хоче допомагати майбутнім студентам).",
        "«Okazuje się, ___, tym łatwiej» → D (що чим раніше сплануємо).",
        "«z kandydatem, ___» → B (щоб побудувати точний профіль).",
        "«mają znaczenie, ___» → G (але важливіше — позаакадемічне)."],
)

# ── CZYTANIE — Zad IV: заголовки↔тексти (цифрова гігієна) ──
# Приклад = B. Ключ (klucz): F,A,E,G,D,C,H.
_ZAD4 = MatchTask(
    section="czytanie",
    title="2024-04 Читання Zad IV — заголовок до тексту (цифрова гігієна)",
    intro="«Osiem zasad higieny cyfrowej» — до кожного заголовка (1–7) добери фрагмент A–G.",
    options=[
        "Kiedy musisz skoncentrować się na obowiązkach, wyłącz dźwięk w telefonie i alerty "
        "z serwisów społecznościowych.",  # A
        "Kontakty przez internet to nie to samo, co spotkanie ze znajomymi; dobre relacje "
        "chronią przed uzależnieniem.",  # C
        "Minimum godzinę przed zaśnięciem nie sprawdzaj telefonu; najlepiej nie bierz "
        "elektroniki do łóżka.",  # D
        "Jeśli pracujesz, skup się na tym – nie sprawdzaj Facebooka, nie oglądaj filmików.",  # E
        "Nie noś telefonu przez cały czas przy sobie; w pracy zostaw go tam, gdzie go nie "
        "będziesz widział.",  # F
        "Naukowcy udowodnili, że ludzie bez hobby łatwiej uzależniają się od internetu – "
        "znajdź to, co sprawia ci przyjemność.",  # G
        "Co jakiś czas zrób sobie cyfrowy detoks – spędzaj chwile poza siecią: kawiarnia, "
        "park, dzień z bliskimi.",  # H
    ],
    prompts=[
        "1. Odłóż czasem swój smartfon",
        "2. Zaprzyjaźnij się z ciszą",
        "3. Nie rób wielu rzeczy na raz",
        "4. Poszukaj pasji poza internetem",
        "5. Dbaj o jakość snu",
        "6. Dbaj o przyjaźnie",
        "7. Planuj przerwy od internetu",
    ],
    key=[4, 0, 3, 5, 2, 1, 6],  # F,A,E,G,D,C,H
    explain=[
        "відклади смартфон → F (не носи весь час при собі).",
        "потоваришуй з тишею → A (вимкни звук і сповіщення).",
        "не роби багато нараз → E (працюєш — зосередься на цьому).",
        "знайди хобі → G (без хобі легше залежність).",
        "дбай про сон → D (годину до сну без телефону).",
        "дбай про дружбу → C (реальні контакти захищають).",
        "плануй перерви → H (цифровий детокс, час поза мережею)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: підкресли форму (відмінювання) — MCQ. Текст про медицину природну. ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про природну медицину.",
            "Muzykoterapia, joga czy masaże często pomagają ___ w poprawie samopoczucia.",
            ["pacjentów", "pacjentami", "pacjentom"], 2, "pomagać + давальний → <b>pacjentom</b>."),
    MCQItem("gramatyka", "", "Przy problemach ze ___ skuteczne są ziołowe herbatki.",
            ["snem", "śnie", "snowi"], 0, "ze + орудний → <b>snem</b>."),
    MCQItem("gramatyka", "", "Przy problemach ze snem skuteczne są ___ herbatki.",
            ["ziołowymi", "ziołowe", "ziołowych"], 1, "наз. множини (herbatki są) → <b>ziołowe</b>."),
    MCQItem("gramatyka", "", "Naturalne metody sprawdzają się podczas ___.",
            ["przeziębieniu", "przeziębienia", "przeziębieniem"], 1, "podczas + родовий → <b>przeziębienia</b>."),
    MCQItem("gramatyka", "", "Ten sposób jest popularny wśród ___ mam.",
            ["młodych", "młodym", "młodymi"], 0, "wśród + родовий множини → <b>młodych</b>."),
    MCQItem("gramatyka", "", "…ma wady, o ___ powinniśmy wiedzieć.",
            ["które", "której", "których"], 2, "o + місцевий множини → <b>których</b>."),
    MCQItem("gramatyka", "", "Czasami takie ___ powoduje negatywne skutki.",
            ["leczenia", "leczenie", "leczeniu"], 1, "підмет (наз. одн.) → <b>leczenie</b>."),
    MCQItem("gramatyka", "", "Z ___ powodu należy powiedzieć lekarzowi.",
            ["tym", "temu", "tego"], 2, "z tego powodu (з цієї причини) → <b>tego</b>."),
    MCQItem("gramatyka", "", "Wiedza lekarza może ___ zagwarantować, że dobrze postępujemy.",
            ["nas", "nam", "nami"], 1, "gwarantować + давальний → <b>nam</b>."),
    MCQItem("gramatyka", "", "Konsultujmy się z lekarzami, aby unikać ___.",
            ["komplikacje", "komplikację", "komplikacji"], 2, "unikać + родовий → <b>komplikacji</b>."),
    # ── Zad III: ступенювання — MCQ. Текст кіт чи пес. ──
    MCQItem("gramatyka", "Текст: кіт чи пес?",
            "Psy dużo ___ niż koty akceptują podróże.",
            ["najłatwiej", "łatwiej", "łatwo"], 1, "порівняння (niż) → <b>łatwiej</b>."),
    MCQItem("gramatyka", "", "Koty są natomiast ___ od psów.",
            ["niezależnej", "bardziej niezależne", "niezależnie"], 1,
            "вищий ступінь прикметника → <b>bardziej niezależne</b>."),
    MCQItem("gramatyka", "", "Produkty dla zwierząt z każdym rokiem są coraz ___.",
            ["droższe", "drożej", "najdroższe"], 0, "coraz + вищий ступ. (są) → <b>droższe</b>."),
    MCQItem("gramatyka", "", "Utrzymanie kotów jest trochę ___.",
            ["mniejsze kosztowne", "kosztowne", "mniej kosztowne"], 2, "«менш витратне» → <b>mniej kosztowne</b>."),
    MCQItem("gramatyka", "", "Ze wszystkich ___ żyją papugi, żółwie i węże.",
            ["najdłuższe", "dłużej", "najdłużej"], 2, "«ze wszystkich» → найвищий ступ. присл. → <b>najdłużej</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: lub) → MCQ-per-gap ──
    MCQItem("gramatyka", "Текст про харчові звички. Встав сполучник (зайве слово — <i>lub</i>).",
            "Naukowcy odkryli, ___ prawidłowe nawyki kształtują się od najmłodszych lat.",
            ["że", "a", "ale", "więc", "bo", "lub"], 0, "«odkryli, ___» → <b>że</b>."),
    MCQItem("gramatyka", "", "Dziecko uczy się, co jest zdrowe, ___ co nie.",
            ["że", "a", "ale", "więc", "bo", "lub"], 1, "зіставлення → <b>a</b> co nie."),
    MCQItem("gramatyka", "", "Ważne jest nie tylko to, co je, ___ także jak je.",
            ["że", "a", "ale", "więc", "bo", "lub"], 2, "«nie tylko… ___ także» → <b>ale</b>."),
    MCQItem("gramatyka", "", "Je szybko, zjada więcej niż potrzebuje, ___ tyje.",
            ["że", "a", "ale", "więc", "bo", "lub"], 3, "наслідок → <b>więc</b> (тому)."),
    MCQItem("gramatyka", "", "Nie zje śniadania, ___ „nie ma na to czasu”.",
            ["że", "a", "ale", "więc", "bo", "lub"], 4, "причина → <b>bo</b> (бо)."),
    # ── Zad VII: підкресли форму (вид/способи) — MCQ. Діалог про співбесіду. ──
    MCQItem("gramatyka", "Діалог: Joanna готується до першої співбесіди, радиться з батьками.",
            "Ojciec: My? Jak ___ ci poradzić?",
            ["miałby", "miejmy", "mielibyśmy"], 2, "умовний, 1 ос. мн. (my) → <b>mielibyśmy</b>."),
    MCQItem("gramatyka", "", "Joanna: ___, o czym powinnam pamiętać.",
            ["Powiedzieliby", "Powiedzcie", "Mówmy"], 1, "наказ до «wy» (батьки) → <b>Powiedzcie</b>."),
    MCQItem("gramatyka", "", "Ojciec: ___ punktualnie, odpowiednio ubrana…",
            ["Przyjdź", "Przychodź", "Przyszłabyś"], 0, "наказ докон. до «ty» → <b>Przyjdź</b>."),
    MCQItem("gramatyka", "", "Matka: …i ___ telefon komórkowy.",
            ["wyłączaj", "włączyliby", "wyłącz"], 2, "наказ докон. → <b>wyłącz</b>."),
    MCQItem("gramatyka", "", "Joanna: nie ___ sobie ze mnie!",
            ["żartowałbyś", "żartujcie", "żartujmy"], 1, "наказ до «wy» → <b>żartujcie</b>."),
    MCQItem("gramatyka", "", "…to może lepiej ___ mi o waszych rozmowach o pracę.",
            ["opowiedzielibyście", "opowiadalibyście", "opowiedz"], 0,
            "умовний, 2 ос. мн. (wy) → <b>opowiedzielibyście</b>."),
    MCQItem("gramatyka", "", "Ojciec: Nic by ci to nie ___.",
            ["pomagaj", "pomagałoby", "pomogło"], 2, "«by… ___» докон. → <b>pomogło</b>."),
    MCQItem("gramatyka", "", "Może niech Bartek ci ___ swoje doświadczenia.",
            ["przedstawi", "przedstaw", "przedstawiałby"], 0, "«niech ___» докон. → <b>przedstawi</b>."),
    MCQItem("gramatyka", "", "Gdyby ___ tę pracę, zadzwoniłabym do niego.",
            ["dostawał", "dostał", "dostałby"], 1, "«gdyby ___» — умова, форма на -ł → <b>dostał</b>."),
    MCQItem("gramatyka", "", "…na pewno ___ do niego i poprosiła o pomoc.",
            ["zadzwoń", "dzwoniłabym", "zadzwoniłabym"], 2, "умовний докон., 1 ос. одн. жін. → <b>zadzwoniłabym</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: przy) → MCQ-per-gap ──
    MCQItem("gramatyka", "Текст про Музей моторизації. Встав прийменник (зайве слово — <i>przy</i>).",
            "Muzeum posiada ___ swojej kolekcji ponad trzysta pojazdów.",
            ["w", "na", "do", "przez", "z", "przy"], 0, "w + місцевий (у колекції) → <b>w</b>."),
    MCQItem("gramatyka", "", "Muzeum oferuje prelekcje ___ temat historii motoryzacji.",
            ["w", "na", "do", "przez", "z", "przy"], 1, "стійке «na temat» → <b>na</b>."),
    MCQItem("gramatyka", "", "…dla dzieci możliwość wchodzenia ___ wybranych samochodów.",
            ["w", "na", "do", "przez", "z", "przy"], 2, "wchodzić do + родовий → <b>do</b>."),
    MCQItem("gramatyka", "", "Kolekcję można oglądać ___ najbliższe dwa miesiące.",
            ["w", "na", "do", "przez", "z", "przy"], 3, "тривалість «przez… miesiące» → <b>przez</b>."),
    MCQItem("gramatyka", "", "Znajduje się tam mały sklep ___ pamiątkami.",
            ["w", "na", "do", "przez", "z", "przy"], 4, "sklep z + орудний → <b>z</b> pamiątkami."),
]

# ── Zad IV: вписати форми (тепер./мин. час) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2024-04 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або минулий час). Текст про підсумок року.\n\n"
           "<i>Приклад: dzięki nim <b>widzą</b> (widzieć), jak wiele <b>osiągnęli</b> (osiągnąć).</i>"),
    prompts=[
        "1. Już dziś ___ (my – móc) podsumować pierwszą część roku.",
        "2. Jakie decyzje ___ (ty – podjąć) w zeszłym miesiącu?",
        "3. Czy obecnie ___ (ty – zastanawiać się) nad własnym rozwojem?",
        "4. Współcześni mistrzowie jogi ___ (uważać), że warto zadać sobie pytanie.",
        "5. …czego ___ (my – nauczyć się) w przeszłości.",
        "6. Jakie doświadczenia ___ (zdobyć) ostatnio inne osoby?",
        "7. Jakie projekty ty sam niedawno ___ (zrealizować)?",
        "8. Jak dzisiaj ___ (ja – dbać) o swoje ciało i umysł?",
        "9. Czy ___ (ja – kontrolować) czas spędzany w internecie?",
        "10. Każdy ___ (chcieć) widzieć w swoim życiu pozytywne zmiany.",
    ],
    accepted=[
        ["możemy"], ["podjąłeś"], ["zastanawiasz się"], ["uważają"], ["nauczyliśmy się"],
        ["zdobyły"], ["zrealizowałeś"], ["dbam"], ["kontroluję"], ["chce"],
    ],
    explain=[
        "тепер., 1 ос. мн. (my) → <b>możemy</b>.",
        "минулий, 2 ос. одн. чол. (ty) → <b>podjąłeś</b>.",
        "тепер., 2 ос. одн. → <b>zastanawiasz się</b>.",
        "тепер., 3 ос. мн. → <b>uważają</b>.",
        "минулий, 1 ос. мн. → <b>nauczyliśmy się</b>.",
        "минулий, 3 ос. мн. (не-чол.-ос.: doświadczenia) → <b>zdobyły</b>.",
        "минулий, 2 ос. одн. чол. → <b>zrealizowałeś</b>.",
        "тепер., 1 ос. одн. (ja) → <b>dbam</b>.",
        "тепер., 1 ос. одн. → <b>kontroluję</b>.",
        "тепер., 3 ос. одн. (każdy) → <b>chce</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2024-04 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: czekała «na list» → Na co?</i>"),
    prompts=[
        "Anna była wczoraj w teatrze «z mężem i z dziećmi».",
        "Nauczyciel zapytał uczniów «o ich plany wakacyjne».",
        "Uczniowie byli w kinie na filmie «przyrodniczym».",
        "Panna młoda «pięknie» wyglądała w białej sukni.",
        "Paweł podkreślił najważniejsze zdanie «długopisem».",
    ],
    accepted=[["z kim"], ["o co"], ["na jakim"], ["jak"], ["czym"]],
    explain=[
        "з людьми → <b>Z kim?</b>",
        "zapytać o + знах. → <b>O co?</b>",
        "«na jakim filmie» → <b>Na jakim?</b>",
        "спосіб (як?) → <b>Jak?</b>",
        "długopisem — орудний → <b>Czym?</b>",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2024-04 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «muszę kupić pieczywo» (potrzebuję) → potrzebuję pieczywa.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Mój brat lubi zupę pomidorową.",
        "Wujek mojej żony jest bardzo dobrym pianistą.",
        "Naukowców zaciekawiło nagłe ocieplenie klimatu.",
        "Lampę postaw obok tamtego niskiego stolika nocnego.",
        "Dorotka cieszy się, że dostała tort urodzinowy.",
    ],
    words=["smakuje", "gra na", "zainteresowali się", "przy", "cieszy się z"],
    models=[
        ["Mojemu bratu smakuje zupa pomidorowa."],
        ["Wujek mojej żony bardzo dobrze gra na pianinie.",
         "Wujek mojej żony bardzo dobrze gra na fortepianie."],
        ["Naukowcy zainteresowali się nagłym ociepleniem klimatu."],
        ["Lampę postaw przy tamtym niskim stoliku nocnym."],
        ["Dorotka cieszy się z tortu urodzinowego."],
    ],
)

EXAM = Exam(
    id="2024-04",
    label="Реальний іспит квітень-2024 (офіц.)",
    kind="real",
    year=2024,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
