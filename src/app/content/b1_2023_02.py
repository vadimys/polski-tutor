"""РЕАЛЬНИЙ минулий іспит B1 — лютий 2023 (certyfikatpolski.pl).

Джерело: 2023_02_5_6_B1_arkusz + …_transkrypcja.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН ключ
звірено з офіц. klucz. Czytanie + Gramatyka (усі 8 Zad):
- Czytanie: Zad I (×5) + Zad II (TAK/NIE ×6) + Zad V (×10) MCQ; Zad III/IV matching.
- Gramatyka: I(×10)+II(×5)+III(×5)+VII(×10)+VIII(×5) MCQ; IV(×10)+V(×5) free-fill; VI(×5) open.
Далі: Słuchanie (5 Zad).
"""

from __future__ import annotations

from app.content.schema import Exam, FreeFillTask, MatchTask, MCQItem, OpenTask

_READING: list[MCQItem] = [
    MCQItem("czytanie",
            "Sędzia przerwał mecz piłki nożnej po 26 minutach, ponieważ kibice byli bardzo "
            "agresywni. Interweniowała policja i sytuacja została opanowana, ale sędzia nie "
            "kontynuował gry. Oba kluby mogą spodziewać się wysokich kar.",
            "Z tego tekstu wynika, że:",
            ["piłkarze z przeciwnych drużyn pokłócili się podczas gry",
             "kibice zachowywali się podczas meczu nieodpowiednio",
             "po interwencji policji drużyny dokończyły spotkanie"], 1,
            "«kibice byli agresywni» → поводилися неналежно. Матч НЕ дограли."),
    MCQItem("czytanie",
            "Dentysty boją się dzieci i dorośli – to najczęstszy powód rezygnacji z wizyt, co "
            "wpływa na stan zębów. Główną przyczyną strachu są złe wspomnienia związane z bólem, "
            "który kiedyś odczuwaliśmy w gabinecie.",
            "Z tego tekstu wynika, że:",
            ["dzieci boją się dentysty bardziej niż dorośli",
             "nie chodzimy do dentysty, bo nie bolą nas zęby",
             "boimy się dentysty, ponieważ pamiętamy ból z wcześniejszych wizyt"], 2,
            "«złe wspomnienia związane z bólem» → пам'ятаємо біль."),
    MCQItem("czytanie",
            "W Polsce niezadowoleni klienci najczęściej oddają buty i zegarki, ale nie zawsze "
            "wiedzą, jakiego dokumentu potrzebują. Często nie odróżniają reklamacji od zwrotu ani "
            "paragonu od faktury. Konsumenci nadal nie znają dobrze swoich praw.",
            "Z tego tekstu wynika, że:",
            ["Polacy niechętnie zwracają kupione obuwie",
             "w Polsce klienci słabo orientują się w prawach konsumenta",
             "reklamy produktów powinny informować o prawach konsumentów"], 1,
            "«nie znają dobrze swoich praw» → погано орієнтуються у правах."),
    MCQItem("czytanie",
            "Najnowszą produkcję Netfliksa „Broad Peak” w reżyserii Leszka Dawida można było "
            "obejrzeć po raz pierwszy w niektórych kinach 9 września. To film o miłości do gór, "
            "pasji i determinacji. W roli głównej występuje Ireneusz Czop.",
            "Z tego tekstu wynika, że:",
            ["Leszek Dawid wystąpił w filmie o górach",
             "premiera Broad Peak odbyła się dziewiątego września",
             "film można obejrzeć tylko na platformie Netflix"], 1,
            "«po raz pierwszy… 9 września» → прем'єра 9 вересня. Dawid — режисер (не грав); "
            "показ був і в кіно."),
    MCQItem("czytanie",
            "Opakowania i transport są coraz droższe, dlatego restauracje muszą kupować np. "
            "dziesięć beczek piwa zamiast czterech, ale brakuje im pieniędzy. Właściciele nie "
            "podnoszą jednak cen, bo boją się, że biedniejsi klienci przestaną ich odwiedzać.",
            "Z tego tekstu wynika, że:",
            ["restauracje utrzymują stałe ceny, bo chcą zatrzymać klientów",
             "właściciele zarabiają coraz mniej na sprzedaży piwa",
             "klienci nie kupują piwa w restauracjach, bo jego ceny są zbyt wysokie"], 0,
            "«nie podnoszą cen, bo boją się stracić klientów» → тримають сталі ціни."),
    # ── Zad II: TAK/NIE — «Poszukiwacz skarbów» ─────────────────────────
    MCQItem("czytanie",
            "TEKST: Joseph Cook (37, Флорида) — шукач скарбів (хобі). Ходить пляжем із "
            "металошукачем. Знайшов перстень із діамантом (вартий 40 тис. доларів), але не "
            "лишив собі: опублікував відео, обійшов ювелірів. Згодом отримав дзвінки з "
            "невідомого номера — власники (подружжя на відпустці). Жінка описала перстень — усе "
            "збіглося. Через 3 тижні Cook БЕЗКОШТОВНО повернув знахідку. Має ще ~30 перснів, що "
            "чекають власників.",
            "TAK/NIE: Joseph Cook znalazł na plaży pierścionek z drogim kamieniem.",
            ["TAK", "NIE"], 0, "ТАК — перстень із діамантом."),
    MCQItem("czytanie", "",
            "TAK/NIE: Znalazca postanowił sprzedać pierścionek jednemu z jubilerów.",
            ["TAK", "NIE"], 1, "НІ — ходив до ювелірів, щоб знайти власника, не продати."),
    MCQItem("czytanie", "",
            "TAK/NIE: Właściciele pierścionka zadzwonili do Cooka.",
            ["TAK", "NIE"], 0, "ТАК — почав отримувати дзвінки з невідомого номера (власники)."),
    MCQItem("czytanie", "",
            "TAK/NIE: Po wideorozmowie z kobietą Cook był pewien, że pierścionek należy do niej.",
            ["TAK", "NIE"], 0, "ТАК — усі деталі збіглися."),
    MCQItem("czytanie", "",
            "TAK/NIE: Małżeństwo zapłaciło Cookowi 40 tys. dolarów za pierścionek.",
            ["TAK", "NIE"], 1, "НІ — повернув БЕЗКОШТОВНО."),
    MCQItem("czytanie", "",
            "TAK/NIE: Na ostatnim spacerze Cook znalazł jeszcze 30 pierścionków.",
            ["TAK", "NIE"], 1, "НІ — має ~30 перснів загалом (не знайшов на останній прогулянці)."),
    # ── Zad V: обери найкраще слово («Dlaczego warto robić listę zakupów») ──
    MCQItem("czytanie", "Текст: чому варто робити список покупок. Обери найкраще слово.",
            "Jeśli należysz do drugiej grupy ___, przemyśl, jak skuteczniej robić zakupy.",
            ["sprzedawców", "klientów", "producentów"], 1, "друга група покупців → <b>klientów</b>."),
    MCQItem("czytanie", "", "Lista pomaga w ___ organizacji wizyty w sklepie.",
            ["gorszej", "lepszej", "tańszej"], 1, "у кращій організації → <b>lepszej</b>."),
    MCQItem("czytanie", "", "Nie wracasz ___ raz do tej samej półki.",
            ["następny", "kolejny", "ostatni"], 1, "вкотре → <b>kolejny</b> raz."),
    MCQItem("czytanie", "", "W ten sposób ___ czas i kupujesz tylko to, co potrzebne.",
            ["oszczędzasz", "spędzasz", "tracisz"], 0, "заощаджуєш час → <b>oszczędzasz</b>."),
    MCQItem("czytanie", "", "Po ___ ze sklepu nie musisz się martwić zakupami.",
            ["wejściu", "wyjściu", "przejściu"], 1, "по виході → <b>wyjściu</b>."),
    MCQItem("czytanie", "", "…nie musisz się ___ tym, że kupiłeś zbyt wiele.",
            ["cieszyć", "męczyć", "martwić"], 2, "перейматися → <b>martwić</b> się."),
    MCQItem("czytanie", "", "Metodą na przemyślane zakupy ___ jest zaplanowanie posiłków.",
            ["elektronicznych", "spożywczych", "odzieżowych"], 1, "продуктові покупки → <b>spożywczych</b>."),
    MCQItem("czytanie", "", "Jeśli ___, co będziesz jeść, kupisz tylko potrzebne.",
            ["znasz", "wiesz", "umiesz"], 1, "«wiesz, co» → <b>wiesz</b>."),
    MCQItem("czytanie", "", "…albo właśnie ci się ___ (produkt w kuchni).",
            ["kończy", "zaczyna", "otwiera"], 0, "закінчується → <b>kończy</b> się."),
    MCQItem("czytanie", "", "…produkty, które nie przydadzą się w ___ czasie, ale są tańsze.",
            ["przyszłym", "najbliższym", "najdłuższym"], 1, "у найближчому часі → <b>najbliższym</b>."),
]

