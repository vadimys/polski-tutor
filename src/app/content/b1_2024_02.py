"""РЕАЛЬНИЙ минулий іспит B1 — лютий 2024 (certyfikatpolski.pl, egzamin certyfikatowy).

Джерело: 4-5.02.2024-B1_arkusz_egzaminacyjny.pdf + …_transkrypcja.pdf (містить KLUCZ).
ДОСЛІВНО з arkusz, КОЖЕН ключ звірено з офіц. klucz. Наразі — секція Czytanie:
- Zad I (a/b/c ×5, ключ b,a,c,b,c) + Zad II (TAK/NIE ×6, ключ N,N,T,T,T,T)
  + Zad V (вибір слова ×10) — MCQ;
- Zad III (вставити фрагменти) + Zad IV (заголовки↔тексти) — matching.
Далі: Gramatyka (8 Zad) + Słuchanie (5 Zad).
"""

from __future__ import annotations

from app.content.schema import Exam, MatchTask, MCQItem

# ── CZYTANIE — Zad I: «Z tego tekstu wynika…» (a/b/c) ────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Dzień kuriera zaczyna się wcześnie rano w magazynie, gdzie odbiera przesyłki, "
            "sprawdza je i aktualizuje ich dane w systemie informatycznym. Praca jest dynamiczna. "
            "Kurierzy muszą być punktualni, mieć dobrą orientację w terenie i nie bać się pracy "
            "fizycznej.",
            "Z tego tekstu wynika, że:",
            ["kurierzy rano przywożą paczki do magazynu",
             "kurierzy muszą obsługiwać programy komputerowe",
             "praca kuriera jest stresująca i niebezpieczna"], 1,
            "«aktualizuje dane w systemie informatycznym» → мусять працювати з програмами. "
            "Вони ЗАБИРАЮТЬ посилки; про стрес/небезпеку не сказано."),
    MCQItem("czytanie",
            "W tureckiej Kapadocji można oglądać piękne krajobrazy. To najpopularniejsze miejsce "
            "na lot balonem. Tysiące balonów lata tam co rano przez około 250 dni w roku – również "
            "zimą. Bilety należy zarezerwować wcześniej, bo chętnych jest dużo.",
            "Z tego tekstu wynika, że:",
            ["Kapadocję można oglądać również z powietrza",
             "od grudnia do marca loty balonem się nie odbywają",
             "zainteresowanie atrakcją jest niewielkie"], 0,
            "лот балоном → огляд з повітря. Літають «również зимою»; охочих багато."),
    MCQItem("czytanie",
            "Rodzice zastanawiają się, kiedy pójść z dzieckiem do teatru. Odpowiedź: jak "
            "najwcześniej, ale repertuar powinien być dostosowany do wieku. W ofercie są spektakle "
            "nawet dla dzieci, które mają dopiero kilka miesięcy.",
            "Z tego tekstu wynika, że:",
            ["rodzice rzadko szukają przedstawień dla dzieci",
             "dzieci najlepiej bawią się na spektaklach porannych",
             "teatry proponują przedstawienia dla różnych grup wiekowych"], 2,
            "«repertuar dostosowany do wieku», спектаклі навіть для кількамісячних → різні вікові групи."),
    MCQItem("czytanie",
            "Od września do szkoły w Kętach codziennie przychodzi pies Wally i towarzyszy uczniom "
            "na lekcjach. Uczniowie byli bardziej zainteresowani tematyką zajęć, kreatywni, "
            "spokojniejsi i szybciej pracowali, gdy Wally był w klasie.",
            "Z tego tekstu wynika, że:",
            ["Wally bawi się z uczniami między lekcjami",
             "pomysł nauczycielki daje dobre efekty",
             "pies Wally przeszkadza dzieciom w nauce"], 1,
            "учні спокійніші, уважніші, швидше працювали → ідея дає добрі результати."),
    MCQItem("czytanie",
            "Najbardziej depresyjny dzień w roku to trzeci poniedziałek stycznia (Blue Monday). "
            "Termin w 2004 roku wymyślił Cliff Arnall. Przeanalizował: niezbyt dobrą pogodę, złą "
            "kondycję finansową po świętach i niską motywację. Wielu naukowców nie akceptuje "
            "jednak jego analiz.",
            "Z tego tekstu wynika, że:",
            ["Blue Monday przypada pod koniec roku",
             "stan konta nie decyduje o naszym samopoczuciu",
             "część badaczy nie zgadza się z teorią Arnalla"], 2,
            "«wielu naukowców nie akceptuje» → частина не згодна. Blue Monday — у січні; "
            "фінанси якраз є чинником."),
    # ── Zad II: TAK/NIE до тексту «Dzień Nauki Polskiej» ────────────────
    MCQItem("czytanie",
            "TEKST «Dzień Nauki Polskiej»: одне з наймолодших держсвят Польщі, вперше святкували "
            "у 2021 році. Мета — вшанувати найвидатніших ПОЛЬСЬКИХ учених і заохотити молодь до "
            "науки. Дата — 19 лютого, день народження Міколая Коперника. Прості дослідження "
            "доступні кожному (телескопи, мікроскопи). Свято варто відзначати в школах і "
            "університетах; долучатися мають і фірми, що використовують наукові відкриття.",
            "TAK/NIE: Dzień Nauki Polskiej świętujemy już od dawna.",
            ["TAK", "NIE"], 1, "НІ — вперше у 2021 р., одне з наймолодших свят."),
    MCQItem("czytanie", "",
            "TAK/NIE: W tym dniu mówi się o naukowcach z całego świata.",
            ["TAK", "NIE"], 1, "НІ — про ПОЛЬСЬКИХ учених."),
    MCQItem("czytanie", "",
            "TAK/NIE: Głównym celem święta jest promocja nauki wśród dzieci i młodzieży.",
            ["TAK", "NIE"], 0, "ТАК — заохотити молодь, змотивувати учнів до наукової кар'єри."),
    MCQItem("czytanie", "",
            "TAK/NIE: Data Dnia Nauki Polskiej jest wyrazem szacunku dla osiągnięć wielkiego Polaka.",
            ["TAK", "NIE"], 0, "ТАК — день народження Коперника."),
    MCQItem("czytanie", "",
            "TAK/NIE: Nieskomplikowaną aparaturę do badań można łatwo kupić.",
            ["TAK", "NIE"], 0, "ТАК — прості дослідження доступні кожному (телескопи, мікроскопи)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Dzień Nauki Polskiej jest okazją do współpracy szkół z biznesem.",
            ["TAK", "NIE"], 0, "ТАК — фірми/підприємства мають долучатися й показувати відкриття молоді."),
    # ── Zad V: обери найкраще слово (текст про комедію «Sami swoi») ──────
    MCQItem("czytanie",
            "Текст про культову польську комедію «Sami swoi». Обери найкраще слово.",
            "Produkcja powstała w 1967 roku, a jej ___ był Sylwester Chęciński.",
            ["dyrektorem", "reżyserem", "aktorem"], 1, "фільм має → <b>reżysera</b> (режисера)."),
    MCQItem("czytanie", "",
            "Jasiek „John” Pawlak dawno temu ___ do Stanów Zjednoczonych.",
            ["wrócił", "wyjechał", "poszedł"], 1, "до США (напрямок, надовго) → <b>wyjechał</b>."),
    MCQItem("czytanie", "",
            "W czasie jego nieobecności w rodzinnej wsi ___ się zmieniło.",
            ["dużo", "nic", "długo"], 0, "багато змінилося → <b>dużo</b>."),
    MCQItem("czytanie", "",
            "Wesoły nastrój ___ się kończy – a wszystko z powodu sąsiada Kargula.",
            ["krótko", "mało", "szybko"], 2, "настрій ШВИДКО закінчується → <b>szybko</b>."),
    MCQItem("czytanie", "",
            "Opisując losy dwóch rodzin, scenarzysta ___ historię swojego wujka.",
            ["zrobił", "wykorzystał", "wymyślił"], 1, "використав історію дядька → <b>wykorzystał</b>."),
    MCQItem("czytanie", "",
            "___ konfliktu między sąsiadami jest w komediach częstym motywem.",
            ["Temat", "Tytuł", "Plan"], 0, "тема конфлікту → <b>Temat</b>."),
    MCQItem("czytanie", "",
            "Bohaterowie „Samych swoich” ___ o wszystko; symbolem niezgody jest płot.",
            ["wołają", "proszą", "kłócą się"], 2, "сваряться за все → <b>kłócą się</b>."),
    MCQItem("czytanie", "",
            "Nawet widzowie, którzy nie są ___ filmu, uważają go za część kultury.",
            ["fanami", "ulubieńcami", "adoratorami"], 0, "не є <b>fanami</b> (фанатами) фільму."),
    MCQItem("czytanie", "",
            "Dużą ___ miały też dwie kontynuacje komedii.",
            ["opinię", "popularność", "sławę"], 1, "мали велику <b>popularność</b> (популярність)."),
    MCQItem("czytanie", "",
            "Festiwal filmów komediowych jest organizowany ___ na Dolnym Śląsku.",
            ["regularnie", "przypadkowo", "czasowo"], 0, "щороку → <b>regularnie</b> (регулярно)."),
]

