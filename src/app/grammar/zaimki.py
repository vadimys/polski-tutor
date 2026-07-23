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
                    "• <code>mój</code> — мій\n• <code>twój</code> — твій\n• <code>jego</code> — його\n"
                    "• <code>jej</code> — її\n• <code>nasz</code> — наш\n• <code>wasz</code> — ваш\n• <code>ich</code> — їхній",
                ),
                Card(
                    "mój теж узгоджується за родом",
                    "<code>mój</code> (ч.) · <code>moja</code> (ж.) · <code>moje</code> (с.). Так само twój, nasz, wasz.",
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
                    "<code>ten</code> (ч.) · <code>ta</code> (ж.) · <code>to</code> (с.). Множина: <code>ci</code> (люди-чол.) "
                    "/ <code>te</code> (решта).",
                    [("ten dom", "цей дім"), ("ta książka", "ця книжка"), ("te domy", "ці будинки")],
                ),
                Card(
                    "Той — tamten",
                    "Дальший обʼєкт: <code>tamten / tamta / tamto</code> (той/та/те).",
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
                    "• ja → <code>mnie</code> (мене/мені)\n• ty → <code>cię/ciebie</code> (тебе)\n"
                    "• on → <code>go/jego</code> · ona → <code>ją</code>",
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
                    "się = «-ся/-сь»",
                    "Багато дій «на себе» мають <code>się</code> — як українське «-ся».",
                    [("myć się", "митися"), ("uczyć się", "вчитися"),
                     ("nazywać się", "називатися")],
                ),
                Card(
                    "się «плаває» в реченні",
                    "На відміну від українського «-ся», польське <code>się</code> — окреме слово й може стояти "
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