# ── CZYTANIE — Zad III: вставити фрагменти («Staruszkowo» — притулок для старих псів) ──
# Приклад = F. Ключ: B,G,E,A,H,C,D.
_ZAD3 = MatchTask(
    section="czytanie",
    title="2023-02 Читання Zad III — встав фрагменти (Staruszkowo)",
    intro="Прочитай текст про фонд «Staruszkowo» для старих псів. Заповни пропуски 1–7 фрагментами A–G.",
    options=[
        "że tu każdą złotówkę należy mądrze wydawać",  # A
        "ile takie stworzenie wymaga czasu i pieniędzy",  # B
        "że dzięki tym zmianom schronisko przetrwa",  # C
        "jak wiele innych fundacji w Polsce",  # D
        "ponieważ nie chcą się nim dłużej opiekować",  # E
        "w którym psy spędzają swoją starość",  # G
        "którego nie mają zazwyczaj małe kliniki weterynaryjne",  # H
    ],
    prompts=[
        "1. Każdy, kto zajmował się starym psem, wie, ___",
        "2. Z założenia jest to hospicjum, ___",
        "3. Nie rozumie ludzi, którzy chcą oddać swojego przyjaciela, ___",
        "4. Na każdym kroku widać, ___. Może nie ma luksusów, ale zawsze jest zapas karmy.",
        "5. Staruszkowo ma profesjonalny sprzęt medyczny, ___",
        "6. Ma nadzieję, ___ nawet wtedy, gdy ona nie będzie miała siły.",
        "7. …podobnie ___ bardzo liczy na 1% dotacji z podatków.",
    ],
    key=[1, 5, 4, 0, 6, 2, 3],  # B,G,E,A,H,C,D
    explain=[
        "«wie, ___» → B (скільки часу й грошей вимагає така істота).",
        "«hospicjum, ___» → G (у якому пси проводять старість).",
        "«oddać przyjaciela, ___» → E (бо не хочуть далі опікуватися).",
        "«widać, ___» → A (що тут кожну копійку слід витрачати з розумом).",
        "«sprzęt medyczny, ___» → H (якого зазвичай не мають малі клініки).",
        "«ma nadzieję, ___» → C (що завдяки змінам притулок виживе).",
        "«podobnie ___» → D (як багато інших фондів у Польщі)."],
)

