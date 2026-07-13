"""РЕАЛЬНИЙ минулий іспит B1 — листопад 2022 (certyfikatpolski.pl).

Джерело: 2022.11.5-6_B1_arkusz + _Transkrypcja_nagran.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН
ключ звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad); аудіювання — у listening.py.
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

# ── CZYTANIE — Zad I. Ключ: a,c,b,a,b. ──────────────────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Festiwal Letnie Brzmienia to cykl ponad 100 koncertów na świeżym powietrzu w 13 "
            "miastach Polski. Na scenie pojawią się najpopularniejsi polscy artyści. Występy będą "
            "trwać całe wakacje i zakończą się dwudniowym koncertem finałowym.",
            "Z tego tekstu wynika, że festiwal Letnie Brzmienia:",
            ["to seria koncertów wakacyjnych", "odbędzie się w stu polskich miastach",
             "to imprezy w 13 dużych salach koncertowych"], 0,
            "«całe wakacje, na świeżym powietrzu» → серія літніх концертів. 13 міст (не 100); просто неба (не в залах)."),
    MCQItem("czytanie",
            "Europejczycy kupują w sieci częściej niż kiedykolwiek. W grudniu ok. 80% mieszkańców "
            "Wielkiej Brytanii zrobiło zakupy online. Spędzamy też więcej czasu w aplikacjach "
            "zakupowych – korzystamy z nich o 45% dłużej niż w ubiegłym roku.",
            "Z tego tekstu wynika, że:",
            ["internauci spędzają 45% wolnego czasu na zakupach online",
             "w ostatnim roku 80% Europejczyków kupiło coś w internecie",
             "aplikacje zakupowe są coraz popularniejsze"], 2,
            "«частіше ніж будь-коли, о 45% довше» → застосунки дедалі популярніші. 45% — довше, не «часу»; 80% британців у грудні."),
    MCQItem("czytanie",
            "Zapraszamy do odnowionego hotelu ze spokojnym wypoczynkiem. Mamy dwa baseny i SPA, "
            "eleganckie wnętrza. 500 m od obiektu jest prywatna plaża, do której dojeżdża darmowy "
            "bus hotelowy. Goście nie płacą za parking.",
            "Z tego tekstu wynika, że:",
            ["z plaży mogą korzystać wszyscy", "bus na plażę jest bezpłatny",
             "hotel jest nowym budynkiem"], 1,
            "«darmowy bus hotelowy» → безкоштовний. Пляж ПРИВАТНИЙ; готель ВІДНОВЛЕНИЙ (не новий)."),
    MCQItem("czytanie",
            "Andy Warhol namalował „Shot Sage Blue Marilyn” w 1964 roku, dwa lata po śmierci "
            "aktorki. Po 58 latach dom aukcyjny sprzedał dzieło w niewiele ponad 3 minuty – "
            "biznesmen wylicytował je za 195 milionów dolarów.",
            "Z tego tekstu wynika, że:",
            ["klient kupił obraz w niecałe cztery minuty", "obraz powstał za życia Marylin Monroe",
             "zorganizowanie aukcji kosztowało 195 milionów dolarów"], 0,
            "«niewiele ponad 3 minuty» → менш ніж 4 хв. Намалював через 2 роки після смерті; 195 млн — ціна продажу."),
    MCQItem("czytanie",
            "W środku Warszawy, obok najwyższego budynku w stolicy, powstanie nowoczesne osiedle. "
            "W siedmiopiętrowych blokach będzie ponad 200 mieszkań różnej wielkości, które można "
            "kupować od stycznia. Na dachach zaprojektowano zielone tarasy.",
            "Z tego tekstu wynika, że nowe osiedle w Warszawie będzie:",
            ["znajdować się poza centrum miasta", "oferowało ponad 200 lokali",
             "najwyższym osiedlem w stolicy"], 1,
            "«ponad 200 mieszkań» → понад 200 помешкань. У центрі (не поза); поряд із найвищим (само не найвище)."),
    # ── Zad II: TAK/NIE — «Green Velo». Ключ: T,N,T,N,N,N. ──────────────
    MCQItem("czytanie",
            "TEKСТ «Green Velo»: найдовша система велодоріжок у Польщі (понад 2000 км). Ідея — 2008, "
            "як відповідь на інтерес до активного відпочинку й ПРОМОЦІЮ СХІДНОЇ Польщі. Проходить "
            "через 5 воєводств. Турист САМ вирішує, звідки стартувати й де закінчити. Траса "
            "підходить і початківцям, і досвідченим (початківці планують коротші поїздки). Проїхати "
            "весь шлях (від вармінсько-мазурського до свєнтокшиського) — близько 3 ТИЖНІВ. Багато "
            "цікавих місць: від собору у Фромборку до нацпарків, де є тварини, що РІДКО трапляються "
            "в інших регіонах.",
            "TAK/NIE: Szlak rowerowy promuje turystykę we wschodnich regionach Polski.",
            ["TAK", "NIE"], 0, "ТАК — промоція східної частини Польщі."),
    MCQItem("czytanie", "",
            "TAK/NIE: Jeśli zdecydujemy się podróżować szlakiem Green Velo, zwiedzimy pięć "
            "najważniejszych zabytków Polski.",
            ["TAK", "NIE"], 1, "НІ — проходить через 5 ВОЄВОДСТВ (не «5 найважливіших пам'яток»)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Każdy turysta samodzielnie wybiera punkt początkowy i końcowy wycieczki.",
            ["TAK", "NIE"], 0, "ТАК — турист сам вирішує старт і фініш."),
    MCQItem("czytanie", "",
            "TAK/NIE: Korzystanie ze szlaku Green Velo jest polecane tylko doświadczonym rowerzystom.",
            ["TAK", "NIE"], 1, "НІ — і початківцям також (коротші поїздки)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Przejechanie całego szlaku Green Velo zajmuje ponad miesiąc.",
            ["TAK", "NIE"], 1, "НІ — близько 3 тижнів (менше місяця)."),
    MCQItem("czytanie", "",
            "TAK/NIE: W parkach na trasie Green Velo można zobaczyć zwierzęta dobrze znane w całej Polsce.",
            ["TAK", "NIE"], 1, "НІ — тварини, що РІДКО трапляються в інших регіонах."),
    # ── Zad V: обери найкраще слово («Chuseok»). ────────────────────────
    MCQItem("czytanie", "Текст про корейське свято Chuseok. Обери найкраще слово.",
            "Chuseok jest świętem ruchomym, które ___ zgodnie z kalendarzem księżycowym.",
            ["urodzi się", "obchodzi się", "organizuje się"], 1, "святкується → <b>obchodzi się</b>."),
    MCQItem("czytanie", "", "Koreańczycy wracają do domów, żeby ___ w uroczystościach.",
            ["uczestniczyć", "angażować się", "startować"], 0, "брати участь → <b>uczestniczyć</b>."),
    MCQItem("czytanie", "", "W Korei nie ma cmentarzy ___ do tych europejskich.",
            ["zwykłych", "podobnych", "innych"], 1, "«podobnych do» (схожих на) → <b>podobnych</b>."),
    MCQItem("czytanie", "", "Dzień przed i po święcie jest wolny – takie ___ ułatwia przyjazd.",
            ["rozwiązanie", "wytłumaczenie", "konsekwencje"], 0, "таке рішення → <b>rozwiązanie</b>."),
    MCQItem("czytanie", "", "To okres masowych ___ – autostrady są zakorkowane.",
            ["spacerów", "podróży", "dróg"], 1, "масових подорожей → <b>podróży</b>."),
    MCQItem("czytanie", "", "Do domu nie wypada przyjeżdżać z ___ rękami.",
            ["pustymi", "pełnymi", "otwartymi"], 0, "«z pustymi rękami» → <b>pustymi</b>."),
    MCQItem("czytanie", "", "Na spotkaniach nie może ___ świątecznych dań.",
            ["zjeść", "zabraknąć", "ugotować"], 1, "«nie może zabraknąć» → <b>zabraknąć</b>."),
    MCQItem("czytanie", "", "Wielu Koreańczyków ___ tradycyjny strój hanbok.",
            ["kupuje", "prasuje", "zakłada"], 2, "вдягає стрій → <b>zakłada</b>."),
    MCQItem("czytanie", "", "Coraz więcej ___ związanych z tym świętem zanika.",
            ["kultur", "zwyczajów", "przepisów"], 1, "звичаїв → <b>zwyczajów</b>."),
    MCQItem("czytanie", "", "Wiele Koreanek wykorzystuje Chuseok na ___ swojej urody.",
            ["operację", "remont", "poprawę"], 2, "покращення вроди → <b>poprawę</b>."),
]

# ── Zad III: вставити фрагменти (Booksy). Приклад=C. Ключ: G,E,A,H,B,F,D. ──
_ZAD3 = MatchTask(
    section="czytanie",
    title="2022-11 Читання Zad III — встав фрагменти (застосунок Booksy)",
    intro="Прочитай текст про застосунок Booksy. Заповни пропуски 1–7 фрагментами A–H.",
    options=[
        "nawet w środku nocy możesz rezerwować wizytę",  # A
        "odwołać wizytę lub zmienić jej termin",  # B
        "aby umówić się do wybranego specjalisty",  # D
        "w prosty i szybki sposób",  # E
        "na początku warto utworzyć konto w systemie",  # F
        "we współczesnym świecie czas to pieniądz",  # G
        "otrzymasz SMS z przypomnieniem",  # H
    ],
    prompts=[
        "1. …poświęcamy więcej czasu, niż planowaliśmy, a przecież ___, więc liczy się każda minuta.",
        "2. Aplikacja Booksy, dzięki której ___ umówisz się z fryzjerem czy masażystą.",
        "3. Usługa jest dostępna całodobowo, więc ___, a termin będzie na ciebie czekał.",
        "4. Dzień przed spotkaniem ___, dlatego nie musisz się martwić, że zapomnisz.",
        "5. W dowolnym momencie możesz także ___, gdyby coś skomplikowało twoje plany.",
        "6. Aby korzystać z bogatej oferty, ___.",
        "7. Rejestracja nie jest konieczna do przeglądania, ale jest obowiązkowa, ___.",
    ],
    key=[5, 3, 0, 6, 1, 4, 2],  # G,E,A,H,B,F,D
    explain=[
        "«a przecież ___» → G (у сучасному світі час — це гроші).",
        "«dzięki której ___» → E (просто і швидко).",
        "«całodobowo, więc ___» → A (навіть посеред ночі можеш бронювати).",
        "«Dzień przed ___» → H (отримаєш SMS-нагадування).",
        "«możesz także ___» → B (скасувати візит або змінити термін).",
        "«Aby korzystać, ___» → F (варто створити акаунт).",
        "«obowiązkowa, ___» → D (щоб записатися до фахівця)."],
)

# ── Zad IV: заголовок↔текст (екологія). Приклад=B. Ключ: F,H,A,D,G,C,E. ──
_ZAD4 = MatchTask(
    section="czytanie",
    title="2022-11 Читання Zad IV — заголовок↔порада (екологія)",
    intro="«Ekologia w życiu codziennym» — до кожного заголовка (1–7) добери фрагмент A–H.",
    options=[
        "Rozmawiajmy ze znajomymi i rodziną o ekologii; bądźmy cierpliwi i uświadamiajmy innych.",  # A
        "Dbajmy o otoczenie i podnośmy śmieci z ulicy; jeśli widzimy, że ktoś śmieci, zwróćmy "
        "mu uwagę.",  # C
        "Zrezygnujmy z jednorazowych kubków, sztućców i reklamówek; miejmy materiałowe torby "
        "i kubek termiczny.",  # D
        "Wybierzmy rower lub komunikację miejską; jeśli musimy autem – wspólne przejazdy "
        "z kolegami.",  # E
        "Zepsuty telefon? Oddajmy do serwisu, nie kupujmy od razu nowego; ze starego krzesła "
        "można wyczarować cuda.",  # F
        "40% ludzi nadal nie sortuje śmieci, a to jedna z najprostszych metod na poprawę stanu "
        "środowiska.",  # G
        "Reklamy przekonują nas, że powinniśmy mieć coś niepotrzebnego – pomyślmy dwa razy, "
        "zanim kupimy kolejny gadżet.",  # H
    ],
    prompts=[
        "1. Naprawiajmy, nie wyrzucajmy",
        "2. Kupujmy mniej i mądrzej",
        "3. Dyskutujmy i edukujmy",
        "4. Wielorazowy – niech to będzie nasze nowe ulubione słowo",
        "5. Segregujmy odpady",
        "6. Sprzątajmy",
        "7. Zmieńmy myślenie o transporcie",
    ],
    key=[4, 6, 0, 2, 5, 1, 3],  # F,H,A,D,G,C,E
    explain=[
        "ремонтуй, не викидай → F (віддай телефон у сервіс).",
        "купуй менше й розумніше → H (подумай, перш ніж купити гаджет).",
        "дискутуй і навчай → A (розмовляй про екологію).",
        "багаторазовий → D (відмовся від одноразового).",
        "сортуй відходи → G (40% не сортують).",
        "прибираймо → C (піднось сміття з вулиці).",
        "зміни мислення про транспорт → E (велосипед, громадський транспорт)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: відмінювання. Текст про собаку — друга людини. ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про собаку як найкращого друга.",
            "Zwierzęta te są bardzo ___ i potrafią poprawić nam humor.",
            ["towarzyscy", "towarzyskimi", "towarzyskie"], 2, "są ___ (наз. мн. неос.) → <b>towarzyskie</b>."),
    MCQItem("gramatyka", "", "…poprawić humor nawet w ___ dniu tygodnia.",
            ["najgorszy", "najgorszym", "najgorszemu"], 1, "w + місцевий → <b>najgorszym</b> dniu."),
    MCQItem("gramatyka", "", "Plusy posiadania psa można wymieniać bez ___.",
            ["końca", "końcem", "końce"], 0, "bez + родовий → <b>końca</b>."),
    MCQItem("gramatyka", "", "Musimy wspomnieć też o ___, które są trudne.",
            ["momenty", "momentach", "momentów"], 1, "o + місцевий мн. → <b>momentach</b>."),
    MCQItem("gramatyka", "", "Jeśli zdecydujemy się na ___, żeby mieć psa…",
            ["tym", "tego", "to"], 2, "zdecydować się na + знах. → <b>to</b>."),
    MCQItem("gramatyka", "", "…powinniśmy przemyśleć zalety i wady ___ wyboru.",
            ["swojego", "swój", "swojemu"], 0, "wady (чого?) родовий → <b>swojego</b> wyboru."),
    MCQItem("gramatyka", "", "Pies wnosi radość, ale też wiele ___.",
            ["obowiązki", "obowiązków", "obowiązek"], 1, "wiele + родовий мн. → <b>obowiązków</b>."),
    MCQItem("gramatyka", "", "Trzeba wychodzić z ___ na spacery kilka razy dziennie.",
            ["niego", "nich", "nim"], 2, "z + орудний (з ним) → <b>nim</b>."),
    MCQItem("gramatyka", "", "…dbać o regularne wizyty u ___.",
            ["weterynarzom", "weterynarza", "weterynarzem"], 1, "u + родовий → <b>weterynarza</b>."),
    MCQItem("gramatyka", "", "…co zrobimy z psem w czasie ___.",
            ["wakacji", "wakacjach", "wakacje"], 0, "w czasie + родовий → <b>wakacji</b>."),
    # ── Zad III: ступенювання. Текст про сон. ──
    MCQItem("gramatyka", "Текст про важливість сну.",
            "Sen gwarantuje dobrą formę na ___ czas niż kilka filiżanek kawy.",
            ["długo", "dłuższy", "dłużej"], 1, "вищий ступ. прикметника (czas) → <b>dłuższy</b>."),
    MCQItem("gramatyka", "", "Ważnym elementem leczenia jest ___ sen.",
            ["dobrze", "dobry", "lepiej"], 1, "прикметник (який сон?) → <b>dobry</b>."),
    MCQItem("gramatyka", "", "Osoby, które śpią ___ niż 6 godzin, mają wyższe ryzyko zawału.",
            ["najmniej", "mało", "mniej"], 2, "порівняння (niż) → <b>mniej</b>."),
    MCQItem("gramatyka", "", "…mają ___ ryzyko zawału od osób wyspanych.",
            ["najwyższe", "wyższe", "wysokie"], 1, "вищий ступ. (od) → <b>wyższe</b>."),
    MCQItem("gramatyka", "", "Sen jest absolutnie ___ czynnikiem prozdrowotnym.",
            ["najważniejszym", "ważnym", "ważniejszym"], 0, "«absolutnie ___» → найвищий → <b>najważniejszym</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: ani). ──
    MCQItem("gramatyka", "Текст про письменника Miłoszewського. Встав сполучник (зайве слово — <b>ani</b>).",
            "Gdyby pisał tylko wtedy, ___ ma ochotę, nie stworzyłby tekstu.",
            ["ani", "lub", "i", "ponieważ", "kiedy", "a"], 4, "час → <b>kiedy</b> (коли)."),
    MCQItem("gramatyka", "", "Siedzę przy komputerze sześć ___ osiem godzin.",
            ["ani", "lub", "i", "ponieważ", "kiedy", "a"], 1, "вибір → <b>lub</b> (або)."),
    MCQItem("gramatyka", "", "…piję dużo kawy ___ czasem napiszę dziesięć stron.",
            ["ani", "lub", "i", "ponieważ", "kiedy", "a"], 2, "перелік → <b>i</b> (і)."),
    MCQItem("gramatyka", "", "…czasem napiszę dziesięć stron, ___ czasem nic.",
            ["ani", "lub", "i", "ponieważ", "kiedy", "a"], 5, "зіставлення → <b>a</b> (а)."),
    MCQItem("gramatyka", "", "Zawód pisarza jest trudny, ___ wymaga cierpliwości.",
            ["ani", "lub", "i", "ponieważ", "kiedy", "a"], 3, "причина → <b>ponieważ</b> (бо)."),
    # ── Zad VII: вид/способи. Текст-запрошення на Polesie. ──
    MCQItem("gramatyka", "Текст-запрошення відвідати Polesie.",
            "Najchętniej ___ tam każdą wolną chwilę.",
            ["spędźmy", "spędzalibyśmy", "spędzaliby"], 1, "умовний, 1 ос. мн. → <b>spędzalibyśmy</b>."),
    MCQItem("gramatyka", "", "I wy ___ na Polesiu coś dla siebie, gdybyście tam pojechali.",
            ["znaleźlibyście", "znajdujcie", "znaleźliby"], 0, "умовний, 2 ос. мн. (wy) → <b>znaleźlibyście</b>."),
    MCQItem("gramatyka", "", "…gdybyście tam ___.",
            ["pojechali", "pojechalibyście", "jechaliby"], 0, "«gdybyście ___» форма на -li → <b>pojechali</b>."),
    MCQItem("gramatyka", "", "Niech idzie do lasu, a przy okazji ___ grzybów.",
            ["nazbierałbyś", "niech nazbiera", "niech zbiera"], 1, "спонукання 3 ос. докон. → <b>niech nazbiera</b>."),
    MCQItem("gramatyka", "", "Lubicie pływać? ___ w jednym z dwudziestu jezior!",
            ["Wykąpcie się", "Wykąp się", "Kąpalibyście się"], 0, "наказ до «wy» → <b>Wykąpcie się</b>."),
    MCQItem("gramatyka", "", "Jeżeli kogoś ___ ptaki, spotka wiele gatunków.",
            ["interesowaliby", "zainteresowaliby", "interesowałyby"], 2, "умовний, 3 ос. мн. (ptaki) → <b>interesowałyby</b>."),
    MCQItem("gramatyka", "", "…na pewno ___ wiele różnych gatunków.",
            ["spotkałby", "spotkałyby", "niech spotka"], 0, "умовний, 3 ос. одн. (ktoś) → <b>spotkałby</b>."),
    MCQItem("gramatyka", "", "A może ktoś inny ___ zwiedzać zabytki?",
            ["wolałby", "wolałyby", "woleliby"], 0, "умовний, 3 ос. одн. (ktoś) → <b>wolałby</b>."),
    MCQItem("gramatyka", "", "Drogi podróżniku, ___ przyjaciół…",
            ["zabierz", "niech zabierze", "zabierałbyś"], 0, "наказ до «ty» → <b>zabierz</b>."),
    MCQItem("gramatyka", "", "…i razem ___ Włodawę.",
            ["odwiedzalibyście", "odwiedźcie", "odwiedziliby"], 1, "наказ до «wy» → <b>odwiedźcie</b>."),
    # ── Zad VIII: прийменники (вибір у дужках, 3 варіанти). ──
    MCQItem("gramatyka", "Текст про Anetę і «Starą Lodziarnię». Обери правильний прийменник.",
            "Aneta prowadzi „Starą Lodziarnię” ___ znanym warszawskim osiedlu.",
            ["na", "w", "o"], 0, "na + місцевий (на осідлі) → <b>na</b>."),
    MCQItem("gramatyka", "", "Zostawiła dobrze płatną pracę ___ innej branży.",
            ["na", "od", "w"], 2, "w + місцевий (у галузі) → <b>w</b>."),
    MCQItem("gramatyka", "", "…bo ważniejsza była ___ niej rodzinna tradycja.",
            ["do", "dla", "z"], 1, "dla + родовий (для неї) → <b>dla</b>."),
    MCQItem("gramatyka", "", "Jajka ___ produkcji deserów pochodzą z lokalnych ferm.",
            ["do", "dla", "na"], 0, "do + родовий (для виробництва) → <b>do</b>."),
    MCQItem("gramatyka", "", "…pochodzą wyłącznie ___ lokalnych ferm.",
            ["znad", "wśród", "z"], 2, "z + родовий (з ферм) → <b>z</b>."),
]

# ── Zad IV: вписати форми (тепер./майб.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2022-11 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або майбутній час). Текст про екологічну "
           "їзду.\n\n<i>Приклад: ekonomiści <b>mówią</b> (mówić), że ceny nie <b>spadną</b> (spaść).</i>"),
    prompts=[
        "1. Pozytywne efekty każdy kierowca ___ (zobaczyć) w portfelu po kilku tygodniach.",
        "2. Przede wszystkim ___ (my – powinien) zmniejszyć prędkość,",
        "3. …wtedy rzadziej ___ (my – musieć) kupować benzynę.",
        "4. Teraz codziennie ___ (jeździć) do pracy samochodem",
        "5. …i ___ (wydawać) na benzynę bardzo dużo pieniędzy.",
        "6. Na wycieczki zwykle ___ (pakować) za dużo rzeczy do bagażnika.",
        "7. Samochody z dużym bagażem zawsze ___ (palić) więcej.",
        "8. Postanowiłem, że wkrótce ___ (wziąć) kredyt",
        "9. …i za jakiś czas ___ (kupić) auto elektryczne.",
        "10. Za rok żona i ja ___ (wybrać się) na ekologiczne wakacje.",
    ],
    accepted=[
        ["zobaczy"], ["powinniśmy"], ["będziemy musieli"], ["jeżdżę"], ["wydaję"],
        ["pakuję"], ["palą"], ["wezmę"], ["kupię"], ["wybierzemy się"],
    ],
    explain=[
        "майб. докон., 3 ос. одн. (kierowca) → <b>zobaczy</b>.",
        "тепер., 1 ос. мн. → <b>powinniśmy</b>.",
        "майб., 1 ос. мн. → <b>będziemy musieli</b>.",
        "тепер., 1 ос. одн. → <b>jeżdżę</b>.",
        "тепер., 1 ос. одн. → <b>wydaję</b>.",
        "тепер., 1 ос. одн. → <b>pakuję</b>.",
        "тепер., 3 ос. мн. (samochody) → <b>palą</b>.",
        "майб. докон., 1 ос. одн. → <b>wezmę</b>.",
        "майб. докон., 1 ос. одн. → <b>kupię</b>.",
        "майб. докон., 1 ос. мн. → <b>wybierzemy się</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2022-11 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: dowiedzieli się «tydzień temu» → Kiedy?</i>"),
    prompts=[
        "Magda zapłaciła za zakupy «kartą».",
        "Dyskutowali o książce «Doroty Masłowskiej».",
        "Marek spędził całe wakacje «u swojego kuzyna».",
        "Kowalscy wrócili wczoraj «znad morza».",
        "Kierowca jechał «bardzo wolno» po śliskiej drodze.",
    ],
    accepted=[["czym", "jak"], ["o czyjej"], ["u kogo", "gdzie"], ["skąd"], ["jak"]],
    explain=[
        "спосіб оплати → <b>Czym?</b> (Jak?)",
        "«o czyjej książce» → <b>O czyjej?</b>",
        "«u kogo» / місце → <b>U kogo?</b> (Gdzie?)",
        "звідки → <b>Skąd?</b>",
        "спосіб → <b>Jak?</b>",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2022-11 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «Nie wiem, kim jest ten pan» (znam) → Nie znam tego pana.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "W lecie często noszę krótkie spodnie.",
        "Ludwik przepada za lodami czekoladowymi.",
        "Krzysiek zawsze zapomina o moich urodzinach.",
        "Jakiego koloru jest twój samochód?",
        "Niestety, nie było ich na tym koncercie.",
    ],
    words=["chodzę", "uwielbia", "pamięta", "kolor", "nie przyszli"],
    models=[
        ["W lecie często chodzę w krótkich spodniach."],
        ["Ludwik uwielbia lody czekoladowe."],
        ["Krzysiek nigdy nie pamięta o moich urodzinach."],
        ["Jaki kolor ma twój samochód?"],
        ["Niestety, nie przyszli na ten koncert."],
    ],
)

EXAM = Exam(
    id="2022-11",
    label="Реальний іспит листопад-2022 (офіц.)",
    kind="real",
    year=2022,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
