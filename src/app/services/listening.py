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
    # ══ РЕАЛЬНИЙ іспит квітень-2023 ════════════════════════════════════════
    # Zad I: 14 висловлювань. Ключ: c,b,c,b,a,c,a,c,b,b,a,c,b,c.
    Exercise(
        "s2304_1", "Іспит 2023-04 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Chciałbym kupić poradnik dla ogrodników.",
                    [LQ("Ta wypowiedź jest typowa:", ["w bibliotece", "w kasie biletowej", "w księgarni"], 2,
                        "купити довідник → книгарня.")]),
            Segment("Uważam, że dieta wegetariańska będzie dla pani najlepsza.",
                    [LQ("Ta wypowiedź oznacza, że kobieta:",
                        ["proponuje komuś mięso", "poleca komuś tę dietę", "krytykuje taką dietę"], 1, "радить дієту.")]),
            Segment("Zapomnij o wyjściu do kina, dopóki nie poprawisz ocen z biologii.",
                    [LQ("Ta wypowiedź oznacza:", ["pomoc", "gratulacje", "zakaz"], 2, "«zapomnij o wyjściu» → заборона.")]),
            Segment("W całej Polsce będzie duże zachmurzenie, na północy możliwe burze.",
                    [LQ("Ta wypowiedź oznacza, że w całym kraju:",
                        ["będzie dosyć zimno", "będzie brakować słońca", "będzie padał deszcz"], 1,
                        "велика хмарність → бракуватиме сонця.")]),
            Segment("Będzie mi miło, jeśli wpadniecie do mnie w sobotę wieczorem.",
                    [LQ("Ta wypowiedź to:", ["zaproszenie", "pozdrowienia", "komplement"], 0, "запрошення в гості.")]),
            Segment("Czy te babeczki z kremem cytrynowym są świeże?",
                    [LQ("Ta wypowiedź jest typowa:", ["na stoisku z owocami", "w warzywniaku", "w cukierni"], 2,
                        "тістечка → кондитерська.")]),
            Segment("Ma pan brzydki kaszel, powinien pan rzucić palenie.",
                    [LQ("Ta wypowiedź jest typowa:", ["u lekarza", "na przyjęciu", "w barze"], 0, "порада щодо здоров'я → лікар.")]),
            Segment("Przepraszam, szukam drukarki, a nie mogę znaleźć działu z elektroniką.",
                    [LQ("Ta wypowiedź jest typowa dla:",
                        ["pracownika sklepu", "kierownika działu", "klienta w sklepie"], 2, "шукає товар → покупець.")]),
            Segment("Gratulacje dla szczęśliwych rodziców! Jak mała ma na imię?",
                    [LQ("Ta wypowiedź dotyczy:", ["ślubu znajomych", "narodzin dziecka", "nadchodzących świąt"], 1,
                        "«szczęśliwi rodzice, mała» → народження дитини.")]),
            Segment("Jedź z nimi, na pewno nie będziesz żałować. Toruń to piękne miasto.",
                    [LQ("Ta wypowiedź oznacza:", ["prośbę", "radę", "odmowę"], 1, "«jedź, nie będziesz żałować» → порада.")]),
            Segment("Ten ekspres do kawy był tani, ale nie myślałam, że po tygodniu przestanie działać.",
                    [LQ("Ta wypowiedź oznacza, że ekspres:", ["jest zepsuty", "jest w promocji", "jest niedostępny"], 0,
                        "«przestał działać» → зламаний.")]),
            Segment("Wyglądasz na chorą. Na twoim miejscu skonsultowałabym się z lekarzem.",
                    [LQ("Ta wypowiedź oznacza:", ["krytykę", "rozkaz", "radę"], 2, "«na twoim miejscu» → порада.")]),
            Segment("Miło było pana spotkać. Zapraszamy ponownie!",
                    [LQ("Ta wypowiedź to:", ["powitanie", "pożegnanie", "przeprosiny"], 1, "«miło było spotkać» → прощання.")]),
            Segment("Ta błękitna sukienka jest bardzo ładna, ale czy jest o numer większa?",
                    [LQ("Ta wypowiedź to pytanie o:", ["kolor", "cenę", "rozmiar"], 2, "«o numer większa» → розмір.")]),
        ],
    ),
    # Zad II: 8 діалогів. Ключ: c,b,a,c,b,a,b,a.
    Exercise(
        "s2304_2", "Іспит 2023-04 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Pójdziesz z nami w sobotę na mecz? – Czemu nie!",
                    [LQ("Z dialogu wynika, że:", ["on odmawia wyjścia", "ona nie chce wyjść", "on zgadza się na wyjście"], 2,
                        "«Czemu nie!» → погоджується.")]),
            Segment("– Dziś polecam żurek w chlebie i stek wołowy. – A mają państwo coś dla wegetarian?",
                    [LQ("Z dialogu wynika, że ona:",
                        ["nie chce jeść kanapek", "pyta o dania bezmięsne", "zamawia proponowane potrawy"], 1,
                        "питає про вегетаріанське.")]),
            Segment("– Doliczyć papierową torbę? – Dziękuję, nie trzeba, mam swoją.",
                    [LQ("Z dialogu wynika, że:",
                        ["on przyniósł własną torbę", "w sklepie reklamówki są za darmo", "on rezygnuje z zakupów"], 0,
                        "«mam swoją» → має власну торбу.")]),
            Segment("– Do twarzy ci w tych krótkich włosach. – Nie wyglądam zbyt poważnie?",
                    [LQ("Z dialogu wynika, że:",
                        ["on krytykuje fryzurę kobiety", "ona jest zadowolona ze swojej fryzury", "on mówi kobiecie komplement"], 2,
                        "«do twarzy ci» → комплімент.")]),
            Segment("– Kiedy przyjmuje doktor Nowak? – Codziennie od ósmej do trzynastej, ale do "
                    "piątku jest na urlopie.",
                    [LQ("Z dialogu wynika, że:",
                        ["wizyta jest możliwa w tym tygodniu", "lekarz w tym tygodniu ma wolne", "lekarz w piątki ma wizyty domowe"], 1,
                        "до п'ятниці у відпустці → цього тижня вільний.")]),
            Segment("– Spakowałeś walizkę? Za chwilę musimy wyjść. – Nie radzę sobie sam z pakowaniem.",
                    [LQ("Z dialogu wynika, że:",
                        ["oni mają mało czasu", "on nie potrzebuje pomocy", "on już przygotował bagaż"], 0,
                        "«za chwilę musimy wyjść» → мало часу.")]),
            Segment("– Słyszałem, że kupiłaś mieszkanie. – Trzy pokoje z aneksem kuchennym i widokiem na las.",
                    [LQ("Z dialogu wynika, że:",
                        ["ona kupiła małą kawalerkę", "z okien mieszkania widać drzewa", "mieszkanie ma dużą kuchnię"], 1,
                        "«widok na las» → видно дерева.")]),
            Segment("– Dziadku, straciłam pracę. – Bardzo mi przykro, moje dziecko.",
                    [LQ("Z dialogu wynika, że:",
                        ["ona przekazuje złą wiadomość", "ona dostała pracę", "on gratuluje kobiecie decyzji"], 0,
                        "«straciłam pracę» → погана новина.")]),
        ],
    ),
    # Zad III: інтерв'ю про велотуризм. Ключ: c,c,b,a,b.
    Exercise(
        "s2304_3", "Іспит 2023-04 — Zad III (велотуризм)",
        "Прослухай інтерв'ю з Henrykiem про велосипедний туризм. На іспиті лунає двічі.",
        [
            Segment(
                "Dziś rozmawiam z Henrykiem Konopką, którego pasją jest jazda rowerem. Henryku, od "
                "kiedy uprawiasz turystykę rowerową? Rower od najmłodszych lat był dla mnie ważny "
                "– mieszkałem na wsi, jeździłem nim do szkoły, do sklepu. Ale turystyką rowerową "
                "zainteresowałem się wiosną 2010 roku, minęło już ponad 10 lat. Dlaczego lubisz "
                "jeździć na rowerze? To dla mnie nie tylko relaks, ale najlepszy moment na "
                "przemyślenia – analizuję trudne sprawy zawodowe, myślę o przyszłości, podejmuję "
                "ważne decyzje. Czego nie lubisz? Nie lubię jeździć w tym samym tempie co inni; "
                "nawet w grupie nie dostosowuję się – jestem rowerowym indywidualistą. Po jakich "
                "drogach jeździsz? Planuję wycieczki tam, gdzie jest mały ruch, najlepiej w lesie. "
                "Mam ulubioną trasę wokół Jeziora Nidzkiego. Jakie jest twoje rowerowe marzenie? "
                "Od kilku lat planuję polecieć do Chin, żeby tam pojeździć, ale zawsze coś mi wypada.",
                [
                    LQ("Henryk zaczął uprawiać turystykę rowerową:",
                       ["dokładnie rok temu", "pod koniec ubiegłego roku", "już jakiś czas temu"], 2,
                       "від 2010 → понад 10 років тому."),
                    LQ("Dla Henryka jazda na rowerze to:",
                       ["przede wszystkim trening fizyczny", "czas na rozmowy z innymi",
                        "czas na planowanie i refleksję"], 2, "«najlepszy moment na przemyślenia»."),
                    LQ("Henryk Konopka zwykle wybiera:",
                       ["zorganizowane wycieczki rowerowe", "jazdę samodzielną", "bardzo szybką jazdę"], 1,
                       "індивідуаліст, не пристосовується."),
                    LQ("Henryk najbardziej lubi jeździć:",
                       ["po spokojnych okolicach", "w kilkudniowe trasy", "po miejskich trasach rowerowych"], 0,
                       "малий рух, ліс."),
                    LQ("Henryk Konopka chciałby:",
                       ["pojechać rowerem do Chin", "pojeździć na rowerze za granicą", "wziąć udział w wyścigu rowerowym"], 1,
                       "полетіти в Китай, щоб там покататися → покататися за кордоном."),
                ],
            )
        ],
    ),
    # Zad IV: поради з облаштування малого житла, TAK/NIE (5). Ключ: N,N,T,N,T.
    Exercise(
        "s2304_4", "Іспит 2023-04 — Zad IV (мале житло)",
        "Прослухай поради, як облаштувати мале житло. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Dziś opowiem, jak urządzić małe mieszkanie – rok temu sama kupiłam kawalerkę. "
                "Niewielkie mieszkania zwykle mają salon połączony z kuchnią, dzięki czemu mamy "
                "więcej miejsca; między kuchnią a pokojem można postawić funkcjonalny stół. Do "
                "salonu warto kupić sofę z funkcją spania, by zaproponować nocleg gościom. Nad sofą "
                "dobrze zawiesić lustro – optycznie powiększy mieszkanie. Stolik kawowy wybierzmy "
                "raczej nieduży, bo w małym mieszkaniu mieszka jedna osoba lub para. Warto pamiętać "
                "o roślinach, których widok uspokaja. Jeśli mamy małą sypialnię, łóżko warto "
                "postawić pod ścianą, którą zabudujemy szafkami aż do sufitu – na ubrania i książki.",
                [
                    LQ("Do dużego pokoju trzeba wybrać wygodne fotele dla gości.", _TAKNIE, 1,
                       "НІ — радять софу з функцією спання, не фотелі."),
                    LQ("W małym pokoju warto postawić na podłodze lustro.", _TAKNIE, 1,
                       "НІ — дзеркало вішають НАД софою."),
                    LQ("W małym salonie nie musimy rezygnować ze stolika kawowego.", _TAKNIE, 0,
                       "ТАК — просто обираємо невеликий столик."),
                    LQ("Rośliny są najlepszą dekoracją mieszkania.", _TAKNIE, 1,
                       "НІ — про рослини варто пам'ятати, але «найкраща» не сказано."),
                    LQ("Szafki powinny wisieć w sypialni nad łóżkiem.", _TAKNIE, 0,
                       "ТАК — стіну над ліжком забудовуємо шафками."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ іспит червень-2023 ════════════════════════════════════════
    # Zad I: 14 висловлювань. Ключ: a,c,a,b,a,c,b,a,c,b,b,c,a,b.
    Exercise(
        "s2306_1", "Іспит 2023-06 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Tomku, dostajesz jedynkę, znowu się nie nauczyłeś.",
                    [LQ("To wypowiedź:", ["nauczyciela", "ucznia", "rodzica"], 0, "виставляє оцінку → вчитель.")]),
            Segment("Przepraszam, chciałbym kupić przewodnik po Austrii.",
                    [LQ("Ta wypowiedź jest typowa:", ["w biurze podróży", "na dworcu PKP", "w księgarni"], 2,
                        "купити путівник → книгарня.")]),
            Segment("Jutro można spodziewać się silnego wiatru i opadów deszczu.",
                    [LQ("Ta wypowiedź to fragment:", ["prognozy pogody", "porady lekarskiej", "audycji kulinarnej"], 0,
                        "вітер, дощ → прогноз погоди.")]),
            Segment("Tankowałem paliwo przy czwórce. Poproszę jeszcze małą kawę.",
                    [LQ("Ta wypowiedź jest typowa:", ["w restauracji", "na stacji benzynowej", "w sklepie motoryzacyjnym"], 1,
                        "заправлявся паливом → АЗС.")]),
            Segment("Po wielu miesiącach wreszcie znalazłam wymarzoną kawalerkę.",
                    [LQ("Ta wypowiedź oznacza, że osoba:",
                        ["długo szukała mieszkania", "wynajęła mieszkanie kawalerowi", "kupiła trzypokojowy apartament"], 0,
                        "«po wielu miesiącach» → довго шукала.")]),
            Segment("Dostałem awans i podwyżkę. Nie spodziewałem się tego.",
                    [LQ("Ta wypowiedź oznacza:", ["zdenerwowanie", "rozczarowanie", "zaskoczenie"], 2, "«nie spodziewałem się» → здивування.")]),
            Segment("Czy mają państwo w karcie coś dla wegetarian?",
                    [LQ("Ta wypowiedź oznacza, że osoba pyta o dania:",
                        ["dla alergików", "bez mięsa", "niskokaloryczne"], 1, "для вегетаріанців → без м'яса.")]),
            Segment("Dzień dobry, poproszę dwa ulgowe i jeden normalny.",
                    [LQ("Ta wypowiedź jest typowa:", ["w kasie biletowej", "na poczcie", "w przychodni"], 0,
                        "пільгові/звичайні квитки → каса.")]),
            Segment("Mam trzydzieści dziewięć stopni i dreszcze.",
                    [LQ("Ta wypowiedź oznacza, że:", ["jest upalny dzień", "ona czuje się dobrze", "ona ma gorączkę"], 2,
                        "39° + дрож → гарячка.")]),
            Segment("Ile mniej więcej będzie kosztował kurs na dworzec?",
                    [LQ("Ta wypowiedź jest typowa:", ["w autobusie", "w taksówce", "w pociągu"], 1, "«kurs na dworzec» → таксі.")]),
            Segment("Przed wejściem do sali proszę zostawić kurtki w szatni.",
                    [LQ("Ta wypowiedź oznacza, że ciepłe ubrania:",
                        ["należy włożyć na siebie", "trzeba zostawić poza salą", "trzeba mieć przy sobie"], 1,
                        "«zostawić w szatni» → поза залою.")]),
            Segment("Czy możesz się pospieszyć? Za pół godziny musimy wyjść.",
                    [LQ("Ta wypowiedź oznacza, że osoby:",
                        ["niedawno wróciły do domu", "za kilka minut wychodzą", "do wyjścia mają 30 minut"], 2,
                        "«za pół godziny» → 30 хв до виходу.")]),
            Segment("Będziemy mieli dzisiaj gości, posprzątałbyś w domu?",
                    [LQ("Ta wypowiedź to:", ["prośba", "rada", "odmowa"], 0, "«posprzątałbyś?» → прохання.")]),
            Segment("Nasi siatkarze zagrali dobry mecz, ale złoty medal mają rywale.",
                    [LQ("To wypowiedź:", ["kibica piłki nożnej", "fana przegranej drużyny", "fana wygranej drużyny"], 1,
                        "медаль у суперників → фан програлої команди.")]),
        ],
    ),
    # Zad II: 8 діалогів. Ключ: a,b,c,c,a,c,a,b.
    Exercise(
        "s2306_2", "Іспит 2023-06 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Wiesz, że pani Ela nie jest już naszą sąsiadką? Zamieszkała na Ochocie. "
                    "– Nie wiedziałem, jesteś pierwszą osobą, która mi to mówi.",
                    [LQ("Ta wypowiedź oznacza, że kobieta:",
                        ["przeprowadziła się", "zrobiła w domu remont", "wzięła kredyt na mieszkanie"], 0,
                        "Ela переїхала на Ochotę.")]),
            Segment("– Niestety, nie może pan zapłacić kartą, nasz terminal jest zepsuty. – Ale ja nie mam gotówki!",
                    [LQ("Z dialogu dowiadujemy się, że klient:",
                        ["ma pieniądze w portfelu", "ma pieniądze na koncie", "negocjuje cenę produktu"], 1,
                        "нема готівки, але має картку → гроші на рахунку.")]),
            Segment("– Kochanie, tym razem zapiekanka nie wyszła ci zbyt dobrze. – Masz rację, dodałam za dużo soli.",
                    [LQ("Z dialogu dowiadujemy się, że:",
                        ["mężczyzna chwali potrawę", "kobieta zrobiła pyszne danie", "kobieta zgadza się z mężczyzną"], 2,
                        "«masz rację» → погоджується.")]),
            Segment("– Czy posiłki są wliczone w cenę pokoju? – W tej ofercie jest tylko śniadanie.",
                    [LQ("Z dialogu dowiadujemy się, że:",
                        ["za śniadanie trzeba dodatkowo zapłacić", "wszystkie posiłki są gratis", "cena zawiera jeden posiłek"], 2,
                        "лише сніданок включено → один посилок.")]),
            Segment("– Mamo, Kamil dostał na urodziny chomika, ja też chcę! – No nie wiem, muszę porozmawiać o tym z ojcem.",
                    [LQ("Z dialogu dowiadujemy się, że:",
                        ["syn marzy o własnym zwierzątku", "kolega kupił sobie zwierzątko", "mama nie zgadza się na zwierzątko"], 0,
                        "«ja też chcę» → мріє про тваринку.")]),
            Segment("– Znowu boli mnie ząb. – Mogę ci polecić mojego dentystę, to bardzo dobry specjalista.",
                    [LQ("Z dialogu dowiadujemy się, że:",
                        ["kobieta umawia znajomego na wizytę", "mężczyzna nie chce iść do dentysty", "mężczyzna kolejny raz czuje ból"], 2,
                        "«znowu boli» → вкотре болить.")]),
            Segment("– Przepraszam, jak dojść do muzeum narodowego? – To nie ten kierunek, radzę wziąć taksówkę.",
                    [LQ("Z dialogu dowiadujemy się, że mężczyzna:",
                        ["szedł w złą stronę", "jedzie taksówką do muzeum", "pyta taksówkarza o drogę"], 0,
                        "«to nie ten kierunek» → йшов не туди.")]),
            Segment("– Proszę zająć miejsce, spektakl rozpocznie się za kilka minut. – Całe szczęście, że się nie spóźniłem.",
                    [LQ("Z dialogu dowiadujemy się, że mężczyzna:",
                        ["nie zdążył na spektakl", "przyszedł na czas", "przyszedł za wcześnie"], 1,
                        "«nie spóźniłem się» → вчасно.")]),
        ],
    ),
    # Zad III: інтерв'ю з Лєвандовським про батьків. Ключ: c,b,a,b,c.
    Exercise(
        "s2306_3", "Іспит 2023-06 — Zad III (Lewandowski про батьків)",
        "Прослухай інтерв'ю з Robertem Lewandowskim про його батьків. На іспиті лунає двічі.",
        [
            Segment(
                "O swoim dzieciństwie opowie znany piłkarz Robert Lewandowski. Robercie, jak "
                "pamiętasz swoich rodziców? Rodzice całe życie byli związani ze sportem. Podczas "
                "studiów na Akademii Wychowania Fizycznego w Warszawie ojciec trenował judo, tam "
                "poznał moją mamę – siatkarkę. Potem przeprowadzili się do Leszna i oboje uczyli "
                "WF-u w tej samej szkole podstawowej; tata był też dyrektorem lokalnego ośrodka "
                "sportu. Jaką rolę odegrał ojciec? Był moim pierwszym trenerem i to dzięki niemu "
                "wybrałem piłkę nożną. Mama widziała we mnie siatkarza. Co zawdzięczasz rodzicom? "
                "Pokazali mi, jaki powinien być sportowiec: uczciwy, lojalny, taki, który dzieli "
                "się swoim sukcesem z innymi. Twój tata zachorował, gdy byłeś nastolatkiem? Tak, "
                "miał problemy z sercem i zdiagnozowano u niego nowotwór. Odszedł, kiedy miałem 16 "
                "lat. Zawsze będę żałował, że nigdy nie widział moich meczów w reprezentacji.",
                [
                    LQ("Rodzice Roberta Lewandowskiego:",
                       ["uprawiali ten sam sport", "pracowali na uniwersytecie", "razem studiowali i pracowali"], 2,
                       "разом на AWF, потім оба вчили WF у тій самій школі."),
                    LQ("Ojciec Roberta był:",
                       ["instruktorem judo", "kierownikiem instytucji sportowej", "kierownikiem szkoły"], 1,
                       "директор місцевого осередку спорту."),
                    LQ("Ojciec Roberta:",
                       ["pomógł synowi zdecydować o przyszłości", "odradzał synowi karierę sportową",
                        "trenował syna na siatkarza"], 0, "завдяки йому обрав футбол."),
                    LQ("Rodzice uczyli Roberta:",
                       ["jak szybko wygrywać", "jak zachowywać się po zwycięstwie", "gdzie inwestować pieniądze"], 1,
                       "ділитися успіхом з іншими."),
                    LQ("Ojciec Roberta zmarł:",
                       ["nagle po intensywnym treningu", "przed ważnym meczem syna", "w wyniku poważnej choroby"], 2,
                       "серце + пухлина → тяжка хвороба."),
                ],
            )
        ],
    ),
    # Zad IV: розмова з гідом у Fromborku, TAK/NIE (5). Ключ: N,N,T,N,T.
    Exercise(
        "s2306_4", "Іспит 2023-06 — Zad IV (Frombork)",
        "Прослухай розмову туриста з гідом по Fromborku. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Frombork to niezwykłe miasto, a wieża wodna jest bardzo interesująca. Naprzeciwko "
                "wieży jest pomnik Mikołaja Kopernika, stoimy przy głównej ulicy, w sercu miasta. "
                "Potem pójdziemy w stronę katedry. Aby do niej dojść, można przejść przez drewniany "
                "most lub wybrać inną drogę – przez bramę od strony zachodniej. Czy Kopernik "
                "mieszkał w pobliżu? Miał dwa domy: jednym była wieża katedralna, gdzie bywał od "
                "czasu do czasu i trzymał sprzęty astronomiczne, ale na co dzień mieszkał daleko od "
                "katedry – ten budynek dziś już nie istnieje. Jak powstał Frombork? Przez prawie "
                "700 lat katedrę z budynkami nazywaliśmy miastem, a pobliskie domy były we wsi "
                "obok; te osobne części stały się jednym miastem na początku dwudziestego wieku. "
                "Dlaczego katedrę zbudowano daleko? Kościół jest na górze, na wysokości 20 metrów – "
                "to naturalna obrona tego miejsca.",
                [
                    LQ("Do katedry można dojść tylko jedną trasą.", _TAKNIE, 1,
                       "НІ — можна через міст або через браму."),
                    LQ("Kopernik częściej mieszkał w pracowni niż w swoim domu.", _TAKNIE, 1,
                       "НІ — у вежі бував час від часу; на щодень жив далеко."),
                    LQ("We Fromborku już nie ma domu Mikołaja Kopernika.", _TAKNIE, 0,
                       "ТАК — той будинок уже не існує."),
                    LQ("Frombork powstał z połączenia dwóch różnych miast.", _TAKNIE, 1,
                       "НІ — з міста (собор) і села поряд."),
                    LQ("Na lokalizację katedry wybrano szczególnie bezpieczne miejsce.", _TAKNIE, 0,
                       "ТАК — на горі, природний захист."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ іспит листопад-2023 ═══════════════════════════════════════
    # Zad I: 14 висловлювань. Ключ: b,c,a,c,b,c,a,b,c,c,b,a,b,c.
    Exercise(
        "s2311_1", "Іспит 2023-11 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Pyszna zupa, dawno nie jadłem lepszej.",
                    [LQ("Ta wypowiedź to:", ["rada", "komplement", "krytyka"], 1, "«pyszna» → комплімент.")]),
            Segment("Panie doktorze, mam zawroty głowy i dreszcze.",
                    [LQ("Ta wypowiedź jest typowa:", ["u ortopedy", "u dentysty", "u internisty"], 2, "загальні симптоми → терапевт.")]),
            Segment("Jutro zmiana pogody, wrócą upały.",
                    [LQ("Ta wypowiedź oznacza, że jutro:", ["będzie gorąco", "będzie chłodno", "pogoda będzie taka sama"], 0,
                        "«upały» → спека.")]),
            Segment("Bardzo mi przykro, że tak się stało.",
                    [LQ("Ta wypowiedź oznacza:", ["zadowolenie", "złość", "smutek"], 2, "«przykro» → смуток.")]),
            Segment("W wakacje biuro jest czynne codziennie od trzynastej do szesnastej.",
                    [LQ("Ta wypowiedź oznacza, że biuro jest otwarte:", ["w wybrane dni", "po południu", "tylko rano"], 1,
                        "13:00–16:00 → пополудні.")]),
            Segment("Czy jest większy rozmiar tych sandałów?",
                    [LQ("Ta wypowiedź jest typowa w sklepie:", ["meblowym", "ogrodniczym", "obuwniczym"], 2, "сандалі → взуття.")]),
            Segment("Gratuluję, dostała pani awans i podwyżkę.",
                    [LQ("Ta wypowiedź jest typowa dla:", ["dyrektora", "pracownika", "urzędnika"], 0, "хто дає підвищення → директор.")]),
            Segment("Rower jest w dobrym stanie, cena do negocjacji.",
                    [LQ("Ta wypowiedź oznacza, że:", ["cena roweru jest wysoka", "o cenie można rozmawiać", "rower wymaga naprawy"], 1,
                        "«cena do negocjacji» → можна торгуватися.")]),
            Segment("Chciałbym zgłosić kradzież telefonu.",
                    [LQ("Ta wypowiedź jest typowa:", ["w serwisie", "w sklepie", "na policji"], 2, "заявити про крадіжку → поліція.")]),
            Segment("Mój syn jest o głowę wyższy niż ja.",
                    [LQ("Ta wypowiedź dotyczy:", ["rozmiaru", "wagi", "wzrostu"], 2, "«wyższy» → зріст.")]),
            Segment("Niesamowity film! Musisz go obejrzeć.",
                    [LQ("Ta wypowiedź to:", ["prośba o radę", "pozytywna opinia", "negatywna opinia"], 1, "«niesamowity» → позитивна.")]),
            Segment("A teraz czas na poranny przegląd prasy.",
                    [LQ("Ta wypowiedź to fragment:", ["audycji radiowej", "prognozy pogody", "porady lekarskiej"], 0,
                        "«przegląd prasy» → радіопередача.")]),
            Segment("Poproszę plaster i syrop na kaszel.",
                    [LQ("Ta wypowiedź jest typowa:", ["w kiosku", "w aptece", "u lekarza"], 1, "пластир, сироп → аптека.")]),
            Segment("Papier wrzuć do niebieskiego pojemnika.",
                    [LQ("Ta wypowiedź dotyczy:", ["kolorowego papieru", "zakupów w sklepie", "segregacji śmieci"], 2,
                        "«do pojemnika» → сортування сміття.")]),
        ],
    ),
    # Zad II: 6 діалогів. Ключ: a,b,c,b,c,b.
    Exercise(
        "s2311_2", "Іспит 2023-11 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Basiu, wszystkiego najlepszego z okazji urodzin. – Moje urodziny były w zeszłym tygodniu.",
                    [LQ("Z dialogu wynika, że Basia:", ["już miała urodziny", "nie świętuje swoich urodzin", "zapomniała o urodzinach"], 0,
                        "«były w zeszłym tygodniu» → вже минули.")]),
            Segment("– Prosiłam, żebyście nie grali pod oknami. Połamaliście kwiaty. – Ale tutaj jest "
                    "najlepsza trawa do gry, a tam kałuże i błoto.",
                    [LQ("Z dialogu dowiadujemy się, że dzieci:", ["nie lubią grać na trawie", "nie słuchały próśb mamy", "wybiły okno"], 1,
                        "просила не гратися, а вони поламали квіти → не слухали.")]),
            Segment("– Ile kosztuje bilet na wystawę kwiatów egzotycznych? – W sezonie letnim wstęp jest bezpłatny.",
                    [LQ("Z dialogu dowiadujemy się, że:",
                        ["cały rok można oglądać wystawę za darmo", "latem wystawa jest nieczynna", "oglądanie wystawy latem nic nie kosztuje"], 2,
                        "влітку вхід безкоштовний.")]),
            Segment("– Co pani myśli o tym projekcie mieszkania? – Nie do końca podoba mi się ta garderoba.",
                    [LQ("Z dialogu wynika, że:",
                        ["kobieta jest bardzo zadowolona z projektu", "to nie jest projekt, jaki chciała klientka", "projekt garderoby jest bardzo ładny"], 1,
                        "«nie do końca podoba się» → не той, що хотіла.")]),
            Segment("– Aniu, pamiętasz o ślubie Marka? – Tak, już zamówiłam prezent. Jutro będzie kurier, możesz odebrać?",
                    [LQ("Z dialogu dowiadujemy się, że kobieta:", ["zapomniała o ślubie", "jeszcze nie wybrała prezentu", "prosi o odbiór paczki"], 2,
                        "«możesz odebrać?» → просить забрати посилку.")]),
            Segment("– Oglądałeś finał piłki nożnej? – Nie, ale słyszałem, że nasza drużyna wygrała.",
                    [LQ("Z dialogu wynika, że:", ["mężczyzna obejrzał finał", "ulubiony zespół zajął pierwsze miejsce", "mężczyzna słuchał meczu w radiu"], 1,
                        "«nasza drużyna wygrała» → перше місце.")]),
        ],
    ),
    # Zad III: інтерв'ю про e-sport. Ключ: c,b,a,b,c.
    Exercise(
        "s2311_3", "Іспит 2023-11 — Zad III (e-sport)",
        "Прослухай інтерв'ю про кіберспорт. На іспиті лунає двічі.",
        [
            Segment(
                "Rozmawiamy z zawodnikiem e-sportowym. Kamilu, czym charakteryzuje się e-sport? "
                "To forma sportu, w której zawodnicy rywalizują w wirtualnym świecie – w grach "
                "komputerowych i wideo; gracze kontrolują postacie za pomocą klawiatury i myszy. "
                "Czy to nowa forma rywalizacji? E-sport kojarzy się z dwudziestym pierwszym wiekiem, "
                "ale początki sięgają lat siedemdziesiątych dwudziestego wieku, kiedy na "
                "Uniwersytecie Stanforda zorganizowano pierwsze zawody w grze wideo – brali w nich "
                "udział studenci i pracownicy naukowi. Jak rozwijała się ta dyscyplina? Kiedy "
                "pojawił się internet, można było rywalizować z graczami na całym świecie. Firmy "
                "organizują coraz więcej turniejów; turnieje na skalę światową odbywają się dwa "
                "razy do roku i przyciągają miliony fanów do hal sportowych i przed monitory w "
                "domu. Jakie umiejętności są potrzebne? Kluczem do sukcesu jest szybkie myślenie, "
                "dokładna analiza sytuacji i podejmowanie decyzji w krótkim czasie.",
                [
                    LQ("Zawody e-sportowe miały początek:",
                       ["w dwudziestym pierwszym wieku", "ponad siedemdziesiąt lat temu", "w latach siedemdziesiątych"], 2,
                       "у 70-х роках XX ст."),
                    LQ("W pierwszych zawodach gier wideo uczestniczyli:",
                       ["profesjonalni gracze", "ludzie związani z uniwersytetem", "studenci informatyki"], 1,
                       "студенти й наукові працівники Стенфорда."),
                    LQ("Międzynarodowe zawody są organizowane:", ["dwa razy w roku", "co roku", "co dwa lata"], 0,
                       "двічі на рік."),
                    LQ("Turnieje e-sportowe można oglądać:", ["jedynie online", "na żywo oraz online", "na specjalnych ekranach"], 1,
                       "у залах і перед моніторами вдома."),
                    LQ("Najważniejsze umiejętności w e-sporcie to:",
                       ["lata praktyki w grach komputerowych", "znajomość wszystkich gier na rynku", "szybkość i myślenie analityczne"], 2,
                       "швидке мислення й аналіз."),
                ],
            )
        ],
    ),
    # Zad IV: гід по театру Шекспіра, TAK/NIE (6). Ключ: N,T,N,N,T,T.
    Exercise(
        "s2311_4", "Іспит 2023-11 — Zad IV (театр Шекспіра)",
        "Прослухай гіда по Gdańskim Teatrze Szekspirowskim. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Żeby dojść do Gdańskiego Teatru Szekspirowskiego, trzeba iść w kierunku ulicy "
                "Długiej, zatrzymać się przed Złotą Bramą i skręcić w prawo. Zobaczymy ciemny "
                "budynek w kolorze węgla. Niełatwo znaleźć wejście, bo architekt zaprojektował "
                "wokół teatru mur z kilkoma mało widocznymi przerwami – jedna to główne wejście. "
                "W środku zaskoczenie: wnętrza są jasne, pełne światła, inaczej niż mury. Dlaczego "
                "patronem jest Szekspir? Niestety Szekspir nigdy nie był w Gdańsku, natomiast "
                "przyjechali tu jego kompani teatralni. Współczesny teatr to rekonstrukcja teatru "
                "elżbietańskiego, którego budowę zamówiły władze miasta w 1635 roku. Początkowo "
                "aktorzy grali po angielsku, ale nie nawiązali relacji z publicznością mówiącą po "
                "niemiecku. Największa atrakcja to otwierany dach. Na trzecim poziomie jest wyjście "
                "na ścieżkę spacerową po murze – dopiero stąd widać, że mur to osobna konstrukcja.",
                [
                    LQ("Główne drzwi do teatru są duże i widać je z daleka.", _TAKNIE, 1,
                       "НІ — вхід малопомітний, у мурі."),
                    LQ("Kolory wnętrza budynku kontrastują z zewnętrznymi.", _TAKNIE, 0,
                       "ТАК — всередині ясно, мури темні."),
                    LQ("Szekspir w Gdańsku napisał jedną ze swoich sztuk.", _TAKNIE, 1,
                       "НІ — Шекспір ніколи не був у Гданську."),
                    LQ("Budowę dawnego teatru sfinansował prywatny inwestor.", _TAKNIE, 1,
                       "НІ — будову замовила влада міста."),
                    LQ("Pierwsze spektakle odbywały się w języku angielskim.", _TAKNIE, 0,
                       "ТАК — спершу грали англійською."),
                    LQ("Wokół teatru na wysokości 3. piętra jest trasa spacerowa.", _TAKNIE, 0,
                       "ТАК — на третьому рівні стежка по муру."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ іспит лютий-2022 ══════════════════════════════════════════
    # Zad I: 14 висловлювань. Ключ: b,b,c,a,c,b,c,b,a,b,c,a,c,a.
    Exercise(
        "s2202_1", "Іспит 2022-02 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Szef zwolnił mnie z pracy.",
                    [LQ("Ta wypowiedź oznacza, że ona:", ["pracuje za wolno", "straciła pracę", "szuka pracy"], 1,
                        "«zwolnił z pracy» → втратила роботу.")]),
            Segment("W życiu się tak nie nudziłem w kinie!",
                    [LQ("Ta wypowiedź oznacza:", ["zainteresowanie", "niezadowolenie", "radość"], 1, "нудьга → невдоволення.")]),
            Segment("Miejsce przy oknie jest moje. Proszę się przesiąść.",
                    [LQ("Ta wypowiedź jest typowa:", ["w restauracji", "w sklepie", "w pociągu"], 2, "місце біля вікна → потяг.")]),
            Segment("Tę książkę może pan wypożyczyć na trzy tygodnie.",
                    [LQ("Ta wypowiedź jest typowa:", ["w bibliotece", "w księgarni", "w kiosku"], 0, "«wypożyczyć» → бібліотека.")]),
            Segment("Ta piosenka mnie denerwuje.",
                    [LQ("Ta wypowiedź oznacza:", ["uspokojenie", "zainteresowanie", "irytację"], 2, "«denerwuje» → роздратування.")]),
            Segment("Kupiłem w tym sklepie szafę, chciałbym złożyć reklamację.",
                    [LQ("Ta wypowiedź oznacza, że klient:", ["poleca innym ten zakup", "nie jest zadowolony z zakupu", "musi się zastanowić"], 1,
                        "рекламація → незадоволений.")]),
            Segment("Rowery można przewozić w ostatnim wagonie.",
                    [LQ("Ta wypowiedź jest typowa:", ["na przystanku autobusowym", "na ścieżce rowerowej", "na dworcu kolejowym"], 2,
                        "«wagon» → залізниця.")]),
            Segment("Nie mam już siły więcej pracować.",
                    [LQ("Ta wypowiedź oznacza, że on:", ["jest silny", "jest zmęczony", "jest biedny"], 1, "«nie mam siły» → втомлений.")]),
            Segment("Ten syrop należy pić codziennie po jedzeniu.",
                    [LQ("Ta wypowiedź jest typowa:", ["w przychodni", "w barze", "w cukierni"], 0, "сироп (ліки) → поліклініка.")]),
            Segment("Jak mogłaś powiedzieć coś takiego?",
                    [LQ("Ta wypowiedź oznacza:", ["ciekawość", "krytykę", "niepewność"], 1, "докір → критика.")]),
            Segment("Wreszcie umeblowałem swój dom!",
                    [LQ("Ta wypowiedź oznacza, że on:", ["sprzedał wszystkie meble", "kupił dom z meblami", "ma w domu nowe meble"], 2,
                        "«umeblowałem» → нові меблі вдома.")]),
            Segment("Nikt nie zrobiłby tego lepiej!",
                    [LQ("Ta wypowiedź to:", ["pochwała", "krytyka", "zakaz"], 0, "«nikt nie zrobiłby lepiej» → похвала.")]),
            Segment("Przed wylotem na wakacje chciałbym ubezpieczyć bagaż.",
                    [LQ("Ta wypowiedź jest typowa:", ["w pociągu", "w samolocie", "w biurze podróży"], 2,
                        "застрахувати багаж перед вильотом → турбюро.")]),
            Segment("Opłaty za mieszkanie wzrosły o siedemdziesiąt złotych.",
                    [LQ("Ta wypowiedź oznacza, że ona:", ["płaci teraz wyższy czynsz", "zmieniła mieszkanie", "będzie płacić 70 zł"], 0,
                        "оплати зросли → вищий чинш.")]),
        ],
    ),
    # Zad II: 8 діалогів. Ключ: a,c,a,c,b,b,a,c.
    Exercise(
        "s2202_2", "Іспит 2022-02 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Czy ma pan skierowanie na badania? – Tak, na kiedy mogę się umówić?",
                    [LQ("Z dialogu wynika, że mężczyzna:", ["umawia się na wizytę w poradni", "organizuje spotkanie biznesowe", "pyta o koszt badań"], 0,
                        "скерування на обстеження → запис у поліклініку.")]),
            Segment("– Popatrz, autobus przyjedzie dopiero za osiem minut. – Niepotrzebnie tak się spieszyłyśmy.",
                    [LQ("Z dialogu wynika, że kobiety:", ["spóźniły się na autobus", "jadą autobusem", "czekają na autobus"], 2,
                        "автобус за 8 хв → чекають.")]),
            Segment("– Pije pani herbatę z cukrem czy bez? – Dziękuję, cytryna wystarczy.",
                    [LQ("Z dialogu wynika, że kobieta:", ["woli gorzką herbatę", "prosi o cukier", "nie chce herbaty"], 0,
                        "лимон без цукру → гіркий чай.")]),
            Segment("– Smakowała ci kolacja u Ani? – Ania musi się jeszcze wiele nauczyć.",
                    [LQ("Z dialogu wynika, że:", ["potrawy były smaczne", "dania były drogie", "ona nie jest zadowolona z kolacji"], 2,
                        "«musi się nauczyć» → незадоволена.")]),
            Segment("– Wychodzę z kolegami na rower. – Weź coś na wypadek deszczu.",
                    [LQ("Z dialogu wynika, że:", ["zaczął padać deszcz", "może zacząć padać deszcz", "podczas deszczu łatwo o wypadek"], 1,
                        "«na wypadek deszczu» → може піти дощ.")]),
            Segment("– Jutro dostarczymy paczkę na pana adres domowy. – Będę cały dzień w pracy. Podaję nowy adres dostawy.",
                    [LQ("Z dialogu wynika, że mężczyzna:", ["odbierze paczkę w domu", "odbierze paczkę w innym miejscu", "zwraca paczkę"], 1,
                        "новий адрес доставки → інше місце.")]),
            Segment("– Och, zobacz, nasza nawigacja w samochodzie nie działa. – Nie martw się, poradzimy sobie bez niej.",
                    [LQ("Z dialogu wynika, że oni:", ["sami znajdą drogę", "zmienią plany", "nie dojadą na miejsce"], 0,
                        "«poradzimy sobie bez niej» → знайдуть дорогу самі.")]),
            Segment("– Czy problem jest poważny? – To hamulce. Musi pani zostawić samochód w warsztacie.",
                    [LQ("Z dialogu wynika, że samochód:", ["jest sprawny", "należy sprzedać", "trzeba naprawić"], 2,
                        "гальма, лишити в майстерні → ремонт.")]),
        ],
    ),
    # Zad III: інтерв'ю з найкращим роботодавцем. Ключ: b,c,a,b,c.
    Exercise(
        "s2202_3", "Іспит 2022-02 — Zad III (найкращий роботодавець)",
        "Прослухай інтерв'ю з найкращим роботодавцем Польщі. На іспиті лунає двічі.",
        [
            Segment(
                "Zdobył pan tytuł Najlepszego Pracodawcy w Polsce, pokonując stu kandydatów. Jak "
                "powinien postępować szef, by pracownicy byli zadowoleni? Traktuję wszystkich tak, "
                "jak sam chciałbym być traktowany. Nie chciałbym, żeby praca mnie ograniczała, "
                "dlatego mój zespół może sam wybrać miejsce i czas pracy. Jak stworzyć dobrą "
                "atmosferę? Chcę, żeby pracownicy dobrze znali firmę – niczego nie ukrywam i daję "
                "im dostęp do wielu informacji. Czy wiedzą, ile kto zarabia? Nie – tych informacji "
                "o wynagrodzeniu nie przekazuję innym. Na co jeszcze mogą liczyć? Chcę, by cały "
                "czas się rozwijali: organizuję warsztaty i seminaria; wybieram projekty "
                "wymagające kreatywności. Czy relacje między pracownikami są ważne? Bardzo – dwa "
                "razy w roku organizuję wyjazdy integracyjne, żebyśmy poznali się w mniej "
                "formalnych sytuacjach.",
                [
                    LQ("Według pracodawcy jego pracownicy:",
                       ["za bardzo go kontrolują", "decydują, gdzie chcą pracować", "mają za dużo czasu"], 1,
                       "самі обирають місце й час праці."),
                    LQ("Dane o wysokości pensji kolegów:",
                       ["są dostępne dla wszystkich", "są omawiane na zebraniach", "nie są znane pracownikom"], 2,
                       "інформацію про зарплати не передає."),
                    LQ("Pracownicy firmy:",
                       ["mogą brać udział w szkoleniach", "sami płacą za różne szkolenia", "prowadzą kursy dla innych"], 0,
                       "організовує майстерні й семінари."),
                    LQ("Pracodawca szuka projektów, które:",
                       ["będą łatwe dla pracowników", "będą interesujące dla pracowników", "pozwolą mu więcej zarobić"], 1,
                       "які вимагають креативності."),
                    LQ("Pracownicy co jakiś czas:",
                       ["organizują konferencje", "odwiedzają szefa w domu", "wspólnie wyjeżdżają"], 2,
                       "виїзди для інтеграції двічі на рік."),
                ],
            )
        ],
    ),
    # Zad IV: рутина королеви Єлизавети II, TAK/NIE (5). Ключ: T,N,N,N,T.
    Exercise(
        "s2202_4", "Іспит 2022-02 — Zad IV (день королеви)",
        "Прослухай розмову про розпорядок дня королеви Єлизавети II. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Wczoraj oglądałam program o królowej Elżbiecie. Zamiast budzika używa dźwięku "
                "tradycyjnego drewnianego instrumentu, który lubi. Zaczyna dzień o wpół do ósmej. "
                "Na śniadanie wybiera płatki, owsiankę, tost z dżemem pomarańczowym lub jajecznicę "
                "– zwykle rano nie je mięsa. Po śniadaniu zaczyna pracę: w biurze czyta listy, "
                "odpowiada na korespondencję i podpisuje dokumenty; nie korzysta z pomocy "
                "sekretarek, wszystko robi sama. Ważnym elementem dnia są spotkania – jest bardzo "
                "zorganizowana, każde trwa około dwudziestu minut, a ona wie, kiedy czas minął, bez "
                "patrzenia na zegarek. Wieczorami czyta raporty z dyskusji parlamentarnych, a w "
                "każdą środę spotyka się z premierem Wielkiej Brytanii. Po pracy uwielbia spacery "
                "z psami i jazdę konną.",
                [
                    LQ("Królowa zwykle je bezmięsne śniadanie.", _TAKNIE, 0,
                       "ТАК — зазвичай уранці не їсть м'яса."),
                    LQ("Sekretarki pomagają królowej w biurowych obowiązkach.", _TAKNIE, 1,
                       "НІ — не користується допомогою секретарок."),
                    LQ("Królowa podczas spotkań co 20 min kontroluje czas.", _TAKNIE, 1,
                       "НІ — знає, коли час минув, БЕЗ погляду на годинник."),
                    LQ("Wieczorami Elżbieta II czyta literaturę kryminalną.", _TAKNIE, 1,
                       "НІ — читає звіти з парламентських дискусій."),
                    LQ("Królowa regularnie spotyka się z premierem Wielkiej Brytanii.", _TAKNIE, 0,
                       "ТАК — щосереди."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ іспит березень-2022 ═══════════════════════════════════════
    # Zad I: 14 висловлювань. Ключ: c,b,a,a,b,c,b,c,a,c,c,b,a,b.
    Exercise(
        "s2203_1", "Іспит 2022-03 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Czy może pani spakować wszystkie owoce i warzywa razem?",
                    [LQ("Ta wypowiedź jest typowa:", ["w barze", "w kwiaciarni", "na targu"], 2, "овочі й фрукти → базар.")]),
            Segment("Czy podczas spektaklu dla dzieci będą przerwy?",
                    [LQ("Ta wypowiedź jest typowa:", ["w muzeum", "w teatrze", "w kinie"], 1, "спектакль → театр.")]),
            Segment("Znowu wszystkie miejsca parkingowe są zajęte!",
                    [LQ("Ta wypowiedź oznacza:", ["zdenerwowanie", "radość", "strach"], 0, "«znowu zajęte» → роздратування.")]),
            Segment("Te buty są trochę za małe. Poproszę większy rozmiar.",
                    [LQ("Ta wypowiedź jest typowa:", ["w sklepie obuwniczym", "w księgarni", "w restauracji"], 0, "взуття → взуттєвий.")]),
            Segment("Poproszę krople do oczu i coś na ból głowy.",
                    [LQ("Ta wypowiedź jest typowa:", ["u optyka", "w aptece", "u okulisty"], 1, "краплі + ліки → аптека.")]),
            Segment("Poproszę prawo jazdy i dowód osobisty.",
                    [LQ("Ta wypowiedź jest typowa podczas:", ["kontroli biletów", "odprawy na lotnisku", "kontroli drogowej"], 2,
                        "права + посвідчення → дорожній контроль.")]),
            Segment("Proszę zrobić miejsce dla tej starszej pani!",
                    [LQ("Ta wypowiedź oznacza:", ["krytykę", "polecenie", "sympatię"], 1, "прохання-вказівка → polecenie.")]),
            Segment("Ten obraz jest z osiemnastego wieku.",
                    [LQ("Ta wypowiedź jest typowa:", ["w galerii handlowej", "w księgarni", "w muzeum"], 2, "картина XVIII ст. → музей.")]),
            Segment("Polecam ci ten sklep ze zdrową żywnością.",
                    [LQ("Ta wypowiedź oznacza:", ["rekomendację", "prośbę", "rezygnację"], 0, "«polecam» → рекомендація.")]),
            Segment("Czy może pan zapłacić gotówką? Terminal nie działa.",
                    [LQ("Ta wypowiedź oznacza problemy:", ["z wydaniem reszty", "z płatnością gotówką", "z płatnością kartą"], 2,
                        "термінал не діє → карткою не можна.")]),
            Segment("Co tak późno? Wszyscy na ciebie czekamy!",
                    [LQ("Ta wypowiedź oznacza, że osoba jest:", ["przed czasem", "na czas", "po czasie"], 2, "«tak późno» → запізнилася.")]),
            Segment("Zgubiłam nowy zegarek, który dostałam od dziadka.",
                    [LQ("Ta osoba jest:", ["zadowolona", "smutna", "zmęczona"], 1, "загубила подарунок → сумна.")]),
            Segment("Wyobraź sobie, że wreszcie dostałem awans.",
                    [LQ("Ta wypowiedź jest typowa dla:", ["pracownika", "studenta", "bezrobotnego"], 0, "підвищення → працівник.")]),
            Segment("Chciałabym zamówić na jutro tort czekoladowy.",
                    [LQ("Ta wypowiedź jest typowa:", ["w sklepie mięsnym", "w cukierni", "w barze"], 1, "торт → кондитерська.")]),
        ],
    ),
    # Zad II: 8 діалогів. Ключ: c,b,c,a,b,b,a,b.
    Exercise(
        "s2203_2", "Іспит 2022-03 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Czy oglądał pan już projekt mieszkania? Co pan o tym myśli? – Salon w "
                    "porządku, ale aranżacja sypialni jest chyba zbyt awangardowa.",
                    [LQ("Z dialogu dowiadujemy się, że:", ["klient jest zadowolony z projektu", "projekt sypialni jest za drogi", "projekt sypialni nie odpowiada klientowi"], 2,
                        "спальня надто авангардна → не влаштовує.")]),
            Segment("– To co? Widzimy się w weekend u Michała? – Tym razem nie dam rady. Jedźcie sami.",
                    [LQ("Z dialogu dowiadujemy się, że ona:", ["planuje spotkanie z przyjaciółmi", "jest w sobotę i niedzielę zajęta", "jeszcze nie wie, czy może się spotkać"], 1,
                        "«nie dam rady» → зайнята на вихідних.")]),
            Segment("– Co się stało? Rozmawiałeś dziś z szefem? – Tak, niestety, od dziś jestem bezrobotny.",
                    [LQ("Z dialogu dowiadujemy się, że mężczyzna:", ["dostał urlop", "dostał podwyżkę", "nie ma już pracy"], 2, "«bezrobotny» → без роботи.")]),
            Segment("– Przepraszam za spóźnienie. Straszne dziś korki. – To już kolejny raz. Następnym razem zaczniemy bez pana!",
                    [LQ("Z dialogu dowiadujemy się, że mężczyzna:", ["nie jest punktualny", "zwykle jest punktualny", "obiecuje poprawę"], 0, "«kolejny raz» → непунктуальний.")]),
            Segment("– Mamo, kupisz mi psa? – Hmm… zastanowię się. A kto będzie się nim opiekował?",
                    [LQ("Z dialogu dowiadujemy się, że matka:", ["uważa, że syn ma dobry pomysł", "jeszcze nie zdecydowała, co zrobi", "chce zajmować się psem"], 1,
                        "«zastanowię się» → ще не вирішила.")]),
            Segment("– Pomożesz mi? Nie mogę wydrukować tego dokumentu. – Oj, wydaje mi się, że musisz kupić nową drukarkę.",
                    [LQ("Z dialogu dowiadujemy się, że:", ["mężczyzna sprzedaje drukarki", "drukarka nie działa", "kobieta pomaga mężczyźnie"], 1, "не друкує → принтер не працює.")]),
            Segment("– Gdzie znajdę ładowarki do smartfonów? – Są na piątym regale po prawej stronie.",
                    [LQ("Z dialogu dowiadujemy się, że on:", ["szuka produktu", "szuka swojej ładowarki", "reklamuje produkt"], 0, "шукає зарядки → шукає товар.")]),
            Segment("– Wszystkiego najlepszego z okazji imienin. – Ale moje imieniny będą dopiero w przyszłym tygodniu.",
                    [LQ("Z dialogu dowiadujemy się, że:", ["kobieta już miała imieniny", "mężczyzna się pomylił", "kobieta ma urodziny"], 1, "іменини лише наступного тижня → помилився.")]),
        ],
    ),
    # Zad III: інтерв'ю про 4-денний тиждень. Ключ: b,c,a,b,c.
    Exercise(
        "s2203_3", "Іспит 2022-03 — Zad III (чотириденний тиждень)",
        "Прослухай інтерв'ю про коротший робочий тиждень. На іспиті лунає двічі.",
        [
            Segment(
                "Praca tylko cztery dni w tygodniu – czy to dobry pomysł? Tak. Najlepszym "
                "przykładem jest nasza firma, która wprowadziła taką organizację pracy dwa lata "
                "temu. Zainspirowały nas firmy z Islandii, które pierwsze wprowadziły to "
                "rozwiązanie w 2015 roku – niektórzy mieszkańcy pracowali tylko cztery dni w "
                "tygodniu, można było zobaczyć, jak krótszy tydzień wpłynie na pracowników. "
                "Mówimy o około trzystu firmach prywatnych i państwowych – reklama, handel, "
                "produkcja, edukacja. Jakie były efekty? Pracownicy byli mniej zestresowani, "
                "bardziej szczęśliwi i mieli więcej czasu dla rodziny. Czy jakość pracy była taka "
                "sama? Osoby, które przepracowały mniej godzin, miały podobne, a nawet lepsze "
                "wyniki. Pensja była taka sama i nikt nie zostawał po godzinach.",
                [
                    LQ("W Islandii można było zaobserwować:",
                       ["jak zaoszczędzić pieniądze", "jakie są minusy i plusy pracy przez 4 dni w tygodniu",
                        "jak pracownicy będą odpoczywać w tygodniu"], 1, "як коротший тиждень вплине."),
                    LQ("Pracodawcy obserwowali zachowanie:",
                       ["dyrektorów instytucji państwowych", "studentów prywatnych uczelni", "przedstawicieli różnych zawodów"], 2,
                       "реклама, торгівля, виробництво, освіта."),
                    LQ("Pracownicy:", ["czuli się lepiej", "czuli się zmęczeni", "zarobili więcej"], 0,
                       "менш стресовані, щасливіші."),
                    LQ("Osoby, które pracowały krócej:",
                       ["nie miały ochoty pracować", "miały lepsze rezultaty niż wcześniej", "miały problem z organizacją czasu"], 1,
                       "подібні, а навіть кращі результати."),
                    LQ("Podczas krótszego tygodnia pracy:",
                       ["wynagrodzenie było niższe", "przerwy na obiad były dłuższe", "warunki finansowe nie zmieniły się"], 2,
                       "зарплата така сама."),
                ],
            )
        ],
    ),
    # Zad IV: історія телефону, TAK/NIE (5). Ключ: N,N,T,N,T.
    Exercise(
        "s2203_4", "Іспит 2022-03 — Zad IV (історія телефону)",
        "Прослухай розмову про історію телефону. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Wszyscy mówią, że Aleksander Bell jest wynalazcą telefonu, bo pod koniec "
                "dziewiętnastego wieku jako pierwszy zarejestrował swój wynalazek w Kanadzie. "
                "Jednak ostatnio słuchałem audycji radiowej i dowiedziałem się, że było dwóch "
                "inżynierów pracujących nad telefonem: Elisha Gray w USA i Aleksander Bell w "
                "Kanadzie. Amerykanin zarejestrował telefon dwie godziny później niż Bell, dlatego "
                "wszyscy uważają, że to Bell. Ale tak naprawdę ani jeden, ani drugi nie jest "
                "prawdziwym ojcem telefonu. Pierwsze urządzenie skonstruował około 20 lat "
                "wcześniej Włoch Antonio Meucci – opracował aparat, żeby rozmawiać z chorą żoną, "
                "gdy pracował w warsztacie. Połączył pierwsze piętro domu, gdzie była sypialnia "
                "żony, z piwnicą, gdzie był warsztat. Opublikował nawet artykuł w gazecie, ale ze "
                "względu na brak pieniędzy nie mógł zarejestrować projektu – kosztowało to 250 dolarów.",
                [
                    LQ("Mężczyzna przeczytał artykuł w gazecie na temat historii telefonu.", _TAKNIE, 1,
                       "НІ — слухав РАДІОпередачу, не читав статтю."),
                    LQ("Pierwszym nieoficjalnym twórcą telefonu był Amerykanin.", _TAKNIE, 1,
                       "НІ — італієць Antonio Meucci (на 20 років раніше)."),
                    LQ("Włoch skonstruował swoje urządzenie, żeby komunikować się z bliską osobą.", _TAKNIE, 0,
                       "ТАК — щоб розмовляти з хворою дружиною."),
                    LQ("Pierwszy telefon łączył ze sobą kilka domów.", _TAKNIE, 1,
                       "НІ — з'єднував поверхи ОДНОГО дому (спальню з майстернею)."),
                    LQ("Rejestracja urządzenia była dla Włocha za droga.", _TAKNIE, 0,
                       "ТАК — бракувало грошей (250 доларів)."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ іспит червень-2022 ════════════════════════════════════════
    # Zad I: 14 висловлювань. Ключ: b,a,c,b,c,a,a,b,c,c,a,b,c,a.
    Exercise(
        "s2206_1", "Іспит 2022-06 — Zad I (короткі висловлювання)",
        "Прослухай коротку фразу й обери правильну відповідь. На іспиті лунає ОДИН раз.",
        [
            Segment("Znowu nie odrobiłeś pracy domowej.",
                    [LQ("Ta wypowiedź jest typowa dla:", ["kelnerki", "nauczycielki", "sprzątaczki"], 1, "про домашнє завдання → вчителька.")]),
            Segment("Aniu, czy poszłabyś ze mną na kolację?",
                    [LQ("Ta wypowiedź oznacza:", ["propozycję", "przeprosiny", "odmowę"], 0, "запрошення на вечерю → пропозиція.")]),
            Segment("Na widowni proszę zajmować co drugie miejsce.",
                    [LQ("Ta wypowiedź oznacza, że:", ["można siadać wszędzie", "wszystkie miejsca są zajęte", "połowa miejsc musi być wolna"], 2,
                        "«co drugie» → половина вільна.")]),
            Segment("Poproszę bułkę i razowy krojony.",
                    [LQ("Ta wypowiedź jest typowa:", ["w kawiarni", "w piekarni", "w sklepie mięsnym"], 1, "булка, хліб → пекарня.")]),
            Segment("Jaka szkoda, że nie przyjedziesz.",
                    [LQ("Ta wypowiedź oznacza:", ["złość", "zadowolenie", "smutek"], 2, "«jaka szkoda» → смуток.")]),
            Segment("Kochani, dzisiaj świętujemy mój awans, więc ja płacę rachunek za obiad.",
                    [LQ("Ta wypowiedź oznacza, że ta osoba:", ["płaci za wszystkich", "płaci tylko za siebie", "inni płacą za niego"], 0,
                        "«ja płacę rachunek» → платить за всіх.")]),
            Segment("Wczoraj nasi skoczkowie narciarscy wywalczyli złoto.",
                    [LQ("Ta wypowiedź oznacza, że sportowcy:", ["zdobyli pierwsze miejsce", "nie zdobyli medalu", "przegrali zawody"], 0,
                        "золото → перше місце.")]),
            Segment("W naszej firmie panuje naprawdę dobra atmosfera.",
                    [LQ("Ta wypowiedź oznacza, że w firmie:", ["jest świeże powietrze", "miło się pracuje", "są ładne kolory ścian"], 1,
                        "добра атмосфера → приємно працювати.")]),
            Segment("Poproszę dwa bilety na spektakl o dwudziestej.",
                    [LQ("Ta wypowiedź jest typowa:", ["w autobusie", "w kinie", "w teatrze"], 2, "спектакль → театр.")]),
            Segment("Proszę pani, to szczepienie jest obowiązkowe przed operacją.",
                    [LQ("Ta wypowiedź oznacza, że:", ["można się zaszczepić", "nie trzeba się szczepić", "trzeba przyjąć szczepionkę"], 2,
                        "«obowiązkowe» → треба щепитися.")]),
            Segment("Ten zielony płaszcz jest dla mnie w sam raz.",
                    [LQ("Ta wypowiedź oznacza, że ubranie:", ["pasuje", "jest za duże", "jest za małe"], 0, "«w sam raz» → пасує.")]),
            Segment("Jedzenie i transport są wliczone w cenę wycieczki.",
                    [LQ("Ta wypowiedź oznacza, że:", ["za dojazd płaci się dodatkowo", "w ofercie jest wyżywienie", "trzeba kupić osobno obiady"], 1,
                        "їжа включена → харчування в оферті.")]),
            Segment("Dziś polecamy ogórkową na żeberkach.",
                    [LQ("Ta wypowiedź jest typowa dla:", ["lekarza", "klienta", "kelnera"], 2, "«polecamy zupę» → офіціант.")]),
            Segment("Jak mogłaś pokazać jej te zdjęcia?!",
                    [LQ("Ta wypowiedź oznacza:", ["złość", "radość", "zainteresowanie"], 0, "докір → злість.")]),
        ],
    ),
    # Zad II: 8 діалогів. Ключ: b,c,c,a,c,b,b,a.
    Exercise(
        "s2206_2", "Іспит 2022-06 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Ile kosztował cię remont łazienki? – Już przestałam liczyć, żeby się nie denerwować.",
                    [LQ("Z dialogu dowiadujemy się, że:", ["remont kosztował zgodnie z planem", "jej zdaniem remont kosztował zbyt dużo", "udało się zaoszczędzić trochę pieniędzy"], 1,
                        "«przestałam liczyć, żeby się nie denerwować» → задорого.")]),
            Segment("– Przekroczyła pani dozwoloną prędkość o 30 km. – To niemożliwe, wydawało mi się, że jechałam wolniej.",
                    [LQ("Z dialogu wynika, że kobieta:", ["jechała za wolno", "jechała zgodnie z przepisami", "nie zgadza się z policjantem"], 2,
                        "«to niemożliwe» → не згодна.")]),
            Segment("– Co ci przeszkadza w tym mieście? – Głównie hałas, ale też zbyt szybkie tempo życia.",
                    [LQ("Z dialogu wynika, że ona:", ["lubi miejski rytm życia", "nie lubi korków", "ceni ciszę i spokój"], 2,
                        "заважає шум і темп → цінує тишу.")]),
            Segment("– Co powiesz na urlop nad morzem? Słońce, plaża, leniuchowanie… – Czyli to samo co rok temu?",
                    [LQ("Z dialogu dowiadujemy się, że on proponuje:", ["wakacje podobne do poprzednich", "nowy sposób spędzenia urlopu", "aktywne wakacje nad wodą"], 0,
                        "«to samo co rok temu» → як торік.")]),
            Segment("– I jak egzamin? – Znowu źle napisałam część teoretyczną.",
                    [LQ("Z dialogu wynika, że kobieta:", ["zdała egzamin", "pierwszy raz podeszła do egzaminu", "ponownie zdawała egzamin"], 2,
                        "«znowu» → повторно складала.")]),
            Segment("– Chciałabym się umówić na mycie i strzyżenie. – Najbliższy wolny termin mamy w następnym tygodniu w środę.",
                    [LQ("Z dialogu dowiadujemy się, że:", ["wizyta jest możliwa pod koniec tygodnia", "wolne terminy są w przyszłym tygodniu", "ona planuje wizytę w myjni"], 1,
                        "термін наступного тижня.")]),
            Segment("– Codziennie tracę mnóstwo czasu na dojazd do pracy. – Gdybyś jeździł tramwajem zamiast samochodem, nie stałbyś w korkach.",
                    [LQ("Z dialogu dowiadujemy się, że:", ["on narzeka na transport publiczny", "ona radzi mu dojazd transportem publicznym", "tramwaj jest tańszy niż samochód"], 1,
                        "радить трамвай → громадський транспорт.")]),
            Segment("– Kochanie, dzisiaj wrócę później z pracy. – Jak to? Przecież obiecaliśmy pojechać po ciocię do szpitala.",
                    [LQ("Z dialogu wynika, że:", ["oni mieli odebrać ciocię ze szpitala", "ona przypomina mu o wizycie u cioci", "oni powinni zawieźć ciocię do lekarza"], 0,
                        "обіцяли забрати тітку зі шпиталю.")]),
        ],
    ),
    # Zad III: розмова про домашню освіту, TAK/NIE (5). Ключ: T,T,N,T,N.
    Exercise(
        "s2206_3", "Іспит 2022-06 — Zad III (домашня освіта)",
        "Прослухай розмову про домашню освіту. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Jak rozpocząć edukację domową? To proste. Wystarczy zgłosić się do dyrektora "
                "szkoły i powiedzieć, że chcielibyśmy przejść na edukację pozaszkolną. Trzeba "
                "wypełnić wniosek z prośbą o zezwolenie, dołączyć oświadczenie, że mamy warunki w "
                "domu, i zobowiązanie, że dziecko przystąpi do egzaminów klasyfikacyjnych – trzy "
                "dokumenty. Podczas egzaminów nie wszystkie przedmioty są brane pod uwagę, np. WF "
                "czy przedmioty artystyczne. Czy można to realizować w dowolnej placówce? "
                "Doradzałbym szkołę przyjaźnie nastawioną do edukacji domowej, bo nie każda "
                "publiczna ma dobre doświadczenia. Edukacja pozaszkolna jest bezpłatna – są "
                "dotacje, które idą za dzieckiem. Ale edukacja domowa nie jest dla każdego: rodzice "
                "muszą się naprawdę zaangażować, nikt ich nie zastąpi.",
                [
                    LQ("Rodzice sami deklarują, że dzieci mogą uczyć się w domu.", _TAKNIE, 0,
                       "ТАК — подають заяву й oświadczenie про умови."),
                    LQ("Egzaminy klasyfikacyjne nie obejmują plastyki czy muzyki.", _TAKNIE, 0,
                       "ТАК — не всі предмети (напр. WF, мистецькі)."),
                    LQ("Podczas edukacji domowej warto wybrać najbliższą szkołę.", _TAKNIE, 1,
                       "НІ — варто школу, ПРИХИЛЬНУ до домашньої освіти, не найближчу."),
                    LQ("Rodzice nie płacą za nauczanie domowe.", _TAKNIE, 0,
                       "ТАК — безкоштовно (дотації йдуть за дитиною)."),
                    LQ("Rodzice mogą liczyć na pomoc nauczycieli.", _TAKNIE, 1,
                       "НІ — мусять самі залучитися, ніхто їх не замінить."),
                ],
            )
        ],
    ),
    # Zad IV: інтерв'ю з лікаркою про домашнє лікування, MCQ (5). Ключ: a,b,b,a,c.
    Exercise(
        "s2206_4", "Іспит 2022-06 — Zad IV (домашнє лікування)",
        "Прослухай інтерв'ю з лікаркою про домашні способи лікування. На іспиті лунає двічі.",
        [
            Segment(
                "Kiedy dziecko gorączkuje, zimne okłady pomagają? Jak najbardziej, ale jeśli mały "
                "pacjent ma 39-40 stopni, najpierw podajemy lek przeciwgorączkowy, a po jakimś "
                "czasie stosujemy okłady na kark lub szyję. Z czego je zrobić? Z zimnej wody – "
                "lepiej nie przykładać kostek lodu, bo to nieprzyjemne. Każdy z nas jest po trochu "
                "lekarzem dla siebie: potrafimy powiedzieć, co nam służy. Są tacy, którzy nie lubią "
                "okładów, i tacy, którzy od razu kładą ręcznik na głowie. Dzieci w gorączce "
                "domagają się zimnych płynów, a rodzice odmawiają, bo się boją – ale to bardzo "
                "dobra metoda, żeby obniżyć temperaturę. A kąpiele? Kąpiel chłodząca dla dziecka z "
                "40 stopniami gorączki powinna odbywać się w wodzie 39 stopni, czyli o stopień "
                "niżej. Nie wrzucamy chorego do zimnej, trzydziestostopniowej wody, bo można "
                "spowodować wstrząs termiczny.",
                [
                    LQ("Kiedy dziecko ma około 40 stopni, należy:",
                       ["podać środek na obniżenie temperatury", "natychmiast zrobić zimny okład", "od razu zastosować obie metody"], 0,
                       "спершу жарознижувальне, потім компрес."),
                    LQ("Najlepiej stosować okłady:", ["z lodu", "z chłodnej wody", "na brzuch"], 1,
                       "із прохолодної води (не лід)."),
                    LQ("Lekarka uważa, że pacjenci:", ["najlepiej leczą się sami", "mają swoje preferencje", "rzadko mówią, co im dolega"], 1,
                       "одні не люблять компресів, інші навпаки → мають уподобання."),
                    LQ("Według lekarki chłodne napoje:",
                       ["mogą pomagać małym pacjentom", "nie powinny być podawane chorym dzieciom", "są podawane chorym dzieciom przez rodziców"], 0,
                       "холодні напої — добрий спосіб знизити температуру."),
                    LQ("Dla dziecka z wysoką gorączką temperatura kąpieli chłodzącej powinna:",
                       ["wynosić maksymalnie 30 stopni", "wynosić tyle stopni, ile temperatura ciała", "być niewiele niższa niż temperatura ciała"], 2,
                       "на один градус нижче (39 при 40)."),
                ],
            )
        ],
    ),
    # ══ РЕАЛЬНИЙ ІСПИТ листопад-2022 (офіц.). Ключі звірено з klucz. ══
    # Zad I: 14 висловлювань. Ключ: a,b,a,c,c,b,a,c,b,c,b,a,c,a.
    Exercise(
        "s2211_1", "Іспит 2022-11 — Zad I (висловлювання)",
        "Прослухай висловлювання й обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("Na pewno zdasz! Jesteś świetnie przygotowana.",
                    [LQ("Ta wypowiedź dotyczy:", ["egzaminu", "rozmowy o pracę", "spektaklu"], 0,
                        "«zdasz, przygotowana» → іспит.")]),
            Segment("Sto lat młodej parze i szczęścia na nowej drodze życia!",
                    [LQ("Ta wypowiedź jest z okazji:", ["urodzin", "ślubu", "awansu"], 1,
                        "«młoda para, nowa droga życia» → весілля.")]),
            Segment("Jutro zrobię przelew za cały kurs.",
                    [LQ("Ta wypowiedź oznacza, że kobieta:", ["jutro zapłaci za lekcje", "jutro zacznie lekcje", "będzie prowadzić lekcje"], 0,
                        "«zrobię przelew za kurs» → завтра заплатить.")]),
            Segment("Czy doliczyć do tych podręczników reklamówkę?",
                    [LQ("Ta wypowiedź jest typowa:", ["w punkcie informacji", "w przebieralni", "przy kasie"], 2,
                        "«doliczyć reklamówkę» → біля каси.")]),
            Segment("Jakie jest danie dnia i jak długo będę czekać?",
                    [LQ("Ta wypowiedź jest typowa:", ["w lodziarni", "w sklepie rybnym", "w barze"], 2,
                        "«danie dnia» → бар/їдальня.")]),
            Segment("Nie mam drobnych, ale reszty nie trzeba.",
                    [LQ("Ta wypowiedź jest typowa dla:", ["kelnera", "klienta", "sprzedawcy"], 1,
                        "«reszty nie trzeba» → клієнт.")]),
            Segment("Pociąg do Warszawy Centralnej wjedzie na tor pierwszy przy peronie drugim.",
                    [LQ("Ta wypowiedź jest typowa:", ["na dworcu PKP", "na dworcu autobusowym", "na przystanku tramwajowym"], 0,
                        "«pociąg, tor, peron» → залізничний вокзал.")]),
            Segment("Ciągle spóźnia się na spotkania. Denerwuje mnie jego zachowanie.",
                    [LQ("Ta wypowiedź wyraża:", ["obawę", "radę", "krytykę"], 2,
                        "«denerwuje mnie zachowanie» → критика.")]),
            Segment("Czy wszystko panu smakowało? Podać coś jeszcze?",
                    [LQ("Ta wypowiedź jest typowa:", ["przed posiłkiem", "po posiłku", "przy wyjściu"], 1,
                        "«czy smakowało» → після їжі.")]),
            Segment("Gdzie mogę odebrać prawo jazdy?",
                    [LQ("Ta wypowiedź jest typowa:", ["na poczcie", "w biurze podróży", "w urzędzie"], 2,
                        "«odebrać prawo jazdy» → в установі.")]),
            Segment("Czy dostanę zniżkę przy zakupie drugiego produktu?",
                    [LQ("To pytanie o:", ["datę ważności", "możliwe rabaty", "dostępność towaru"], 1,
                        "«zniżkę» → про знижки.")]),
            Segment("Mam dwa bilety na piątkowy koncert. Pójdziesz ze mną?",
                    [LQ("Ta wypowiedź to:", ["zaproszenie", "rekomendacja", "rezygnacja"], 0,
                        "«pójdziesz ze mną» → запрошення.")]),
            Segment("W cenie kursu otrzyma pan również wszystkie materiały.",
                    [LQ("Ta wypowiedź jest typowa:", ["w firmie cateringowej", "w biurze tłumaczeń", "w szkole językowej"], 2,
                        "«kurs, materiały» → мовна школа.")]),
            Segment("Czy z tego rachunku mogę robić przelewy w dolarach?",
                    [LQ("Ta wypowiedź jest typowa:", ["w banku", "na poczcie", "w kantorze"], 0,
                        "«rachunek, przelewy» → банк.")]),
        ],
    ),
    # Zad II: 8 діалогів. Ключ: a,c,b,a,b,c,b,c.
    Exercise(
        "s2211_2", "Іспит 2022-11 — Zad II (діалоги)",
        "Прослухай короткий діалог і обери правильну відповідь. На іспиті лунає двічі.",
        [
            Segment("– Słyszałam, że Anka przeprowadza się z Polski do Francji? – Tak, już nawet wynajęła tam mieszkanie.",
                    [LQ("Z dialogu wynika, że Anka:", ["planuje mieszkać za granicą", "chce spędzić wakacje we Francji", "za miesiąc wróci do Polski"], 0,
                        "«przeprowadza się, wynajęła mieszkanie» → житиме за кордоном.")]),
            Segment("– Babciu, zagramy w szachy? – Nie tym razem, kochanie, najpierw musisz odrobić lekcje.",
                    [LQ("Z dialogu wynika, że wnuczka:", ["nie umie grać w szachy", "jest niezdecydowana", "ma inne obowiązki"], 2,
                        "«musisz odrobić lekcje» → інші обов'язки.")]),
            Segment("– Zrobiłem kurczaka po tajsku. – Świetnie, lubię poznawać nowe smaki.",
                    [LQ("Z dialogu wynika, że:", ["kobieta bardzo lubi kuchnię tajską", "kobieta nigdy nie próbowała tej potrawy", "mężczyzna nie umie gotować"], 1,
                        "«nowe smaki» → ще не куштувала.")]),
            Segment("– Ile kosztuje bilet na wystawę? – 30 złotych, ale od jutra wstęp jest bezpłatny.",
                    [LQ("Z dialogu wynika, że:", ["eksponaty niedługo będzie można oglądać za darmo", "wejście na wystawę jest zamknięte", "wystawę można zobaczyć dopiero od jutra"], 0,
                        "«od jutra bezpłatny» → скоро безкоштовно.")]),
            Segment("– Może polecimy na jakąś egzotyczną wyspę? – Wiesz przecież, że boję się latać samolotem.",
                    [LQ("Z dialogu wynika, że:", ["para zaplanowała już podróż", "kobieta marzy o dalekiej podróży", "mężczyzna pierwszy raz poleci samolotem"], 1,
                        "жінка пропонує/мріє, чоловік боїться → мріє про подорож.")]),
            Segment("– Gratuluję odważnej decyzji! – Skąd wiesz, że chcę zrezygnować z pracy i założyć szkołę jazdy?",
                    [LQ("Z dialogu wynika, że mężczyzna:", ["zdał kurs na prawo jazdy", "dostał podwyżkę", "planuje otworzyć własny biznes"], 2,
                        "«założyć szkołę jazdy» → власний бізнес.")]),
            Segment("– I jak oceniasz to biuro rachunkowe? – Myślałem, że nie jest dobre, ale myliłem się.",
                    [LQ("Z dialogu wynika, że mężczyzna:", ["pomylił dwa biura", "zmienił zdanie o biurze", "zgubił rachunek"], 1,
                        "«myliłem się» → змінив думку.")]),
            Segment("– Co chciałbyś dostać na urodziny? – Wiesz, że lubię niespodzianki.",
                    [LQ("Z dialogu wynika, że:", ["kobieta już kupiła prezent", "mężczyzna nie chce prezentu", "kobieta jeszcze nie zdecydowała, co kupić"], 2,
                        "«lubię niespodzianki» → ще не вирішила.")]),
        ],
    ),
    # Zad III: інтерв'ю з maestro czekolady (Janusz Profus), MCQ (5). Ключ: b,a,c,b,c.
    Exercise(
        "s2211_3", "Іспит 2022-11 — Zad III (maestro czekolady)",
        "Прослухай інтерв'ю з майстром шоколаду. Обери правильну відповідь. Лунає двічі.",
        [
            Segment(
                "Jak zaczęła się Pana przygoda z czekoladą? Kiedyś zrobiłem czekoladową rzeźbę na "
                "pewne wydarzenie. Prezes firmy Wedel zobaczył ją i był tak zachwycony, że "
                "postanowił poznać jej twórcę — i tak trafiłem do firmy. Gdzie zdobywał Pan "
                "umiejętności? Przez wiele lat uczyłem się za granicą, u najlepszych mistrzów — tam "
                "zdobywałem kwalifikacje. Jaki powinien być prawdziwy maestro czekolady? Przede "
                "wszystkim musi kochać to, co robi; praca musi sprawiać mu przyjemność, inaczej nic "
                "z tego nie będzie. Co jest największym problemem w Pana pracy? Ciągły pośpiech, "
                "wyścig z czasem — zamówień jest dużo i wszystko na już. Skąd czerpie Pan pomysły "
                "na nowe produkty? Najczęściej z wyjazdów zagranicznych: jeżdżę na targi poza "
                "Polską i tam szukam inspiracji.",
                [
                    LQ("Prezes firmy Wedel:",
                       ["kupił czekoladową rzeźbę", "chciał poznać twórcę rzeźby", "zaproponował mu praktykę"], 1,
                       "«postanowił poznać jej twórcę» → хотів познайомитися з творцем."),
                    LQ("Janusz za granicą:",
                       ["zdobywał kwalifikacje", "prowadził warsztaty", "pracował w fabryce"], 0,
                       "«uczyłem się za granicą» → здобував кваліфікацію."),
                    LQ("Prawdziwy maestro czekolady powinien:",
                       ["mieć własną cukiernię", "uwielbiać smak czekolady", "pracować z pasją"], 2,
                       "«musi kochać to, co robi» → працювати з пристрастю."),
                    LQ("Największym problemem w jego pracy jest:",
                       ["brak zamówień", "ciągły pośpiech", "praca w nocy"], 1,
                       "«wyścig z czasem» → постійний поспіх."),
                    LQ("Pomysły na nowe produkty czerpie:",
                       ["sam w pracowni", "podczas wizyt w polskich fabrykach", "dzięki wyjazdom zagranicznym"], 2,
                       "«z wyjazdów zagranicznych, targi poza Polską» → закордонні поїздки."),
                ],
            )
        ],
    ),
    # Zad IV: styl prowansalski, TAK/NIE (5). Ключ: T,N,T,N,N.
    Exercise(
        "s2211_4", "Іспит 2022-11 — Zad IV (styl prowansalski)",
        "Прослухай текст про провансальський стиль. Познач TAK/NIE. Лунає двічі.",
        [
            Segment(
                "Styl prowansalski pochodzi z południa Francji. Jego najważniejszą cechą jest "
                "naturalność — używa się naturalnych materiałów: drewna, kamienia, lnu. Meble nie "
                "powinny być nowoczesne; wręcz przeciwnie — im starsze, tym lepiej, cenione są stare, "
                "tradycyjne sprzęty. Na tkaninach królują motywy roślinne i kwiatowe, zwłaszcza "
                "lawenda. Trzeba jednak przyznać, że dziś ten styl nie jest już tak popularny jak "
                "minimalistyczny, choć wciąż ma wielu miłośników. Domy w stylu prowansalskim "
                "najczęściej buduje się na wsi, w otoczeniu natury, z dala od wielkich miast.",
                [
                    LQ("Cechą budynków w stylu prowansalskim jest naturalność.", _TAKNIE, 0,
                       "ТАК — натуральність, природні матеріали."),
                    LQ("Meble powinny być nowoczesne.", _TAKNIE, 1,
                       "НІ — цінуються старі, традиційні меблі."),
                    LQ("Na materiałach znajdują się wzory kwiatowe.", _TAKNIE, 0,
                       "ТАК — рослинні й квіткові мотиви, лаванда."),
                    LQ("Dziś styl prowansalski jest tak samo modny jak minimalistyczny.", _TAKNIE, 1,
                       "НІ — не такий популярний, як мінімалістичний."),
                    LQ("Domy w tym stylu buduje się najczęściej w dużych miastach.", _TAKNIE, 1,
                       "НІ — на селі, серед природи, подалі від великих міст."),
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