# ── CZYTANIE — Zad IV: заголовки↔тексти (дешеві авіаквитки) ──
# Приклад = B. Ключ: H,F,A,D,E,C,G.
_ZAD4 = MatchTask(
    section="czytanie",
    title="2023-02 Читання Zad IV — порада↔опис (дешеві квитки)",
    intro="«8 порад, як заощадити на авіаквитках» — до кожної поради (1–7) добери опис A–G.",
    options=[
        "Jeśli zgodzisz się otrzymywać e-maile od linii lotniczych, skorzystasz z wielu zniżek "
        "– warunek: trzeba je czytać.",  # A
        "Nie zawsze to, co początkowo tanie, jest naprawdę niedrogie – warto oglądać strony "
        "różnych firm transportowych.",  # C
        "Podczas rezerwacji system proponuje drogie usługi nie wliczone w cenę (wybór miejsca, "
        "wynajem auta) – zwracaj uwagę, co wybierasz.",  # D
        "Stolice i wielkie aglomeracje obsługuje dużo firm lotniczych; duża konkurencja → można "
        "liczyć na promocje.",  # E
        "Dla większości to jedyne wolne chwile, by usiąść przy komputerze i szukać urlopu – "
        "marketingowcy o tym wiedzą, ceny wyższe.",  # F
        "Jeśli masz konto w złotówkach, a kupujesz w euro, bank przeliczy cenę przez dolary.",  # G
        "Szczyt sezonu = większe zainteresowanie; linie podnoszą ceny, bo i tak znajdą się "
        "chętni.",  # H
    ],
    prompts=[
        "1. Unikaj okresu wakacyjnego",
        "2. Nie kupuj w weekend",
        "3. Zapisz się do newslettera",
        "4. Uważaj na dodatkowe opłaty",
        "5. Wybieraj wielkie miasta",
        "6. Porównuj oferty, nie myśl stereotypami",
        "7. Sprawdź walutę przelewu",
    ],
    key=[6, 4, 0, 2, 3, 1, 5],  # H,F,A,D,E,C,G
    explain=[
        "уникай сезону відпусток → H (пік сезону — ціни вищі).",
        "не купуй у вихідні → F (усі шукають у вихідні → дорожче).",
        "підпишись на розсилку → A (email-знижки).",
        "стережись доплат → D (додаткові послуги поза ціною).",
        "обирай великі міста → E (велика конкуренція → промоції).",
        "порівнюй, не мисли стереотипами → C (дешеве не завжди дешеве).",
        "перевір валюту переказу → G (конвертація через долар)."],
)

