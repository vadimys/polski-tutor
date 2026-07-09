"""Офіційний ПРОБНИЙ тест B1 2019 (certyfikatpolski.pl /2019/09/B1_test.pdf).

Секції Czytanie (Rozumienie tekstów pisanych) і Gramatyka (Poprawność gramatyczna) —
дослівно з тесту. Ключ: граматика за правилами польської, читання зі змісту текстів.
Нічого не вигадано. Мігровано зі старого services/mock.py без змін.
"""

from __future__ import annotations

from app.content.schema import Exam, MCQItem

# ── CZYTANIE (Rozumienie tekstów pisanych) ──────────────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Jeśli masz ponad 30 lat i zarejestrowałeś się jako bezrobotny, możesz otrzymać "
            "pomoc finansową na otwarcie firmy. Projekt adresowany jest też do osób po 50. roku "
            "życia o niskich kwalifikacjach.",
            "Z tekstu wynika, że z projektu może skorzystać:",
            ["każdy, kto chce otworzyć własną firmę", "bezrobotny powyżej 30. roku życia",
             "każda osoba bez wykształcenia"], 1,
            "У тексті: безробітний >30 років. «Кожен» і «без освіти» — надто загально."),
    MCQItem("czytanie",
            "Od października działa nowy klub fitness. Przez pierwsze dwa tygodnie zajęcia grupowe "
            "są bezpłatne. Do dyspozycji jest siłownia, szatnie z prysznicami i bufet.",
            "Z tekstu wynika, że w klubie fitness:",
            ["po zajęciach można się wykąpać", "przez cały rok zajęcia są za darmo",
             "popularni instruktorzy prowadzą bufet"], 0,
            "Є «szatnie z prysznicami» → можна викупатись. Безкоштовно лише 2 тижні."),
    MCQItem("czytanie",
            "Obraz Tamary Łempickiej sprzedano za blisko 9,1 mln dolarów. Nikt nie myślał, że kwota "
            "będzie tak wysoka. To najdroższy w historii obraz polskiego artysty.",
            "Z tekstu wynika, że:",
            ["to najdroższy obraz na świecie", "cena obrazu była dla wszystkich zaskoczeniem",
             "obraz kupił amerykański biznesmen"], 1,
            "«Nikt nie myślał, że tak wysoka» = несподіванка. Найдорожчий польського, не світу."),
    MCQItem("czytanie",
            "Już trzeci raz najlepszą polską uczelnią ekonomiczną została Szkoła Główna Handlowa. "
            "W konkursie brało udział sześć uniwersytetów i 28 wydziałów.",
            "Z tekstu wynika, że:",
            ["w rankingu znalazło się 28 uczelni", "konkurs zorganizowały szkoły i media",
             "Szkoła Główna Handlowa niejednokrotnie wygrała ten konkurs"], 2,
            "«Już trzeci raz» = не раз перемагала. 28 — це wydziały, не uczelnie."),
    MCQItem("czytanie",
            "TEKST: W pierwszej połowie 2016 r. aż 256 lotów jednej z linii było opóźnionych o "
            "więcej niż 3 godziny. Zgodnie z prawem UE pasażerowie mogą dostać zwrot za lot "
            "(nawet 600 euro, zależnie od długości), jeśli rejs odwołano krócej niż 14 dni przed "
            "wylotem lub opóźniono o ponad 3 godziny. Linie nie podają statystyk opóźnień. "
            "Pasażerowie często rezygnują, bo to skomplikowane. Rozwijają się firmy, które pomagają "
            "odzyskać pieniądze.",
            "TAK/NIE: W ciągu pół roku 256 lotów jednej z linii było opóźnionych o ponad 3 godziny.",
            ["TAK", "NIE"], 0, "У тексті прямо: 256 lotów, >3 godziny."),
    MCQItem("czytanie", "",
            "TAK/NIE: Według przepisów pasażerowie mogą otrzymać pieniądze za opóźniony lub "
            "odwołany lot.", ["TAK", "NIE"], 0, "Так, згідно з правом ЄС."),
    MCQItem("czytanie", "",
            "TAK/NIE: Linie lotnicze regularnie publikują dane o faktycznych godzinach lądowania.",
            ["TAK", "NIE"], 1, "Ні — «takich informacji nie podają linie lotnicze»."),
    MCQItem("czytanie", "",
            "TAK/NIE: Pieniądze mogą być zwrócone, jeśli lot odwołano tydzień przed wylotem.",
            ["TAK", "NIE"], 0, "Тиждень (7 днів) < 14 днів → так."),
    MCQItem("czytanie", "",
            "TAK/NIE: Za anulowanie każdego biletu pasażerowie zawsze dostają 600 euro.",
            ["TAK", "NIE"], 1, "Ні — «nawet 600 euro», залежить від довжини рейсу."),
    MCQItem("czytanie", "",
            "TAK/NIE: Formularze o zwrot pasażerowie wypełniają zazwyczaj starannie i szybko.",
            ["TAK", "NIE"], 1, "Ні — часто відмовляються, бо це складно."),
    MCQItem("czytanie", "",
            "TAK/NIE: Pasażerowie mogą liczyć na pomoc specjalnych firm.",
            ["TAK", "NIE"], 0, "Так — «rozwijają się firmy, które pomagają»."),
]