# ── CZYTANIE — Zad III: вставити фрагменти (A–H) у текст про мікроапартаменти ──
# Приклад = фрагмент C (у пул не входить). Ключ (klucz): E,A,H,B,G,D,F.
_ZAD3 = MatchTask(
    section="czytanie",
    title="2024 Читання Zad III — встав фрагменти (мікроапартаменти)",
    intro=(
        "Прочитай текст про мікроапартаменти (крихітні квартири). Заповни пропуски 1–7 "
        "фрагментами A–G, що логічно й граматично продовжують речення."
    ),
    options=[
        "na przykład przy uniwersytetach",  # A
        "a konkretnie z Nowego Jorku",  # B
        "które planowały kupić mieszkanie",  # D
        "które aktualnie mają młodzi Polacy",  # E
        "gdzie metr kwadratowy kosztuje",  # F
        "a pierwsze mikrokawalerki powstały",  # G
        "więc zawsze będą zainteresowani",  # H
    ],
    prompts=[
        "1. …są odpowiedzią deweloperów na problemy lokalowe, ___",
        "2. …mikroapartamenty powstają w atrakcyjnych lokalizacjach, ___",
        "3. Młodzi chcą żyć szybko, blisko miasta, ___ takimi mieszkaniami.",
        "4. Idea dotarła do Europy i Azji z Ameryki, ___",
        "5. W Polsce moda pojawiła się na początku XX wieku, ___ we Wrocławiu.",
        "6. …ofertę kierowano do osób, ___ dla swojego dziecka – studenta.",
        "7. …oferty lokali blisko centrum Warszawy, ___ nawet 18 000 zł.",
    ],
    key=[3, 0, 6, 1, 5, 2, 4],  # E,A,H,B,G,D,F
    explain=[
        "«problemy lokalowe, ___» → E (які зараз мають молоді поляки).",
        "«atrakcyjnych lokalizacjach, ___» → A (напр. біля університетів).",
        "«blisko miasta, ___ takimi mieszkaniami» → H (тож завжди будуть зацікавлені).",
        "«z Ameryki, ___» → B (а конкретно з Нью-Йорка).",
        "«na początku XX wieku, ___ we Wrocławiu» → G (а перші мікрокавалерки постали).",
        "«do osób, ___ dla dziecka» → D (які планували купити житло).",
        "«blisko centrum Warszawy, ___ 18 000 zł» → F (де квадратний метр коштує).",
    ],
)