_MATCHING = [_ZAD3, _ZAD4]

# ══ GRAMATYKA ═══════════════════════════════════════════════════════════
# ── Zad I: підкресли форму (відмінювання) — MCQ. Текст про власний дім. ──
_GRAMMAR: list[MCQItem] = [
    MCQItem("gramatyka", "Текст про мрію поляків — власний дім.",
            "Własny dom jest marzeniem, które ___ spełniają przed czterdziestką.",
            ["Polakom", "Polacy", "Polaków"], 1, "підмет (наз. мн., чол.-ос.) → <b>Polacy</b>."),
    MCQItem("gramatyka", "", "Niektórzy twierdzą, że ___ domu bardziej się opłaca niż kupno mieszkania.",
            ["budowie", "budowy", "budowa"], 2, "підмет (наз.) → <b>budowa</b>."),
    MCQItem("gramatyka", "", "Wiele osób decyduje się na ___ krok, gdy ma stałą pracę.",
            ["tego", "ten", "tę"], 1, "на ___ krok (знах. чол.) → <b>ten</b>."),
    MCQItem("gramatyka", "", "Jaki jest ___ powód budowy domu?",
            ["najczęstszego", "najczęstszy", "najczęstszym"], 1, "наз. (який powód?) → <b>najczęstszy</b>."),
    MCQItem("gramatyka", "", "Ludzie chcą odpoczywać we ___ ogrodzie.",
            ["własnego", "własnym", "własny"], 1, "we + місцевий → <b>własnym</b>."),
    MCQItem("gramatyka", "", "To właśnie na ___ powstaje najwięcej domów.",
            ["wieś", "wsi", "wsią"], 1, "na + місцевий (на селі) → <b>wsi</b>."),
    MCQItem("gramatyka", "", "…najwięcej ___ domów.",
            ["nowym", "nowymi", "nowych"], 2, "najwięcej + родовий множини → <b>nowych</b>."),
    MCQItem("gramatyka", "", "Budowa trwa kilka ___ i dużo kosztuje.",
            ["lat", "lata", "latami"], 0, "kilka + родовий множини → <b>lat</b>."),
    MCQItem("gramatyka", "", "…często więcej, niż ___ inwestorzy planowali.",
            ["jej", "niej", "nią"], 0, "присвійний (її інвестори) → <b>jej</b>."),
    MCQItem("gramatyka", "", "Nie zawsze udaje się zakończyć prace bez ___.",
            ["kredytem", "kredycie", "kredytu"], 2, "bez + родовий → <b>kredytu</b>."),
    # ── Zad III: ступенювання — MCQ. Текст про вивчення мов дорослими. ──
    MCQItem("gramatyka", "Текст: чи діти вчать мови швидше за дорослих.",
            "Boją się, że są już za ___ na naukę.",
            ["stare", "starzy", "starsi"], 1, "за ___ (наз. мн. чол.-ос.) → <b>starzy</b>."),
    MCQItem("gramatyka", "", "Dzieci uczą się języków ___ niż dorośli.",
            ["szybko", "szybciej", "najszybciej"], 1, "порівняння (niż) → <b>szybciej</b>."),
    MCQItem("gramatyka", "", "Stwierdzenie „naukę ___ zacząć w dzieciństwie” to stereotyp.",
            ["najlepszy", "najlepsi", "najlepiej"], 2, "прислівник (як почати?) → <b>najlepiej</b>."),
    MCQItem("gramatyka", "", "___ od wieku jest silna motywacja i systematyczna praca.",
            ["Ważniejsza", "Najważniejsza", "Ważniej"], 0, "вищий ступ. (від віку) → <b>Ważniejsza</b>."),
    MCQItem("gramatyka", "", "Dorośli mają dużo ___ zdolność rozumienia reguł.",
            ["więcej", "większą", "wielką"], 1, "вищий ступ. прикметника (яку здатність) → <b>większą</b>."),
    # ── Zad II: сполучники з рамки (1 зайвий: dlatego) → MCQ-per-gap ──
    MCQItem("gramatyka", "Текст про читання в Європі. Встав сполучник (зайве слово — <b>dlatego</b>).",
            "Eurostat przeprowadził badania, ___ się dowiedzieć, ile czasu ludzie czytają.",
            ["żeby", "lecz", "więc", "dlatego", "bo", "oraz"], 0, "мета → <b>żeby</b>."),
    MCQItem("gramatyka", "", "…nie dłużej niż 13 minut dziennie, ___ to naprawdę niewiele.",
            ["żeby", "lecz", "więc", "dlatego", "bo", "oraz"], 2, "висновок → <b>więc</b> (отже)."),
    MCQItem("gramatyka", "", "Polacy ___ Finowie są na drugim miejscu.",
            ["żeby", "lecz", "więc", "dlatego", "bo", "oraz"], 5, "перелік → <b>oraz</b> (та)."),
    MCQItem("gramatyka", "", "Najgorzej wypada Francja, ___ tam czyta się tylko 2 minuty.",
            ["żeby", "lecz", "więc", "dlatego", "bo", "oraz"], 4, "причина → <b>bo</b> (бо)."),
    MCQItem("gramatyka", "", "Może inni nie czytają mniej, ___ robią to szybciej?",
            ["żeby", "lecz", "więc", "dlatego", "bo", "oraz"], 1, "протиставлення → <b>lecz</b> (а radше)."),
    # ── Zad VII: підкресли форму (вид/способи) — MCQ. Діалог про День Землі. ──
    MCQItem("gramatyka", "Діалог: Andrzej і Joanna планують конкурс до Дня Землі.",
            "Joanna: Bardzo ___ ci w tym pomóc.",
            ["chciałabym", "chciałbyś", "chcieliby"], 0, "умовний, 1 ос. одн. жін. (Joanna) → <b>chciałabym</b>."),
    MCQItem("gramatyka", "", "___, co mogę zrobić.",
            ["Niech powie", "Powiedz", "Mówiłbyś"], 1, "наказ до «ty» → <b>Powiedz</b>."),
    MCQItem("gramatyka", "", "Może ___ plakat informacyjny o konkursie?",
            ["malowałabyś", "namalowałabyś", "maluj"], 1, "умовний докон., 2 ос. одн. жін. → <b>namalowałabyś</b>."),
    MCQItem("gramatyka", "", "Gdybyśmy zaraz ___, co powinno się znaleźć na plakacie…",
            ["omówiliśmy", "omawiamy", "omówili"], 2, "«gdybyśmy ___» — форма на -li → <b>omówili</b>."),
    MCQItem("gramatyka", "", "Jeśli masz czas, to ___ wspólnie, kogo zaprosić do jury.",
            ["zastanówmy się", "zastanów się", "zastanowiłabyś się"], 0, "«нумо» 1 ос. мн. → <b>zastanówmy się</b>."),
    MCQItem("gramatyka", "", "Nauczyciele plastyki najprofesjonalniej ___ prace dzieci.",
            ["niech ocenią", "oceniliby", "oceniałyby"], 1, "умовний, 3 ос. мн. чол.-ос. → <b>oceniliby</b>."),
    MCQItem("gramatyka", "", "Myślę, że ___ współpracę też nauczycielowi biologii.",
            ["zaproponowałby", "proponuj", "zaproponowałbym"], 2, "умовний, 1 ос. одн. (ja) → <b>zaproponowałbym</b>."),
    MCQItem("gramatyka", "", "___ go do komitetu organizacyjnego!",
            ["Zaprosiłby", "Zaprośmy", "Zaprosiliby"], 1, "«нумо запросімо» 1 ос. мн. → <b>Zaprośmy</b>."),
    MCQItem("gramatyka", "", "Najlepiej ___ o tym z panią dyrektor.",
            ["porozmawialiby", "rozmawiałbyś", "porozmawiaj"], 2, "наказ докон. до «ty» → <b>porozmawiaj</b>."),
    MCQItem("gramatyka", "", "___ ci znaleźć jakiegoś sponsora.",
            ["Pomógłby", "Niech pomoże", "Pomóż"], 1, "спонукання 3 ос. → <b>Niech pomoże</b>."),
    # ── Zad VIII: прийменники з рамки (1 зайвий: od) → MCQ-per-gap ──
    MCQItem("gramatyka", "Текст про осінній настрій. Встав прийменник (зайве слово — <b>od</b>).",
            "___ oknem pada deszcz, jest szaro i smutno.",
            ["po", "z", "od", "dla", "za", "na"], 4, "za + орудний (за вікном) → <b>za</b>."),
    MCQItem("gramatyka", "", "___ pierwsze warto udekorować dom kwiatami.",
            ["po", "z", "od", "dla", "za", "na"], 0, "«Po pierwsze» → <b>po</b>."),
    MCQItem("gramatyka", "", "Kolory to dobre lekarstwo ___ zmęczenie i stres.",
            ["po", "z", "od", "dla", "za", "na"], 5, "lekarstwo na + знах. → <b>na</b> zmęczenie."),
    MCQItem("gramatyka", "", "…jeść sałatki ___ warzyw.",
            ["po", "z", "od", "dla", "za", "na"], 1, "sałatki z + родовий → <b>z</b> warzyw."),
    MCQItem("gramatyka", "", "Ruch jest ważny ___ dobrego samopoczucia.",
            ["po", "z", "od", "dla", "za", "na"], 3, "dla + родовий (для) → <b>dla</b>."),
]

