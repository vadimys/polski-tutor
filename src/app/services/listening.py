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
]


def by_id(exercise_id: str) -> Exercise | None:
    return next((e for e in EXERCISES if e.id == exercise_id), None)


def pick() -> Exercise:
    return random.choice(EXERCISES)


def total_questions(ex: Exercise) -> int:
    return sum(len(s.questions) for s in ex.segments)
