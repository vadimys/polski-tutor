"""Офіційний ПРОБНИЙ тест B1 2020 (certyfikatpolski.pl /2020/12/B1_przykladowy_test_2020_03.pdf).

Наразі авто-оцінювані MCQ-завдання, ДОСЛІВНО з arkusz, ключ звірено з офіц. klucz PDF:
- Czytanie Zad I (a/b/c ×5) + Zad II (TAK/NIE ×7) + Zad V (вибір слова ×8);
- Gramatyka Zad I (форми ×10) + Zad III (ступенювання ×5) + Zad II (сполучники ×5).
Разом 40 авто-оцінюваних питань. Решта (dopasowanie Czyt III/IV, форми Gram IV,
pytania/transformacje Gram V/VI, аудіювання) — після рушіїв відповідних типів.
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem

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
        "нарощення переліку («навіть з мешканцями інших континентів») → D.",
        "протиставлення «не лише розвага, ___» → B (але стають працею й джерелом доходу).",
        "«у багатьох країнах, ___» → E (зокрема й у Польщі).",
        "конструкція «tak popularne, ___» (такі популярні, що…) → G.",
        "контраст kiedyś/teraz: «tylko w internecie, ___» → A (натомість тепер і в ТБ).",
        "означальне речення «klasa, ___» → H (у якій навчаються майбутні гравці).",
        "означальне речення «idolami nastolatków, ___» → F (які цікавляться e-sportem).",
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
        "штрафи водіям → H (straż miejska виписує мандати водіям).",
        "хвороби взимку → E (смог, інфекції горла, кашель).",
        "за півціни → C (промоція −50% у ресторані).",
        "плата вгору → G (ціни за вивіз сміття вищі + штрафи).",
        "робота в міській варті → A (вимоги: 21 рік, освіта, іспити).",
        "покупки дорожчають → F (більше платимо за м'ясо, масло, яйця).",
        "нові правила сортування → D (від 1 квітня більше груп, кошики BIO).",
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

EXAM = Exam(
    id="2020",
    label="Пробний тест 2020 (офіц.)",
    kind="sample",
    year=2020,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4],
)
