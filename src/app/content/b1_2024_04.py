"""РЕАЛЬНИЙ минулий іспит B1 — квітень 2024 (certyfikatpolski.pl).

Джерело: 20-21.04.2024-B1_arkusz + …_transkrypcja.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН
ключ звірено з офіц. klucz. Наразі — Czytanie:
- Zad I (a/b/c ×5, ключ b,b,c,c,c) + Zad II (TAK/NIE ×6, ключ T,N,T,N,T,N)
  + Zad V (вибір слова ×10) — MCQ; Zad III/IV — matching.
Далі: Gramatyka (8 Zad) + Słuchanie (5 Zad).
"""

from __future__ import annotations

from app.content.schema import Exam, MatchTask, MCQItem

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

EXAM = Exam(
    id="2024-04",
    label="Реальний іспит квітень-2024 (офіц.)",
    kind="real",
    year=2024,
    items=_READING,
    tasks=_MATCHING,
)