# ── Zad IV: вписати форми (тепер./мин.) → free-fill ──
_GRAM_ZAD4 = FreeFillTask(
    section="gramatyka",
    title="2023-02 Граматика Zad IV — впиши форму дієслова",
    intro=("Впиши правильну форму дієслова (тепер. або минулий час). Текст про сусідку Аню.\n\n"
           "<i>Приклад: Ania <b>pracuje</b> (pracować), w dzieciństwie <b>marzyła</b> (marzyć).</i>"),
    prompts=[
        "1. Po liceum brat ___ (poradzić) jej, żeby poszła na Zarządzanie.",
        "2. Na uczelni Ania bardzo ___ (zainteresować się) marketingiem.",
        "3. Dwa razy ___ (ona – mieć) praktykę studencką.",
        "4. Ania ___ (spotkać) tam życzliwych ludzi,",
        "5. …którzy ___ (pokazać) jej, jak przygotować kampanię.",
        "6. Teraz sama ___ (prowadzić) badania konsumenckie",
        "7. …i ___ (planować) promocję produktów.",
        "8. Chętnie ___ (rozwijać) swoje umiejętności na kursach.",
        "9. ___ (ja – wiedzieć), że ona lubi swoją pracę.",
        "10. …ona i osoby z jej działu ___ (uwielbiać) swoją pracę.",
    ],
    accepted=[
        ["poradził"], ["zainteresowała się"], ["miała"], ["spotkała"], ["pokazali"],
        ["prowadzi"], ["planuje"], ["rozwija"], ["wiem"], ["uwielbiają"],
    ],
    explain=[
        "минулий, 3 ос. одн. чол. (brat) → <b>poradził</b>.",
        "минулий, 3 ос. одн. жін. (Ania) → <b>zainteresowała się</b>.",
        "минулий, 3 ос. одн. жін. → <b>miała</b>.",
        "минулий, 3 ос. одн. жін. → <b>spotkała</b>.",
        "минулий, 3 ос. мн. чол.-ос. (ludzie) → <b>pokazali</b>.",
        "тепер., 3 ос. одн. → <b>prowadzi</b>.",
        "тепер., 3 ос. одн. → <b>planuje</b>.",
        "тепер., 3 ос. одн. → <b>rozwija</b>.",
        "тепер., 1 ос. одн. (ja) → <b>wiem</b>.",
        "тепер., 3 ос. мн. → <b>uwielbiają</b>.",
    ],
)

