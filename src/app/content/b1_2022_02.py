"""РЕАЛЬНИЙ минулий іспит B1 — лютий 2022 (certyfikatpolski.pl).

Джерело: 2022.02.6-7_B1_arkusz + _Transkrypcja_nagran.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН
ключ звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad); аудіювання — у listening.py.
Reading Zad V — «luki z ramki» (спільний банк слів) → MCQ-per-gap.
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

_ZAD5_BANK = ["dań", "owocowe", "potrawy", "przepis", "próbują",
              "słodko-kwaśnym", "smaku", "wino", "wracają", "zmieniamy"]

# ── CZYTANIE — Zad I. Ключ: a,b,c,a,b. ──────────────────────────────────
_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Firma Apple pracuje nad nowymi funkcjami smartfona. Jedną z nich będzie aplikacja, "
            "która pomoże zdiagnozować problemy psychiczne, m.in. depresję. Jeśli rozpozna objawy, "
            "system wygeneruje skierowanie do lekarza specjalisty.",
            "Z tego tekstu wynika, że:",
            ["w przyszłości smartfony będą rozpoznawać choroby",
             "nowe smartfony już diagnozują choroby",
             "nowa aplikacja poinformuje, jak wyleczyć depresję"], 0,
            "«pracuje nad… będzie aplikacja» → у майбутньому. Ще не діагностують; скерування, не лікування."),
    MCQItem("czytanie",
            "Wśród uczestników castingu do programu sportowego było wiele wysportowanych pań. Były "
            "silne i sprawne, dlatego wzięły udział w półfinale, ale do finału dostali się tylko "
            "mężczyźni.",
            "Z tego tekstu wynika, że:",
            ["kobiety pokazały, że mają większą siłę niż mężczyźni",
             "kobiety nie wzięły udziału w finale programu sportowego",
             "w finale programu są mężczyźni i kobiety"], 1,
            "«do finału tylko mężczyźni» → жінки не у фіналі."),
    MCQItem("czytanie",
            "Grupa polskich turystów miała problem z powrotem. Wylot był zaplanowany w południe, "
            "ale samolot nie przyleciał na lotnisko. Dzięki interwencji biura podróży wszyscy około "
            "23.00 wrócili do kraju.",
            "Z tego tekstu wynika, że:",
            ["biuro podróży nie pomogło w organizacji powrotu turystów",
             "turyści wrócili do Polski następnego dnia o 12:00",
             "samolot nie wystartował o godzinie 12.00"], 2,
            "виліт планувався опівдні, але літак не прилетів → не вилетів о 12. Біуро допомогло; повернулися того ж дня ~23:00."),
    MCQItem("czytanie",
            "Jazda po drogach szybkiego ruchu nie jest elementem kursu na prawo jazdy, dlatego ci, "
            "którzy niedawno zdobyli uprawnienia, nie potrafią jeździć po autostradach. Dla nich "
            "powstał w Poznaniu kurs jazdy autostradą.",
            "Z tego tekstu wynika, że:",
            ["kurs jazdy po autostradzie jest dla osób, które już mają prawo jazdy",
             "w wielu szkołach można uczyć się jeździć autostradą",
             "autostradą nie umieją jeździć doświadczeni kierowcy"], 0,
            "для тих, хто НЕДАВНО здобув права → вони вже мають права. Курс перший такий; недосвідчені, не досвідчені."),
    MCQItem("czytanie",
            "„Jeśli kolejny raz zostanę wybrany na prezesa NBP, będę chciał wprowadzić nowy banknot "
            "o nominale 1000 złotych” – powiedział Adam Glapiński w wywiadzie.",
            "Z tego tekstu wynika, że:",
            ["niedługo w Polsce zostanie wprowadzony banknot 1000 złotych",
             "obecnie w Polsce nie ma banknotu 1000 złotych",
             "Adam Glapiński ponownie zostanie prezesem Narodowego Banku Polskiego"], 1,
            "«будę хотів wprowadzić NOWY banknot 1000» → зараз такого нема. Це умова («jeśli»), не факт."),
    # ── Zad II: TAK/NIE — «Zrezygnujcie czasami z prysznica». Ключ: T,N,N,T,N,T. ──
    MCQItem("czytanie",
            "TEKСТ: автори просять не мити(ся) РІДШЕ роздумати про гігієну. Часте миття → шкіра "
            "менше регенерує, стає сухою й червоною (ризик проблем зі здоров'ям). Бруд важливий: "
            "допомагає шкірі захищати організм від інфекцій; надто часте миття вбиває корисні "
            "бактерії, може дати проблеми зі шлунком/серцем. Порада: приймати душ кілька разів на "
            "тиждень, менше мила (мило теж шкодить шкірі). Хто не хоче відмовлятися від щоденних "
            "купань — скоротити до 3-4 хв і мити лише деякі частини (це й для довкілля добре). Про "
            "Св. Агнешку/Олімпію — НЕ приклад для наслідування.",
            "TAK/NIE: Tekst informuje o negatywnych skutkach częstych kąpieli.",
            ["TAK", "NIE"], 0, "ТАК — суха шкіра, проблеми зі здоров'ям."),
    MCQItem("czytanie", "",
            "TAK/NIE: Kąpiemy się często, ponieważ jesteśmy brudni.",
            ["TAK", "NIE"], 1, "НІ — «nie jesteśmy brudni», миємося за звичкою."),
    MCQItem("czytanie", "",
            "TAK/NIE: Autorzy uważają, że powinniśmy brać przykład ze Świętej Agnieszki i Olimpii.",
            ["TAK", "NIE"], 1, "НІ — «nie prosimy, żebyście przestali się myć»."),
    MCQItem("czytanie", "",
            "TAK/NIE: Jeśli będziemy myć się rzadziej, to będziemy zdrowsi.",
            ["TAK", "NIE"], 0, "ТАК — рідше = менше проблем зі здоров'ям (корисні бактерії)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Według specjalistów należy zrezygnować z kosmetyków do kąpieli.",
            ["TAK", "NIE"], 1, "НІ — радять МЕНШЕ мила, не повна відмова."),
    MCQItem("czytanie", "",
            "TAK/NIE: Warto mniej czasu spędzać w wannie.",
            ["TAK", "NIE"], 0, "ТАК — скоротити купання до 3-4 хв."),
    # ── Zad V: luki z ramki (спільний банк, кожен пропуск = вибір слова) ──
    MCQItem("czytanie", "Текст-реклама рослинного ресторану. Обери слово з рамки для кожного пропуску.",
            "Serwujemy duży wybór ___ kuchni roślinnej.", _ZAD5_BANK, 0, "wybór чого? → <b>dań</b>."),
    MCQItem("czytanie", "", "…szeroki asortyment napojów oraz ___ herbaty.", _ZAD5_BANK, 1,
            "фруктові чаї → <b>owocowe</b>."),
    MCQItem("czytanie", "", "Wiele osób uważa kuchnię wegetariańską za nieciekawą i bez ___.", _ZAD5_BANK, 6,
            "без смаку → <b>smaku</b>."),
    MCQItem("czytanie", "", "Stworzyliśmy miejsce, w którym ___ są zdrowe i pięknie wyglądają.", _ZAD5_BANK, 2,
            "страви → <b>potrawy</b>."),
    MCQItem("czytanie", "", "Menu wegańskie ___ cztery razy w roku.", _ZAD5_BANK, 9, "змінюємо → <b>zmieniamy</b>."),
    MCQItem("czytanie", "", "Nową potrawę najpierw ___ pracownicy, a potem goście.", _ZAD5_BANK, 4, "куштують → <b>próbują</b>."),
    MCQItem("czytanie", "", "Bierzemy pod uwagę sugestie i modyfikujemy ___ na daną potrawę.", _ZAD5_BANK, 3,
            "рецепт → <b>przepis</b>."),
    MCQItem("czytanie", "", "…wegańska „kaczka” w sosie ___ czy tatar z buraka.", _ZAD5_BANK, 5,
            "кисло-солодкий соус → <b>słodko-kwaśnym</b>."),
    MCQItem("czytanie", "", "Doradzamy, jakie ___ wybrać, by uzupełniło smak potrawy.", _ZAD5_BANK, 7,
            "вино → <b>wino</b>."),
    MCQItem("czytanie", "", "…restauracją, do której klienci ___ z radością.", _ZAD5_BANK, 8, "повертаються → <b>wracają</b>."),
]

# ── Zad III: вставити фрагменти (спорт для сеньйорів). Приклад=C. Ключ: B,E,G,A,F,D,H. ──
_ZAD3 = MatchTask(
    section="czytanie",
    title="2022-02 Читання Zad III — встав фрагменти (спорт для сеньйорів)",
    intro="Прочитай текст про спорт для сеньйорів. Заповни пропуски 1–7 фрагментами A–H.",
    options=[
        "czyli popularne spacery z kijami",  # A
        "a inne można dla nich trochę zmodyfikować",  # B
        "że to też jest rodzaj sportu",  # D
        "żeby osoby nie mogły dotykać stopami dna basenu",  # E
        "czyli na świeżym powietrzu",  # F
        "każda z osób ma specjalne ubranie",  # G
        "dlatego warto zapisać się do klubu seniora",  # H
    ],
    prompts=[
        "1. Niektóre dyscypliny są idealne dla seniorów, ___.",
        "2. Ćwiczenia odbywają się w głębokim basenie po to, ___.",
        "3. Dla bezpieczeństwa ___. Jest ono potrzebne, aby się nie utopić.",
        "4. Drugi pomysł to nordic walking dla seniorów, ___.",
        "5. Ten sport jest uprawiany w lasach lub parkach, ___.",
        "6. Prawie wszyscy lubią wycieczki, ale nie wszyscy wiedzą, ___.",
        "7. Najlepiej zwiedzać z grupą osób w naszym wieku, ___.",
    ],
    key=[1, 3, 5, 0, 4, 2, 6],  # B,E,G,A,F,D,H
    explain=[
        "«idealne dla seniorów, ___» → B (а інші можна трохи змінити).",
        "«w głębokim basenie po to, ___» → D (щоб не діставати ногами дна).",
        "«Dla bezpieczeństwa ___» → F (кожен має спеціальний одяг).",
        "«nordic walking, ___» → A (тобто популярні прогулянки з палицями).",
        "«w lasach lub parkach, ___» → E (тобто на свіжому повітрі).",
        "«nie wszyscy wiedzą, ___» → C (що це теж вид спорту).",
        "«osób w naszym wieku, ___» → G (тому варто записатися до клубу сеньйора)."],
)

# ── Zad IV: заголовки↔тексти (як обрати школу). Приклад=C. Ключ: F,G,H,A,B,E,D. ──
_ZAD4 = MatchTask(
    section="czytanie",
    title="2022-02 Читання Zad IV — заголовок↔текст (вибір школи)",
    intro="«Jak wybrać szkołę średnią?» — до кожного заголовка (1–7) добери фрагмент A–H.",
    options=[
        "Nie warto kierować się rankingami i prestiżem – szkoła powinna pomóc ci się rozwinąć, "
        "a nie zmuszać do wysokich ocen.",  # A
        "Zastanów się, co ma dla ciebie największe znaczenie: duża szkoła? rozwijanie "
        "zainteresowań? oceny? koledzy?",  # B
        "Wygodnie jest mieć szkołę blisko – długie dojazdy kosztują i wpływają na jakość życia "
        "(np. czy się wyśpisz).",  # D
        "Wielu uczniów szuka szkoły pod koniec ósmej klasy; szkoły średnie to licea, technika "
        "i szkoły branżowe.",  # E
        "Szkoła średnia to ważny etap: otwiera drogę do kariery, poznasz nowych ludzi, niektóre "
        "chwile zapamiętasz na całe życie.",  # F
        "Twój temperament jest ważny; wybór szkoły to TWÓJ wybór, nie twoich rodziców.",  # G
        "Warto zainteresować się tym, co szkoła oferuje poza programem: kursy, warsztaty, akcje, "
        "zawody, konkursy.",  # H
    ],
    prompts=[
        "1. Po co szkoła średnia?",
        "2. To nie decyzja mamy czy taty",
        "3. Po lekcjach",
        "4. Czy opinia o szkole jest ważna?",
        "5. Najważniejsze w edukacji",
        "6. Jaki typ szkoły wybrać?",
        "7. Droga do szkoły",
    ],
    key=[4, 5, 6, 0, 1, 3, 2],  # F,G,H,A,B,E,D (без przykładu C)
    explain=[
        "нащо середня школа → E (важливий етап, шлях до кар'єри).",
        "не рішення мами чи тата → F (це ТВІЙ вибір).",
        "після уроків → G (гуртки, майстерні, конкурси поза програмою).",
        "чи важлива думка про школу → A (не орієнтуйся на рейтинги/престиж).",
        "найважливіше в освіті → B (що для тебе має значення).",
        "який тип школи → D (ліцей, технікум, галузева).",
        "дорога до школи → C (зручно мати школу поряд)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: відмінювання. Текст про Aleksandrę (репортерку в зонах війни). ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про Олю, яка їздить у небезпечні країни.",
            "Dziewczyna zawsze obiecuje ___, że to będzie ostatni wyjazd.",
            ["babci", "babcię", "babcie"], 0, "obiecać + давальний → <b>babci</b>."),
    MCQItem("gramatyka", "", "…że to będzie jej ___ wyjazd.",
            ["ostatnim", "ostatni", "ostatniego"], 1, "наз. (який виїзд?) → <b>ostatni</b>."),
    MCQItem("gramatyka", "", "…wciąż wraca do niebezpiecznych ___.",
            ["miejsc", "miejsca", "miejscach"], 0, "do + родовий мн. → <b>miejsc</b>."),
    MCQItem("gramatyka", "", "„Ola od dziecka była ___” – opowiada mama.",
            ["odważna", "odważnej", "odważną"], 0, "była + називний (яка?) → <b>odważna</b>."),
    MCQItem("gramatyka", "", "W szkole i na ___ zawsze była liderem.",
            ["podwórko", "podwórku", "podwórka"], 1, "na + місцевий → <b>podwórku</b>."),
    MCQItem("gramatyka", "", "Najbardziej interesowała ___ historia i polityka.",
            ["jej", "ją", "nią"], 1, "interesować + знах. (кого?) → <b>ją</b>."),
    MCQItem("gramatyka", "", "…dlatego ukończyła ___ na uniwersytecie.",
            ["politologię", "politologią", "politologii"], 0, "ukończyć + знах. → <b>politologię</b>."),
    MCQItem("gramatyka", "", "Podczas studiów pracowała jako ___ w organizacjach.",
            ["wolontariusz", "wolontariuszem", "wolontariuszu"], 0, "pracować jako + називний → <b>wolontariusz</b>."),
    MCQItem("gramatyka", "", "Nigdy nie przeszła obojętnie obok ___, kto potrzebował pomocy.",
            ["nikt", "nikogo", "nikim"], 1, "obok + родовий → <b>nikogo</b>."),
    MCQItem("gramatyka", "", "Oboje z mężem jesteśmy z niej ___.",
            ["dumni", "dumne", "dumnymi"], 0, "jesteśmy ___ (наз. мн. чол.-ос.) → <b>dumni</b>."),
    # ── Zad III: ступенювання. Текст про чай. ──
    MCQItem("gramatyka", "Текст про чай.",
            "Herbata i posiłek to ___ połączenie.",
            ["źle", "złe", "gorzej"], 1, "погане поєднання (наз.) → <b>złe</b>."),
    MCQItem("gramatyka", "", "Powinno się ją pić nie ___ niż godzinę po jedzeniu.",
            ["wcześniej", "wcześnie", "najwcześniej"], 0, "порівняння (niż) → <b>wcześniej</b>."),
    MCQItem("gramatyka", "", "Biała herbata ma smak ___ od innych.",
            ["delikatniejszy", "najdelikatniejszy", "delikatny"], 0, "вищий ступ. (od innych) → <b>delikatniejszy</b>."),
    MCQItem("gramatyka", "", "Zielona nazywana jest ___ napojem świata.",
            ["zdrowym", "zdrowszym", "najzdrowszym"], 2, "найздоровішим (у світі) → <b>najzdrowszym</b>."),
    MCQItem("gramatyka", "", "Czerwona ___ działa na osoby, które się odchudzają.",
            ["korzystny", "korzystnie", "najkorzystniejsza"], 1, "прислівник (як діє?) → <b>korzystnie</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: więc). ──
    MCQItem("gramatyka", "Текст про вік і здоров'я. Встав сполучник (зайве слово — <b>więc</b>).",
            "Teraz zmieniła zdanie, ___ sama ma już tyle lat.",
            ["żeby", "że", "więc", "chociaż", "bo", "i"], 4, "причина → <b>bo</b>."),
    MCQItem("gramatyka", "", "Kobieta uważa, ___ wiek biologiczny nie jest ważny.",
            ["żeby", "że", "więc", "chociaż", "bo", "i"], 1, "«uważa, ___» → <b>że</b>."),
    MCQItem("gramatyka", "", "Najważniejsze jest zdrowie ___ aktywność fizyczna.",
            ["żeby", "że", "więc", "chociaż", "bo", "i"], 5, "перелік → <b>i</b> (та)."),
    MCQItem("gramatyka", "", "Co trzeba robić, ___ czuć się młodo?",
            ["żeby", "że", "więc", "chociaż", "bo", "i"], 0, "мета → <b>żeby</b>."),
    MCQItem("gramatyka", "", "Mama wygląda świetnie, ___ ma już 70 lat.",
            ["żeby", "że", "więc", "chociaż", "bo", "i"], 3, "допуст → <b>chociaż</b> (хоча)."),
    # ── Zad VII: вид/способи. Діалог з блогерами-велосипедистами. ──
    MCQItem("gramatyka", "Діалог: подружжя-блогери про велоподорожі Австрією.",
            "Gdybyśmy tego nie ___, nasze życie nie byłoby tak kolorowe.",
            ["robili", "robilibyśmy", "zrobilibyśmy"], 0, "«gdybyśmy nie ___» форма на -li → <b>robili</b>."),
    MCQItem("gramatyka", "", "…nasze życie nie ___ tak kolorowo.",
            ["wyglądajmy", "wyglądałoby", "wyglądaliby"], 1, "умовний, ніяк. → <b>wyglądałoby</b>."),
    MCQItem("gramatyka", "", "„___, tak jak my, miłośnikiem podróży!”",
            ["Zostawałbyś", "Zostańmy", "Zostań"], 2, "наказ до «ty» → <b>Zostań</b>."),
    MCQItem("gramatyka", "", "Nie ___ wypraw rowerowych z Austrią, gdyby nie znajomy.",
            ["połączylibyśmy", "połączmy", "łączmy"], 0, "умовний, 1 ос. мн. → <b>połączylibyśmy</b>."),
    MCQItem("gramatyka", "", "„___ rowery i jedźcie ze mną do Austrii”.",
            ["Wzięłybyście", "Wzięliby", "Weźcie"], 2, "наказ до «wy» → <b>Weźcie</b>."),
    MCQItem("gramatyka", "", "„Weźcie rowery i ___ ze mną w lipcu do Austrii”.",
            ["jechalibyście", "jedźcie", "pojechaliby"], 1, "наказ до «wy» → <b>jedźcie</b>."),
    MCQItem("gramatyka", "", "Kto by ___, że Austria latem ma dużo do zaoferowania!",
            ["uwierzył", "uwierzyłabym", "uwierzyła"], 0, "«Kto by ___» → <b>uwierzył</b>."),
    MCQItem("gramatyka", "", "…czy seniorzy i dzieci też by sobie na tych trasach ___.",
            ["poradzili", "poradziliby", "radziłyby"], 0, "«by… ___» → <b>poradzili</b> (розділений умовний)."),
    MCQItem("gramatyka", "", "„Nie ___ zbyt długo…”",
            ["myślelibyście", "myślcie", "pomyślcie"], 1, "наказ до «wy», недок. → <b>myślcie</b>."),
    MCQItem("gramatyka", "", "„…i ___ swoich bliskich na aktywne wakacje”.",
            ["zapraszalibyście", "zaprosilibyście", "zaproście"], 2, "наказ докон. до «wy» → <b>zaproście</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: na). Текст про Каліфорнію. ──
    MCQItem("gramatyka", "Текст про акторку в Каліфорнії. Встав прийменник (зайве слово — <b>na</b>).",
            "Małgorzata zamieszkała ___ Kalifornii.",
            ["z", "w", "nad", "przez", "na", "za"], 1, "w + місцевий → <b>w</b> Kalifornii."),
    MCQItem("gramatyka", "", "Los Angeles leży ___ oceanem.",
            ["z", "w", "nad", "przez", "na", "za"], 2, "nad + орудний (біля води) → <b>nad</b>."),
    MCQItem("gramatyka", "", "Niedaleko ___ miastem są wzgórza i piękne widoki.",
            ["z", "w", "nad", "przez", "na", "za"], 5, "za + орудний (за містом) → <b>za</b>."),
    MCQItem("gramatyka", "", "W mieście jest dużo turystów ___ cały rok.",
            ["z", "w", "nad", "przez", "na", "za"], 3, "тривалість → <b>przez</b> cały rok."),
    MCQItem("gramatyka", "", "Często odwiedza mały klub ___ muzyką na żywo.",
            ["z", "w", "nad", "przez", "na", "za"], 0, "klub z + орудний → <b>z</b> muzyką."),
]

# ── Zad IV: вписати форми (тепер./мин.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2022-02 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або минулий час). Текст Sary з Англії про "
           "життя в Польщі.\n\n<i>Приклад: nie <b>planowałam</b> (planować), <b>mówi</b> (mówić).</i>"),
    prompts=[
        "1. Kiedy po sześciu latach ___ (ja – przylecieć) do Polski, była zima.",
        "2. …i wasz kraj mi się nie ___ (spodobać).",
        "3. Wiosną zielone krajobrazy ___ (przypominać) mi rodzinną Anglię.",
        "4. Kilka miesięcy później ___ (ja – poznać) tu swojego męża.",
        "5. …i razem ___ (my – zdecydować się) zamieszkać w Polsce.",
        "6. Sara i Witold są aktywni, ___ (kochać) podróże.",
        "7. Z każdego wyjazdu zwykle ___ (my – kupować) tradycyjne pamiątki.",
        "8. Kilka lat temu w domu ___ (urządzić) pensjonat.",
        "9. …i do dzisiaj ___ (wynajmować) apartamenty dla gości.",
        "10. Na ścianach ___ (wisieć) pamiątki z ich podróży.",
    ],
    accepted=[
        ["przyleciałam"], ["spodobał"], ["przypominały"], ["poznałam"], ["zdecydowaliśmy się"],
        ["kochają"], ["kupujemy"], ["urządzili"], ["wynajmują"], ["wiszą"],
    ],
    explain=[
        "минулий, 1 ос. одн. жін. → <b>przyleciałam</b>.",
        "минулий, 3 ос. одн. чол. (kraj) → <b>spodobał</b>.",
        "минулий, 3 ос. мн. не-чол.-ос. (krajobrazy) → <b>przypominały</b>.",
        "минулий, 1 ос. одн. жін. → <b>poznałam</b>.",
        "минулий, 1 ос. мн. → <b>zdecydowaliśmy się</b>.",
        "тепер., 3 ос. мн. → <b>kochają</b>.",
        "тепер., 1 ос. мн. → <b>kupujemy</b>.",
        "минулий, 3 ос. мн. чол.-ос. (Sara i Witold) → <b>urządzili</b>.",
        "тепер., 3 ос. мн. → <b>wynajmują</b>.",
        "тепер., 3 ос. мн. (pamiątki) → <b>wiszą</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2022-02 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: przyglądała się «zdjęciom» → Czemu?</i>"),
    prompts=[
        "Dyrektor szukał «dobrego pracownika».",
        "Przez pomyłkę zjadłam frytki «Filipa».",
        "Poprosiliśmy «o potrzebne dokumenty».",
        "Polski tenisista wygrał «z hiszpańskim zawodnikiem».",
        "Ola planuje «piąty» wyjazd do Chorwacji.",
    ],
    accepted=[["kogo", "jakiego pracownika"], ["czyje"], ["o co"], ["z kim"], ["który"]],
    explain=[
        "szukać + родовий → <b>Kogo?</b> (Jakiego pracownika?)",
        "«czyje frytki» → <b>Czyje?</b>",
        "poprosić o + знах. → <b>O co?</b>",
        "wygrać z + орудний → <b>Z kim?</b>",
        "«który wyjazd» → <b>Który?</b>",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2022-02 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «zna angielski» (mówi) → mówi po angielsku.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Mój przyjaciel sprzeda mi rower.",
        "Kasia opiekowała się młodszą siostrą.",
        "Ile kosztuje ta sukienka?",
        "Nie smakuje mi sałatka jarzynowa.",
        "Tę znaną melodię skomponował polski muzyk.",
    ],
    words=["kupię", "dbała o", "cena", "nie lubię", "autorem"],
    models=[
        ["Kupię rower od mojego przyjaciela."],
        ["Kasia dbała o młodszą siostrę."],
        ["Jaka jest cena tej sukienki?", "Jaka cena tej sukienki?"],
        ["Nie lubię sałatki jarzynowej."],
        ["Autorem znanej melodii jest polski muzyk.",
         "Polski muzyk jest autorem znanej melodii."],
    ],
)

EXAM = Exam(
    id="2022-02",
    label="Реальний іспит лютий-2022 (офіц.)",
    kind="real",
    year=2022,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
