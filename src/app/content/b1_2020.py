"""Офіційний ПРОБНИЙ тест B1 2020 (certyfikatpolski.pl /2020/12/B1_przykladowy_test_2020_03.pdf).

Наразі авто-оцінювані MCQ-завдання, ДОСЛІВНО з arkusz, ключ звірено з офіц. klucz PDF:
- Czytanie Zad I (a/b/c ×5) + Zad II (TAK/NIE ×7) + Zad V (вибір слова ×8);
- Gramatyka Zad I (форми ×10) + Zad III (ступенювання ×5) + Zad II (сполучники ×5).
Разом 40 авто-оцінюваних питань. Решта (dopasowanie Czyt III/IV, форми Gram IV,
pytania/transformacje Gram V/VI, аудіювання) — після рушіїв відповідних типів.
"""

from __future__ import annotations

from app.content.schema import Exam, MCQItem

# ── CZYTANIE — Zad I: «Z tego tekstu wynika…» (a/b/c) ────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Pomysł wprowadzenia opłat za wjazd do Wenecji pojawił się już dawno. Od tego roku "
            "turyści – w zależności od terminu – będą musieli zapłacić od 3 do 10 euro. Władze "
            "Wenecji planują zniżki dla osób, które przyjadą na imprezy organizowane przez miasto.",
            "Z tego tekstu wynika, że opłata za wjazd do Wenecji:",
            ["nie będzie taka sama przez cały rok", "obowiązuje już od dawna",
             "będzie wyższa dla uczestników imprez miejskich"], 0,
            "«od 3 do 10 euro w zależności od terminu» → не однакова цілий рік. Ідея давня, "
            "але оплата — з цього року; для учасників імпрез — знижки, не вище."),
    MCQItem("czytanie",
            "Konkurs teatralny „Więcej niż teatr!” jest zmienioną wersją zeszłorocznego przeglądu "
            "teatrów amatorskich. W spektaklach występują aktorzy z całej Polski, zarówno amatorzy, "
            "jak i profesjonaliści. W tym roku obejrzymy 10 przedstawień na podstawie znanych "
            "tekstów literackich.",
            "Z tego tekstu wynika, że:",
            ["konkurs teatralny od lat istnieje w takiej samej formie",
             "w spektaklach mogą wziąć udział zawodowi aktorzy",
             "aktorzy będą prezentować znane wiersze"], 1,
            "«zarówno amatorzy, jak i profesjonaliści» → професійні теж. Це змінена версія "
            "(не та сама); тексти літературні, не обов'язково вірші."),
    MCQItem("czytanie",
            "Znany dom mody zaprezentował swoje nowe logo, przygotowane na potrzeby kampanii "
            "reklamującej modę męską na sezon jesień/zima 2020. Nowy znak wygląda, jakby był pisany "
            "przez dziecko, co – według niektórych – ma się łączyć z pozytywnymi emocjami.",
            "Z tego tekstu wynika, że nowy znak reklamowy:",
            ["był inspirowany jesienną modą", "stworzyły dzieci",
             "ma przywoływać dobry nastrój"], 2,
            "«ma się łączyć z pozytywnymi emocjami» → добрий настрій. Виглядає ЯК дитячий "
            "(не діти малювали); кампанія про моду, а не натхнення осінню."),
    MCQItem("czytanie",
            "6 na 10 rodziców w Europie mówi, że ma problemy ze skoncentrowaniem się na drodze "
            "w czasie, gdy ich dzieci źle zachowują się w samochodzie. Jeszcze bardziej może "
            "martwić sytuacja, że prawie co trzeci dorosły zauważa, że niegrzeczne dzieci w aucie "
            "mają negatywny wpływ na bezpieczeństwo jazdy.",
            "Ten tekst informuje, że:",
            ["złe zachowanie dzieci w samochodzie powoduje brak uwagi u kierowcy",
             "co trzeci kierowca ma problem z koncentracją na drodze",
             "kierowcy, którzy są rodzicami, nie potrafią ostrożnie jeździć"], 0,
            "6/10 батьків втрачають концентрацію через погану поведінку дітей → брак уваги. "
            "«co trzeci» — про вплив на безпеку, не про концентрацію; узагальнення (c) — хибне."),
    MCQItem("czytanie",
            "W tym roku bardzo dużo osób chciało wziąć udział w maratonie organizowanym w Łodzi "
            "6 stycznia. Lista startowa Biegu Trzech Króli była zamknięta już 2 stycznia. Kilku "
            "zapisanych zawodników się nie pojawiło, więc nieliczne osoby mogły dołączyć do "
            "wyścigu w ostatniej chwili.",
            "Z tego tekstu wynika, że:",
            ["w maratonie biegło mało zawodników", "lista zapisów była otwarta do 6 stycznia",
             "były osoby, które zrezygnowały z biegu"], 2,
            "«Kilku zapisanych się nie pojawiło» → дехто відмовився. Бажаючих було багато; "
            "список закрили 2 січня (не до 6-го)."),
    # ── Zad II: TAK/NIE до тексту «Świat według Kiepskich» ──────────────
    MCQItem("czytanie",
            "TEKST «Świat według Kiepskich»: serial komediowy, od ponad 20 lat pokazywany w "
            "polskiej TV. Pierwszy odcinek (1999) obejrzało 6,5 mln widzów – duży sukces, dlatego "
            "powstały kolejne odcinki. Do dziś ponad 560 odcinków. Pokazuje codzienne życie "
            "zwykłych ludzi. Ferdynand Kiepski nie może znaleźć pracy (brak wykształcenia), żona "
            "Halina jest pielęgniarką, sąsiad sprzedaje bieliznę na targu. Początkowo nagrywany w "
            "kamienicy, potem przeniesiono nagrania do studia. Różowy szlafrok Haliny jest w "
            "serialu od pierwszych do ostatnich odcinków. Najnowsze odcinki można oglądać już nie "
            "tylko w telewizji, ale także w internecie.",
            "TAK/NIE: Pierwszy odcinek serialu był nieudany.",
            ["TAK", "NIE"], 1, "НІ — перший епізод був великим успіхом (6,5 млн глядачів)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Nagrywanie kolejnych odcinków zależało od zainteresowania widzów.",
            ["TAK", "NIE"], 0, "ТАК — «sukces, dlatego powstały kolejne odcinki»."),
    MCQItem("czytanie", "",
            "TAK/NIE: Bohaterowie serialu należą do najbogatszych ludzi w Polsce.",
            ["TAK", "NIE"], 1, "НІ — серіал показує звичайних людей."),
    MCQItem("czytanie", "",
            "TAK/NIE: Sąsiad Ferdynanda zajmuje się handlem.",
            ["TAK", "NIE"], 0, "ТАК — «sąsiad sprzedaje bieliznę na targu»."),
    MCQItem("czytanie", "",
            "TAK/NIE: Serial od początku jest nagrywany w studiu filmowym.",
            ["TAK", "NIE"], 1, "НІ — спершу знімали в kamienicy, потім перенесли в студію."),
    MCQItem("czytanie", "",
            "TAK/NIE: Niektóre przedmioty można zobaczyć w serialu od pierwszych odcinków aż do dziś.",
            ["TAK", "NIE"], 0, "ТАК — рожевий szlafrok Haliny від перших до останніх епізодів."),
    MCQItem("czytanie", "",
            "TAK/NIE: Cały serial jest dostępny w telewizji i w internecie.",
            ["TAK", "NIE"], 1, "НІ — лише НАЙНОВІШІ епізоди також в інтернеті, не весь серіал."),
    # ── Zad V: обери найкращий варіант у дужках (текст про свято Holi) ──────
    MCQItem("czytanie",
            "Текст про індійське свято кольорів Holi. Обери найкраще слово.",
            "Na ulicach można ___ radość.",
            ["widać", "zobaczyć", "przeglądać"], 1,
            "«можна + інфінітив» → <b>zobaczyć</b> (побачити). «можна widać» — граматично хибно."),
    MCQItem("czytanie", "",
            "Ludzie są dla siebie bardziej serdeczni niż ___.",
            ["zwykle", "często", "rzadko"], 0,
            "«ніж зазвичай» → <b>zwykle</b>."),
    MCQItem("czytanie", "",
            "___ dnia rano odbywa się karnawał kolorów.",
            ["Następnego", "dalszego", "przyszłego"], 0,
            "наступного дня → <b>Następnego</b> (dalszego/przyszłego dnia так не кажуть)."),
    MCQItem("czytanie", "",
            "Uczestnicy ___ przyjaciół i rodzinę, żeby podzielić się radością.",
            ["zwiedzają", "odwiedzają", "widzą"], 1,
            "⚠️ фальшивий друг: <b>odwiedzają</b> = відвідують ЛЮДЕЙ; zwiedzać = оглядати "
            "місця (музей, місто)."),
    MCQItem("czytanie", "",
            "W Polsce także ___ to święto – nazywa się Festiwal Kolorów.",
            ["odbywamy", "obchodzimy", "bierzemy"], 1,
            "«obchodzić święto» = святкувати → <b>obchodzimy</b>."),
    MCQItem("czytanie", "",
            "Jednak nie ma wiele ___ z kulturą Indii.",
            ["takiego samego", "identycznego", "wspólnego"], 2,
            "стійкий вислів «mieć wspólnego z» = мати спільне → <b>wspólnego</b>."),
    MCQItem("czytanie", "",
            "To ma być przede wszystkim dobra ___.",
            ["gra", "zabawa", "nauka"], 1,
            "добра розвага → <b>zabawa</b> (gra = гра за правилами)."),
    MCQItem("czytanie", "",
            "Dla uczestników przygotowano wiele dodatkowych ___.",
            ["spektakli", "pomysłów", "atrakcji"], 2,
            "багато атракцій/розваг → <b>atrakcji</b>."),
]

