"""РЕАЛЬНИЙ минулий іспит B1 — лютий 2023 (certyfikatpolski.pl).

Джерело: 2023_02_5_6_B1_arkusz + …_transkrypcja.pdf (з KLUCZ). ДОСЛІВНО, КОЖЕН ключ
звірено з офіц. klucz. Czytanie:
- Zad I (a/b/c ×5, ключ b,c,b,b,a) + Zad II (TAK/NIE ×6, T,N,T,T,N,N)
  + Zad V (вибір слова ×10) — MCQ; Zad III/IV — matching.
Далі: Gramatyka (8 Zad) + Słuchanie (5 Zad).
"""

from __future__ import annotations

from app.content.schema import Exam, MatchTask, MCQItem

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

EXAM = Exam(
    id="2023-02",
    label="Реальний іспит лютий-2023 (офіц.)",
    kind="real",
    year=2023,
    items=_READING,
    tasks=_MATCHING,
)
