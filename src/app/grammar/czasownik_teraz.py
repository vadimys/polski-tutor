"""Модуль 5 — Дієслово: теперішній час. Як відмінювати дії «зараз»."""

from __future__ import annotations

from app.grammar.schema import Card, Lesson, Module, Quiz

MODULE = Module(
    id="czas_terazniejszy",
    icon="🏃",
    title="Дієслово: теперішній час",
    subtitle="Як сказати «я роблю, ти робиш…»: три групи дієвідмінювання.",
    lessons=[
        # ── Вступ ──
        Lesson(
            id="cz_wstep",
            title="Дієслово й особові закінчення",
            cards=[
                Card(
                    "Інфінітив на -ć",
                    "Початкова форма дієслова (у словнику) майже завжди на <code>-ć</code>: "
                    "<i>czytać, robić, pić</i>. Від неї утворюємо всі особи.",
                ),
                Card(
                    "Логіка як в українській",
                    "Дієслово змінюється за особами (я/ти/він…). Займенник часто опускають — "
                    "особу видно із закінчення.",
                    [("czytam", "(я) читаю"), ("czytasz", "(ти) читаєш")],
                ),
                Card(
                    "Три групи",
                    "Є 3 основні моделі відмінювання. Різниця — у формах «я» і «ти». Пройдемо кожну "
                    "на прикладі. Спільне: <code>my</code> → -my, <code>wy</code> → -cie.",
                    tip="Не треба зубрити — вловиш модель на кількох дієсловах, і решта підуть за аналогією.",
                ),
            ],
        ),
        # ── Група 1: -am/-asz ──
        Lesson(
            id="cz_grupa1",
            title="Група 1: -am, -asz (czytać)",
            cards=[
                Card(
                    "Найлегша й найчастіша",
                    "Дієслова типу <code>czytać</code> (читати): проста, регулярна модель.",
                    [("(ja) czytam", "читаю"), ("(ty) czytasz", "читаєш"), ("(on) czyta", "читає"),
                     ("(my) czytamy", "читаємо"), ("(wy) czytacie", "читаєте"), ("(oni) czytają", "читають")],
                ),
                Card(
                    "За тією ж моделлю",
                    "Так само відмінюються: <code>mieszkać</code> (жити), <code>pytać</code> (питати), "
                    "<code>kochać</code> (кохати), <code>mieć</code> (мати: mam, masz, ma…).",
                    [("Mieszkam w Polsce.", "Живу в Польщі."), ("Mam czas.", "Маю час.")],
                    tip="Запамʼятай ключ: ja -am, ty -asz, oni -ają. Дуже багато дієслів сюди належать.",
                ),
            ],
            quiz=[
                Quiz("«(ти) читаєш» —", ["czytam", "czytasz", "czyta"], 1, "ty → -asz: czytasz."),
                Quiz("«Живу в Польщі»: mieszkać, форма «я» —", ["mieszkam", "mieszkasz", "mieszka"], 0,
                     "ja → -am: mieszkam."),
            ],
        ),
        # ── Група 2: -ę/-isz ──
        Lesson(
            id="cz_grupa2",
            title="Група 2: -ę, -isz (robić)",
            cards=[
                Card(
                    "Модель robić (робити)",
                    "Форма «я» на <code>-ę</code>, «ти» на <code>-isz</code> (або -ysz).",
                    [("(ja) robię", "роблю"), ("(ty) robisz", "робиш"), ("(on) robi", "робить"),
                     ("(my) robimy", "робимо"), ("(wy) robicie", "робите"), ("(oni) robią", "роблять")],
                ),
                Card(
                    "За тією ж моделлю",
                    "<code>mówić</code> (говорити), <code>lubić</code> (любити), <code>myśleć</code> (думати), "
                    "<code>uczyć się</code> (вчитися).",
                    [("Mówię po polsku.", "Говорю польською."), ("Lubię kawę.", "Люблю каву.")],
                    tip="Ключ: ja -ę, ty -isz, oni -ą. Порівняй із групою 1 — відрізняються «я» і «ти».",
                ),
            ],
            quiz=[
                Quiz("«Говорю польською»: mówić, форма «я» —", ["mówę", "mówię", "mówisz"], 1,
                     "ja → -ę: mówię."),
            ],
        ),
        # ── Група 3: -ę/-esz ──
        Lesson(
            id="cz_grupa3",
            title="Група 3: -ę, -esz (pić, pisać)",
            cards=[
                Card(
                    "Форма «ти» на -esz",
                    "«Я» на <code>-ę</code>, «ти» на <code>-esz</code>. Часто основа трохи змінюється.",
                    [("(ja) piję", "пʼю"), ("(ty) pijesz", "пʼєш"), ("(on) pije", "пʼє"),
                     ("(oni) piją", "пʼють")],
                ),
                Card(
                    "Ще приклади",
                    "<code>pisać</code> (писати: piszę, piszesz), <code>iść</code> (йти: idę, idziesz), "
                    "<code>móc</code> (могти: mogę, możesz).",
                    [("Piszę list.", "Пишу листа."), ("Idę do domu.", "Іду додому.")],
                    tip="Тут основа буває «капризна» (pisać→piszę). Такі дієслова просто варто запамʼятати.",
                ),
            ],
            quiz=[
                Quiz("«Пишу листа»: pisać, форма «я» —", ["pisam", "piszę", "pisze"], 1,
                     "pisać → piszę (основа змінюється)."),
            ],
        ),
        # ── Неправильні ──
        Lesson(
            id="cz_nieregularne",
            title="Найважливіші неправильні",
            cards=[
                Card(
                    "być — бути",
                    "Найголовніше (повторення з модуля 2): jestem, jesteś, jest, jesteśmy, "
                    "jesteście, są.",
                ),
                Card(
                    "iść, jeść, wiedzieć",
                    "<code>iść</code> (йти): idę, idziesz, idzie…\n<code>jeść</code> (їсти): jem, jesz, je, jemy, "
                    "jecie, jedzą\n<code>wiedzieć</code> (знати факт): wiem, wiesz, wie, wiedzą",
                    [("Idę do pracy.", "Іду на роботу."), ("Wiem, gdzie to jest.", "Знаю, де це.")],
                ),
                Card(
                    "chcieć, móc",
                    "<code>chcieć</code> (хотіти): chcę, chcesz, chce…\n<code>móc</code> (могти): mogę, możesz, może…",
                    [("Chcę kawę.", "Хочу каву."), ("Mogę ci pomóc.", "Можу тобі допомогти.")],
                    tip="Ці 5-6 дієслів — у щоденному вжитку. Варто вивчити напамʼять, як «być».",
                ),
            ],
            quiz=[
                Quiz("«Знаю, де це» — wiedzieć, форма «я» —", ["wiedzę", "wiem", "wieszę"], 1,
                     "wiedzieć → wiem (неправильне)."),
                Quiz("«Хочу каву» —", ["Chcem kawę.", "Chcę kawę.", "Chcesz kawę."], 1, "chcieć → chcę."),
            ],
        ),
    ],
)
