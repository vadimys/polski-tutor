"""Модуль 9 — Займенники (zaimki): присвійні, вказівні, особові у відмінках, się."""

from __future__ import annotations

from app.grammar.schema import Card, Lesson, Module, Quiz

MODULE = Module(
    id="zaimki",
    icon="👉",
    title="Займенники",
    subtitle="Мій/твій, цей/той, мене/тебе та зворотне «się».",
    lessons=[
        # ── Присвійні ──
        Lesson(
            id="za_dzierzawcze",
            title="Присвійні: mój, twój, jego…",
            cards=[
                Card(
                    "Чий?",
                    "• <b>mój</b> — мій\n• <b>twój</b> — твій\n• <b>jego</b> — його\n"
                    "• <b>jej</b> — її\n• <b>nasz</b> — наш\n• <b>wasz</b> — ваш\n• <b>ich</b> — їхній",
                ),
                Card(
                    "mój теж узгоджується за родом",
                    "<b>mój</b> (ч.) · <b>moja</b> (ж.) · <b>moje</b> (с.). Так само twój, nasz, wasz.",
                    [("mój dom", "мій дім"), ("moja mama", "моя мама"), ("moje auto", "моє авто")],
                    tip="Але jego, jej, ich НЕ змінюються: jego dom, jego mama, jego auto.",
                ),
            ],
            quiz=[
                Quiz("«моя мама» —", ["mój mama", "moja mama", "moje mama"], 1,
                     "Жін. рід → moja."),
                Quiz("«його дім» —", ["jego dom", "jej dom", "ich dom"], 0, "його = jego."),
            ],
        ),
        # ── Вказівні ──
        Lesson(
            id="za_wskazujace",
            title="Вказівні: ten, ta, to / tamten",
            cards=[
                Card(
                    "Цей / ця / це",
                    "<b>ten</b> (ч.) · <b>ta</b> (ж.) · <b>to</b> (с.). Множина: <b>ci</b> (люди-чол.) "
                    "/ <b>te</b> (решта).",
                    [("ten dom", "цей дім"), ("ta książka", "ця книжка"), ("te domy", "ці будинки")],
                ),
                Card(
                    "Той — tamten",
                    "Дальший обʼєкт: <b>tamten / tamta / tamto</b> (той/та/те).",
                    [("Tamten dom jest większy.", "Той дім більший.")],
                    tip="Не плутай: «to jest…» (це є…) — то службове «to»; а «ten/ta/to» узгоджуються з іменником.",
                ),
            ],
            quiz=[
                Quiz("«ця книжка» —", ["ten książka", "ta książka", "to książka"], 1, "Жін. → ta."),
            ],
        ),
        # ── Особові у відмінках ──
        Lesson(
            id="za_osobowe",
            title="Особові у відмінках: mnie, cię, go…",
            cards=[
                Card(
                    "«Я» теж відмінюється",
                    "Як і іменники, займенники змінюються за відмінками:\n"
                    "• ja → <b>mnie</b> (мене/мені)\n• ty → <b>cię/ciebie</b> (тебе)\n"
                    "• on → <b>go/jego</b> · ona → <b>ją</b>",
                    [("Znasz mnie?", "Знаєш мене?"), ("Widzę cię.", "Бачу тебе."),
                     ("Lubię go.", "Люблю його.")],
                ),
                Card(
                    "Короткі й довгі форми",
                    "Часто є коротка (без наголосу) і довга (з наголосом/після прийменника) форма.",
                    [("Daj mi to.", "Дай мені це (коротка mi)."),
                     ("To dla mnie.", "Це для мене (довга після прийменника).")],
                    tip="Новачку досить упізнавати mnie/cię/go/ją у мовленні — активне вживання прийде з практикою.",
                ),
            ],
            quiz=[
                Quiz("«Бачу тебе» —", ["Widzę ty.", "Widzę cię.", "Widzę mnie."], 1, "ty → cię: Widzę cię."),
            ],
        ),
        # ── się ──
        Lesson(
            id="za_sie",
            title="Зворотне «się» (миється, вчиться)",
            cards=[
                Card(
                    "się = -ся/-сь",
                    "Багато дій «на себе» мають <b>się</b> — як українське -ся.",
                    [("myć się", "митися"), ("uczyć się", "вчитися"),
                     ("nazywać się", "називатися")],
                ),
                Card(
                    "się «плаває» в реченні",
                    "На відміну від українського -ся, польське <b>się</b> — окреме слово й може стояти "
                    "не впритул до дієслова.",
                    [("Uczę się polskiego.", "Вчу польську (вчуся)."),
                     ("Jak się nazywasz?", "Як тебе звати?"), ("Dobrze się czuję.", "Добре почуваюся.")],
                    tip="«się» не приклеюється: часто йде перед дієсловом або після першого слова речення.",
                ),
            ],
            quiz=[
                Quiz("«Як тебе звати?» —", ["Jak nazywasz?", "Jak się nazywasz?", "Jak nazywasz się to?"], 1,
                     "nazywać się → Jak się nazywasz?"),
            ],
        ),
    ],
)
