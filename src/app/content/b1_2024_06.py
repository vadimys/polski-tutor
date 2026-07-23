"""РЕАЛЬНИЙ минулий іспит B1 — червень 2024 (certyfikatpolski.pl).

Джерело: 22-23.06.2024-B1_arkusz + …_transkrypcja.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН
ключ звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad):
- Czytanie: Zad I (×5) + Zad II (TAK/NIE ×6) + Zad V (×10) MCQ; Zad III/IV matching.
- Gramatyka: I(×10)+II(×5)+III(×5)+VII(×10)+VIII(×5) MCQ; IV(×10)+V(×5) free-fill; VI(×5) open.
Далі: Słuchanie (5 Zad).
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Bilety na komunikację są drogie, ale lepiej je kupić niż spotkać kontrolera. "
            "W Gdańsku brak biletu może kosztować nawet 300 zł. Kwota będzie niższa, jeśli "
            "zapłacimy mandat od razu lub najpóźniej w ciągu 7 dni.",
            "Z tego tekstu wynika, że w Gdańsku wysokość mandatu:",
            ["jest zawsze taka sama", "zależy od terminu zapłaty", "zależy od kontrolera"], 1,
            "нижча, якщо заплатити одразу/за 7 днів → залежить від строку оплати."),
    MCQItem("czytanie",
            "W ostatnim meczu Iga Świątek pokonała rywalkę i awansowała do finału turnieju "
            "w Dubaju. Sukces był wyjątkowy: Polka kontynuuje szczęśliwą serię zwycięstw, która "
            "trwa od października ubiegłego roku.",
            "Z tego tekstu wynika, że Iga Świątek:",
            ["nie przegrała meczu od zeszłego roku", "wygrała turniej tenisa w Dubaju",
             "zagrała ostatni raz w tym turnieju"], 0,
            "серія перемог від жовтня минулого року → не програвала. Вийшла у ФІНАЛ (ще не виграла турнір)."),
    MCQItem("czytanie",
            "Nowe badania pokazują, że w najlepszej sytuacji psychicznej są dzieci bez rodzeństwa "
            "lub z tylko jednym bratem/siostrą. Duża różnica wieku między rodzeństwem wpływa "
            "negatywnie na stan psychiczny najmłodszych.",
            "Z tego tekstu wynika, że:",
            ["badanie dotyczyło tylko dzieci, które mają starsze rodzeństwo",
             "wiek rodzeństwa nie jest ważny dla psychiki dziecka",
             "na emocje dziecka dobrze wpływa fakt, że nie ma siostry lub brata"], 2,
            "найкраще — без братів/сестер або з одним → відсутність рідні добре впливає."),
    MCQItem("czytanie",
            "Już w najbliższych latach Europa odczuje efekty zmiany klimatu. Skutki nie będą "
            "takie same we wszystkich regionach. W Polsce można spodziewać się rzadkich opadów "
            "i częstych upałów, dlatego trzeba liczyć się z wyższymi cenami żywności.",
            "Z tego tekstu wynika, że:",
            ["w niektórych częściach Europy klimat się nie zmieni",
             "w całej Europie będzie podobna pogoda",
             "niedługo w Polsce jedzenie może być droższe"], 2,
            "«wyższe ceny żywności» → їжа може подорожчати. Клімат зміниться всюди (по-різному)."),
    MCQItem("czytanie",
            "Podczas wakacji Park Legend odwiedzali głównie turyści indywidualni, a teraz coraz "
            "więcej wycieczek rezerwują szkoły. W tym muzeum dzięki technice komputerowej możemy "
            "dowiedzieć się więcej o wydarzeniach, które miały miejsce dawno temu.",
            "Z tego tekstu wynika, że Park Legend:",
            ["wcześniej był atrakcją popularną tylko wśród uczniów",
             "prezentuje przeszłość w nowoczesny sposób",
             "można zwiedzić także przez internet"], 1,
            "«dzięki technice komputerowej… o wydarzeniach dawno temu» → минуле в сучасний спосіб."),
    # ── Zad II: TAK/NIE — застосунок Yazio ──────────────────────────────
    MCQItem("czytanie",
            "TEKST «Yazio»: дієтичний застосунок для трьох цілей — важити менше, не більше або "
            "наростити м'язи. Реєстрація: досить вписати e-mail. Далі обираєш ціль і вводиш дані "
            "(стать, зріст, вага, дата народження) — програма створює план харчування, дбає про "
            "воду, має пошук їжі, позначення улюблених страв і сканер штрихкодів (показує базову "
            "інфо про продукт). Контролює й фізичну активність (широка база; «біг» = 10 варіантів). "
            "Дуже проста. Мінус: безкоштовний акаунт має рекламу й не всі функції.",
            "TAK/NIE: Yazio pomaga utrzymać wagę i modelować sylwetkę.",
            ["TAK", "NIE"], 0, "ТАК — важити менше/не більше/наростити м'язи."),
    MCQItem("czytanie", "",
            "TAK/NIE: Przy rejestracji należy podać kilka informacji o sobie.",
            ["TAK", "NIE"], 1, "НІ — для реєстрації досить e-mail (дані вводимо пізніше, обираючи ціль)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Aplikacja proponuje ilość płynów, które mamy wypić każdego dnia.",
            ["TAK", "NIE"], 0, "ТАК — дбає про належну кількість води щодня."),
    MCQItem("czytanie", "",
            "TAK/NIE: Skaner kodów pomoże nam znaleźć najsmaczniejszy posiłek.",
            ["TAK", "NIE"], 1, "НІ — сканер показує базову інформацію про продукт, не «найсмачніший»."),
    MCQItem("czytanie", "",
            "TAK/NIE: Program ma wbudowaną bogatą listę ćwiczeń sportowych.",
            ["TAK", "NIE"], 0, "ТАК — широка база активностей («біг» — 10 опцій)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Podczas rejestracji trzeba zapłacić za korzystanie z Yazio.",
            ["TAK", "NIE"], 1, "НІ — є безкоштовний акаунт (з рекламою)."),
    # ── Zad V: обери найкраще слово (текст «Czas wolny») ─────────────────
    MCQItem("czytanie", "Текст про вільний час. Обери найкраще слово.",
            "Najczęściej ___ kanapę i telewizor.",
            ["wybieramy", "wymyślamy", "rozkładamy"], 0, "обираємо диван → <b>wybieramy</b>."),
    MCQItem("czytanie", "", "Niektórzy przez długie godziny ___ internet bez celu.",
            ["oglądają", "analizują", "przeglądają"], 2, "переглядають інтернет → <b>przeglądają</b>."),
    MCQItem("czytanie", "", "Zbyt mało czasu spędzamy na ___ powietrzu.",
            ["czystym", "świeżym", "dobrym"], 1, "стійке «na świeżym powietrzu» → <b>świeżym</b>."),
    MCQItem("czytanie", "", "Często ___ o ruchu, nie uprawiamy sportu.",
            ["zapominamy", "pamiętamy", "przypominamy"], 0, "забуваємо про рух → <b>zapominamy</b>."),
    MCQItem("czytanie", "", "Codzienny trening daje dużo ___ do działania.",
            ["kondycji", "aktywności", "energii"], 2, "багато енергії → <b>energii</b>."),
    MCQItem("czytanie", "", "Każdy wysiłek fizyczny pozytywnie ___ na nasze zdrowie.",
            ["robi", "wpływa", "pomaga"], 1, "«wpływać na» → <b>wpływa</b>."),
    MCQItem("czytanie", "", "Czas po pracy to okazja do ___ ze znajomymi.",
            ["poznania", "spotkania", "mówienia"], 1, "зустріч зі знайомими → <b>spotkania</b>."),
    MCQItem("czytanie", "", "Chwile z przyjaciółmi można spędzać na wiele ___.",
            ["sposobów", "pomysłów", "okazji"], 0, "на багато способів → <b>sposobów</b>."),
    MCQItem("czytanie", "", "Warto ___ dnia znaleźć moment tylko dla siebie.",
            ["wszystkiego", "całego", "każdego"], 2, "щодня → <b>każdego</b> dnia."),
    MCQItem("czytanie", "", "Najważniejsze, żebyśmy robili to, co ___ radość i satysfakcję.",
            ["daje", "otrzymuje", "czuje"], 0, "«___ radość» (дає) → <b>daje</b>."),
]

# ── CZYTANIE — Zad III: вставити фрагменти («Mój nauczyciel jest robotem») ──
# Приклад = C. Ключ: H,B,E,D,F,A,G.
_ZAD3 = MatchTask(
    section="czytanie",
    title="2024-06 Читання Zad III — встав фрагменти (научитель-робот)",
    intro="Прочитай текст про можливих учителів-роботів. Заповни пропуски 1–7 фрагментами A–G.",
    options=[
        "ale nie będzie rozumiał ich uczuć",  # A
        "żeby trochę odpocząć czy spędzić czas z rodziną",  # B
        "czy kolejny raz spóźni się na lekcję",  # D
        "którzy dzięki specjalnemu programowi",  # E
        "który nawiąże z nim emocjonalną relację",  # F
        "i może już za kilka lat będzie faktem",  # G
        "że pozwoli zastąpić nauczycieli robotami",  # H
    ],
    prompts=[
        "1. …sztucznej inteligencji na takim poziomie, ___. To wcale nie jest niemożliwe!",
        "2. Robot nigdy nie poprosi o urlop, ___",
        "3. Uczniom spodobają się mechaniczni nauczyciele, ___ będą znali odpowiedź na każde pytanie.",
        "4. Jeśli uczeń nie odda zadania domowego ___, robot mu przypomni.",
        "5. Dziecko nie będzie miało obok siebie człowieka, ___. Bez niej straci motywację.",
        "6. Nauczyciel-robot będzie znał dane uczniów, ___. A to ważny element.",
        "7. Pomysł ma wiele zalet ___. Jednak dziś nic nie zastąpi kontaktu z ludźmi.",
    ],
    key=[6, 1, 3, 2, 4, 0, 5],  # H,B,E,D,F,A,G
    explain=[
        "«na takim poziomie, ___» → G (що дозволить замінити вчителів роботами).",
        "«nie poprosi o urlop, ___» → B (щоб відпочити чи побути з родиною).",
        "«nauczyciele, ___ будуть знати відповідь» → D (котрі завдяки програмі).",
        "«nie odda zadania ___» → C (чи вкотре спізниться на урок).",
        "«człowieka, ___» → E (який налагодить емоційний зв'язок; «bez niej» = relacji).",
        "«dane uczniów, ___» → A (але не розумітиме їхніх почуттів).",
        "«ma wiele zalet ___» → F (і, можливо, за кілька років стане фактом)."],
)

# ── CZYTANIE — Zad IV: заголовки↔тексти (8 питань зі співбесіди) ──
# Приклад = B. Ключ: G,A,F,H,E,D,C.
_ZAD4 = MatchTask(
    section="czytanie",
    title="2024-06 Читання Zad IV — питання↔відповідь (співбесіда)",
    intro="«8 pytań z rozmowy o pracę» — до кожного питання (1–7) добери відповідь A–G.",
    options=[
        "Mój ostatni kierownik był świetnym specjalistą, ale czasem mieliśmy różne opinie – "
        "zawsze jednak umieliśmy się porozumieć.",  # A
        "Mimo że najbardziej lubię wykonywać zadania samodzielnie, cenię ludzi kreatywnych, "
        "którzy mają swoje zdanie.",  # C
        "Kiedy się stresuję, gorzej wykonuję obowiązki i mam problem z koncentracją – dlatego "
        "unikam konfliktów, a projekty realizuję na czas.",  # D
        "W ciągu ostatniego roku współpracowałem z ważnymi klientami i zrealizowałem kilka "
        "dużych projektów – dzięki temu firma otrzymała prestiżową nagrodę.",  # E
        "Zawsze chciałem być ekspertem w swojej dziedzinie; marzę o stanowisku menadżera "
        "i chcę nauczyć się kierować zespołem.",  # F
        "Jestem sumienny i szybko się uczę; moje zalety to odpowiedzialność i łatwość "
        "w nawiązywaniu kontaktów – będę dobrym pracownikiem.",  # G
        "Moje obecne miejsce pracy nie oferuje już awansu; chciałbym pracować w firmie, która "
        "korzysta z najnowszych technologii.",  # H
    ],
    prompts=[
        "1. Dlaczego powinniśmy cię zatrudnić?",
        "2. Jak układała się współpraca z innymi szefami?",
        "3. Gdzie widzisz siebie za pięć lat?",
        "4. Z jakiego powodu chcesz zmienić pracę?",
        "5. Co uważasz za swój największy zawodowy sukces?",
        "6. Jakie są twoje słabe strony?",
        "7. Z kim lubisz pracować?",
    ],
    key=[5, 0, 4, 6, 3, 2, 1],  # G,A,F,H,E,D,C
    explain=[
        "чому взяти тебе → F (сумлінний, відповідальний, легко контактує).",
        "співпраця з шефами → A (керівник-фахівець, різні думки, але порозуміння).",
        "де за 5 років → E (мрію про посаду менеджера).",
        "чому змінюєш роботу → G (нема підвищення, хочу сучасні технології).",
        "найбільший успіх → D (проєкти з клієнтами, фірма отримала нагороду).",
        "слабкі сторони → C (стрес погіршує роботу, тож уникаю конфліктів).",
        "з ким любиш працювати → B (люблю самостійність, ціную креативних)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: підкресли форму (відмінювання) — MCQ. Лист до тата про немовля. ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Лист до тата про перші місяці життя дитини.",
            "Gdy w nocy dziecko płacze i jest ___, zajmujesz się nim z partnerką.",
            ["głodny", "głodnym", "głodne"], 2, "dziecko jest ___ (ніяк. рід) → <b>głodne</b>."),
    MCQItem("gramatyka", "", "…zwykle zajmujesz się ___ wspólnie z partnerką.",
            ["nią", "nim", "go"], 1, "zajmować się + орудний (dzieckiem→ним) → <b>nim</b>."),
    MCQItem("gramatyka", "", "Musisz iść do ___ i spędzić tam wiele godzin.",
            ["prace", "pracy", "pracą"], 1, "do + родовий → <b>pracy</b>."),
    MCQItem("gramatyka", "", "…spędzić tam wiele ___.",
            ["godzinie", "godziny", "godzin"], 2, "wiele + родовий множини → <b>godzin</b>."),
    MCQItem("gramatyka", "", "Mimo zmęczenia po ___ do domu wychodzisz na spacer.",
            ["powrocie", "powrotem", "powrotu"], 0, "po + місцевий → <b>powrocie</b>."),
    MCQItem("gramatyka", "", "…starasz się wyjść na ___ z maluchem.",
            ["spacerze", "spacer", "spaceru"], 1, "wyjść na + знахідний → <b>spacer</b>."),
    MCQItem("gramatyka", "", "…prezent, jaki możesz dać swojej ___.",
            ["ukochaną", "ukochana", "ukochanej"], 2, "dać + давальний → <b>ukochanej</b>."),
    MCQItem("gramatyka", "", "Rozmawiasz z ___ – słuchasz uważnie.",
            ["niej", "nią", "jej"], 1, "z + орудний → <b>nią</b>."),
    MCQItem("gramatyka", "", "…opowiadasz, co słychać w ___ świecie.",
            ["twojej", "twojego", "twoim"], 2, "w + місцевий (чол. рід) → <b>twoim</b>."),
    MCQItem("gramatyka", "", "Razem jesteście ___ i na pewno dacie radę!",
            ["silni", "silnymi", "silny"], 0, "jesteście + називний мн. чол.-ос. → <b>silni</b>."),
    # ── Zad III: ступенювання — MCQ. Текст про овочі й Makłowicza. ──
    MCQItem("gramatyka", "Текст про зміну кулінарних смаків.",
            "Uważałam, że ___ warzywem na świecie jest marchewka.",
            ["gorszym", "najgorzej", "najgorszym"], 2, "«___ на світі» → найвищий ступ. → <b>najgorszym</b>."),
    MCQItem("gramatyka", "", "Każde inne warzywo wydawało mi się ___ od niej.",
            ["smaczniejsze", "najsmaczniejszym", "smaczniej"], 0, "вищий ступ. (od niej) → <b>smaczniejsze</b>."),
    MCQItem("gramatyka", "", "…gdy dorosłam i ___ obejrzałam programy kulinarne.",
            ["uważne", "uważnie", "najuważniej"], 1, "прислівник (як обійшла?) → <b>uważnie</b>."),
    MCQItem("gramatyka", "", "…można podać tak, by podkreślić jego ___ smak.",
            ["wyjątkowo", "wyjątkowy", "bardziej wyjątkowo"], 1, "прикметник (який смак?) → <b>wyjątkowy</b>."),
    MCQItem("gramatyka", "", "Teraz gotuję warzywa dużo ___.",
            ["chętniej", "chętnie", "najchętniej"], 0, "dużo + вищий ступ. присл. → <b>chętniej</b>."),
    # ── Zad II: wskaźniki zespolenia з рамки (1 зайвий: więc) → MCQ-per-gap ──
    MCQItem("gramatyka", "Текст «місто чи село». Встав слово з рамки (зайве — <b>więc</b>).",
            "To jest pytanie, ___ często słyszymy w dyskusjach o stylu życia.",
            ["które", "a", "Jeśli", "lub", "niż", "więc"], 0, "означальне → <b>które</b> słyszymy."),
    MCQItem("gramatyka", "", "Można wymienić wiele zalet ___ także wad każdego z miejsc.",
            ["które", "a", "Jeśli", "lub", "niż", "więc"], 1, "«zalet, ___ także wad» → <b>a</b>."),
    MCQItem("gramatyka", "", "___ ktoś lubi spokój i naturę, powinien wybrać wieś.",
            ["które", "a", "Jeśli", "lub", "niż", "więc"], 2, "умова → <b>Jeśli</b>."),
    MCQItem("gramatyka", "", "Chciałby pójść na koncert ___ na mecz – niech mieszka w mieście.",
            ["które", "a", "Jeśli", "lub", "niż", "więc"], 3, "вибір → <b>lub</b>."),
    MCQItem("gramatyka", "", "W miastach jest dużo lepszy ___ na wsi dostęp do opieki zdrowotnej.",
            ["które", "a", "Jeśli", "lub", "niż", "więc"], 4, "порівняння (lepszy ___) → <b>niż</b>."),
    # ── Zad VII: підкресли форму (вид/способи) — MCQ. Діалог про ювілей. ──
    MCQItem("gramatyka", "Діалог: Anna й Bartosz планують ювілей батьків.",
            "Bartosz: Dobrze, jak ___ ci pomóc?",
            ["miałbym", "mielibyśmy", "miałabyś"], 0, "умовний, 1 ос. одн. чол. → <b>miałbym</b>."),
    MCQItem("gramatyka", "", "Anna: Może ___ zaproszenia dla gości?",
            ["przygotowywalibyśmy", "przygotowałbyś", "przygotowałbym"], 1,
            "умовний докон., 2 ос. одн. (ty) → <b>przygotowałbyś</b>."),
    MCQItem("gramatyka", "", "Bartosz: Nie ___! Nie jestem w tym dobry.",
            ["zażartujmy", "żartuj", "żartowałabym"], 1, "наказ до «ty» → <b>żartuj</b>."),
    MCQItem("gramatyka", "", "___ zaproszenia w firmie graficznej.",
            ["Zamówmy", "Zamawiajmy", "Zamawiaj"], 0, "«нумо замовмо» докон., 1 ос. мн. → <b>Zamówmy</b>."),
    MCQItem("gramatyka", "", "Lepiej ___ listę gości razem.",
            ["róbmy", "zróbmy", "zróbcie"], 1, "докон., 1 ос. мн. (my) → <b>zróbmy</b>."),
    MCQItem("gramatyka", "", "Anna: Wiesz, ___ się tym nie zajmować.",
            ["wolałbyś", "wolałaby", "wolałabym"], 2, "умовний, 1 ос. одн. жін. (Anna) → <b>wolałabym</b>."),
    MCQItem("gramatyka", "", "Bartosz: Jadłospis ___ przygotować z moją Basią.",
            ["mogłabym", "mogłybyśmy", "moglibyśmy"], 2, "умовний, 1 ос. мн. чол.-ос. → <b>moglibyśmy</b>."),
    MCQItem("gramatyka", "", "…w pracach kuchennych chętnie ___ udział moje córki.",
            ["wzięłyby", "wzięliby", "brałaby"], 0, "умовний докон., 3 ос. мн. жін. (córki) → <b>wzięłyby</b>."),
    MCQItem("gramatyka", "", "Niech twój mąż ___ nam, co kupić.",
            ["poradzi", "radziłby", "poradziłby"], 0, "«niech ___» + докон. → <b>poradzi</b>."),
    MCQItem("gramatyka", "", "…ty i Basia ___ też kwiatami.",
            ["zajmujcie się", "zajęłybyście się", "zajmijcie się"], 2, "наказ докон. до «wy» → <b>zajmijcie się</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: na) → MCQ-per-gap ──
    MCQItem("gramatyka", "Текст про пікнік біля озера. Встав прийменник (зайве слово — <b>na</b>).",
            "___ dużego drzewa rozłożył kolorowe koce.",
            ["koło", "ze", "w", "przez", "z", "na"], 0, "koło + родовий (біля) → <b>koło</b> drzewa."),
    MCQItem("gramatyka", "", "Koledzy przynieśli ___ sobą smaczne przekąski.",
            ["koło", "ze", "w", "przez", "z", "na"], 1, "«ze sobą» → <b>ze</b>."),
    MCQItem("gramatyka", "", "…przekąski ___ dużym koszu.",
            ["koło", "ze", "w", "przez", "z", "na"], 2, "w + місцевий (у кошику) → <b>w</b>."),
    MCQItem("gramatyka", "", "Janek ___ pół godziny nie mógł rozpalić grilla.",
            ["koło", "ze", "w", "przez", "z", "na"], 3, "тривалість «przez pół godziny» → <b>przez</b>."),
    MCQItem("gramatyka", "", "___ pomocą przyszła mu koleżanka Ewa.",
            ["koło", "ze", "w", "przez", "z", "na"], 4, "«z pomocą» → <b>z</b>."),
]

# ── Zad IV: вписати форми (тепер./мин.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2024-06 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або минулий час). Текст Magdy про "
           "велоподорож.\n\n<i>Приклад: <b>marzyłam</b> (marzyć), dziś <b>mogę</b> (móc).</i>"),
    prompts=[
        "1. Nareszcie moja córka i ja ___ (jechać) na wyprawę rowerową.",
        "2. ___ (my – zorganizować) ją zupełnie same!",
        "3. Dawniej, bez internetu, ___ (być) to trudne zadanie.",
        "4. Wiele lat temu ___ (ja – widzieć), ile czasu to zajmuje.",
        "5. …ile czasu moi rodzice ___ (planować) takie wyjazdy.",
        "6. Teraz ja i córka ___ (siadać) przed komputerem.",
        "7. …i po prostu ___ (znajdować) propozycje wycieczek.",
        "8. …które w poprzednich latach ___ (opublikować) inni podróżnicy.",
        "9. Następnie ___ (ja – musieć) wpisać dane w aplikacji.",
        "10. …aplikacja, która ___ (obliczać) długość trasy i czas.",
    ],
    accepted=[
        ["jedziemy"], ["zorganizowałyśmy"], ["było"], ["widziałam"], ["planowali"],
        ["siadamy"], ["znajdujemy"], ["opublikowali"], ["muszę"], ["oblicza"],
    ],
    explain=[
        "тепер., 1 ос. мн. → <b>jedziemy</b>.",
        "минулий, 1 ос. мн. жін. (my same) → <b>zorganizowałyśmy</b>.",
        "минулий, ніяк. рід → <b>było</b>.",
        "минулий, 1 ос. одн. жін. → <b>widziałam</b>.",
        "минулий, 3 ос. мн. чол.-ос. (rodzice) → <b>planowali</b>.",
        "тепер., 1 ос. мн. → <b>siadamy</b>.",
        "тепер., 1 ос. мн. → <b>znajdujemy</b>.",
        "минулий, 3 ос. мн. чол.-ос. (podróżnicy) → <b>opublikowali</b>.",
        "тепер., 1 ос. одн. → <b>muszę</b>.",
        "тепер., 3 ос. одн. → <b>oblicza</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2024-06 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: uczy się «od pół roku» → Od kiedy?</i>"),
    prompts=[
        "Córka wysłała «swojej matce» życzenia urodzinowe.",
        "Marta «pięknie» udekorowała swoje mieszkanie.",
        "Rano poszłam do przedszkola «po siostrę».",
        "Dyrektor pije kawę tylko «w tym» kubku.",
        "Wojciech przez 5 lat kierował «firmą».",
    ],
    accepted=[["komu"], ["jak"], ["po kogo"], ["w którym", "w jakim"], ["czym"]],
    explain=[
        "matce — давальний → <b>Komu?</b>",
        "спосіб → <b>Jak?</b>",
        "«po siostrę» (по когось) → <b>Po kogo?</b>",
        "«w tym kubku» → <b>W którym?</b> (W jakim?)",
        "kierować + орудний → <b>Czym?</b>",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2024-06 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «chciał pojechać na wakacje» (marzył) → marzył o wakacjach.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Magda dopiero wczoraj dowiedziała się o nowym terminie egzaminu.",
        "Ile lat ma ich córka?",
        "Mała dziewczynka przyglądała się kolorowemu zegarowi.",
        "Sąsiad sprzedał mi używany samochód.",
        "Zimą brakuje nam słońca.",
    ],
    words=["poznała", "wieku", "patrzyła", "Kupiłem", "tęsknimy"],
    models=[
        ["Magda dopiero wczoraj poznała nowy termin egzaminu."],
        ["W jakim wieku jest ich córka?"],
        ["Mała dziewczynka patrzyła na kolorowy zegar."],
        ["Kupiłem od sąsiada używany samochód."],
        ["Zimą tęsknimy za słońcem."],
    ],
)

EXAM = Exam(
    id="2024-06",
    label="Реальний іспит червень-2024 (офіц.)",
    kind="real",
    year=2024,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
