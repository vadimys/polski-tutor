"""Повна стартова сітка IG: каруселі 1-9, кадри рілсів 2-3, сторіс-квізи 2-5.

Реюз движка ig_gen (стиль апрувнуто). Факти: 170 € — ціна іспиту; закон з 30.06.2026
(лише офіц. сертифікат B1 для karty rezydenta); сесії 2026 — з certyfikatpolski.pl.
Використання: python3 scripts/ig_batch.py
"""

from __future__ import annotations

import ig_gen as G
from ig_gen import DARK, GREY, M, RED, WHITE, f  # noqa: F401

CHIP_DIM = dict(bg=(245, 240, 238), fg=DARK)


def _pairs(d, y, pairs, chip_size=44, gap1=104, gap2=76):
    for pl, uk in pairs:
        G._chip(d, (M, y), pl, f(G._MONO_F, chip_size), pad=(34, 18))
        y += gap1
        d.text((M + 6, y), uk, font=f(G._REG_F, 36), fill=GREY)
        y += gap2
    return y


# ── Пост 1: Хто ми ───────────────────────────────────────────────────────────
def post1():
    T = 4

    def s1(img, d, y, w):
        y += 20
        y = G._text_block(d, (M, y),
                          "Тренажер, який готує САМЕ до державного іспиту — а не «до польської взагалі».",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 40
        d.text((M, y), "гортай — покажемо, що всередині →", font=f(G._REG_F, 40), fill=GREY)

    G.slide(0, T, "знайомство", "Готуєшся\nдо B1?", s1, "p1_s1.png")

    def s2(img, d, y, w):
        items = [
            "реальні минулі іспити 2022–2024",
            "усі 5 модулів — від słuchania до mówienia",
            "AI перевіряє письмо й мовлення\nза офіційними критеріями",
            "пояснення простою українською",
        ]
        for it in items:
            d.ellipse((M, y + 14, M + 22, y + 36), fill=RED)
            y = G._text_block(d, (M + 48, y), it, f(G._BOLD_F, 44), DARK, w - 2 * M - 48,
                              lh=1.2) + 34

    G.slide(1, T, "що всередині", "Не курс.\nТренажер", s2, "p1_s2.png")

    def s3(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y), "15 хвилин на день у Telegram.\nБез застосунків і реєстрацій.",
                          f(G._BOLD_F, 50), DARK, w - 2 * M, lh=1.25) + 44
        y = G._text_block(d, (M, y),
                          "Почни з безкоштовного тесту рівня — він покаже твою готовність "
                          "по кожному з 5 модулів.",
                          f(G._REG_F, 44), GREY, w - 2 * M, lh=1.3)

    G.slide(2, T, "як це працює", "15 хв\nна день", s3, "p1_s3.png")

    def s4(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y), "Безкоштовний тест рівня — за 2 хвилини.",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 50
        G._chip(d, (M, y), "→ лінк у шапці профілю", f(G._BOLD_F, 46))

    G.slide(3, T, "почни сьогодні", "Перевір свій\nрівень зараз", s4, "p1_s4.png", swipe=False)


# ── Пост 2: Закон 30.06.2026 ─────────────────────────────────────────────────
def post2():
    T = 4

    def s1(img, d, y, w):
        y += 20
        y = G._text_block(d, (M, y),
                          "З 30 червня 2026 шкільні довідки більше не діють для karty rezydenta.",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 36
        d.text((M, y), "що це значить для тебе →", font=f(G._REG_F, 40), fill=GREY)

    G.slide(0, T, "важлива зміна", "Сертифікат B1\nтепер обовʼязковий", s1, "p2_s1.png")

    def s2(img, d, y, w):
        items = [
            ("pobyt stały / karta rezydenta", "лише офіційний сертифікат ≥B1"),
            ("громадянство", "теж вимагає підтвердження мови"),
            ("іспит складається 1 раз", "сертифікат — безстроковий"),
        ]
        for t1, t2 in items:
            G._chip(d, (M, y), t1, f(G._MONO_F, 40), pad=(30, 16))
            y += 96
            d.text((M + 6, y), t2, font=f(G._REG_F, 38), fill=GREY)
            y += 82

    G.slide(1, T, "кому потрібен", "Кому без нього\nніяк", s2, "p2_s2.png")

    def s3(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y), "170 € — ціна однієї спроби.",
                          f(G._BLACK_F, 62), RED, w - 2 * M, lh=1.15) + 30
        y = G._text_block(d, (M, y),
                          "Провалив — платиш знову і чекаєш наступної сесії (їх лише 5 на рік). "
                          "Тому готуватись «на авось» — найдорожча стратегія.",
                          f(G._REG_F, 44), DARK, w - 2 * M, lh=1.3)

    G.slide(2, T, "ціна помилки", "Іспит платний.\nІ не дешевий", s3, "p2_s3.png")

    def s4(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y),
                          "Підготовка в нашому боті — 15 хв на день на реальних минулих іспитах. "
                          "Це найкоротший шлях скласти з першого разу.",
                          f(G._REG_F, 46), DARK, w - 2 * M, lh=1.3) + 44
        G._chip(d, (M, y), "→ безкоштовний тест рівня", f(G._BOLD_F, 46))

    G.slide(3, T, "що робити", "Склади\nз першого разу", s4, "p2_s4.png", swipe=False)