# ── GRAMATYKA — Zad I: підкресли правильну форму (відмінювання) ──────────
# «podkreślić poprawne formy» = вибір 1 з 3 = MCQ. Ключ звірено з klucz PDF.
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka",
            "Текст про шкільні лектури (учень Mateusz ділиться враженнями).",
            "W szkole czytamy wiele ___ – ale czy wszystkie podobają się nam tak samo?",
            ["książki", "książek", "książkach"], 1,
            "wiele + родовий множини → <b>książek</b>."),
    MCQItem("gramatyka", "",
            "Czy wszystkie podobają się ___ tak samo?",
            ["nam", "nas", "nami"], 0,
            "podobać się + давальний → <b>nam</b> (нам)."),
    MCQItem("gramatyka", "",
            "Poprosiliśmy ___ ludzi, żeby opisali te, które zapamiętali.",
            ["młodzi", "młodymi", "młodych"], 2,
            "poprosić кого? знахідний → <b>młodych</b> ludzi."),
    MCQItem("gramatyka", "",
            "Mateusz zna opinie ___ o różnych lekturach.",
            ["koledzy", "kolegom", "kolegów"], 2,
            "opinie кого? родовий множини → <b>kolegów</b>."),
    MCQItem("gramatyka", "",
            "Uważa, że przeczytał już ___ najtrudniejszą lekturę.",
            ["tej", "te", "tę"], 2,
            "знахідний однини жін. роду → <b>tę</b>."),
    MCQItem("gramatyka", "",
            "Historia w „Krzyżakach” jest dosyć ___.",
            ["ciekawą", "ciekawa", "ciekawej"], 1,
            "jest + називний (яка?) → <b>ciekawa</b>."),
    MCQItem("gramatyka", "",
            "…ale napisana trudnym ___.",
            ["językiem", "języka", "języku"], 0,
            "napisana чим? орудний → <b>językiem</b>."),
    MCQItem("gramatyka", "",
            "„Krzyżaków” czytałem razem z ___.",
            ["rodzicach", "rodzicami", "rodziców"], 1,
            "z + орудний → <b>rodzicami</b>."),
    MCQItem("gramatyka", "",
            "Musiałem pytać, co znaczą ___ słowa.",
            ["dawni", "dawne", "dawnymi"], 1,
            "słowa (ніяк. множина, наз./знах.) → <b>dawne</b>."),
    MCQItem("gramatyka", "",
            "Ale już po kilku ___ wiedziałem, że to książka dla mnie.",
            ["stron", "stronach", "strony"], 1,
            "po + місцевий → <b>stronach</b>."),
    # ── Zad III: підкресли правильну форму (ступенювання) ──────────────
    MCQItem("gramatyka",
            "Текст про активних сеньйорів на пенсії.",
            "Starzy ludzie nie chcą być ___ od młodych.",
            ["gorszymi", "gorsi", "najgorsze"], 1,
            "być + називний множини чол.-особ. → <b>gorsi</b> (вищий ступінь від zły)."),
    MCQItem("gramatyka", "",
            "Emeryci mają ___ obowiązków, więc mają czas na pasje.",
            ["mniej", "mniejszych", "najmniejsze"], 0,
            "___ + родовий (менше чого?) → <b>mniej</b> obowiązków."),
    MCQItem("gramatyka", "",
            "___ wybierane przez seniorów formy aktywności to sport i podróże.",
            ["Częste", "Najczęstsze", "Najczęściej"], 2,
            "прислівник при дієприкметнику → <b>Najczęściej</b> (найчастіше)."),
    MCQItem("gramatyka", "",
            "Dzisiaj jest ___ niż kiedyś rozwijać niezwykłe zainteresowania.",
            ["łatwo", "łatwiej", "łatwiejszy"], 1,
            "порівняння (niż) → вищий ступінь прислівника → <b>łatwiej</b>."),
    MCQItem("gramatyka", "",
            "Pan Jurek zajął się grafiką i teraz jest w tym ___ od swojego wnuka.",
            ["lepiej", "najlepszy", "lepszy"], 2,
            "jest ___ od… → вищий ступінь прикметника → <b>lepszy</b>."),
    # ── Zad II: сполучники з рамки (luki z ramki, 1 зайвий) → MCQ-per-gap ──
    # Банк: że/oraz/ale/czyli/ani/więc (приклад «chociaż» вже використано; зайве — ani).
    MCQItem("gramatyka",
            "Текст про «Niemy Chór». Встав сполучник із рамки (одне слово — зайве: <i>ani</i>).",
            "Studenci używają języka migowego, ___ języka osób niesłyszących.",
            ["że", "oraz", "ale", "czyli", "ani", "więc"], 3,
            "пояснення/уточнення («тобто») → <b>czyli</b>."),
    MCQItem("gramatyka", "",
            "W chórze występują osoby po kursach tego języka ___ tacy, którzy go nie znają…",
            ["że", "oraz", "ale", "czyli", "ani", "więc"], 1,
            "перелік («та/і») → <b>oraz</b>."),
    MCQItem("gramatyka", "",
            "…tacy, którzy go nie znają, ___ bardzo chcą się go nauczyć.",
            ["że", "oraz", "ale", "czyli", "ani", "więc"], 2,
            "протиставлення («але») → <b>ale</b>."),
    MCQItem("gramatyka", "",
            "Utwory są tak ciekawe, ___ wszyscy mogą się czegoś nowego dowiedzieć.",
            ["że", "oraz", "ale", "czyli", "ani", "więc"], 0,
            "конструкція «tak… ___» (так… що) → <b>że</b>."),
    MCQItem("gramatyka", "",
            "Zainteresowanie chórem rośnie, ___ spotkania muszą odbywać się coraz częściej.",
            ["że", "oraz", "ale", "czyli", "ani", "więc"], 5,
            "наслідок («тому/отже») → <b>więc</b>."),
]

EXAM = Exam(
    id="2020",
    label="Пробний тест 2020 (офіц.)",
    kind="sample",
    year=2020,
    items=_READING + _GRAMMAR,
)