# ── Zad V: постав питання → free-fill ──
_GRAM_ZAD5 = FreeFillTask(
    section="gramatyka",
    title="2023-02 Граматика Zad V — постав питання",
    intro=("Постав питання до виділеної в «лапках» частини. Впиши ЛИШЕ питальне слово.\n\n"
           "<i>Приклад: rozmawiać «o podróżach» → O czym?</i>"),
    prompts=[
        "Jego ulubiony piórnik jest «z metalu».",
        "Jej brat nigdy nie słuchał muzyki «klasycznej».",
        "Dom «rodziców Zenka» stoi na wzgórzu.",
        "Adam dobrze zna «rodzinę Kowalskich».",
        "Jan mieszka na «pierwszym» piętrze.",
    ],
    accepted=[["z czego", "z jakiego materiału"], ["jakiej"], ["czyj"], ["kogo"], ["na którym"]],
    explain=[
        "матеріал → <b>Z czego?</b> (Z jakiego materiału?)",
        "«jakiej muzyki» → <b>Jakiej?</b>",
        "чий дім → <b>Czyj?</b>",
        "znać + знах. (кого?) → <b>Kogo?</b>",
        "«na którym piętrze» → <b>Na którym?</b>",
    ],
)

# ── Zad VI: трансформація → open ──
_GRAM_ZAD6 = OpenTask(
    section="gramatyka",
    title="2023-02 Граматика Zad VI — перетвори речення",
    intro=("Перепиши речення, зберігаючи сенс і вживши слово з дужок.\n\n"
           "<i>Приклад: «ma na sobie ten płaszcz» (ubrana) → jest ubrana w ten płaszcz.</i>\n\n"
           "📊 Оцінює AI за офіційним зразком."),
    criterion="Той самий сенс + вжите слово з дужок у правильній формі, граматично коректно.",
    prompts=[
        "Pani Basia jest dzisiaj piękna i elegancka.",
        "Wczoraj byliśmy z wizytą u naszej cioci.",
        "Adam jest wyższy niż mój brat.",
        "Rodzice dali Janowi rower.",
        "Ani nie było na urodzinowej kolacji.",
    ],
    words=["wygląda", "odwiedziliśmy", "od", "dostał", "nie przyszła"],
    models=[
        ["Pani Basia wygląda dzisiaj pięknie i elegancko."],
        ["Wczoraj odwiedziliśmy naszą ciocię."],
        ["Adam jest wyższy od mojego brata."],
        ["Jan dostał od rodziców rower."],
        ["Ania nie przyszła na urodzinową kolację."],
    ],
)

EXAM = Exam(
    id="2023-02",
    label="Реальний іспит лютий-2023 (офіц.)",
    kind="real",
    year=2023,
    items=_READING + _GRAMMAR,
    tasks=[*_MATCHING, _GRAM_ZAD4, _GRAM_ZAD5, _GRAM_ZAD6],
)