# ── Пост 4: фальшиві друзі ───────────────────────────────────────────────────
def post4():
    T = 4

    def s1(img, d, y, w):
        y += 20
        y = G._text_block(d, (M, y),
                          "Слова, які звучать «по-нашому», але означають зовсім інше. "
                          "На іспиті вони коштують балів.",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 36
        d.text((M, y), "перевір, чи знаєш усі 5 →", font=f(G._REG_F, 40), fill=GREY)

    G.slide(0, T, "лексика", "5 фальшивих\nдрузів", s1, "p4_s1.png")

    def s2(img, d, y, w):
        y = _pairs(d, y, [
            ("dywan", "це КИЛИМ (а не диван)"),
            ("sklep", "це МАГАЗИН (а не склеп)"),
            ("owoce", "це ФРУКТИ (а не овочі)"),
        ], chip_size=48)

    G.slide(1, T, "перша трійка", "Не те,\nщо думаєш", s2, "p4_s2.png")

    def s3(img, d, y, w):
        y = _pairs(d, y, [
            ("pensja", "це ЗАРПЛАТА (а не пенсія)"),
            ("zapomnieć", "це ЗАБУТИ (а не запамʼятати!)"),
        ], chip_size=48)
        y += 14
        y = G._text_block(d, (M, y),
                          "«Zapomniałem» = «я забув». Найпідступніший з усіх.",
                          f(G._BOLD_F, 42), DARK, w - 2 * M, lh=1.25)

    G.slide(2, T, "друга пара", "І ще два\nпідступні", s3, "p4_s3.png")

    def s4(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y),
                          "У боті є словник за темами і повторення слів за інтервалами — "
                          "фальшиві друзі закріплюються самі.",
                          f(G._REG_F, 46), DARK, w - 2 * M, lh=1.3) + 44
        G._chip(d, (M, y), "→ лінк у шапці", f(G._BOLD_F, 46))

    G.slide(3, T, "запамʼятати назавжди", "Тренуй лексику\nщодня", s4, "p4_s4.png", swipe=False)


# ── Пост 5: формат іспиту ────────────────────────────────────────────────────
def post5():
    T = 4

    def s1(img, d, y, w):
        y += 20
        y = G._text_block(d, (M, y),
                          "Багато хто йде на іспит, не знаючи його формату. І втрачає бали "
                          "не через мову, а через несподіванки.",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 36
        d.text((M, y), "ось як він влаштований →", font=f(G._REG_F, 40), fill=GREY)

    G.slide(0, T, "іспит зсередини", "Що на тебе\nчекає на B1", s1, "p5_s1.png")

    def s2(img, d, y, w):
        mods = ["1. Słuchanie — аудіювання", "2. Czytanie — читання",
                "3. Gramatyka — граматика", "4. Pisanie — два письмові тексти",
                "5. Mówienie — усна частина"]
        for m_ in mods:
            G._chip(d, (M, y), m_, f(G._MONO_F, 40), pad=(30, 16))
            y += 118

    G.slide(1, T, "структура", "5 модулів\nза день-два", s2, "p5_s2.png")

    def s3(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y), "Потрібно ≥50% у КОЖНОМУ модулі.",
                          f(G._BLACK_F, 58), RED, w - 2 * M, lh=1.15) + 34
        y = G._text_block(d, (M, y),
                          "Набрав 90% у читанні, але 45% в усній частині? Іспит не складено. "
                          "Тому готувати треба всі пʼять — рівномірно.",
                          f(G._REG_F, 44), DARK, w - 2 * M, lh=1.3)

    G.slide(2, T, "головне правило", "Завалив один —\nзавалив усе", s3, "p5_s3.png")

    def s4(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y),
                          "Бот показує твою готовність по кожному з 5 модулів окремо — "
                          "одразу видно, де підтягувати.",
                          f(G._REG_F, 46), DARK, w - 2 * M, lh=1.3) + 44
        G._chip(d, (M, y), "→ тест рівня в шапці", f(G._BOLD_F, 46))

    G.slide(3, T, "твоя стратегія", "Знай свої\nслабкі місця", s4, "p5_s4.png", swipe=False)


