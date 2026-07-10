"""Модуль аудіювання (Słuchanie) — на ОФІЦІЙНИХ матеріалах Держкомісії.

Транскрипти записів, питання й КЛЮЧ відповідей — з офіц. збірника ROZUMIENIE ZE
SŁUCHU B1 (розділ «KLUCZ I TRANSKRYPCJA NAGRAŃ», /tmp/b1_sluchanie.txt). Текст
озвучуємо локальним TTS (piper); якщо TTS недоступний — показуємо транскрипт.
Жодних вигаданих відповідей: усе з офіційного ключа.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class LQ:
    text: str
    options: list[str]
    correct: int  # з офіційного ключа
    explain: str = ""


@dataclass
class Segment:
    audio: str  # текст запису для озвучення (verbatim з транскрипту)
    questions: list[LQ] = field(default_factory=list)


@dataclass
class Exercise:
    id: str
    title: str
    intro: str
    segments: list[Segment]


SOURCE = "офіційний зразок Держкомісії (B1)"

_TAKNIE = ["TAK", "NIE"]

# спільні описи-опції для Zad V тесту 2020 (порядок A-F; C — дистрактор із прикладу)
_ZAD5_OPTS = [
    "sport, który nie wymagał specjalnego stroju",  # A
    "dyscyplina, w której Polacy odnosili sukcesy",  # B
    "sport tak samo popularny jak jazda na nartach",  # C (przykład: hokej)
    "aktywność związana też z turystyką",  # D
    "sport stosunkowo niedrogi",  # E
    "dyscyplina związana z modą sportową",  # F
]

EXERCISES: list[Exercise] = [
    # Zadanie I — короткі висловлювання: «до чого належить фраза» (офіц. ключ I)
    Exercise(
        "u1", "Krótkie wypowiedzi (Zadanie 1)",
        "Прослухай коротку фразу й обери, де/що це. (на іспиті — лунає ОДИН раз)",
        [
            Segment("Czy jest jeszcze świeży chleb?",
                    [LQ("Taką wypowiedź najczęściej słyszymy:",
                        ["w restauracji", "w cukierni", "w sklepie spożywczym"], 2)]),
            Segment("Wszystkiego najlepszego na nowej drodze życia!",
                    [LQ("Taką wypowiedź najczęściej słyszymy:",
                        ["po egzaminie dyplomowym", "po ceremonii ślubnej", "po otrzymaniu awansu"], 1)]),
            Segment("Obiady wydajemy od trzynastej do piętnastej.",
                    [LQ("Ta wypowiedź jest typowa:", ["w barze", "w domu", "w kawiarni"], 0)]),
            Segment("Dałbyś już spokój!",
                    [LQ("Ta wypowiedź znaczy:", ["proszę o spokój", "jesteś niespokojny", "skończ, proszę!"], 2)]),
            Segment("W tym tygodniu Ryby mają szansę na awans.",
                    [LQ("Ta wypowiedź to:", ["reklama sklepu rybnego", "horoskop", "oferta restauracji"], 1)]),
            Segment("Proszę nie wchodzić bez obuwia ochronnego!",
                    [LQ("Ta wypowiedź jest typowa:",
                        ["w szpitalu", "kiedy robimy porządki w domu", "w sklepie z obuwiem"], 0)]),
            Segment("Proszę głęboko oddychać. Nie oddychać.",
                    [LQ("Ta wypowiedź jest typowa:", ["na spacerze", "w perfumerii", "u lekarza"], 2)]),
            Segment("Proszę nie karmić zwierząt!",
                    [LQ("Ta wypowiedź jest typowa:", ["w sklepie", "w ZOO", "w lesie"], 1)]),
            Segment("Do czego to podobne!",
                    [LQ("Ta wypowiedź oznacza:",
                        ["oburzenie", "pytanie o podobieństwo", "pytanie o skojarzenia"], 0)]),
            Segment("Ulgowy proszę!",
                    [LQ("Taką wypowiedź najczęściej słyszymy:", ["w kiosku", "w aptece", "w urzędzie"], 0)]),
        ],
    ),
    # Zadanie III — монолог «willa wśród róż»: TAK/NIE (офіц. ключ III)
    Exercise(
        "willa", "Willa wśród róż (Zadanie — prawda/fałsz)",
        "Прослухай розповідь і познач TAK (правда) / NIE (неправда).",
        [
            Segment(
                "Znajdujemy się na Alei Wielkopolskiej, przy której stoi mój rodzinny dom, "
                "w którym mój dziadek spędził najpiękniejsze lata swojego życia. Według jego pomysłu "
                "został ten dom wybudowany w tysiąc dziewięćset dwudziestym dziewiątym roku, a w "
                "trzydziestym dziewiątym roku rodzina Nowowiejskich musiała opuścić ten dom, przenieść "
                "się do Krakowa i spędzić tam lata okupacji. Powrócili do Poznania na Aleję Wielkopolską "
                "w roku tysiąc dziewięćset czterdziestym piątym, gdzie dziadek Nowowiejski spędził jeszcze "
                "rok swojego życia i tutaj zmarł. Na wprost wejścia frontowego znajduje się salonik, "
                "ulubione instrumenty mojego dziadka, a z okien saloniku ulubiony widok. W tym ogrodzie "
                "hodowane były róże, które uwielbiała moja babcia, dlatego willę nazywano willą wśród róż.",
                [
                    LQ("W tym domu mieszkała rodzina kobiety.", _TAKNIE, 0),
                    LQ("Dom zaprojektował znany architekt.", _TAKNIE, 1,
                       "Дім збудовано за задумом дідуся, не відомого архітектора."),
                    LQ("Dziadek w 1929 roku przeprowadził się do Krakowa.", _TAKNIE, 1,
                       "1929 — збудували дім; до Кракова переїхали 1939."),
                    LQ("Nowowiejscy mieszkali przed wojną na Alei Wielkopolskiej 10 lat.", _TAKNIE, 0,
                       "1929–1939 = 10 років."),
                    LQ("Dziadek zmarł w 1945 roku.", _TAKNIE, 1,
                       "Повернулись 1945 і прожив ще рік → помер близько 1946."),
                    LQ("Instrumenty dziadka stoją przed wejściem do domu.", _TAKNIE, 1,
                       "Інструменти в саліонику навпроти входу, не перед домом."),
                    LQ("Dziadek lubił widok z okna saloniku.", _TAKNIE, 0),
                    LQ("„Willa wśród róż” znajduje się w Poznaniu.", _TAKNIE, 0),
                ],
            )
        ],
    ),
    # Zadanie IV — монолог про музей: a/b/c (офіц. ключ IV)
    Exercise(
        "muzeum", "Muzeum Kultury Łemkowskiej (Zadanie a/b/c)",
        "Прослухай розповідь і обери правильну відповідь.",
        [
            Segment(
                "Jedzie się w kierunku Barwinka – to jest przejście graniczne – i w Tylawie na lewo "
                "skręca się do Zyndranowej; to jest trzy kilometry i od razu na samym początku pod "
                "numerem pierwszym znajduje się Muzeum Kultury Łemkowskiej. Muzeum już istnieje "
                "trzydzieści sześć lat. Jest to taki zestaw budynków łemkowskich: budynek mieszkalny, "
                "koniusznia i taki mniejszy gospodarczy budynek. Myśmy na początku, jeszcze kiedy nie "
                "było tego muzeum, mieszkali w tych budynkach, a obok budowaliśmy nowy dom. Kiedy "
                "zamieszkaliśmy w nowym domu, wtedy powstał pomysł, żeby stworzyć muzeum. Obecnie "
                "można by to nazwać takim małym skansenem.",
                [
                    LQ("Muzeum znajduje się pod numerem:", ["pierwszym", "piętnastym", "piątym"], 0),
                    LQ("Jest to muzeum:",
                       ["literatury łemkowskiej", "muzyki łemkowskiej", "kultury łemkowskiej"], 2),
                    LQ("Muzeum istnieje:", ["46 lat", "36 lat", "6 lat"], 1),
                    LQ("Rodzina kobiety mieszkała:",
                       ["w skansenie", "w bloku", "w budynkach, gdzie dziś jest muzeum"], 2),
                    LQ("Dzisiaj rodzina mieszka:",
                       ["w muzeum", "w domu blisko muzeum", "w małym skansenie"], 1),
                ],
            )
        ],
    ),
    # ── Пробний тест 2020 (офіц.) — Zad I: короткі висловлювання (12×a/b/c) ──
    Exercise(
        "s2020_1", "Тест 2020 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Przy zakupach powyżej tysiąca złotych transport jest za darmo.",
                    [LQ("Ta wypowiedź jest typowa:",
                        ["na stacji benzynowej", "w sklepie z meblami", "w kinie przy kasie"], 1,
                        "безкоштовна доставка при покупці >1000 зл → магазин меблів.")]),
            Segment("Proszę o klucz do pokoju sześćset dwanaście.",
                    [LQ("Ta wypowiedź jest typowa w:",
                        ["siłowni", "restauracji", "hotelu"], 2, "ключ від номера → готель.")]),
            Segment("Wysiadamy na następnym przystanku.",
                    [LQ("Ta wypowiedź jest typowa w:",
                        ["samolocie", "taksówce", "autobusie"], 2, "«наступна зупинка» → автобус.")]),
            Segment("Proszę coś na przeziębienie.",
                    [LQ("Ta wypowiedź jest typowa:",
                        ["w aptece", "u dentysty", "w sekretariacie"], 0, "щось від застуди → аптека.")]),
            Segment("Polecamy najnowsze modele we wszystkich kolorach.",
                    [LQ("Ta wypowiedź to fragment:",
                        ["komunikatu na dworcu", "reklamy radiowej", "instrukcji obsługi"], 1,
                        "«рекомендуємо новинки» → реклама.")]),
            Segment("Halo, dzień dobry, szukam mieszkania blisko uniwersytetu.",
                    [LQ("Ta wypowiedź to fragment rozmowy:",
                        ["w dziekanacie", "przez telefon", "dwóch koleżanek"], 1,
                        "«Halo, dzień dobry» → телефонна розмова.")]),
            Segment("Czym najszybciej dojechać do ogrodu zoologicznego?",
                    [LQ("Ta wypowiedź to pytanie o:",
                        ["czas", "miejsce", "środek transportu"], 2, "«Czym dojechać» → засіб транспорту.")]),
            Segment("Nie pamiętam, kiedy ostatnio byłem u dentysty.",
                    [LQ("Ta wypowiedź oznacza, że ta osoba:",
                        ["planuje wizytę u lekarza", "dawno nie leczyła zębów", "często odwiedza dentystę"],
                        1, "давно не був у стоматолога.")]),
            Segment("Ta zupa jest za słona.",
                    [LQ("Ta wypowiedź oznacza:",
                        ["krytykę", "życzenie", "akceptację"], 0, "суп пересолений → критика.")]),
            Segment("To się może źle skończyć.",
                    [LQ("Ta wypowiedź oznacza:",
                        ["niepokój", "radość", "satysfakcję"], 0, "«може погано скінчитися» → занепокоєння.")]),
            Segment("Stoimy w korku, a powinniśmy już być na miejscu.",
                    [LQ("Ta wypowiedź oznacza, że:",
                        ["mamy dużo czasu", "będziemy punktualnie", "spóźnimy się"], 2,
                        "стоїмо в заторі → запізнимося.")]),
            Segment("Dlaczego tu tak ciemno?",
                    [LQ("Ta wypowiedź oznacza, że trzeba:",
                        ["włączyć światło", "zamknąć okno", "zgasić światło"], 0, "«чому темно» → увімкнути світло.")]),
        ],
    ),
    # ── Тест 2020 — Zad II: діалоги (7×a/b/c) ──────────────────────────────
    Exercise(
        "s2020_2", "Тест 2020 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Jak dojechać do hotelu Polonia? – Na skrzyżowaniu musi pan zawrócić.",
                    [LQ("Z dialogu wynika, że mężczyzna:",
                        ["idzie do hotelu", "zatrzymuje taksówkę", "jedzie w złym kierunku"], 2,
                        "«musi zawrócić» → їде не в тому напрямку.")]),
            Segment("– Jak łączy pani naukę z obowiązkami domowymi? – Mąż wykonuje część zajęć domowych.",
                    [LQ("Z dialogu wynika, że:",
                        ["kobieta studiuje i zajmuje się domem", "mąż robi wszystko w domu",
                         "kobiecie nikt nie pomaga"], 0, "вчиться + дім; чоловік частину домашніх справ.")]),
            Segment("– Co sądzisz o nowym projekcie? – Na razie wolę milczeć.",
                    [LQ("Z dialogu wynika, że mężczyzna:",
                        ["jest autorem projektu", "krytykuje projekt", "nie mówi, co myśli"], 2,
                        "«wolę milczeć» → не висловлює думки.")]),
            Segment("– Kiedy planuje pan wydać nową płytę? – Niestety. Wiek mi już na to nie pozwala.",
                    [LQ("Z dialogu wynika, że mężczyzna:",
                        ["chce wydać nową płytę", "jest za stary na kolejną płytę",
                         "komponuje muzykę do nowej płyty"], 1, "«wiek nie pozwala» → застарий.")]),
            Segment("– Uprawiasz jakiś sport? – Od dziecka jeżdżę regularnie na rowerze.",
                    [LQ("Z dialogu wynika, że mężczyzna:",
                        ["jeździ na rowerze z dzieckiem", "dostał rower od dziecka",
                         "jeździł na rowerze już w dzieciństwie"], 2, "«od dziecka» → з дитинства.")]),
            Segment("– Czy uczestnicy płacą za kurs? – Za wszystko zapłacił urząd miasta.",
                    [LQ("Z dialogu wynika, że uczestnicy kursu:",
                        ["są pracownikami urzędu miasta", "biorą w nim udział bezpłatnie",
                         "muszą zapłacić za zajęcia"], 1, "місто оплатило → безкоштовно.")]),
            Segment("– Zarezerwowałam dla nas stolik na sobotni wieczór. "
                    "– Ale ja będę oglądał mecz z kolegami od dziewiętnastej.",
                    [LQ("Z dialogu wynika, że w sobotę kobieta i mężczyzna:",
                        ["mają inne plany na wieczór", "spędzą razem wieczór", "idą wieczorem na mecz"], 0,
                        "столик vs матч із друзями → різні плани.")]),
        ],
    ),
    # ── Тест 2020 — Zad III: інтерв'ю, TAK/NIE (5) ────────────────────────
    Exercise(
        "s2020_3", "Тест 2020 — Zad III (інтерв'ю)",
        "Прослухай інтерв'ю з Joanną Kamińską й познач TAK/NIE. На іспиті лунає двічі.",
        [
            Segment(
                "– Czym zajmujesz się na co dzień? "
                "– Mamy z mężem międzynarodową firmę meblową. To pozwala nam łączyć pracę "
                "z podróżami, naszym hobby. "
                "– Kiedy zaczęłaś podróżować? "
                "– Od piątego roku życia tańczyłam w balecie. Występowaliśmy w całej Europie. "
                "Odwiedzałam inne kraje i poznawałam życie ich mieszkańców. Natomiast liceum to "
                "początek moich samodzielnych wyjazdów do szkół językowych w Anglii i Francji. "
                "– A teraz podróżujesz sama czy w grupie? "
                "– Podróżuję z mężem i synem. To zaleta naszej biznesowo-turystycznej pracy. "
                "– Jaki środek transportu lubisz najbardziej? "
                "– Dalekie podróże to oczywiście samolot. Poza tym korzystamy z różnych środków "
                "lokomocji – to zależy od kraju, w którym jesteśmy. W Tajlandii jeździliśmy na "
                "skuterze, w Holandii – rowerami. "
                "– Ile znasz języków obcych? "
                "– Mówię po angielsku, więc praktycznie wszędzie mogę się porozumieć i w razie "
                "problemów wiem, że sobie poradzę. "
                "– Twoje największe marzenie podróżnicze to… – Meksyk. A w dalszej kolejności Kanada.",
                [
                    LQ("Bohaterka w dzieciństwie podróżowała po Europie.", _TAKNIE, 0,
                       "від 5 років танцювала в балеті, виступали в усій Європі."),
                    LQ("W szkole średniej wyjeżdżała z rodzicami do Anglii.", _TAKNIE, 1,
                       "liceum = початок САМОСТІЙНИХ виїздів, не з батьками."),
                    LQ("Obecnie podróżuje z grupą przyjaciół.", _TAKNIE, 1,
                       "подорожує з чоловіком і сином."),
                    LQ("Wybiera środek transportu w zależności od miejsca, w którym jest.", _TAKNIE, 0,
                       "«to zależy od kraju» (Таїланд — скутер, Нідерланди — велосипеди)."),
                    LQ("Boi się kłopotów z powodu braku znajomości języków obcych.", _TAKNIE, 1,
                       "знає англійську, скрізь порозуміється й дасть раду."),
                ],
            )
        ],
    ),
    # ── Тест 2020 — Zad V: зіставлення (спорт 100 років тому) → MCQ-per-item ──
    # Опис-опції A-F спільні; C (як хокей у прикладі) — дистрактор. Ключ: E,D,B,F,A.
    Exercise(
        "s2020_5", "Тест 2020 — Zad V (спорт 100 років тому)",
        "Прослухай текст про популярні колись види спорту й добери опис до кожного. "
        "На іспиті лунає двічі.",
        [
            Segment(
                "Sto lat temu, podobnie jak dzisiaj, Polacy uwielbiali sport. Zimą dodatkowe "
                "pociągi kursowały do górskich miejscowości, aby można było pojeździć na nartach. "
                "Równie popularny był hokej, ale najwięcej osób jeździło na łyżwach, gdyż sport "
                "ten był dość tani – w miastach były dostępne dla mieszkańców lodowiska, a na "
                "prowincji wystarczyło zamarznięte jezioro. Pływanie żaglówką czy łodzią to "
                "sporty dla bogatych. Pozwalały one zwiedzać kraj, podziwiać piękne, nadwodne "
                "krajobrazy. Jazdę konną uprawiali przede wszystkim żołnierze. Zdobywali liczne "
                "medale na zawodach w Polsce i za granicą. W tenisa chętnie grały panie, więc to "
                "dla nich projektanci mody wymyślili specjalne sportowe stroje. Jednak większość "
                "dyscyplin sportowych kobiety, zwłaszcza te mniej zamożne, uprawiały w zwykłych, "
                "codziennych ubraniach – w tych samych sukienkach robiły zakupy, jeździły na "
                "rowerach, grały w siatkówkę czy badmintona.",
                [
                    LQ("«Łyżwy» to był:", _ZAD5_OPTS, 4,
                       "дешевий спорт: лодовиська в містах, замерзлі озера на провінції."),
                    LQ("«Sporty wodne» (żaglówka, łódź) to:", _ZAD5_OPTS, 3,
                       "дозволяли zwiedzać kraj і милуватися краєвидами → туризм."),
                    LQ("«Jazda konna» to była:", _ZAD5_OPTS, 1,
                       "żołnierze zdobywali medale → Polacy odnosili sukcesy."),
                    LQ("«Tenis» to była:", _ZAD5_OPTS, 5,
                       "projektanci mody створили спеціальні строї → związana z modą."),
                    LQ("«Gra w siatkówkę» to był:", _ZAD5_OPTS, 0,
                       "kobiety grały w zwykłych ubraniach → nie wymagał specjalnego stroju."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ іспит лютий-2024 ══════════════════════════════════════════
    # Zad I: 14 коротких висловлювань (a/b/c). Ключ: b,b,a,c,b,c,a,c,a,a,c,b,c,a.
    Exercise(
        "s2024_1", "Іспит 2024 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Z przykrością, ale muszę ci odmówić.",
                    [LQ("Ta wypowiedź oznacza:",
                        ["zgodę na propozycję", "odrzucenie propozycji", "brak decyzji"], 1,
                        "«muszę odmówić» → відмова.")]),
            Segment("Czy wie pan, jak dojść do urzędu miasta?",
                    [LQ("Ta wypowiedź jest pytaniem o:", ["czas", "drogę", "transport"], 1,
                        "«jak dojść» → дорога.")]),
            Segment("Pociąg do Wrocławia jest opóźniony piętnaście minut.",
                    [LQ("Ta wypowiedź oznacza, że pociąg:",
                        ["przyjedzie niezgodnie z rozkładem", "będzie dokładnie o czasie",
                         "będzie kwadrans stał na stacji"], 0, "«opóźniony» → не за розкладом.")]),
            Segment("Jak mogłeś jej to wszystko powiedzieć!",
                    [LQ("Ta wypowiedź oznacza:", ["zadowolenie", "zainteresowanie", "krytykę"], 2,
                        "докір → критика.")]),
            Segment("Podczas wykładu obowiązuje zakaz używania telefonów.",
                    [LQ("Ta wypowiedź oznacza, że podczas wykładu:",
                        ["można korzystać z telefonów", "nie wolno używać telefonów",
                         "trzeba włączyć telefon"], 1, "«zakaz» → не можна.")]),
            Segment("Chciałabym skrócić tę spódnicę o sześć centymetrów.",
                    [LQ("Ta wypowiedź jest typowa:", ["u szewca", "u fryzjera", "u krawca"], 2,
                        "spódnica (укоротити) → кравець.")]),
            Segment("Synku, odrobiłeś już zadanie domowe?",
                    [LQ("Ta wypowiedź jest typowa dla:", ["rodzica", "nauczyciela", "brata"], 0,
                        "«synku» → батько/мати.")]),
            Segment("Pakiet dodatkowych minut jest w cenie abonamentu.",
                    [LQ("Ta wypowiedź oznacza, że:",
                        ["pakiet jest dodatkowo płatny", "abonament jest darmowy",
                         "pakiet jest wliczony w opłaty"], 2, "«w cenie» → включено в оплату.")]),
            Segment("Poszedłbyś wreszcie z psem na spacer!",
                    [LQ("Ta wypowiedź oznacza:", ["prośbę", "zaproszenie", "gratulacje"], 0,
                        "спонукання-прохання.")]),
            Segment("Bagaż podręczny należy umieścić pod siedzeniem.",
                    [LQ("Ta wypowiedź jest typowa:",
                        ["w czasie podróży", "w czasie wizyty u lekarza", "w sklepie turystycznym"],
                        0, "ручна поклажа під сидінням → у подорожі (літак/потяг).")]),
            Segment("Niesamowita historia! Co było potem?",
                    [LQ("Ta wypowiedź oznacza:", ["obojętność", "znudzenie", "zaciekawienie"], 2,
                        "«co było potem?» → зацікавлення.")]),
            Segment("Proszę brać leki przeciwgorączkowe i odpoczywać.",
                    [LQ("Ta wypowiedź to fragment:",
                        ["prognozy pogody", "porady lekarskiej", "audycji sportowej"], 1,
                        "ліки + відпочинок → лікарська порада.")]),
            Segment("Czy mają państwo w ofercie dania warzywne?",
                    [LQ("Ta wypowiedź oznacza, że klient chce:",
                        ["zestaw z rybą", "potrawę z mięsem", "danie wegetariańskie"], 2,
                        "«dania warzywne» → овочеве/вегетаріанське.")]),
            Segment("Na kurs zapraszamy wszystkie osoby pełnoletnie.",
                    [LQ("Ta wypowiedź oznacza, że kurs jest dla osób:",
                        ["które mają co najmniej 18 lat", "które mają mniej niż 18 lat",
                         "bez względu na wiek"], 0, "«pełnoletnie» → щонайменше 18 років.")]),
        ],
    ),
    # Zad II: 6 діалогів (a/b/c). Ключ: a,b,c,c,b,a.
    Exercise(
        "s2024_2", "Іспит 2024 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Czy problem jest poważny? – To płyta główna. Powinna pani zostawić "
                    "komputer w serwisie.",
                    [LQ("Z dialogu wynika, że komputer:",
                        ["należy naprawić", "jest sprawny", "trzeba sprzedać"], 0,
                        "«zostawić w serwisie» → треба ремонтувати.")]),
            Segment("– Co myślisz o tym nowym sklepie ze zdrową żywnością? – Nie polecam ci. "
                    "Tam jest bardzo drogo.",
                    [LQ("Z dialogu wynika, że kobieta:",
                        ["zachęca do kupowania w tym sklepie", "informuje o wysokich cenach w sklepie",
                         "poleca pracę w sklepie"], 1, "«bardzo drogo» → високі ціни.")]),
            Segment("– O nie, znowu wszystkie miejsca parkingowe przed sklepem są zajęte. "
                    "– Mówiłem ci, że trzeba wychodzić wcześniej z domu.",
                    [LQ("Z dialogu wynika, że:",
                        ["para wyszła za wcześnie z domu", "kobieta bardzo się spieszy na zakupy",
                         "na parkingu nie ma wolnych miejsc"], 2, "усі місця зайняті.")]),
            Segment("– Czy autobus do centrum już odjechał? – Tak, pięć minut temu.",
                    [LQ("Z dialogu dowiadujemy się, że:",
                        ["autobus przyjedzie za kilka minut", "mężczyzna nie wie, o której był autobus",
                         "kobieta przyszła za późno na przystanek"], 2,
                        "автобус поїхав 5 хв тому → прийшла запізно.")]),
            Segment("– Co kupiłaś Basi na imieniny? – Nie mogę powiedzieć, to niespodzianka.",
                    [LQ("Z dialogu dowiadujemy się, że:",
                        ["kobieta jeszcze nic nie kupiła", "prezent dla Basi to sekret",
                         "Basia nie chce prezentu na urodziny"], 1, "«niespodzianka» → секрет.")]),
            Segment("– Czy wszystko panu smakowało? – Tak, ale zupa mogłaby być trochę cieplejsza.",
                    [LQ("Z dialogu dowiadujemy się, że:",
                        ["potrawa była trochę za zimna", "klient jest bardzo niezadowolony",
                         "mężczyzna chwali potrawę"], 0, "«mogłaby być cieplejsza» → трохи холодна.")]),
        ],
    ),
    # Zad III: інтерв'ю про фірму Wtórpol (a/b/c). Ключ: c,b,b,b,c.
    Exercise(
        "s2024_3", "Іспит 2024 — Zad III (інтерв'ю Wtórpol)",
        "Прослухай інтерв'ю про фірму, що переробляє непотрібний одяг. Лунає двічі.",
        [
            Segment(
                "Proszę powiedzieć, czym zajmuje się firma Wtórpol. "
                "Dajemy drugie życie ubraniom. Zbieramy odzież używaną do charakterystycznych, "
                "kremowych pojemników naszych lub Polskiego Czerwonego Krzyża. Dodatkowo "
                "prowadzimy akcje edukacyjne w szkołach. "
                "W jaki sposób odzież trafia do waszej firmy? "
                "Najpierw ubrania trafiają do kontenerów, które znajdują się w każdej mniejszej "
                "lub większej miejscowości. Potem jest sortowanie. Wtórpol to jedna z największych "
                "sortowni w Europie, ale nasza firma sortuje jedynie polską odzież. "
                "Co się potem dzieje z ubraniami? "
                "Te najwyższej jakości – czyste i niezniszczone – trafiają do sklepów z odzieżą "
                "używaną w różnych miastach Polski. Odzież, która nie nadaje się do noszenia, "
                "trafia do schronisk dla zwierząt. "
                "Proszę powiedzieć więcej o akcjach edukacyjnych. "
                "Jedna z nich nazywa się „Zrób porządek w szafie”. Uczniowie zbierają niepotrzebne "
                "ubrania, przygotowują prezentacje i zdobywają wiedzę na temat recyklingu. "
                "Co uczniowie mogą zrobić z ubraniami, których już nie potrzebują? "
                "Mogą je sprzedać na przeznaczonych do tego platformach lub oddać osobom, których "
                "nie stać na nowe rzeczy. Najgorsze to wrzucić ubrania do kosza na odpady zmieszane.",
                [
                    LQ("Kontenery na ubrania znajdują się:",
                       ["przy każdej większej szkole w Polsce", "w największych miastach w Polsce",
                        "zarówno w małych, jak i dużych miastach w Polsce"], 2,
                       "«w każdej mniejszej lub większej miejscowości»."),
                    LQ("Firma Wtórpol:",
                       ["produkuje ubrania z odpadów", "zajmuje się recyklingiem polskich ubrań",
                        "importuje ubrania z Zachodu i sprzedaje w Polsce"], 1,
                       "«drugie życie», сортує лише польський одяг."),
                    LQ("Najlepsze ubrania firmy Wtórpol są:",
                       ["wysyłane za granicę do biedniejszych krajów",
                        "sprzedawane w sklepach w Polsce",
                        "oddawane do miejsc dla bezdomnych psów lub kotów"], 1,
                       "найвищої якості → магазини вживаного одягу в Польщі."),
                    LQ("Podczas akcji „Zrób porządek w szafie” uczniowie:",
                       ["zajmują się w firmie sortowaniem ubrań",
                        "robią prezentacje i uczą się o recyklingu",
                        "pomagają sprzątać w schroniskach"], 1, "презентації + знання про рециклінг."),
                    LQ("Ubrania, których uczniowie już nie potrzebują:",
                       ["powinny być oddane firmie Wtórpol",
                        "muszą zostać wrzucone do specjalnego kontenera",
                        "mogą być przekazane biedniejszym"], 2,
                       "«oddać osobom, których nie stać na nowe rzeczy»."),
                ],
            )
        ],
    ),
    # Zad IV: інфо про застосунок Pola, TAK/NIE (6). Ключ: N,T,N,T,T,N.
    Exercise(
        "s2024_4", "Іспит 2024 — Zad IV (застосунок Pola)",
        "Прослухай інформацію про застосунок Pola й познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Po co nam ta nowa aplikacja? Żeby sprawdzić, czy sok lub wędlina, które kupujemy, "
                "wyprodukowano w Polsce. Dzięki aplikacji Pola możemy zrobić to sami – wystarczy "
                "zeskanować kod kreskowy. "
                "Jak działa aplikacja? To bardzo proste. Bierzemy na przykład jogurt, uruchamiamy "
                "aplikację w smartfonie i skanujemy kod kreskowy. Po chwili możemy sprawdzić, czy "
                "producent jest z Polski i czy płaci tu podatki. "
                "Jak oceniacie produkty? Jest pięć kryteriów. Najwięcej punktów jest za wielkość "
                "polskiego kapitału, produkcję na terenie kraju i badania naukowe. Najmniej za "
                "rejestrację firmy w Polsce. "
                "Ile to kosztuje? Aplikacja jest całkowicie bezpłatna, zarówno dla firm, jak i dla "
                "użytkowników. "
                "Czy tylko z aplikacją możemy sprawdzić, czy kupujemy polskie produkty? Nie – na "
                "przykład jedna z sieci sklepów drukuje takie informacje na paragonie. Pomocny może "
                "być też sam kod kreskowy: trzy pierwsze liczby 590 oznaczają, że firma "
                "zarejestrowała się w Polsce, ale nie ma gwarancji, że tutaj wyprodukowała produkt.",
                [
                    LQ("Dzięki aplikacji możemy sprawdzić, z jakiego kraju pochodzi produkt.",
                       _TAKNIE, 1, "НІ — перевіряє, чи вироблено В ПОЛЬЩІ, не країну загалом."),
                    LQ("Aplikacja jest łatwa w obsłudze.", _TAKNIE, 0, "ТАК — «to bardzo proste»."),
                    LQ("Każdy produkt może otrzymać maksymalnie 5 punktów.", _TAKNIE, 1,
                       "НІ — п'ять КРИТЕРІЇВ, не максимум 5 балів."),
                    LQ("Aplikacja jest darmowa dla klientów i producentów.", _TAKNIE, 0,
                       "ТАК — «bezpłatna dla firm i użytkowników»."),
                    LQ("Czasami z paragonu można dowiedzieć się, czy kupiliśmy polskie produkty.",
                       _TAKNIE, 0, "ТАК — мережа друкує це на чеку."),
                    LQ("Początek kodu 590 oznacza, że firma produkuje towar w Polsce.", _TAKNIE, 1,
                       "НІ — 590 = зареєстрована в Польщі, але не гарантія виробництва тут."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ іспит квітень-2024 ════════════════════════════════════════
    # Zad I: 14 висловлювань (a/b/c). Ключ: b,c,c,a,c,a,b,b,c,a,b,c,a,b.
    Exercise(
        "s2404_1", "Іспит 2024-04 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Czy mają państwo chleb bezglutenowy?",
                    [LQ("Ta wypowiedź jest typowa:", ["w kwiaciarni", "w piekarni", "w sklepie mięsnym"],
                        1, "хліб → пекарня.")]),
            Segment("Boję się jechać sama autostopem.",
                    [LQ("Ta wypowiedź oznacza:", ["złość", "radość", "strach"], 2, "«boję się» → страх.")]),
            Segment("Od jutra mocne ochłodzenie i spadek ciśnienia.",
                    [LQ("Ta wypowiedź to fragment:",
                        ["porady lekarskiej", "reklamy radiowej", "prognozy pogody"], 2, "похолодання → прогноз погоди.")]),
            Segment("Zapraszamy na komputerowe badanie wzroku.",
                    [LQ("Ta wypowiedź jest typowa:", ["u optyka", "u ortopedy", "u informatyka"], 0,
                        "перевірка зору → оптик.")]),
            Segment("Znowu zapomniałaś, przecież byliśmy umówieni.",
                    [LQ("Ta wypowiedź oznacza:", ["zainteresowanie", "zadowolenie", "niezadowolenie"], 2,
                        "докір → невдоволення.")]),
            Segment("Trudno powiedzieć, czy to dobry spektakl.",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["nie jest pewna", "ma problemy z mówieniem", "ogląda ciekawy film"], 0,
                        "«trudno powiedzieć» → не впевнена.")]),
            Segment("Zaspałem, budzik chyba nie zadzwonił.",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["obudziła się za wcześnie", "wstała za późno", "zapomniała o budziku"], 1,
                        "«zaspałem» → проспав, встав запізно.")]),
            Segment("Proszę czekać pod gabinetem.",
                    [LQ("Ta wypowiedź jest typowa:", ["w szatni", "w przychodni", "w przedszkolu"], 1,
                        "gabinet → поліклініка.")]),
            Segment("Co za emocje! Gol! Bramkarz nie miał szans!",
                    [LQ("Ta wypowiedź komentuje:",
                        ["wyścig rowerowy", "skoki narciarskie", "mecz piłki nożnej"], 2, "«gol, bramkarz» → футбол.")]),
            Segment("Basen jest nieczynny do odwołania.",
                    [LQ("Ta wypowiedź oznacza, że basen jest:",
                        ["zamknięty", "otwarty w tygodniu", "nieczynny przez tydzień"], 0,
                        "«nieczynny do odwołania» → зачинений.")]),
            Segment("Powiedz, co zrobiłabyś na moim miejscu?",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["podjęła decyzję", "potrzebuje rady", "szuka swojego miejsca"], 1, "просить поради.")]),
            Segment("Dzisiaj polecamy szarlotkę na ciepło.",
                    [LQ("Ta wypowiedź jest typowa:", ["u kosmetyczki", "na siłowni", "w restauracji"], 2,
                        "«polecamy szarlotkę» → ресторан/кав'ярня.")]),
            Segment("Za centrum handlowym skręć w prawo.",
                    [LQ("Ta wypowiedź to:", ["polecenie", "zakaz", "pytanie"], 0, "вказівка напряму → доручення.")]),
            Segment("Potrafisz zrobić naprawdę wyśmienite pierogi.",
                    [LQ("Ta wypowiedź oznacza:", ["krytykę", "komplement", "poradę"], 1, "«wyśmienite» → комплімент.")]),
        ],
    ),
    # Zad II: 6 діалогів (a/b/c). Ключ: c,b,a,c,b,c.
    Exercise(
        "s2404_2", "Іспит 2024-04 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– W naszym sklepie płatność przyjmujemy jedynie w gotówce. – Ale ja mam przy "
                    "sobie tylko kartę.",
                    [LQ("Z dialogu wynika, że klient:",
                        ["ma tylko gotówkę", "chciałby zapłacić gotówką", "chce zapłacić kartą"], 2,
                        "має лише картку.")]),
            Segment("– Czy śniadania są wliczone w cenę pokoju? – Ta oferta nie zawiera posiłków.",
                    [LQ("Z dialogu wynika, że:",
                        ["wszystkie posiłki są gratis", "za jedzenie trzeba dodatkowo zapłacić",
                         "jeden posiłek jest za darmo"], 1, "оферта без харчування → доплата.")]),
            Segment("– Może polecimy w tym roku na jakieś egzotyczne wakacje? – Ooo, brzmi bardzo "
                    "dobrze, uwielbiam latać samolotem.",
                    [LQ("Z dialogu wynika, że:",
                        ["para planuje egzotyczną podróż", "kobieta od zawsze marzyła o egzotycznej podróży",
                         "mężczyzna pierwszy raz będzie leciał samolotem"], 0, "планують подорож.")]),
            Segment("– I jak oceniasz ten salon fryzjerski? – Myślałam, że to dobry salon, ale "
                    "myliłam się. Zobacz na moją fryzurę.",
                    [LQ("Z dialogu wynika, że kobieta:",
                        ["jest zadowolona z usług salonu", "poleca wizytę w tym salonie",
                         "jest niezadowolona z wizyty"], 2, "«myliłam się» → незадоволена.")]),
            Segment("– Kiedy planuje pan wziąć udział w zawodach pływackich? – Niestety. Wiek mi "
                    "już na to nie pozwala.",
                    [LQ("Z dialogu wynika, że mężczyzna:",
                        ["chce wkrótce wziąć udział w zawodach", "jest za stary na udział w zawodach",
                         "nie jest pewien, czy weźmie udział"], 1, "«wiek nie pozwala» → застарий.")]),
            Segment("– Grasz na jakimś instrumencie? – Od dziecka regularnie gram na skrzypcach.",
                    [LQ("Z dialogu wynika, że kobieta:",
                        ["gra na skrzypcach razem z dzieckiem", "dała swoje skrzypce dziecku",
                         "grała na skrzypcach już w młodym wieku"], 2, "«od dziecka» → з юних літ.")]),
        ],
    ),
    # Zad III: інтерв'ю зі стюардесою (a/b/c). Ключ: a,c,a,b,b.
    Exercise(
        "s2404_3", "Іспит 2024-04 — Zad III (інтерв'ю зі стюардесою)",
        "Прослухай інтерв'ю про роботу стюардеси. На іспиті лунає двічі.",
        [
            Segment(
                "Dlaczego zostałaś stewardessą? Od zawsze marzyłam o ciekawych podróżach, już na "
                "studiach często podróżowałam autostopem po Polsce, żeby odkrywać nowe miejsca. "
                "Co spowodowało, że wybrałaś tę ścieżkę zawodową? Kiedy moja mama nagle "
                "zachorowała, zrozumiałam, że życie jest krótkie i trzeba spełniać swoje marzenia. "
                "To był impuls do działania. Gdy znalazłam ogłoszenie o pracy w liniach "
                "lotniczych, poszłam na rozmowę kwalifikacyjną i trzy dni później podpisałam umowę. "
                "Jak wyglądała rekrutacja i co jest ważne w tej pracy? Pracodawca nie wymagał "
                "wykształcenia lotniczego. Liczyła się biegła znajomość języka obcego, organizacja "
                "pracy, punktualność, komunikatywność oraz umiejętność opanowania stresu. Po "
                "rozmowach i teście z angielskiego był egzamin praktyczny – rozwiązywanie problemów "
                "na pokładzie samolotu. Opowiedz o plusach tej pracy. To przede wszystkim "
                "możliwość zwiedzania świata, często z dłuższymi pobytami. Oczekiwanie na lot "
                "powrotny to przyjemność – firma płaci wtedy za transport i hotele. Czy są minusy? "
                "Głównym problemem jest zmiana czasu i jet lag, który rozregulowuje rytm życia.",
                [
                    LQ("Choroba matki:",
                       ["pomogła podjąć decyzję o pracy", "przeszkodziła w podpisaniu umowy",
                        "opóźniła rekrutację o trzy dni"], 0, "«impuls do działania» → допомогла зважитися."),
                    LQ("Żeby pracować jako stewardessa, trzeba:",
                       ["znać minimum 3 języki obce", "mieć lotnicze wykształcenie",
                        "umieć radzić sobie w stresujących sytuacjach"], 2,
                       "«opanowanie stresu»; освіта не потрібна."),
                    LQ("Podczas rekrutacji kobieta:",
                       ["miała test językowy", "leciała samolotem", "rozmawiała z pilotem"], 0,
                       "тест з англійської."),
                    LQ("Jedną z zalet pracy stewardessy są:",
                       ["stabilność i rutyna", "darmowe noclegi i przejazdy", "ciekawe szkolenia zawodowe"],
                       1, "фірма платить за транспорт і готелі."),
                    LQ("Wady pracy stewardessy to:",
                       ["długie oczekiwanie na lot powrotny", "nieregularny tryb życia",
                        "brak czasu na zwiedzanie"], 1, "jet lag → нерегулярний ритм життя."),
                ],
            )
        ],
    ),
    # Zad IV: AI і ринок праці, TAK/NIE (6). Ключ: N,N,T,N,N,T.
    Exercise(
        "s2404_4", "Іспит 2024-04 — Zad IV (AI і ринок праці)",
        "Прослухай інформацію про штучний інтелект і ринок праці. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Według analityków w najbliższych latach dwadzieścia pięć procent zawodów zastąpi "
                "sztuczna inteligencja. Firmy przyznają, że korzystają z jej pomocy i zrezygnowały "
                "z części pracowników, którzy okazali się mało efektywni w porównaniu do "
                "sztucznej inteligencji. Prawie co trzecia firma zwolniła w ostatnich dwunastu "
                "miesiącach pracownika, którego zastąpiły maszyny. Są jednak zawody, którym to nie "
                "grozi. Zdaniem ekspertów w przypadku hydraulików czy elektryków nie będzie się to "
                "opłacało, ponieważ koszty zatrudnienia człowieka są dużo niższe. Także architekci "
                "czy lekarze nie powinni bać się sztucznej inteligencji – będzie ona dla nich "
                "cenną pomocą, ale w nietypowych przypadkach doświadczenie lekarza jest "
                "ważniejsze. Artyści też mogą być spokojni – melomani chcą zobaczyć człowieka na "
                "koncercie. Z drugiej strony sztuczna inteligencja z łatwością napisze muzykę do "
                "filmu, dlatego kompozytorzy mogą mieć mniej pracy. Co innego muzycy, którzy "
                "świetnie grają na instrumentach – oni mogą czuć się bezpieczni.",
                [
                    LQ("Firmy zwalniają pracowników, którzy nie potrafią pracować z robotami.",
                       _TAKNIE, 1, "НІ — звільняли МАЛО ЕФЕКТИВНИХ порівняно з AI, не «не вміють з роботами»."),
                    LQ("W ostatnim roku wszystkie badane firmy zamieniły pracownika na robota.",
                       _TAKNIE, 1, "НІ — майже КОЖНА ТРЕТЯ фірма, не всі."),
                    LQ("Zastąpienie hydraulika czy elektryka robotem będzie za drogie.",
                       _TAKNIE, 0, "ТАК — вартість найму людини нижча, невигідно."),
                    LQ("Sztuczna inteligencja to duża konkurencja dla lekarzy.",
                       _TAKNIE, 1, "НІ — для лікарів це радше цінна допомога."),
                    LQ("Artyści będą grać coraz mniej koncertów.",
                       _TAKNIE, 1, "НІ — люди хочуть бачити артиста наживо, концерти лишаються."),
                    LQ("Sztuczna inteligencja jest zagrożeniem dla kompozytorów.",
                       _TAKNIE, 0, "ТАК — AI легко напише музику до фільму → менше роботи композиторам."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ іспит червень-2024 ════════════════════════════════════════
    # Zad I: 14 висловлювань (a/b/c). Ключ: a,c,b,c,a,b,c,b,a,c,b,c,b,a.
    Exercise(
        "s2406_1", "Іспит 2024-06 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Wypożyczone książki należy oddać w ciągu miesiąca.",
                    [LQ("Ta wypowiedź jest typowa:", ["w bibliotece", "w księgarni", "w biurze"], 0,
                        "«wypożyczone książki oddać» → бібліотека.")]),
            Segment("Bardzo się cieszę na wspólny wyjazd nad jezioro.",
                    [LQ("Ta wypowiedź oznacza:", ["smutek", "zdenerwowanie", "radość"], 2, "«cieszę się» → радість.")]),
            Segment("CV i list motywacyjny prosimy wysłać na podany adres.",
                    [LQ("Ta wypowiedź to fragment rozmowy:", ["o wakacjach", "o pracy", "o spotkaniu"], 1,
                        "CV, лист мотиваційний → про роботу.")]),
            Segment("Coś przerwało, możesz to powiedzieć jeszcze raz?",
                    [LQ("Ta wypowiedź oznacza, że ona:",
                        ["kończy rozmowę", "wszystko usłyszała", "prosi o powtórzenie"], 2, "«jeszcze raz» → просить повторити.")]),
            Segment("Okulista przyjmuje we wtorki i piątki od czternastej do siedemnastej.",
                    [LQ("Ta wypowiedź oznacza, że lekarz przyjmuje:",
                        ["po południu", "codziennie", "raz w tygodniu"], 0, "14:00–17:00 → пополудні.")]),
            Segment("Mam trzydzieści dziewięć stopni i dreszcze.",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["czuje się dobrze", "ma gorączkę", "narzeka na pogodę"], 1, "39° + дрож → гарячка.")]),
            Segment("Od jutra koniec ze słodyczami i tłustym jedzeniem.",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["będzie sama gotować", "nie planuje zmian", "planuje zacząć dietę"], 2, "кінець солодкому → дієта.")]),
            Segment("Cena wycieczki nie obejmuje wejść do muzeów.",
                    [LQ("Ta wypowiedź oznacza, że:",
                        ["bilety wstępu są wliczone w cenę", "za muzea płaci się dodatkowo",
                         "bilety do muzeów są bardzo tanie"], 1, "«nie obejmuje» → музеї окремо.")]),
            Segment("Mamy złoto! Nasi siatkarze mistrzami świata!",
                    [LQ("Ta wypowiedź oznacza, że siatkarze:",
                        ["wygrali zawody", "przegrali mecz", "mają drugie miejsce"], 0, "золото/чемпіони → виграли.")]),
            Segment("Stopy razem, ręce na biodrach, plecy prosto i skaczemy!",
                    [LQ("Ta wypowiedź jest typowa:",
                        ["u ortopedy", "w salonie urody", "na sali gimnastycznej"], 2, "команди для вправ → спортзал.")]),
            Segment("W naszym biurze jest świetny klimat, wszyscy się lubimy.",
                    [LQ("Ta wypowiedź oznacza, że w biurze:",
                        ["działa klimatyzacja", "jest dobra atmosfera", "jest świeże powietrze"], 1,
                        "«świetny klimat, lubimy się» → хороша атмосфера.")]),
            Segment("Dzień dobry państwu, proszę bilety do kontroli.",
                    [LQ("Ta wypowiedź jest typowa dla:", ["policjanta", "taksówkarza", "konduktora"], 2,
                        "«bilety do kontroli» → кондуктор.")]),
            Segment("Do twarzy ci w zielonym, ładnie wyglądasz.",
                    [LQ("Ta wypowiedź to:", ["krytyka", "komplement", "rada"], 1, "«ładnie wyglądasz» → комплімент.")]),
            Segment("Pani córka często się spóźnia i nie uważa na lekcjach.",
                    [LQ("Ta wypowiedź jest typowa dla:", ["nauczyciela", "rodzica", "pielęgniarki"], 0,
                        "про поведінку на уроках → вчитель.")]),
        ],
    ),
    # Zad II: 6 діалогів (a/b/c). Ключ: c,b,b,c,b,a.
    Exercise(
        "s2406_2", "Іспит 2024-06 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Przepraszam za spóźnienie. Były duże korki w centrum. – To już kolejny raz.",
                    [LQ("Z dialogu wynika, że mężczyzna:",
                        ["spóźnił się pierwszy raz", "szedł pieszo do pracy", "czasami się spóźnia"], 2,
                        "«kolejny raz» → інколи спізнюється.")]),
            Segment("– Podoba mi się ten obraz, czy jest na sprzedaż? – Niestety, nie.",
                    [LQ("Z dialogu wynika, że:",
                        ["obraz jest bardzo drogi", "mężczyzna chciałby kupić obraz", "można kupić ten obraz"], 1,
                        "хоче купити, але не продається.")]),
            Segment("– O której godzinie kończy się seans? – Nie pamiętam dobrze.",
                    [LQ("Z dialogu wynika, że on:",
                        ["wie, o której będzie koniec filmu", "nie jest pewny, o której kończy się film",
                         "nie pamięta tytułu filmu"], 1, "«nie pamiętam» → не певний часу.")]),
            Segment("– Jak najszybciej dojechać do ogrodu zoologicznego? – Nie polecam autobusu, "
                    "lepiej będzie taksówką.",
                    [LQ("Z dialogu wynika, że:",
                        ["kobieta nie chce jechać taksówką do ZOO", "autobus jedzie najszybciej",
                         "mężczyzna poleca taksówkę"], 2, "«lepiej taksówką» → радить таксі.")]),
            Segment("– Nie powinnaś przyjmować tej oferty pracy. – Masz rację, proponują niezbyt "
                    "dobre warunki finansowe.",
                    [LQ("Z dialogu wynika, że:",
                        ["on zachęca ją do pracy", "ona się z nim zgadza", "ona jest zadowolona z oferty"], 1,
                        "«masz rację» → погоджується.")]),
            Segment("– Może przeprowadzimy się do większego mieszkania? – Muszę o tym pomyśleć. "
                    "To poważna decyzja.",
                    [LQ("Z dialogu wynika, że ona:",
                        ["jeszcze nie zdecydowała", "uważa, że to dobry pomysł", "nie chce się przeprowadzać"], 0,
                        "«muszę pomyśleć» → ще не вирішила.")]),
        ],
    ),
    # Zad III: інтерв'ю «Dom za 1 euro» (a/b/c). Ключ: b,c,a,b,c.
    Exercise(
        "s2406_3", "Іспит 2024-06 — Zad III (Dom za 1 euro)",
        "Прослухай інтерв'ю про програму «Dom za 1 euro» в Італії. На іспиті лунає двічі.",
        [
            Segment(
                "Czym jest program „Dom za 1 euro”? To nietypowy sposób, w jaki włoskie miasteczka "
                "starają się znaleźć nowych mieszkańców. Co jakiś czas wystawiają na sprzedaż "
                "nieruchomości i oferują je za cenę włoskiej kawy. "
                "Jakie warunki trzeba spełnić, żeby kupić dom? Warunki różnią się w zależności od "
                "miasteczka lub gminy. Najważniejszy jest remont, który trzeba zrobić w ciągu "
                "trzech lat od akceptacji planu napraw przez gminę. Dopiero po skończeniu renowacji "
                "można kupić nieruchomość. "
                "Gdzie można znaleźć te domy? Przede wszystkim w regionach o niewielkim "
                "zainteresowaniu turystycznym, w miasteczkach, gdzie żyje coraz mniej mieszkańców "
                "– młodzi wyjeżdżają do większych miast, a starsi umierają. "
                "Czy dużo osób korzysta z programu? Program jest skierowany do wszystkich i "
                "popularny w wielu krajach. Bardzo dużo ludzi z Europy kupuje te domy, ale nikt "
                "z Polski nie był zainteresowany. Wiele osób woli tradycyjny zakup z wolnego rynku, "
                "który może być łatwiejszy i tańszy, zwłaszcza na południu Włoch.",
                [
                    LQ("Warunki programu „Dom za 1 euro”:",
                       ["są takie same dla całego kraju", "są inne dla każdej miejscowości",
                        "zmieniają się co rok"], 1, "«różnią się w zależności od gminy»."),
                    LQ("Remont domu:",
                       ["nie jest obowiązkowy", "muszą zaakceptować mieszkańcy miasta",
                        "trzeba skończyć w określonym czasie"], 2, "у межах трьох років."),
                    LQ("„Domy za 1 euro” znajdują się w miastach:",
                       ["w których mieszka mało ludzi", "które są popularne wśród turystów",
                        "w których mieszka dużo studentów"], 0, "де щораз менше мешканців."),
                    LQ("Program „Dom za 1 euro” jest:",
                       ["dostępny tylko dla Europejczyków", "znany na całym świecie",
                        "najbardziej popularny wśród Włochów"], 1, "популярний у багатьох країнах."),
                    LQ("Tradycyjny zakup nieruchomości:",
                       ["jest popularny wśród Polaków", "jest skomplikowany na południu Włoch",
                        "ma więcej zalet niż program „Dom za 1 euro”"], 2,
                       "легший і дешевший (особливо на півдні) → більше переваг."),
                ],
            )
        ],
    ),
    # Zad IV: розмова з тренером, TAK/NIE (6). Ключ: N,T,N,T,T,N.
    Exercise(
        "s2406_4", "Іспит 2024-06 — Zad IV (розмова з тренером)",
        "Прослухай розмову з тренером про весняну активність. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Jak wrócić do formy po zimie? Jestem zwolennikiem biegania, ale nie wszyscy mogą "
                "biegać. Każdy ruch na świeżym powietrzu jest ważny. Jak poprawić kondycję? Dla "
                "początkujących spacery z kijkami, a osoby aktywne namawiam do intensywnego "
                "biegania. Mam dużo lat, ale ciągle regularnie biegam, łącznie z półmaratonami "
                "i maratonami – w każdym wieku jest to możliwe. Można też skorzystać z roweru. "
                "W naszym mieście jest wiele siłowni zewnętrznych – zachęcam do ćwiczenia na nich. "
                "A przygotowanie do treningu? Rozgrzanie mięśni przed i po treningu jest ważne, "
                "żeby uniknąć kontuzji; istotne też, kiedy wybieramy marsz. Czy dziesięciominutowe "
                "treningi mają sens? To za mało – żeby był efekt, potrzebujemy trzydziestu, "
                "czterdziestu minut. Wiosną warto stosować suplementy? Można zażywać minerały, ale "
                "wraz ze słońcem mamy więcej naturalnej witaminy D. Nie potrzebujemy chemii – "
                "wystarczy prawidłowe, zróżnicowane jedzenie. Codziennie należy ćwiczyć? To zależy "
                "od organizmu; żeby pozostać w dobrej kondycji, trenujmy trzy razy w tygodniu. "
                "Codzienne treningi są dobre dla zawodowców.",
                [
                    LQ("Mężczyzna nie startuje w zawodach z powodu wieku.", _TAKNIE, 1,
                       "НІ — біжить півмаратони й маратони, «в кожному віці можливо»."),
                    LQ("W mieście jest dużo siłowni na świeżym powietrzu.", _TAKNIE, 0,
                       "ТАК — «wiele siłowni zewnętrznych»."),
                    LQ("Przed marszem można zrezygnować z dodatkowych ćwiczeń mięśni.", _TAKNIE, 1,
                       "НІ — розігрів важливий і при марші."),
                    LQ("Krótkie treningi nie dają dobrych rezultatów.", _TAKNIE, 0,
                       "ТАК — 10 хв замало, треба 30–40."),
                    LQ("Mężczyzna poleca dobre jedzenie zamiast suplementów.", _TAKNIE, 0,
                       "ТАК — «nie potrzebujemy chemii, wystarczy prawidłowe jedzenie»."),
                    LQ("Według trenera powinno się ćwiczyć każdego dnia.", _TAKNIE, 1,
                       "НІ — 3 рази на тиждень; щодня — для профі."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ іспит лютий-2023 ══════════════════════════════════════════
    # Zad I: 14 висловлювань. Ключ: c,b,a,c,a,c,a,b,b,c,a,a,b,c.
    Exercise(
        "s2302_1", "Іспит 2023-02 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Aniu, życzę ci powodzenia na egzaminie!",
                    [LQ("Ta wypowiedź jest typowa:",
                        ["w czasie egzaminu", "po egzaminie", "przed egzaminem"], 2, "«życzę powodzenia» → перед іспитом.")]),
            Segment("W tym tygodniu wołowina pięćdziesiąt procent taniej.",
                    [LQ("Ta wypowiedź jest typowa:", ["w piekarni", "w supermarkecie", "u dietetyka"], 1,
                        "яловичина зі знижкою → супермаркет.")]),
            Segment("Uwaga! Zaginął pies, mały, czarny, z białym ogonem.",
                    [LQ("Ta wypowiedź to fragment:", ["ogłoszenia", "reklamy", "prośby"], 0, "«zaginął pies» → оголошення.")]),
            Segment("Poproszę pomidorową i zapiekane brokuły.",
                    [LQ("Ta wypowiedź jest typowa:", ["w sklepie warzywnym", "na bazarze", "w barze mlecznym"], 2,
                        "замовлення страв → бар/їдальня.")]),
            Segment("Ale mam widok z okna! Nie mogę się napatrzeć!",
                    [LQ("Ta wypowiedź oznacza:", ["radość", "zazdrość", "znudzenie"], 0, "захват → радість.")]),
            Segment("Ostatnio ty wybierałaś film, teraz moja kolej.",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["czeka na propozycję", "chce oglądać filmy o podróżach", "chce dziś decydować"], 2,
                        "«moja kolej» → хоче вирішувати.")]),
            Segment("Wczoraj znowu wygrałam wyścig kolarski.",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["jeździła rowerem", "brała udział w rejsie", "była ostatnia na mecie"], 0,
                        "wyścig kolarski → їздила велосипедом.")]),
            Segment("Miałem dziś test z matematyki. Dostałem piątkę.",
                    [LQ("Ta wypowiedź jest typowa dla:", ["pacjenta", "ucznia", "kierowcy"], 1, "тест, п'ятірка → учень.")]),
            Segment("Następny przystanek: Gdańsk Główny.",
                    [LQ("Ta wypowiedź jest typowa:", ["na lotnisku", "w tramwaju", "na peronie"], 1, "«następny przystanek» → трамвай.")]),
            Segment("Przed wejściem konieczna jest zmiana obuwia.",
                    [LQ("Ta wypowiedź oznacza, że:",
                        ["można zmienić buty", "nie wolno mieć butów", "trzeba włożyć inne buty"], 2,
                        "«zmiana obuwia konieczna» → треба взути інше.")]),
            Segment("Wprost uwielbiam włoską kuchnię.",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["lubi włoskie dania", "lubi włoskie meble", "mówi o podróżach"], 0, "«kuchnię» → страви.")]),
            Segment("Kasiu, do twarzy ci w tej fryzurze.",
                    [LQ("Ta wypowiedź to:", ["komplement", "krytyka", "porada"], 0, "«do twarzy ci» → комплімент.")]),
            Segment("Chętnie zjadłabym coś słodkiego do kawy.",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["prosi o cukier do kawy", "ma ochotę na deser", "jest bardzo głodna"], 1, "«coś słodkiego» → десерт.")]),
            Segment("Mam iść z tobą do opery? Naprawdę?",
                    [LQ("Ta wypowiedź oznacza, że osoba:", ["jest obojętna", "zgadza się", "jest zdziwiona"], 2,
                        "«Naprawdę?» → здивування.")]),
        ],
    ),
    # Zad II: 8 діалогів. Ключ: c,c,b,a,a,a,c,a.
    Exercise(
        "s2302_2", "Іспит 2023-02 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Wyjeżdżałeś ostatnio na wakacje, gdzie byłeś? – Jeździłem trochę tu i tam.",
                    [LQ("Z dialogu wynika, że:",
                        ["ona pyta o plany wakacyjne", "on odpowiada dokładnie", "on nie podaje szczegółów"], 2,
                        "«tu i tam» → без деталей.")]),
            Segment("– Przy zakupie lodówki pralkę można kupić 30 procent taniej. – Biorę obydwa urządzenia!",
                    [LQ("Z dialogu wynika, że:",
                        ["ona rezygnuje z zakupu", "ona kupuje tylko lodówkę", "ona kupuje lodówkę i pralkę"], 2,
                        "«obydwa urządzenia» → обидва.")]),
            Segment("– O co chodzi w tym zadaniu z fizyki? – Też się zastanawiam.",
                    [LQ("Z dialogu wynika, że:",
                        ["ona potrafi zrobić zadanie", "on nie rozumie zadania", "on wyjaśnia polecenie"], 1,
                        "«też się zastanawiam» → не розуміє.")]),
            Segment("– Robię kolację, o której będziesz w domu? – Trochę się spóźnię, będę za około "
                    "czterdzieści pięć minut. Muszę skończyć raport.",
                    [LQ("Z dialogu wynika, że:",
                        ["coś ją zatrzymało", "ona wróci za kwadrans", "ona będzie punktualnie"], 0, "звіт затримав.")]),
            Segment("– Ile jeszcze mam na ciebie czekać? – Jestem już gotowa.",
                    [LQ("Z dialogu wynika, że kobieta:",
                        ["może już wyjść", "potrzebuje kilku minut", "właśnie gotuje obiad"], 0, "«już gotowa» → може вийти.")]),
            Segment("– Od tygodnia ciągle jest mi niedobrze. – Może masz osłabienie wiosenne?",
                    [LQ("Z dialogu wynika, że kobieta:",
                        ["od kilku dni ma złe samopoczucie", "informuje o wizycie u lekarza",
                         "dzisiaj wyjątkowo źle się czuje"], 0, "«od tygodnia niedobrze» → кілька днів.")]),
            Segment("– Muszę oddać samochód do naprawy. – Nie lepiej kupić nowy? Ten ma już tyle lat.",
                    [LQ("Z dialogu wynika, że:",
                        ["on sam naprawi samochód", "samochód jest u mechanika", "ona nie widzi sensu w naprawie"], 2,
                        "радить купити новий → нема сенсу ремонтувати.")]),
            Segment("– Chciałbym, żebyśmy w tym roku spędzili święta u moich rodziców. – Obiecałam "
                    "babci i dziadkowi, że przyjdziemy do nich.",
                    [LQ("Z dialogu wynika, że:",
                        ["ona już umówiła się z dziadkami", "on chce zaprosić rodziców", "ona zgadza się na propozycję"], 0,
                        "обіцяла бабусі й дідусю.")]),
        ],
    ),
    # Zad III: інтерв'ю про волонтерів у Татрах. Ключ: a,b,c,a,b.
    Exercise(
        "s2302_3", "Іспит 2023-02 — Zad III (волонтаріат у Татрах)",
        "Прослухай інтерв'ю про волонтерів Татранського парку. На іспиті лунає двічі.",
        [
            Segment(
                "Co roku Tatrzański Park Narodowy w ramach programu „Wolontariat dla Tatr” angażuje "
                "młodych ludzi, którzy pomagają w edukowaniu turystów. Jedną z uczestniczek jest "
                "Anna Nowicka. Aniu, jak można dostać się do programu? Najpierw trzeba odwiedzić "
                "stronę Parku i wypełnić formularz zgłoszeniowy online. Następnie wybrać z listy "
                "zadanie, którym chcielibyśmy się zająć – jest kilka form aktywności. Co musi umieć "
                "wolontariusz? Najważniejsze to dobra kondycja fizyczna, podstawowa znajomość Tatr "
                "i regulaminu, a poza tym chęci i wolny czas. Nie jest trudno nim zostać. Co "
                "należało do twoich obowiązków? Przeprowadzałam ankiety wśród turystów i zachęcałam "
                "ich, by zabierali ze sobą to, co przynieśli: puste opakowania, chusteczki, "
                "papierki. Jak długo trwa wolontariat? Programy są tygodniowe, ale na każde siedem "
                "dni pracy mamy dwa wolne dni, które można wykorzystać na wędrowanie po górach.",
                [
                    LQ("Żeby zostać wolontariuszem, należy:",
                       ["zarejestrować się przez internet", "wysłać zgłoszenie pocztą tradycyjną",
                        "wypełnić deklarację w biurze organizacji"], 0, "формуляр онлайн на сайті."),
                    LQ("Wolontariusze wybierają rodzaj pracy:",
                       ["po rozmowie z dyrektorem", "zgodnie ze swoimi preferencjami",
                        "zgodnie z wykształceniem"], 1, "обирають завдання зі списку самі."),
                    LQ("Każdy wolontariusz powinien:",
                       ["przynajmniej raz w życiu być w górach", "bardzo dobrze mówić po angielsku",
                        "być wysportowany i dyspozycyjny"], 2, "добра кондиція + бажання + вільний час."),
                    LQ("Ania jako wolontariuszka:",
                       ["informowała turystów, co robić ze śmieciami", "oprowadzała grupy turystów po górach",
                        "zbierała śmieci w górach"], 0, "закликала забирати сміття із собою."),
                    LQ("Wolontariusze mają:",
                       ["zajęty każdy dzień w tygodniu", "trochę czasu wolnego dla siebie",
                        "wolny weekend co dwa tygodnie"], 1, "на 7 днів — 2 вільні дні."),
                ],
            )
        ],
    ),
    # Zad IV: текст про продукти bio, TAK/NIE (5). Ключ: N,T,N,T,N.
    Exercise(
        "s2302_4", "Іспит 2023-02 — Zad IV (продукти bio)",
        "Прослухай текст про екопродукти в Польщі. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Moda na zdrowy styl życia rozwija się w Polsce od kilku lat, a produkty bio "
                "cieszą się coraz większą popularnością. Prawie czterdzieści procent Polaków "
                "wybiera produkty z certyfikatem ekologicznym, a regularnie kupuje je dziewiętnaście "
                "procent. W porównaniu do Europy Zachodniej Polska wypada gorzej – we Francji czy "
                "w Niemczech ekologiczne restauracje i supermarkety to standard, w Polsce jest ich "
                "dużo mniej. Główną przeszkodą jest wysoka cena. Kilka lat temu bio szukali głównie "
                "ludzie młodzi, ale ostatnio nawyki zmienili też starsi konsumenci. Tę zmianę "
                "spowodowała izolacja podczas pandemii: Polacy kupowali więcej bio, częściej "
                "odwiedzali lokalne bazary, wróciło gotowanie w domu. Na talerzu przeciętnego "
                "Polaka jest teraz więcej warzyw i owoców.",
                [
                    LQ("Ponad połowa Polaków systematycznie kupuje jedzenie bio.", _TAKNIE, 1,
                       "НІ — регулярно лише 19%."),
                    LQ("We Francji i w Niemczech jest więcej restauracji bio niż w Polsce.", _TAKNIE, 0,
                       "ТАК — там це стандарт, у Польщі менше."),
                    LQ("Seniorzy jako pierwsi zainteresowali się produktami bio.", _TAKNIE, 1,
                       "НІ — спершу молоді люди."),
                    LQ("W czasie pandemii Polacy zmienili swoje preferencje zakupowe.", _TAKNIE, 0,
                       "ТАК — купували більше bio, ходили на базари."),
                    LQ("Polacy obecnie jedzą coraz więcej mięsa.", _TAKNIE, 1,
                       "НІ — більше овочів і фруктів."),
                ],
            )
        ],
    ),
]


def by_id(exercise_id: str) -> Exercise | None:
    return next((e for e in EXERCISES if e.id == exercise_id), None)


def pick() -> Exercise:
    return random.choice(EXERCISES)


def total_questions(ex: Exercise) -> int:
    return sum(len(s.questions) for s in ex.segments)