# ── GRAMATYKA (Poprawność gramatyczna) ──────────────────────────────────
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Patrycja i Olaf myślą o ___ większym i wygodniejszym.",
            "Wybierz poprawną formę:", ["czegoś", "czymś", "coś"], 1,
            "Після «o» + прикметник — місцевий: o czymś większym."),
    MCQItem("gramatyka", "Patrycja chce mieszkanie z trzema ___ i dużą kuchnią.",
            "Wybierz poprawną formę:", ["pokojach", "pokoje", "pokojami"], 2,
            "«z trzema» — орудний множини: pokojami."),
    MCQItem("gramatyka", "Olaf potrzebuje ___ balkonu.",
            "Wybierz poprawną formę:", ["słoneczny", "słonecznego", "słonecznemu"], 1,
            "«potrzebować» + родовий: słonecznego."),
    MCQItem("gramatyka", "Olaf potrzebuje słonecznego ___ .",
            "Wybierz poprawną formę:", ["balkonu", "balkon", "balkonowi"], 0,
            "Родовий: balkonu."),
    MCQItem("gramatyka", "Olaf lubi hodować ___ .",
            "Wybierz poprawną formę:", ["kwiatów", "kwiatami", "kwiaty"], 2,
            "«hodować» + знахідний: kwiaty."),
    MCQItem("gramatyka", "Teraz często ___ kupuje na rynku. (kwiaty)",
            "Wybierz poprawną formę:", ["im", "je", "ich"], 1,
            "«kwiaty» → знахідний займенник: je."),
    MCQItem("gramatyka", "Kąpiel to najlepszy relaks po ___ dniu.",
            "Wybierz poprawną formę:", ["męczącym", "męczącego", "męczący"], 0,
            "«po» + місцевий: po męczącym dniu."),
    MCQItem("gramatyka", "Kąpiel to relaks po męczącym ___ .",
            "Wybierz poprawną formę:", ["dzień", "dniu", "dnia"], 1,
            "Місцевий: dniu."),
    MCQItem("gramatyka", "Wygodna wanna jest dla ___ najważniejsza.",
            "Wybierz poprawną formę:", ["niej", "nią", "jej"], 0,
            "«dla» + родовий: dla niej."),
    MCQItem("gramatyka", "Park kiedyś spodoba się ___ .",
            "Wybierz poprawną formę:", ["dziećmi", "dzieciach", "dzieciom"], 2,
            "«spodobać się» + давальний: dzieciom."),
    MCQItem("gramatyka", "To on ___ podkreślał, że chce dużo w życiu.",
            "Wybierz poprawną formę:", ["częstszym", "najczęściej", "częstym"], 1,
            "Прислівник, найвищий ступінь: najczęściej."),
    MCQItem("gramatyka", "Chce wspinać się w górach jeszcze ___ .",
            "Wybierz poprawną formę:", ["wyższy", "najwyżej", "wyżej"], 2,
            "Прислівник, вищий ступінь: wyżej."),
    MCQItem("gramatyka", "Chce jeździć tylko ___ samochodami na świecie.",
            "Wybierz poprawną formę:", ["najszybszymi", "szybszym", "najszybciej"], 0,
            "Прикметник, найвищий, орудний мн.: najszybszymi."),
    MCQItem("gramatyka", "Dziś mówi, że inne sprawy są dużo ___ .",
            "Wybierz poprawną formę:", ["ważniejsze", "ważniej", "najważniejszymi"], 0,
            "Прикметник, вищий ступінь: ważniejsze."),
    MCQItem("gramatyka", "Woli żyć ___ niż kiedyś.",
            "Wybierz poprawną formę:", ["najspokojniej", "spokojniej", "spokojny"], 1,
            "Прислівник, вищий + niż: spokojniej."),
    MCQItem("gramatyka", "Gdybyśmy 10 lat temu posłuchali dziadka, dziś ___ pilotami.",
            "Wybierz poprawną formę:", ["byliśmy", "bylibyśmy", "byli"], 1,
            "Умовний наслідок: bylibyśmy."),
    MCQItem("gramatyka", "Gdybym tylko wtedy ___, co planuje dziadek…",
            "Wybierz poprawną formę:", ["wiedział", "wiedziałem", "wiedzieli"], 0,
            "Після «gdybym» — форма без -em: gdybym wiedział."),
    MCQItem("gramatyka", "Gdyby ___, spędzaliby całe dnie na lotnisku.",
            "Wybierz poprawną formę:", ["mogli", "mogły", "mogliby"], 2,
            "Умовний (чол.-ос.): mogliby."),
    MCQItem("gramatyka", "Dziadek powiedział: «___ jak najlepiej liceum!»",
            "Wybierz poprawną formę:", ["Kończyliby", "Skończcie", "Skończ"], 1,
            "Наказовий, множина (до обох): Skończcie."),
    MCQItem("gramatyka", "«Dziadku, nie ___!» — powiedzieli chłopcy.",
            "Wybierz poprawną formę:", ["żartuj", "zażartowałbyś", "zażartujcie"], 0,
            "Наказовий однини (до дідуся): nie żartuj."),
    MCQItem("gramatyka", "«Skąd ___ tyle pieniędzy?» — spytali.",
            "Wybierz poprawną formę:", ["weź", "brałby", "wziąłbyś"], 2,
            "Умовне запитання (ти): wziąłbyś."),
    MCQItem("gramatyka", "Gdyby wtedy ___ słowa dziadka poważnie, dziś byłoby inaczej.",
            "Wybierz poprawną formę:", ["traktowaliśmy", "potraktowali", "potraktowaliby"], 1,
            "«gdyby» вже несе -by → potraktowali."),
    MCQItem("gramatyka", "Ich kariery zawodowe ___ inaczej.",
            "Wybierz poprawną formę:", ["wyglądajmy", "wyglądałby", "wyglądałyby"], 2,
            "«kariery» (не-чол.-ос.) умовний: wyglądałyby."),
]

EXAM = Exam(
    id="2019",
    label="Пробний тест 2019 (офіц.)",
    kind="sample",
    year=2019,
    items=_READING + _GRAMMAR,
)