# ── Пост 6: byłem/byłam ──────────────────────────────────────────────────────
def post6():
    T = 4

    def s1(img, d, y, w):
        y += 26
        d.text((M, y), "Жінка розповідає про вчора:", font=f(G._BOLD_F, 44), fill=GREY)
        y += 96
        G._chip(d, (M, y), "A)  byłem w domu", f(G._MONO_F, 52), **CHIP_DIM)
        y += 140
        G._chip(d, (M, y), "B)  byłam w domu", f(G._MONO_F, 52), **CHIP_DIM)
        y += 190
        d.text((M, y), "Відповідь — на наступному слайді  →", font=f(G._REG_F, 40), fill=GREY)

    G.slide(0, T, "міні-квіз · минулий час", "byłem\nчи byłam?", s1, "p6_s1.png")

    def s2(img, d, y, w):
        y += 10
        G._chip(d, (M, y), "✓  byłam w domu", f(G._MONO_F, 56))
        y += 170
        y = G._text_block(d, (M, y), "У польському минулому часі є РІД — навіть у «я» і «ти».",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 40
        y = G._text_block(d, (M, y), "Чоловік: byłem. Жінка: byłam. В українській так само — "
                          "«був/була», тож логіка знайома.",
                          f(G._REG_F, 42), GREY, w - 2 * M, lh=1.3)

    G.slide(1, T, "відповідь", "byłAm.\nБо жінка!", s2, "p6_s2.png")

    def s3(img, d, y, w):
        y = _pairs(d, y, [
            ("on robił / ona robiła", "він робив / вона робила"),
            ("oni robili", "вони (є чоловіки)"),
            ("one robiły", "вони (без чоловіків)"),
        ], chip_size=44)

    G.slide(2, T, "запамʼятай", "Рід є\nусюди", s3, "p6_s3.png")

    def s4(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y),
                          "Тренажер дієслів у боті ганяє минулий час по всіх родових формах — "
                          "byłem/byłam більше не сплутаєш.",
                          f(G._REG_F, 46), DARK, w - 2 * M, lh=1.3) + 44
        G._chip(d, (M, y), "→ лінк у шапці", f(G._BOLD_F, 46))

    G.slide(3, T, "тренуйся", "120 дієслів\nу тренажері", s4, "p6_s4.png", swipe=False)


# ── Пост 7: дати сесій ───────────────────────────────────────────────────────
def post7():
    T = 3

    def s1(img, d, y, w):
        y += 20
        y = G._text_block(d, (M, y),
                          "Іспит проводять лише кілька разів на рік. Пропустив осінні сесії — "
                          "чекаєш аж до 2027-го.",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 36
        d.text((M, y), "дати 2026 →", font=f(G._REG_F, 40), fill=GREY)

    G.slide(0, T, "плануй заздалегідь", "Коли можна\nскласти B1", s1, "p7_s1.png")

    def s2(img, d, y, w):
        dates = [("17–18 жовтня 2026", "передостання сесія року"),
                 ("5–6 грудня 2026", "остання сесія 2026")]
        for t1, t2 in dates:
            G._chip(d, (M, y), t1, f(G._MONO_F, 50), pad=(38, 22))
            y += 128
            d.text((M + 6, y), t2, font=f(G._REG_F, 40), fill=GREY)
            y += 96
        y += 8
        y = G._text_block(d, (M, y),
                          "Місця розбирають швидко — реєструйся, щойно центр відкриє запис.",
                          f(G._BOLD_F, 42), RED, w - 2 * M, lh=1.25)

    G.slide(1, T, "сесії 2026", "Лишилось\nдві дати", s2, "p7_s2.png")

    def s3(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y),
                          "До грудня — ще є час підготуватись з нуля: 15 хв на день "
                          "на реальних минулих іспитах.",
                          f(G._REG_F, 46), DARK, w - 2 * M, lh=1.3) + 44
        G._chip(d, (M, y), "→ почни з тесту рівня", f(G._BOLD_F, 46))

    G.slide(2, T, "встигаєш", "Почни сьогодні —\nскладеш у грудні", s3, "p7_s3.png", swipe=False)


