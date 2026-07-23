"""Модуль 12 — Речення: порядок слів, питання/заперечення, сполучники, прислівники, модальні."""

from __future__ import annotations

from app.grammar.schema import Card, Lesson, Module, Quiz

MODULE = Module(
    id="skladnia",
    icon="🧩",
    title="Речення: як усе зʼєднати",
    subtitle="Порядок слів, питання, заперечення, сполучники, прислівники й «мушу/можна».",
    lessons=[
        # ── Порядок слів ──
        Lesson(
            id="sk_szyk",
            title="Порядок слів — гнучкий",
            cards=[
                Card(
                    "Базовий порядок як в українській",
                    "Зазвичай <b>підмет → присудок → додаток</b>: <i>Anna czyta książkę.</i> "
                    "Але порядок <b>вільний</b> — відмінки показують ролі, тож слова можна переставляти.",
                    [("Anna czyta książkę.", "Анна читає книжку."),
                     ("Książkę czyta Anna.", "Книжку читає Анна. (акцент на книжці)")],
                ),
                Card(
                    "Чому це працює",
                    "Оскільки закінчення (відмінки) показують, хто діє, а хто — обʼєкт, порядок "
                    "радше про <b>акцент</b>, ніж про зміст.",
                    tip="Новачку досить триматися звичного порядку. Гнучкість прийде згодом.",
                ),
            ],
            quiz=[
                Quiz("Що показує роль слова в польському реченні?",
                     ["порядок слів", "відмінок (закінчення)", "інтонація"], 1,
                     "Відмінки — тому порядок гнучкий."),
            ],
        ),
        # ── Питання й заперечення ──
        Lesson(
            id="sk_pytania",
            title="Питання та заперечення",
            cards=[
                Card(
                    "Питальні слова",
                    "Kto? Co? Gdzie? Kiedy? (коли) Dlaczego? (чому) Jak? Ile? (скільки)",
                    [("Kiedy wracasz?", "Коли повертаєшся?"), ("Ile to kosztuje?", "Скільки це коштує?")],
                ),
                Card(
                    "«так/ні» через czy",
                    "Без питального слова став <code>czy</code> на початок. У розмові можна й просто "
                    "інтонацією.",
                    [("Czy masz czas?", "Маєш час?"), ("Masz czas?", "Маєш час? (розмовно)")],
                ),
                Card(
                    "Заперечення nie",
                    "<code>nie</code> перед дієсловом. Подвійне заперечення — норма (nikt <code>nie</code> wie).",
                    [("Nie rozumiem.", "Не розумію."), ("Nigdy nie byłem.", "Ніколи не був.")],
                ),
            ],
            quiz=[
                Quiz("«Ніколи не був» —", ["Nigdy byłem.", "Nigdy nie byłem.", "Nie nigdy byłem."], 1,
                     "Подвійне заперечення норма: nigdy nie byłem."),
            ],
        ),
        # ── Сполучники ──
        Lesson(
            id="sk_spojniki",
            title="Сполучники: i, ale, bo, że, żeby",
            cards=[
                Card(
                    "Зʼєднуємо думки",
                    "• <code>i</code> — і\n• <code>a</code> — а (легке протиставлення)\n• <code>ale</code> — але\n"
                    "• <code>lub / albo</code> — або\n• <code>więc</code> — отже\n• <code>bo</code> — бо",
                    [("Mam czas, ale nie mam pieniędzy.", "Маю час, але не маю грошей."),
                     ("Nie idę, bo jestem chory.", "Не йду, бо хворий.")],
                ),
                Card(
                    "że і żeby",
                    "• <code>że</code> — що (факт): <i>Wiem, że masz rację.</i>\n"
                    "• <code>żeby</code> — щоб (мета): <i>Uczę się, żeby zdać egzamin.</i>",
                    [("Myślę, że tak.", "Думаю, що так."),
                     ("Piszę, żeby zaprosić.", "Пишу, щоб запросити.")],
                    tip="że = констатуєш факт; żeby = мета/бажання. Не плутай.",
                ),
            ],
            quiz=[
                Quiz("«Вчуся, ЩОБ скласти іспит» —", ["że", "żeby", "bo"], 1, "мета → żeby."),
                Quiz("«Знаю, ЩО ти маєш рацію» —", ["że", "żeby", "ale"], 0, "факт → że."),
            ],
        ),
        # ── Прислівники ──
        Lesson(
            id="sk_przyslowki",
            title="Прислівники: dobry → dobrze",
            cards=[
                Card(
                    "Як? — прислівник",
                    "Від прикметника: часто <code>-y → -e</code> або <code>-o</code>. Прислівник <b>не змінюється</b>.",
                    [("dobry → dobrze", "добрий → добре"), ("szybki → szybko", "швидкий → швидко"),
                     ("wolny → wolno", "повільний → повільно")],
                ),
                Card(
                    "Ступенювання прислівників",
                    "Теж є: dobrze → <code>lepiej</code> → najlepiej (краще/найкраще); "
                    "źle → gorzej (гірше).",
                    [("Mówię dobrze.", "Говорю добре."), ("Teraz mówię lepiej.", "Тепер говорю краще.")],
                ),
            ],
            quiz=[
                Quiz("Прислівник від «dobry» —", ["dobry", "dobrze", "dobrą"], 1,
                     "dobry → dobrze (як? добре)."),
            ],
        ),
        # ── Модальні ──
        Lesson(
            id="sk_modalne",
            title="Мушу / можу / треба (+ інфінітив)",
            cards=[
                Card(
                    "Обовʼязок і можливість",
                    "Ці слова + <b>інфінітив</b>:\n• <code>musieć</code> — мусити (muszę iść — мушу йти)\n"
                    "• <code>móc</code> — могти (mogę pomóc)\n• <code>chcieć</code> — хотіти (chcę spać)",
                    [("Muszę pracować.", "Мушу працювати."), ("Mogę wejść?", "Можна увійти?")],
                ),
                Card(
                    "Безособові: trzeba, można, wolno",
                    "• <code>trzeba</code> — треба\n• <code>można</code> — можна\n• <code>nie wolno</code> — не можна "
                    "(заборонено). Усі + інфінітив.",
                    [("Trzeba iść.", "Треба йти."), ("Tu można palić?", "Тут можна курити?"),
                     ("Nie wolno wchodzić.", "Заходити не можна.")],
                    tip="Це надзвичайно корисні конструкції для щоденного спілкування — вивчи їх рано.",
                ),
            ],
            quiz=[
                Quiz("«Мушу йти» —", ["Muszę iść.", "Musieć idę.", "Muszę idę."], 0,
                     "musieć + інфінітив: muszę iść."),
                Quiz("«Тут не можна» (заборонено) —", ["nie można", "nie wolno", "nie trzeba"], 1,
                     "Заборона → nie wolno."),
            ],
        ),
    ],
)
