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
]


def by_id(exercise_id: str) -> Exercise | None:
    return next((e for e in EXERCISES if e.id == exercise_id), None)


def pick() -> Exercise:
    return random.choice(EXERCISES)


def total_questions(ex: Exercise) -> int:
    return sum(len(s.questions) for s in ex.segments)