# ── Пост 8: як виглядає тренування ──────────────────────────────────────────
def post8():
    T = 4

    def s1(img, d, y, w):
        y += 20
        y = G._text_block(d, (M, y),
                          "Без застосунків, без реєстрацій, без вебінарів. Відкрив Telegram — "
                          "потренувався — закрив.",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 36
        d.text((M, y), "ось твій день з ботом →", font=f(G._REG_F, 40), fill=GREY)

    G.slide(0, T, "як це виглядає", "Уся підготовка —\nу Telegram", s1, "p8_s1.png")

    def s2(img, d, y, w):
        steps = [("🌅 ранок", "нагадування: 15 хв, найслабший модуль"),
                 ("⚡ вправа", "реальні завдання минулих іспитів"),
                 ("💬 розбір", "кожна помилка — з поясненням українською")]
        for t1, t2 in steps:
            d.text((M, y), t1, font=f(G._BOLD_F, 46), fill=DARK)
            y += 66
            y = G._text_block(d, (M, y), t2, f(G._REG_F, 42), GREY, w - 2 * M, lh=1.25) + 40

    G.slide(1, T, "щоденний ритм", "15 хвилин —\nі вільний", s2, "p8_s2.png")

    def s3(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y),
                          "Пишеш лист польською — AI перевіряє за офіційними критеріями іспиту "
                          "й показує, за що знімуть бали. Надиктовуєш відповідь — розбирає мовлення.",
                          f(G._REG_F, 46), DARK, w - 2 * M, lh=1.3) + 40
        y = G._text_block(d, (M, y), "Це як особистий екзаменатор у кишені.",
                          f(G._BOLD_F, 46), DARK, w - 2 * M, lh=1.25)

    G.slide(2, T, "письмо і мовлення", "AI перевіряє\nяк екзаменатор", s3, "p8_s3.png")

    def s4(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y), "Спробуй сам — перші два тижні безкоштовно, без карти.",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 50
        G._chip(d, (M, y), "→ лінк у шапці профілю", f(G._BOLD_F, 46))

    G.slide(3, T, "спробуй", "14 днів\nбезкоштовно", s4, "p8_s4.png", swipe=False)


# ── Пост 9: чому ми це зробили ───────────────────────────────────────────────
def post9():
    T = 3

    def s1(img, d, y, w):
        y += 20
        y = G._text_block(d, (M, y),
                          "Я сам готуюся до іспиту на грудень 2026. І чесно — нормального "
                          "тренажера під САМЕ цей іспит не знайшов.",
                          f(G._BOLD_F, 48), DARK, w - 2 * M, lh=1.25) + 36
        d.text((M, y), "тому зробив свій →", font=f(G._REG_F, 40), fill=GREY)

    G.slide(0, T, "чесна історія", "Чому цей бот\nіснує", s1, "p9_s1.png")

    def s2(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y),
                          "Зібрав усі відкриті минулі іспити Держкомісії, побудував тренажери "
                          "всіх 5 модулів і додав AI-перевірку письма й мовлення.",
                          f(G._REG_F, 46), DARK, w - 2 * M, lh=1.3) + 40
        y = G._text_block(d, (M, y),
                          "Спершу — для себе. Тепер ним готуються інші українці в Польщі.",
                          f(G._BOLD_F, 46), DARK, w - 2 * M, lh=1.25)

    G.slide(1, T, "що вийшло", "Від зошита —\nдо тренажера", s2, "p9_s2.png")

    def s3(img, d, y, w):
        y += 10
        y = G._text_block(d, (M, y),
                          "Побажання і фідбек — у дірект: бот живий, я допрацьовую його щотижня. "
                          "Складемо B1 разом 💪",
                          f(G._REG_F, 46), DARK, w - 2 * M, lh=1.3) + 44
        G._chip(d, (M, y), "→ спробувати в шапці", f(G._BOLD_F, 46))

    G.slide(2, T, "разом до мети", "Грудень 2026.\nМи готові", s3, "p9_s3.png", swipe=False)