# ── CZYTANIE — Zad IV: зіставити заголовки з фрагментами (адопція пса) ──
# Приклад = фрагмент B (у пул не входить). Ключ (klucz): D,H,A,G,C,F,E.
_ZAD4 = MatchTask(
    section="czytanie",
    title="2024 Читання Zad IV — заголовок до тексту (адопція пса)",
    intro=(
        "«Co trzeba wiedzieć przed adopcją psa» — до кожного заголовка (1–7) добери "
        "правильний фрагмент A–G."
    ),
    options=[
        "Dorosłe zwierzę może zostać w mieszkaniu bez opiekuna, jeśli będziemy go tego "
        "systematycznie uczyć.",  # A
        "Opiekunowie psów są często zaskoczeni, że muszą poświęcić więcej czasu na sprzątanie.",  # C
        "Opieka nad zwierzęciem to nie tylko cena karmy, ale i wizyty u weterynarza czy "
        "regularne szczepienia.",  # D
        "Jeśli nie zgadzamy się na spanie w łóżku czy jedzenie przy stole, powinniśmy ustalić "
        "reguły; cała rodzina musi konsekwentnie wychowywać zwierzę.",  # E
        "Coraz więcej jest hoteli i pensjonatów, do których można przyjechać ze zwierzęciem "
        "i spędzić wakacje.",  # F
        "Wyjście na zewnątrz, gdy świeci słońce, to przyjemność; ale pies nie może zostać "
        "w domu tylko dlatego, że jest zimno lub pada deszcz.",  # G
        "Należy przemyśleć, jaki typ psa będzie pasował do rodziny i jej stylu życia.",  # H
    ],
    prompts=[
        "1. Obowiązki i wydatki",
        "2. Dopasowanie charakterów",
        "3. Samotne chwile",
        "4. Spacer również w niepogodę",
        "5. Porządek musi być",
        "6. Wspólny wypoczynek",
        "7. Szkolenie od pierwszych dni",
    ],
    key=[2, 6, 0, 5, 1, 4, 3],  # D,H,A,G,C,F,E
    explain=[
        "обов'язки й витрати → D (корм, ветеринар, щеплення).",
        "збіг характерів → H (обрати тип пса під стиль життя родини).",
        "самотні миті → A (доросле може лишатися саме, якщо привчати).",
        "прогулянка й у негоду → G (пес не лишається вдома через холод/дощ).",
        "порядок мусить бути → C (більше часу на прибирання).",
        "спільний відпочинок → F (готелі, куди можна з твариною).",
        "виховання з перших днів → E (від початку встановити правила)."
    ],
)

_MATCHING = [_ZAD3, _ZAD4]

EXAM = Exam(
    id="2024-02",
    label="Реальний іспит лютий-2024 (офіц.)",
    kind="real",
    year=2024,
    items=_READING,
    tasks=_MATCHING,
)
