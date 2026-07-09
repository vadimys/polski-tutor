"""Офіційний ПРОБНИЙ тест B1 2020 (certyfikatpolski.pl /2020/12/B1_przykladowy_test_2020_03.pdf).

Наразі — секція Czytanie, Zad I (a/b/c ×5) + Zad II (TAK/NIE ×7), ДОСЛІВНО з arkusz;
ключ звірено з офіційним klucz PDF (Zad I: a,b,c,a,c; Zad II: NIE,TAK,NIE,TAK,NIE,TAK,NIE).
Решта завдань (dopasowanie/luki/граматика) додаються після рушіїв відповідних типів.
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
]

EXAM = Exam(
    id="2020",
    label="Пробний тест 2020 (офіц.)",
    kind="sample",
    year=2020,
    items=_READING,
)
