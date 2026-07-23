"""Офіційний ПРОБНИЙ тест B1 2020 (certyfikatpolski.pl /2020/12/B1_przykladowy_test_2020_03.pdf).

ДОСЛІВНО з arkusz, КОЖЕН ключ звірено з офіц. klucz PDF. Покрито майже весь тест:
- Czytanie: Zad I (a/b/c ×5), Zad II (TAK/NIE ×7), Zad V (вибір слова ×8) — MCQ;
  Zad III/IV — matching (tasks нижче);
- Gramatyka (усі 8 Zad): I(форми ×10), II(сполучники ×5), III(ступенювання ×5),
  VII(вид/способи ×10), VIII(прийменники ×5) — MCQ; IV(форми ×10) + V(питання ×5) —
  free-fill (tasks); VI(трансформація ×5) — open (tasks).
Лишилось для повного 2020: лише Słuchanie (аудіо + транскрипти).
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

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
            "Текст про «Niemy Chór». Встав сполучник із рамки (одне слово — зайве: <b>ani</b>).",
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
    # ── Zad VII: підкресли правильну форму (вид і способи дієслова) ────────
    MCQItem("gramatyka",
            "Діалог Adama й Piotra: що б вони зробили, маючи багато грошей.",
            "___, czy wtedy ty i twoja żona kupilibyście wszystko, o czym marzycie?",
            ["Powiedziałbyś", "Mówcie", "Powiedz"], 2,
            "наказовий спосіб до «ty» → <b>Powiedz</b> (скажи)."),
    MCQItem("gramatyka", "",
            "Czy ty i żona od razu ___ wszystko, o czym marzycie?",
            ["kupujcie", "kupilibyście", "kupiliby"], 1,
            "умовний спосіб, 2 ос. мн. (wy) → <b>kupilibyście</b>."),
    MCQItem("gramatyka", "",
            "Nie wiem, ___ się dłużej nad tym zastanowić.",
            ["musiałem", "musiałbym", "musiałybyśmy"], 1,
            "умовний, 1 ос. одн. чол. → <b>musiałbym</b>."),
    MCQItem("gramatyka", "",
            "Myślę, że często byśmy ___ innym.",
            ["pomogli", "pomagaliśmy", "pomagali"], 2,
            "«byśmy ___» — умовний, форма на -li → <b>pomagali</b>."),
    MCQItem("gramatyka", "",
            "Moja córka pewnie ___, żeby kupić jedzenie dla zwierząt.",
            ["proponowałabym", "proponuje", "zaproponowałaby"], 2,
            "умовний, 3 ос. одн. жін. → <b>zaproponowałaby</b>."),
    MCQItem("gramatyka", "",
            "…a syn by ___ dać pieniądze na ubrania sportowe.",
            ["wolałby", "wolał", "woli"], 1,
            "розділена частка «by ___» + форма на -ł → <b>wolał</b> (умовний)."),
    MCQItem("gramatyka", "",
            "Proszę was, ___ o naszym dziadku.",
            ["pamiętajcie", "pamiętalibyśmy", "zapamiętajcie"], 0,
            "наказовий спосіб до «wy», недок. вид → <b>pamiętajcie</b>."),
    MCQItem("gramatyka", "",
            "___ w nim wygodnie resztę życia.",
            ["Niech spędzi", "Spędzałby", "Spędziłaby"], 0,
            "спонукання до 3 ос. → <b>Niech spędzi</b>."),
    MCQItem("gramatyka", "",
            "Jestem pewien, że tam ___ w pierwszej kolejności.",
            ["pojechalibyśmy", "jedźmy", "pojechaliby"], 0,
            "умовний, 1 ос. мн. (my) → <b>pojechalibyśmy</b>."),
    MCQItem("gramatyka", "",
            "Niech każdy z was ___ swój pomysł na kartce.",
            ["piszcie", "napiszcie", "napisze"], 2,
            "«każdy» = 3 ос. одн. → <b>napisze</b>."),
    # ── Zad VIII: прийменники з рамки (luki z ramki, 1 зайвий: z) → MCQ-per-gap ──
    # Банк: do/w/nad/przed/z/na (приклад «w»). Текст: Piotr i Ola шукають домик на море.
    MCQItem("gramatyka",
            "Текст: Piotr і Ola шукають дачний будиночок. Встав прийменник (зайве слово — <b>z</b>).",
            "Kilka miesięcy ___ wakacjami szukali domku.",
            ["do", "w", "nad", "przed", "z", "na"], 3,
            "przed + орудний (часу — «перед») → <b>przed</b> wakacjami."),
    MCQItem("gramatyka", "",
            "Szukali ___ internecie ładnego domku kampingowego.",
            ["do", "w", "nad", "przed", "z", "na"], 1,
            "w + місцевий (де?) → <b>w</b> internecie."),
    MCQItem("gramatyka", "",
            "…domku kampingowego ___ polskim morzem.",
            ["do", "w", "nad", "przed", "z", "na"], 2,
            "nad + орудний (над/біля води) → <b>nad</b> morzem."),
    MCQItem("gramatyka", "",
            "Chcieli wynająć go ___ trzy tygodnie.",
            ["do", "w", "nad", "przed", "z", "na"], 5,
            "na + знахідний (на який період) → <b>na</b> trzy tygodnie."),
    MCQItem("gramatyka", "",
            "Zdecydowali się na dwutygodniowy wyjazd ___ Grecji.",
            ["do", "w", "nad", "przed", "z", "na"], 0,
            "do + родовий (напрямок «куди») → <b>do</b> Grecji."),
]

# ── CZYTANIE — Zad III: вставити фрагменти (A–H) у текст про кіберспорт ──
# Приклад (PRZYKŁAD) = фрагмент C → у пул не входить. Ключ (klucz): 1-D,2-B,3-E,4-G,5-A,6-H,7-F.
_ZAD3 = MatchTask(
    section="czytanie",
    title="Читання Zad III — встав фрагменти в текст (e-sport)",
    intro=(
        "Прочитай текст про комп'ютерні ігри та e-sport. Кожен пропуск (1–7) треба "
        "заповнити одним із фрагментів A–G. Читай, який фрагмент логічно й граматично "
        "продовжує речення.\n\n<i>«Раніше, щоб зіграти у футбол, треба було зустрітися з "
        "друзями… Сьогодні діти дедалі частіше обирають гру на комп'ютері…»</i>"
    ),
    options=[
        "natomiast teraz także w telewizji",  # A
        "ale powoli stają się pracą i źródłem dochodów",  # B
        "a nawet z mieszkańcami innych kontynentów",  # D
        "w tym także w Polsce",  # E
        "którzy interesują się e-sportem",  # F
        "że oglądają je ludzie z całego świata",  # G
        "w której uczą się przyszli zawodnicy",  # H
    ],
    prompts=[
        "1. Grają z rodziną, kolegami, przyjaciółmi, ze znajomymi z całej Polski, ___",
        "2. Gry nie są już tylko rozrywką, ___",
        "3. Turnieje e-sportowe odbywają się już w wielu krajach, ___",
        "4. Widowiska te są tak bardzo popularne, ___",
        "5. Kiedyś można je było oglądać tylko w internecie, ___",
        "6. W jednej z polskich szkół powstała nawet klasa, ___",
        "7. Stają się oni idolami nastolatków, ___",
    ],
    key=[2, 1, 3, 5, 0, 6, 4],  # D,B,E,G,A,H,F
    explain=[
        "нарощення переліку («навіть з мешканцями інших континентів») → C.",
        "протиставлення «не лише розвага, ___» → B (але стають працею й джерелом доходу).",
        "«у багатьох країнах, ___» → D (зокрема й у Польщі).",
        "конструкція «tak popularne, ___» (такі популярні, що…) → F.",
        "контраст kiedyś/teraz: «tylko w internecie, ___» → A (натомість тепер і в ТБ).",
        "означальне речення «klasa, ___» → G (у якій навчаються майбутні гравці).",
        "означальне речення «idolami nastolatków, ___» → E (які цікавляться e-sportem).",
    ],
)

# ── CZYTANIE — Zad IV: зіставити заголовки з фрагментами (A–H) ──────────
# Приклад: «Pierwszy raz w Polsce» → B (у пул не входить). Ключ: 1-H,2-E,3-C,4-G,5-A,6-F,7-D.
_ZAD4 = MatchTask(
    section="czytanie",
    title="Читання Zad IV — добери заголовок до тексту",
    intro=(
        "«W Polsce ciągle coś się dzieje!» До кожного заголовка (1–7) добери правильний "
        "фрагмент новини A–G. Читай суть кожного повідомлення."
    ),
    options=[
        "Trzeba mieć ukończone 21 lat i średnie wykształcenie. Zarobki powinny być wysokie, "
        "szczególnie dla tych, którzy zdadzą dobrze egzaminy.",  # A
        "Restauracja „Nowa” ogłosiła zimową promocję. W niedziele (od grudnia do końca lutego) "
        "będzie można kupić niektóre dania o 50% taniej.",  # C
        "Od 1 kwietnia będziemy musieli dzielić śmieci na więcej grup niż do tej pory. "
        "Nowością będą obowiązkowe brązowe kosze na odpady BIO.",  # D
        "Palenie w domowych piecach to jedna z przyczyn powstawania smogu, dlatego zimą "
        "częściej pojawiają się infekcje gardła, kaszel, astma.",  # E
        "W ostatnich latach więcej płacimy za mięso, masło, jajka i czekoladę. Wzrost cen "
        "z roku na rok staje się bardziej odczuwalny.",  # F
        "Od nowego roku ceny za wywiezienie śmieci będą wyższe, a tych, którzy nie będą "
        "segregować, czekają kary.",  # G
        "Straż miejska wypisuje mandaty wszystkim zmotoryzowanym, którzy nie przestrzegają "
        "nowych przepisów.",  # H
    ],
    prompts=[
        "1. Kary dla kierowców",
        "2. Choroby w okresie zimowym",
        "3. Za pół ceny",
        "4. Opłaty w górę",
        "5. Praca w straży miejskiej",
        "6. Zakupy coraz droższe",
        "7. Nowe zasady segregacji",
    ],
    key=[6, 3, 1, 5, 0, 4, 2],  # H,E,C,G,A,F,D
    explain=[
        "штрафи водіям → G (straż miejska виписує мандати водіям).",
        "хвороби взимку → D (смог, інфекції горла, кашель).",
        "за півціни → B (промоція −50% у ресторані).",
        "плата вгору → F (ціни за вивіз сміття вищі + штрафи).",
        "робота в міській варті → A (вимоги: 21 рік, освіта, іспити).",
        "покупки дорожчають → E (більше платимо за м'ясо, масло, яйця).",
        "нові правила сортування → C (від 1 квітня більше груп, кошики BIO).",
    ],
)

_MATCHING = [_ZAD3, _ZAD4]

# ── GRAMATYKA — Zad IV: вписати форми дієслів (тепер./майб. час) → free-fill ──
# Ключ звірено з klucz PDF; варіанти («/») внесено як окремі прийнятні відповіді.
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="Граматика Zad IV — впиши форму дієслова",
    intro=(
        "Впиши правильну форму дієслова (у дужках — інфінітив; час теперішній або "
        "майбутній). Текст про «Łódź Design Festival».\n\n"
        "<i>Приклад: co roku <b>zaprasza</b> (zapraszać) projektantów w nadziei, że "
        "<b>pokażą</b> (pokazać) nowe trendy.</i>"
    ),
    prompts=[
        "1. …o tym, co ___ (dawać) nam poczucie komfortu",
        "2. …w jaki sposób na potrzeby człowieka ___ (odpowiadać) artyści",
        "3. – ___ (mówić) Michał Piernikowski, dyrektor",
        "4. …jak ___ (my — pracować) za kilkanaście lat",
        "5. …jak nasze miejsca pracy się ___ (zmienić) za jakiś czas",
        "6. Katarzyna Dubik z biura organizacyjnego ___ (informować):",
        "7. Do Łodzi ___ (przyjechać) najważniejsi projektanci",
        "8. …a jutro ___ (my — mieć) ogromną przyjemność gościć artystów",
        "9. …artystów ze Szwecji, którzy ___ (poprowadzić) warsztaty dla dzieci",
        "10. Już wkrótce wszyscy ___ (móc) oglądać festiwalowe wystawy",
    ],
    accepted=[
        ["daje"],
        ["odpowiadają"],
        ["mówi"],
        ["będziemy pracowali", "będziemy pracować"],
        ["zmienią"],
        ["informuje"],
        ["przyjadą"],
        ["będziemy mieli", "będziemy mieć"],
        ["poprowadzą"],
        ["będą mogli", "będziemy mogli"],
    ],
    explain=[
        "теперішній час, 3 ос. одн. (co = воно) → <b>daje</b>.",
        "теперішній, 3 ос. мн. (artyści) → <b>odpowiadają</b>.",
        "теперішній, 3 ос. одн. (Michał) → <b>mówi</b>.",
        "майбутній, 1 ос. мн. (my) → <b>będziemy pracowali</b> (або <b>będziemy pracować</b>).",
        "майбутній доконаний, 3 ос. мн. (miejsca się) → <b>zmienią</b>.",
        "теперішній, 3 ос. одн. (Katarzyna) → <b>informuje</b>.",
        "майбутній доконаний, 3 ос. мн. (projektanci) → <b>przyjadą</b>.",
        "майбутній, 1 ос. мн. (my) → <b>będziemy mieli</b> (або <b>będziemy mieć</b>).",
        "майбутній доконаний, 3 ос. мн. (którzy) → <b>poprowadzą</b>.",
        "майбутній, 3 ос. мн. (wszyscy) → <b>będą mogli</b> (або <b>będziemy mogli</b>).",
    ],
)

# ── GRAMATYKA — Zad VI: трансформація речення (зберегти сенс) → open ────
# Однозначного ключа нема (офіц. «зараховувати всі інші правильні»). Зразки з klucz PDF.
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="Граматика Zad VI — перетвори речення",
    intro=(
        "Перепиши речення так, щоб зберегти той самий сенс, ОБОВ'ЯЗКОВО вживши слово з "
        "дужок (у потрібній формі). Пиши кожне речення текстом.\n\n"
        "<i>Приклад: «Anna lubi literaturę polską.» (interesuje się) → "
        "Anna interesuje się literaturą polską.</i>\n\n"
        "📊 Оцінює AI за офіційним зразком (можливі й інші правильні варіанти)."
    ),
    criterion="Той самий сенс, що в оригіналі + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Joanna przyglądała się małemu kotu.",
        "W twoim pokoju zawsze jest bałagan.",
        "Marta bez przerwy wspomina ten koncert.",
        "Wczoraj Michał był w teatrze pierwszy raz w życiu.",
        "Czy znasz adres tego sklepu?",
    ],
    words=["obserwowała", "porządku", "opowiada", "poszedł", "wiesz"],
    models=[
        ["Joanna obserwowała małego kota."],
        ["W twoim pokoju nigdy nie ma porządku."],
        ["Marta bez przerwy opowiada o tym koncercie."],
        ["Wczoraj Michał poszedł do teatru pierwszy raz w życiu."],
        ["Czy wiesz, jaki jest adres tego sklepu?", "Czy wiesz, jaki adres ma ten sklep?"],
    ],
)

# ── GRAMATYKA — Zad V: постав питання до підкресленого → free-fill ──────
# Фокус — питальне слово (перевіряє відмінок). Ключ (klucz) з варіантами.
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="Граматика Zad V — постав питання",
    intro=(
        "Постав питання до виділеної в «лапках» частини речення. Впиши ЛИШЕ питальне "
        "слово (одне-два), з якого почнеться питання.\n\n"
        "<i>Приклад: «Nasza decyzja będzie zależeć od pogody» (від «od pogody») → "
        "Od czego?</i>"
    ),
    prompts=[
        "Michał próbował podzielić jabłko «widelcem».",
        "Koledzy czekali «dwa tygodnie» na wyniki egzaminu.",
        "Znalazłem to ogłoszenie «w sklepie».",
        "Matka pomogła «Piotrowi» znaleźć pracę.",
        "Anna czekała na schodach «na koleżankę».",
    ],
    accepted=[
        ["czym", "w jaki sposób"],
        ["jak długo", "ile tygodni", "ile czasu"],
        ["gdzie"],
        ["komu"],
        ["na kogo"],
    ],
    explain=[
        "widelcem — орудний (чим?) → <b>Czym?</b> (або W jaki sposób?)",
        "dwa tygodnie — тривалість → <b>Jak długo?</b> (Ile czasu? / Ile tygodni?)",
        "w sklepie — місце → <b>Gdzie?</b>",
        "Piotrowi — давальний (кому?) → <b>Komu?</b>",
        "na koleżankę — na + знахідний → <b>Na kogo?</b>",
    ],
)

EXAM = Exam(
    id="2020",
    label="Пробний тест 2020 (офіц.)",
    kind="sample",
    year=2020,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