# ── Рілс 2: 170 € (без озвучки) ─────────────────────────────────────────────
def reel2():
    G._reel_frame("reel2_f1.png", "", [
        ("hook", "Іспит B1\nкоштує 170 €"),
        ("gap", "40"), ("dim", "і це ціна лише ОДНІЄЇ спроби"),
    ])
    G._reel_frame("reel2_f2.png", "якщо провалив", [
        ("big", "платиш знову 170 €\nі чекаєш наступної сесії"),
        ("gap", "20"), ("dim", "а їх лише 5 на рік"),
    ])
    G._reel_frame("reel2_f3.png", "дедлайн 2026", [
        ("chip", "17–18 жовтня"), ("chip", "5–6 грудня"),
        ("dim", "останні сесії цього року"),
    ])
    G._reel_frame("reel2_f4.png", "математика проста", [
        ("big", "місяць підготовки в боті — 25 zł.\nПерескладання іспиту — 750 zł."),
    ])
    G._reel_frame("reel2_f5.png", "готуйся розумно", [
        ("hook", "Склади\nз першого\nразу"),
        ("gap", "30"), ("chip", "→ лінк у шапці"),
    ])


# ── Рілс 3: byłem/byłam (з озвучкою) ─────────────────────────────────────────
def reel3():
    G._reel_frame("reel3_f1.png", "", [
        ("hook", "byłem\nчи byłam?"),
        ("gap", "40"), ("dim", "помилка, яку чутно одразу"),
    ])
    G._reel_frame("reel3_f2.png", "минулий час", [
        ("big", "у польському минулому є РІД —\nнавіть у слові «я»"),
    ])
    G._reel_frame("reel3_f3.png", "чоловік каже", [
        ("chip", "byłem w domu"), ("dim", "я був удома"),
    ])
    G._reel_frame("reel3_f4.png", "жінка каже", [
        ("chip", "byłam w domu"), ("dim", "я була вдома"),
    ])
    G._reel_frame("reel3_f5.png", "у множині теж", [
        ("chip", "oni byli"), ("dim", "вони (є чоловіки)"),
        ("chip", "one były"), ("dim", "вони (без чоловіків)"),
    ])
    G._reel_frame("reel3_f6.png", "тренуйся", [
        ("hook", "Тренажер\nганяє всі\nформи"),
        ("gap", "30"), ("chip", "→ лінк у шапці"),
    ])


# ── Сторіс-квізи 2-5 ─────────────────────────────────────────────────────────
def _story(out, kicker, title, a, b, note="голосуй стікером нижче ↓"):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (G.W_ST, G.H_ST), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, G.W_ST, 14), fill=RED)
    logo = Image.open(G.ROOT / "images" / "logo_b1_square.png").convert("RGBA").resize((84, 84))
    img.paste(logo, (M, 220), logo)
    d.text((M + 104, 238), "polski.b1.coach", font=f(G._BOLD_F, 32), fill=GREY)
    y = 420
    d.text((M, y), kicker.upper(), font=f(G._BOLD_F, 40), fill=RED)
    y += 100
    y = G._text_block(d, (M, y), title, f(G._BLACK_F, 88), DARK, G.W_ST - 2 * M, lh=1.1) + 50
    G._chip(d, (M, y), f"A)  {a}", f(G._MONO_F, 54), pad=(40, 24), **CHIP_DIM)
    y += 130
    G._chip(d, (M, y), f"B)  {b}", f(G._MONO_F, 54), pad=(40, 24), **CHIP_DIM)
    y += 170
    G._text_block(d, (M, y), note + "\nвідповідь — у наступній сторіс",
                  f(G._REG_F, 38), GREY, G.W_ST - 2 * M, lh=1.4)
    img.save(G.OUT / out)
    print("OK", out)


def stories():
    _story("story_quiz2.png", "щоденний квіз", "Хворію\nна грип",
           "choruję na grypę", "choruję grypą")
    _story("story_quiz3.png", "щоденний квіз", "Дзвоню\nмамі",
           "dzwonię mamie", "dzwonię do mamy")
    _story("story_quiz4.png", "щоденний квіз", "Чекаю\nна автобус",
           "czekam autobus", "czekam na autobus")
    _story("story_quiz5.png", "щоденний квіз", "Пʼять…\nкотів?",
           "pięć koty", "pięć kotów")


if __name__ == "__main__":
    post1(); post2(); post4(); post5(); post6(); post7(); post8(); post9()
    reel2(); reel3(); stories()
