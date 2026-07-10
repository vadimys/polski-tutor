"""РЕАЛЬНИЙ минулий іспит B1 — червень 2024 (certyfikatpolski.pl).

Джерело: 22-23.06.2024-B1_arkusz + …_transkrypcja.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН
ключ звірено з офіц. klucz. Czytanie:
- Zad I (a/b/c ×5, ключ b,a,c,c,b) + Zad II (TAK/NIE ×6, T,N,T,N,T,N)
  + Zad V (вибір слова ×10) — MCQ; Zad III/IV — matching.
Далі: Gramatyka (8 Zad) + Słuchanie (5 Zad).
"""

from __future__ import annotations

from app.content.schema import Exam, MatchTask, MCQItem

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
        "«na takim poziomie, ___» → H (що дозволить замінити вчителів роботами).",
        "«nie poprosi o urlop, ___» → B (щоб відпочити чи побути з родиною).",
        "«nauczyciele, ___ будуть знати відповідь» → E (котрі завдяки програмі).",
        "«nie odda zadania ___» → D (чи вкотре спізниться на урок).",
        "«człowieka, ___» → F (який налагодить емоційний зв'язок; «bez niej» = relacji).",
        "«dane uczniów, ___» → A (але не розумітиме їхніх почуттів).",
        "«ma wiele zalet ___» → G (і, можливо, за кілька років стане фактом)."],
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
        "чому взяти тебе → G (сумлінний, відповідальний, легко контактує).",
        "співпраця з шефами → A (керівник-фахівець, різні думки, але порозуміння).",
        "де за 5 років → F (мрію про посаду менеджера).",
        "чому змінюєш роботу → H (нема підвищення, хочу сучасні технології).",
        "найбільший успіх → E (проєкти з клієнтами, фірма отримала нагороду).",
        "слабкі сторони → D (стрес погіршує роботу, тож уникаю конфліктів).",
        "з ким любиш працювати → C (люблю самостійність, ціную креативних)."],
)

_MATCHING = [_ZAD3, _ZAD4]

EXAM = Exam(
    id="2024-06",
    label="Реальний іспит червень-2024 (офіц.)",
    kind="real",
    year=2024,
    items=_READING,
    tasks=_MATCHING,
)
