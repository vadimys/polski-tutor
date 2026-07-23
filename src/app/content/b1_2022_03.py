"""РЕАЛЬНИЙ минулий іспит B1 — березень 2022 (certyfikatpolski.pl).

Джерело: 2022.03.26-27_B1_arkusz + _Transkrypcja_nagran.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН
ключ звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad); аудіювання — у listening.py.
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

# ── CZYTANIE — Zad I. Ключ: c,b,a,b,a. ──────────────────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Mieszkańcy Krakowa już po raz dziesiąty sadzą rośliny przy największych ulicach. "
            "Wiosną będziemy podziwiać kompozycje kwiatów i krzewów, wybrane tak, aby były "
            "atrakcyjne o każdej porze roku.",
            "Z tego tekstu wynika, że:",
            ["jest to pierwsza akcja sadzenia kwiatów", "kwiaty będzie można zobaczyć w parkach",
             "rośliny będą wyglądały ładnie przez cały rok"], 2,
            "«atrakcyjne o każdej porze roku» → гарні цілий рік. Це вже 10-та акція; при вулицях, не в парках."),
    MCQItem("czytanie",
            "Od czerwca maksymalna prędkość w mieście to 50 km/h niezależnie od pory dnia. "
            "Wcześniej w nocy można było jechać do 60 km/h. Zgodnie z nowym prawem piesi nie mogą "
            "używać telefonów na pasach.",
            "Z tego tekstu wynika, że obecnie:",
            ["maksymalna prędkość jazdy nocą to 60 km/h",
             "limit prędkości dla samochodów nie zależy od pory dnia",
             "w pobliżu pasów kierowcy nie mogą jechać szybko"], 1,
            "«50 km/h niezależnie od pory dnia» → ліміт не залежить від часу доби."),
    MCQItem("czytanie",
            "Młodzi artyści namalowali obraz przedstawiający Kazimierza Górskiego i jego cytat. "
            "Dzieło powstało w 100. rocznicę urodzin znanego Polaka, na ścianie bloku w Warszawie, "
            "gdzie mieszkał legendarny polski trener.",
            "Z tego tekstu wynika, że Kazimierz Górski:",
            ["urodził się sto lat przed powstaniem obrazu", "był autorem książki o piłce nożnej",
             "był popularnym polskim piłkarzem"], 0,
            "картина у 100-ту річницю народження → народився за 100 років до неї. Він ТРЕНЕР (не гравець)."),
    MCQItem("czytanie",
            "Małe mieszkanie to prawdziwy test dla projektanta. Lustra to idealny element "
            "dekoracji – dają wrażenie większej przestrzeni. W sklepach nie znajdziemy jednak "
            "wielu kształtów i rozmiarów luster, dlatego czasem trzeba je zamawiać.",
            "Z tego tekstu wynika, że:",
            ["łatwo zaprojektować wnętrza małych mieszkań",
             "niektóre kształty luster trzeba wcześniej zamówić",
             "w sklepach jest bardzo duży wybór luster"], 1,
            "«trzeba przygotowywać na zamówienie» → деякі форму треба замовити наперед."),
    MCQItem("czytanie",
            "Dzisiaj rano doszło do pożaru zabytkowego pałacu w Korczewie. W akcji brało udział 30 "
            "strażaków. Ogień zajął cały dach i pierwsze piętro. W pałacu byli pracownicy, którzy "
            "go remontowali, ale nie ma jeszcze informacji o rannych.",
            "Z tego tekstu wynika, że po pożarze:",
            ["nie wiadomo, czy są ranne osoby", "było rannych wielu strażaków",
             "jest niewiele osób rannych"], 0,
            "«nie ma jeszcze informacji o rannych» → невідомо, чи є поранені."),
    # ── Zad II: TAK/NIE — «Połączyła ich miłość do zwierząt». Ключ: T,N,N,T,N,N. ──
    MCQItem("czytanie",
            "TEKСТ: Hanna і Antoni Gucwińscy — подружжя зоологів, вели передачу «Z kamerą wśród "
            "zwierząt» 32 роки. Коли познайомилися, Hanna вже двічі була одружена. Перший чоловік "
            "— багатий, вийшла заміж, бо допоміг родині (не мусили продавати дім); скоро "
            "розлучилися. Другий, Bernard, більшість часу за кордоном на роботі; вона сама вела "
            "дім; згодом розлучення. Antoni мешкав у ТОМУ Ж БУДИНКУ; дружба через кілька років → "
            "1962 шлюб (третій для Hanny). 1971 почали передачу (без телевізійного досвіду). "
            "Мавпи/папуги жили в них удома, тож поводилися природно. Глядачі чекали серій — це "
            "була нагода побачити тварин із зоопарку ВРОЦЛАВА (з різних частин світу).",
            "TAK/NIE: Pierwsze małżeństwo pomogło Hannie uratować rodzinny dom.",
            ["TAK", "NIE"], 0, "ТАК — багатий перший чоловік → батьки не мусили продавати дім."),
    MCQItem("czytanie", "",
            "TAK/NIE: Bernard zabierał Hannę w podróże zagraniczne.",
            ["TAK", "NIE"], 1, "НІ — Bernard був за кордоном САМ (на роботі), вона лишалася вдома."),
    MCQItem("czytanie", "",
            "TAK/NIE: Antoni to drugi mąż Hanny.",
            ["TAK", "NIE"], 1, "НІ — Antoni третій чоловік (Hanna вже двічі була одружена)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Antoni był sąsiadem Hanny i jej kolegą z pracy.",
            ["TAK", "NIE"], 0, "ТАК — мешкав у тому ж будинку + спільна праця в зоопарку."),
    MCQItem("czytanie", "",
            "TAK/NIE: W 1971 roku Antoni i Hanna zostali małżeństwem.",
            ["TAK", "NIE"], 1, "НІ — шлюб у 1962; у 1971 ПОЧАЛИ передачу."),
    MCQItem("czytanie", "",
            "TAK/NIE: W programie występowały zwierzęta z ogrodów zoologicznych z całego świata.",
            ["TAK", "NIE"], 1, "НІ — з зоопарку ВРОЦЛАВА (тварини походили з різних частин світу)."),
    # ── Zad V: обери найкраще слово («Akademia Przyszłości»). ───────────
    MCQItem("czytanie", "Текст-заклик до волонтерства «Akademia Przyszłości». Обери найкраще слово.",
            "___ wolontariusze poznają specjalny program motywacyjny.",
            ["Później", "Najpierw", "Dawniej"], 1, "спершу → <b>Najpierw</b>."),
    MCQItem("czytanie", "", "Stan psychiczny dziecka zmienia się na ___.",
            ["gorsze", "większe", "lepsze"], 2, "змінюється на краще → <b>lepsze</b>."),
    MCQItem("czytanie", "", "96% uczestników ___ wierzyć w siebie!",
            ["zaczyna", "staje", "czuje"], 0, "починає вірити → <b>zaczyna</b>."),
    MCQItem("czytanie", "", "…spotkania z artystami, dziennikarzami czy ___ biznesmenami.",
            ["lokalnymi", "rodzinnymi", "familijnymi"], 0, "місцевими бізнесменами → <b>lokalnymi</b>."),
    MCQItem("czytanie", "", "Skontaktuj się z wolontariuszem, aby ___ na spotkanie.",
            ["zorganizować", "umówić się", "wybrać"], 1, "домовитися про зустріч → <b>umówić się</b>."),
    MCQItem("czytanie", "", "Możesz napisać na ___ wolontariat@akademia.com.",
            ["adres", "numer", "stronę"], 0, "написати на адресу → <b>adres</b>."),
    MCQItem("czytanie", "", "Przez trzy miesiące ___ okres próbny.",
            ["kierujesz", "odbywasz", "pracujesz"], 1, "проходиш випробувальний → <b>odbywasz</b>."),
    MCQItem("czytanie", "", "Jeśli spodoba ci się to zajęcie, zdajesz ___.",
            ["pytania", "test", "sprawę"], 1, "складаєш тест → <b>test</b>."),
    MCQItem("czytanie", "", "Jesteś ___ na ludzi?",
            ["rozmowny", "otwarty", "znany"], 1, "відкритий до людей → <b>otwarty</b>."),
    MCQItem("czytanie", "", "Zgłoś się do ___ „Akademia Przyszłości”!",
            ["programu", "celu", "urzędu"], 0, "долучся до програми → <b>programu</b>."),
]

# ── Zad III: вставити фрагменти («Spacer zamiast spotkania»). Приклад=B. Ключ: G,H,F,A,D,C,E. ──
_ZAD3 = MatchTask(
    section="czytanie",
    title="2022-03 Читання Zad III — встав фрагменти (спацер замість зустрічі)",
    intro="Прочитай текст про ділові зустрічі під час прогулянки. Заповни пропуски 1–7 фрагментами A–H.",
    options=[
        "pierwszych partnerów biznesowych poznawał",  # A
        "jest bardzo szkodliwy dla naszego organizmu",  # C
        "ponieważ możemy łatwiej się skoncentrować",  # D
        "która pracuje w biurze",  # E
        "która jest już popularna w Stanach Zjednoczonych",  # F
        "oraz dbamy o zdrowie",  # G
        "pozytywny wpływ chodzenia na myślenie",  # H
    ],
    prompts=[
        "1. W ten sposób jednocześnie załatwiamy sprawy zawodowe ___.",
        "2. Już tysiące lat temu Arystoteles odkrył ___.",
        "3. Polskie firmy wprowadzają ideę „chodź i rozmawiaj”, ___.",
        "4. Założyciel znanej marki komputerów ___ właśnie w czasie spacerów.",
        "5. Spotkania zwiększają efekty pracy, ___ – nie ma telefonów ani e-maili.",
        "6. Siedzący tryb życia ___, a chodzenie może leczyć wiele chorób.",
        "7. Naukowcy uważają, że osoba, ___, powinna spacerować 2 godziny dziennie.",
    ],
    key=[5, 6, 4, 0, 2, 1, 3],  # G,H,F,A,D,C,E
    explain=[
        "«sprawy zawodowe ___» → F (та дбаємо про здоров'я).",
        "«Arystoteles odkrył ___» → G (позитивний вплив ходьби на мислення).",
        "«ideę, ___» → E (яка вже популярна у США).",
        "«Założyciel… ___ w czasie spacerów» → A (перших партнерів пізнавав).",
        "«zwiększają efekty, ___» → C (бо легше зосередитися).",
        "«Siedzący tryb życia ___» → B (дуже шкідливий для організму).",
        "«osoba, ___, powinna spacerować» → D (яка працює в офісі)."],
)

# ── Zad IV: заголовки↔тексти (типи клієнтів). Приклад=B. Ключ: F,G,A,D,H,C,E. ──
_ZAD4 = MatchTask(
    section="czytanie",
    title="2022-03 Читання Zad IV — тип клієнта↔опис",
    intro="«Jakim typem klienta jesteś?» — до кожного заголовка (1–7) добери фрагмент A–H.",
    options=[
        "Od razu wie, że produkt nie jest dla niego – za kilka dni znów odwiedzi sklep, żeby "
        "oddać towar.",  # A
        "Interesuje go tylko, czy rzecz jest najlepsza; cena nieważna – im wyższa, tym bardziej "
        "zadowolony.",  # C
        "Zadaje wiele pytań, ale zna odpowiedzi – przeczytał wszystko w internecie, instrukcje "
        "umie na pamięć.",  # D
        "Najchętniej pojawia się podczas wyprzedaży; według niego nie warto wchodzić do sklepu "
        "bez promocji.",  # E
        "Zwykle długo dyskutuje ze sprzedawcami: cena za wysoka, kolor nieładny, funkcje "
        "niepraktyczne.",  # F
        "Kupuje mało, wydaje niewiele; chodzi tam, gdzie są darmowe próbki, bo uwielbia je "
        "zbierać.",  # G
        "Spędza minimum 20 minut na powolnym chodzeniu po sklepie, ale wraca z pustą torbą.",  # H
    ],
    prompts=[
        "1. Klient, który szuka wad",
        "2. Klient, który jest kolekcjonerem",
        "3. Klient, który uwielbia zwroty",
        "4. Klient, który wie wszystko",
        "5. Klient, który lubi spacerować",
        "6. Klient, który ma dużo pieniędzy",
        "7. Klient, który szuka rabatów",
    ],
    key=[4, 5, 0, 2, 6, 1, 3],  # F,G,A,D,H,C,E
    explain=[
        "шукає вади → E (довго сперечається про ціну, колір, функції).",
        "колекціонер → F (ходить по безкоштовні зразки).",
        "любить повернення → A (одразу знає, що не для нього, поверне).",
        "знає все → C (усе прочитав, інструкції напам'ять).",
        "любить гуляти → G (20 хв повільно ходить, іде з порожньою торбою).",
        "має багато грошей → B (важливо, щоб було найкраще, ціна неважлива).",
        "шукає знижки → D (приходить на розпродажі)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: відмінювання. Текст про динозаврів. ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про вимирання динозаврів.",
            "Przed ___ katastrofą temperatura na Ziemi była wysoka.",
            ["tę", "tą", "ta"], 1, "przed + орудний → <b>tą</b> katastrofą."),
    MCQItem("gramatyka", "", "…temperatura na ___ Ziemi była wysoka.",
            ["całe", "cały", "całej"], 2, "na + місцевий (жін.) → <b>całej</b>."),
    MCQItem("gramatyka", "", "Temperatura była ___.",
            ["wysoka", "wysoką", "wysokie"], 0, "była + називний (яка?) → <b>wysoka</b>."),
    MCQItem("gramatyka", "", "Dla zwierząt ___ to ochłodzenie było niebezpieczne.",
            ["lądowym", "lądowych", "lądowe"], 1, "dla zwierząt (яких?) родовий мн. → <b>lądowych</b>."),
    MCQItem("gramatyka", "", "Ich ___ nie były przygotowane na takie warunki.",
            ["organizmach", "organizmy", "organizmów"], 1, "підмет (наз. мн.) → <b>organizmy</b>."),
    MCQItem("gramatyka", "", "…nie były przygotowane na ___ warunki.",
            ["takie", "takich", "takim"], 0, "na + знах. (які умови?) → <b>takie</b>."),
    MCQItem("gramatyka", "", "…na takie ___.",
            ["warunkach", "warunków", "warunki"], 2, "na + знах. → <b>warunki</b>."),
    MCQItem("gramatyka", "", "W lepszej sytuacji były zwierzęta, które żyły w ___.",
            ["wodzie", "wodą", "wody"], 0, "w + місцевий → <b>wodzie</b>."),
    MCQItem("gramatyka", "", "Jednak i dla ___ zmieniły się warunki życia.",
            ["nich", "ich", "nim"], 0, "dla + родовий → <b>nich</b>."),
    MCQItem("gramatyka", "", "…z powodu ___ słońca.",
            ["brakiem", "braków", "braku"], 2, "z powodu + родовий → <b>braku</b>."),
    # ── Zad III: ступенювання. Текст про Кашуби. ──
    MCQItem("gramatyka", "Текст про озеро Wdzydze на Кашубах.",
            "Niektórzy sądzą, że jest ono ___ miejscem do kąpieli niż Bałtyk.",
            ["lepszym", "najlepszym", "lepsze"], 0, "вищий ступ. (niż) → <b>lepszym</b>."),
    MCQItem("gramatyka", "", "___ miejscowością wypoczynkową są Wdzydze Kiszewskie.",
            ["Większą", "Największą", "Największej"], 1, "найбільшою → <b>Największą</b>."),
    MCQItem("gramatyka", "", "To właśnie tam ___ odpoczywają turyści.",
            ["częstszych", "częstsze", "najczęściej"], 2, "прислівник (найчастіше) → <b>najczęściej</b>."),
    MCQItem("gramatyka", "", "Atrakcją jest ___ w Polsce park etnograficzny.",
            ["starszy", "najstarszy", "stary"], 1, "найстаріший (у Польщі) → <b>najstarszy</b>."),
    MCQItem("gramatyka", "", "Warto go odwiedzić, aby dowiedzieć się ___ o dawnym życiu.",
            ["większe", "więcej", "większym"], 1, "dowiedzieć się ___ (більше) → <b>więcej</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: więc). ──
    MCQItem("gramatyka", "Текст про Jarmark św. Dominika. Встав сполучник (зайве слово — <b>więc</b>).",
            "Jest głośno i ciekawie, ___ prawie wszędzie coś się dzieje.",
            ["a", "ponieważ", "żeby", "jednak", "lub", "więc"], 1, "причина → <b>ponieważ</b>."),
    MCQItem("gramatyka", "", "Jarmark cieszył się zainteresowaniem, ___ tradycję przerwała II wojna.",
            ["a", "ponieważ", "żeby", "jednak", "lub", "więc"], 3, "протиставлення → <b>jednak</b> (однак)."),
    MCQItem("gramatyka", "", "W 1972 jarmark znów się odbył, ___ zwyczaj istnieje do dziś.",
            ["a", "ponieważ", "żeby", "jednak", "lub", "więc"], 0, "«а звичай» → <b>a</b>."),
    MCQItem("gramatyka", "", "Prezydent przekazuje klucze, ___ impreza mogła się zacząć.",
            ["a", "ponieważ", "żeby", "jednak", "lub", "więc"], 2, "мета → <b>żeby</b>."),
    MCQItem("gramatyka", "", "Turyści przyjeżdżają, aby coś kupić ___ przeżyć piękne chwile.",
            ["a", "ponieważ", "żeby", "jednak", "lub", "więc"], 4, "вибір → <b>lub</b> (або)."),
    # ── Zad VII: вид/способи. Лист Ані до Basi. ──
    MCQItem("gramatyka", "Лист Ані до подруги Basi (планують візит до Кракова).",
            "Jeśli tak, ___, czy to ma być poniedziałek, czy piątek.",
            ["niech wybiorą", "wybralibyście", "wybierzcie"], 2, "наказ до «wy» → <b>wybierzcie</b>."),
    MCQItem("gramatyka", "", "___, jak zareagowaliśmy!",
            ["Zgadnijmy", "Zgadłabyś", "Zgadnij"], 2, "наказ до «ty» → <b>Zgadnij</b>."),
    MCQItem("gramatyka", "", "Gdyby termin Ci ___, przylecielibyśmy w piątek rano.",
            ["pasował", "niech pasuje", "pasowałby"], 0, "«Gdyby ___» форма на -ł → <b>pasował</b>."),
    MCQItem("gramatyka", "", "…___ do Krakowa już w piątek rano.",
            ["przylecieliby", "przylecielibyśmy", "latalibyśmy"], 1, "умовний, 1 ос. мн. → <b>przylecielibyśmy</b>."),
    MCQItem("gramatyka", "", "…a ja ___ pójść do Muzeum Narodowego.",
            ["wolałabym", "wolałaby", "wolałbym"], 0, "умовний, 1 ос. одн. жін. (Ania) → <b>wolałabym</b>."),
    MCQItem("gramatyka", "", "Czy ___ się spotkać z nami po pracy?",
            ["mogłaby", "mogłabyś", "mógłbyś"], 1, "умовний, 2 ос. одн. жін. (Basia) → <b>mogłabyś</b>."),
    MCQItem("gramatyka", "", "Może we troje ___ później do Sukiennic?",
            ["szlibyśmy", "chodzilibyśmy", "poszlibyśmy"], 2, "умовний докон., 1 ос. мн. → <b>poszlibyśmy</b>."),
    MCQItem("gramatyka", "", "Niech Twój brat nam ___, czy będzie ciekawy spektakl.",
            ["powie", "powiedziałby", "mówiłby"], 0, "«niech ___» докон. → <b>powie</b>."),
    MCQItem("gramatyka", "", "___ mi, czy będziemy mogli u Ciebie przenocować.",
            ["Pisz", "Napisz", "Napisałaby"], 1, "наказ докон. до «ty» → <b>Napisz</b>."),
    MCQItem("gramatyka", "", "Jeśli nie, ___ nam pokój w niedrogim hotelu.",
            ["zarezerwuj", "rezerwuj", "rezerwowałabyś"], 0, "наказ докон. до «ty» → <b>zarezerwuj</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: do). Оголошення про квартиру. ──
    MCQItem("gramatyka", "Оголошення про продаж квартири. Встав прийменник (зайве слово — <b>do</b>).",
            "Kawalerka składa się ___ kuchni, łazienki i salonu.",
            ["na", "z", "przez", "do", "pod", "dla"], 1, "składać się z + родовий → <b>z</b>."),
    MCQItem("gramatyka", "", "Na dachu jest taras przeznaczony ___ wszystkich mieszkańców.",
            ["na", "z", "przez", "do", "pod", "dla"], 5, "dla + родовий (для) → <b>dla</b>."),
    MCQItem("gramatyka", "", "Z okna salonu jest piękny widok ___ las i jezioro.",
            ["na", "z", "przez", "do", "pod", "dla"], 0, "widok na + знах. → <b>na</b>."),
    MCQItem("gramatyka", "", "Siłownia będzie czynna ___ całą dobę.",
            ["na", "z", "przez", "do", "pod", "dla"], 2, "тривалість «przez całą dobę» → <b>przez</b>."),
    MCQItem("gramatyka", "", "Proszę dzwonić ___ numer 987654321.",
            ["na", "z", "przez", "do", "pod", "dla"], 4, "dzwonić pod + знах. → <b>pod</b> numer."),
]

# ── Zad IV: вписати форми (тепер./мин.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2022-03 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або минулий час). Текст про фестиваль FETA.\n\n"
           "<i>Приклад: festiwal <b>odbył się</b> (odbyć się) w 1997 roku.</i>"),
    prompts=[
        "1. Obecnie aktorzy ___ (prezentować) spektakle dla różnych widzów.",
        "2. Artyści ___ (zwracać) uwagę na problemy współczesnego świata,",
        "3. …___ (uczyć) i jednocześnie",
        "4. …___ (bawić).",
        "5. Każdy mieszkaniec albo turysta ___ (móc) co roku poznawać teatry uliczne.",
        "6. W zeszłym roku festiwal ___ (obchodzić) 25. urodziny.",
        "7. Organizatorzy ___ (przygotować) wiele niespodzianek.",
        "8. Wolontariuszki ___ (powiesić) piękne plakaty na przystankach.",
        "9. W ciągu 25 lat festiwal ___ (zdobyć) kilka nagród,",
        "10. …a do Gdańska ___ (przyjeżdżać) artyści z całego świata.",
    ],
    accepted=[
        ["prezentują"], ["zwracają"], ["uczą"], ["bawią"], ["może"],
        ["obchodził"], ["przygotowali"], ["powiesiły"], ["zdobył"], ["przyjeżdżali"],
    ],
    explain=[
        "тепер., 3 ос. мн. → <b>prezentują</b>.",
        "тепер., 3 ос. мн. → <b>zwracają</b>.",
        "тепер., 3 ос. мн. → <b>uczą</b>.",
        "тепер., 3 ос. мн. → <b>bawią</b>.",
        "тепер., 3 ос. одн. (każdy) → <b>może</b>.",
        "минулий, 3 ос. одн. чол. (festiwal) → <b>obchodził</b>.",
        "минулий, 3 ос. мн. чол.-ос. → <b>przygotowali</b>.",
        "минулий, 3 ос. мн. жін. (wolontariuszki) → <b>powiesiły</b>.",
        "минулий, 3 ос. одн. чол. → <b>zdobył</b>.",
        "минулий, 3 ос. мн. чол.-ос. → <b>przyjeżdżali</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2022-03 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: pojechała «wczoraj» → Kiedy?</i>"),
    prompts=[
        "Ojciec poszedł na spacer «z synem».",
        "«Mali» chłopcy bawią się wesoło.",
        "«Małgosi» nie było dziś na lekcjach.",
        "Staś poprosił Zosię «o pomarańczę».",
        "To jest pióro «Janka».",
    ],
    accepted=[["z kim"], ["jacy"], ["kogo"], ["o co"], ["czyje"]],
    explain=[
        "з людиною → <b>Z kim?</b>",
        "«jacy chłopcy» → <b>Jacy?</b>",
        "«kogo nie było» → <b>Kogo?</b>",
        "poprosić o + знах. → <b>O co?</b>",
        "«czyje pióro» → <b>Czyje?</b>",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2022-03 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «jeździ nad morze» (spędza) → spędza wakacje nad morzem.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Jakiego koloru jest twój nowy dywan?",
        "Mama narzeka, że cena jabłek jest wysoka.",
        "Zosia przygląda się małym pieskom.",
        "Jakub dał mamie kwiaty.",
        "Nie znam tej kobiety.",
    ],
    words=["ma", "na", "patrzy", "dostała", "kim"],
    models=[
        ["Jaki kolor ma twój nowy dywan?"],
        ["Mama narzeka na wysoką cenę jabłek."],
        ["Zosia patrzy na małe pieski."],
        ["Mama dostała od Jakuba kwiaty."],
        ["Nie wiem, kim jest ta kobieta."],
    ],
)

EXAM = Exam(
    id="2022-03",
    label="Реальний іспит березень-2022 (офіц.)",
    kind="real",
    year=2022,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
