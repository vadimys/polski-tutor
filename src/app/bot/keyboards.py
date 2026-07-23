"""Інлайн-клавіатури бота."""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings


def start_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Пройти стартовий тест", callback_data="placement:start")
    kb.adjust(1)
    return kb.as_markup()


def example_kb(callback_data: str) -> InlineKeyboardMarkup:
    """Кнопка «показати зразок» під продуктивним завданням (мовлення/письмо)."""
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Показати зразок", callback_data=callback_data)
    kb.adjust(1)
    return kb.as_markup()


def exam_dates_kb(
    sessions: list[str], prefix: str, with_unconfirmed: bool = False
) -> InlineKeyboardMarkup:
    """Кнопки лише з ОФІЦІЙНИХ дат сесій. prefix — onb:date (онбординг) / onb:exam (оновлення)."""
    from app.services import exam_dates

    kb = InlineKeyboardBuilder()
    for iso in sessions:
        kb.button(text=f"📅 {exam_dates.label(iso)}", callback_data=f"{prefix}:{iso}")
    if with_unconfirmed:
        kb.button(text="❔ Дата ще не підтверджена", callback_data="onb:unconfirmed")
    kb.adjust(1)
    return kb.as_markup()


def send_request_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🚀 Почати безкоштовно", callback_data="onb:send")
    kb.button(text="⬅️ Змінити дату", callback_data="onb:restart")
    kb.adjust(1)
    return kb.as_markup()


def role_choice_kb() -> InlineKeyboardMarkup:
    """Перший екран онбордингу: учень (платна підписка) чи викладач (безкоштовно)."""
    kb = InlineKeyboardBuilder()
    kb.button(text="🎓 Я учень — готуюсь до іспиту", callback_data="onb:role:student")
    kb.button(text="👩‍🏫 Я викладач — навчаю учнів", callback_data="onb:role:teacher")
    kb.adjust(1)
    return kb.as_markup()


def admin_teacher_kb(user_id: int) -> InlineKeyboardMarkup:
    """Рішення адміна щодо заявки викладача."""
    kb = InlineKeyboardBuilder()
    kb.button(text="👩‍🏫 Схвалити як викладача", callback_data=f"adm:teacher:{user_id}")
    kb.button(text="❌ Відмовити", callback_data=f"adm:no:{user_id}")
    kb.adjust(1)
    return kb.as_markup()


def contact_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✍️ Написати адміну", callback_data="onb:contact")
    kb.adjust(1)
    return kb.as_markup()


def extend_request_kb() -> InlineKeyboardMarkup:
    """Після завершення trial: підписка (Stars) — головний CTA + написати адміну."""
    kb = InlineKeyboardBuilder()
    kb.button(text="💎 Оформити підписку", callback_data="pay:start")
    kb.button(text="✍️ Написати адміну", callback_data="onb:contact")
    kb.adjust(1)
    return kb.as_markup()


def activation_kb(next_cb: str, next_label: str) -> InlineKeyboardMarkup:
    """Перша сесія: один чіткий наступний крок (aha) + меню. Do, don't show."""
    kb = InlineKeyboardBuilder()
    kb.button(text=f"▶️ {next_label}", callback_data=next_cb)
    kb.button(text="📋 Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


def churn_survey_kb() -> InlineKeyboardMarkup:
    """Екран завершення trial: підписка (CTA) + exit-survey причин (churn-prevention).
    Причина → адресний save-offer (див. handlers.onboarding.cb_churn_reason)."""
    from app.services.churn import REASONS

    kb = InlineKeyboardBuilder()
    kb.button(text="💎 Оформити підписку", callback_data="pay:start")
    for key, label in REASONS:
        kb.button(text=label, callback_data=f"churn:reason:{key}")
    kb.button(text="✍️ Написати адміну", callback_data="onb:contact")
    kb.adjust(1)
    return kb.as_markup()


def support_category_kb() -> InlineKeyboardMarkup:
    """Тип звернення до підтримки."""
    kb = InlineKeyboardBuilder()
    kb.button(text="🛠 Проблема", callback_data="support:cat:problem")
    kb.button(text="💡 Ідея / пропозиція", callback_data="support:cat:idea")
    kb.adjust(1)
    return kb.as_markup()


def exam_result_kb() -> InlineKeyboardMarkup:
    """Після іспиту: як пройшло?"""
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Склав!", callback_data="exam:res:passed")
    kb.button(text="❌ Не склав", callback_data="exam:res:failed")
    kb.button(text="⏳ Чекаю результат", callback_data="exam:res:wait")
    kb.adjust(1)
    return kb.as_markup()


def admin_extend_kb(user_id: int) -> InlineKeyboardMarkup:
    """Рішення адміна щодо продовження доступу після trial."""
    kb = InlineKeyboardBuilder()
    kb.button(text="🔓 Продовжити доступ", callback_data=f"adm:extend:{user_id}")
    kb.button(text="❌ Ні", callback_data=f"adm:no:{user_id}")
    kb.adjust(1)
    return kb.as_markup()


def admin_decision_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Схвалити", callback_data=f"adm:ok:{user_id}")
    kb.button(text="❌ Відмовити", callback_data=f"adm:no:{user_id}")
    kb.adjust(2)
    return kb.as_markup()


def approved_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="▶️ Пройти стартовий тест", callback_data="placement:start")
    kb.button(text="📅 Вказати/змінити дату іспиту", callback_data="onb:setdate")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


def cancel_kb() -> InlineKeyboardMarkup:
    """Кнопка «Скасувати» під час введення (письмо/мовлення/керована практика)."""
    kb = InlineKeyboardBuilder()
    kb.button(text="🚫 Скасувати", callback_data="nav:cancel")
    kb.adjust(1)
    return kb.as_markup()


def _mcq_kb(options: list[str], qidx: int, ans_prefix: str, stop_cb: str) -> InlineKeyboardMarkup:
    """Спільна MCQ-клавіатура: варіанти (з індексом питання) + вихід «⏹ Завершити»."""
    kb = InlineKeyboardBuilder()
    for i, opt in enumerate(options):
        kb.button(text=opt, callback_data=f"{ans_prefix}:{qidx}:{i}")
    kb.button(text="⏹ Завершити", callback_data=stop_cb)
    kb.adjust(1)
    return kb.as_markup()


def question_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Кнопки-варіанти (callback містить індекс питання — захист від дублів/сталих тапів)."""
    return _mcq_kb(options, qidx, "pl:ans", "pl:stop")


def menu_kb() -> InlineKeyboardMarkup:
    """Головне меню: практика (що ти РОБИШ) + Панель (прогрес/похід/місії — read-only).

    Похід/Місії/Прогрес окремими кнопками НЕ дублюємо — вони в «📱 Панелі»
    (лишаються командами /quest /misje /postep для тих, хто без панелі)."""
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="⚡ Навчатись зараз", callback_data="coach:now"))  # головний CTA
    if settings.webapp_url:  # хаб прогресу — коли Mini App увімкнено
        kb.row(InlineKeyboardButton(text="📱 Панель прогресу", web_app=WebAppInfo(url=settings.webapp_url)))
    kb.row(InlineKeyboardButton(text="📖 Урок дня", callback_data="lesson:start"))
    kb.row(InlineKeyboardButton(text="📚 Граматика (курс з нуля)", callback_data="grammar:home"))
    practice = [
        ("🔁 Повторення слів", "review:start"),
        ("📚 Словник за темами", "lex:open"),
        ("✍️ Письмо", "writing:start"),
        ("🗣 Мовлення", "speaking:start"),
        ("🖼 Опис фото", "speaking:photo"),
        ("🎧 Аудіювання", "listening:start"),
        ("🎯 Тренування", "drill:start"),
        ("🧩 Зіставлення", "match:open"),
        ("🔗 Аудіо-зіставлення", "amatch:open"),
        ("✏️ Впиши форму", "fill:open"),
        ("🔄 Трансформації", "open:open"),
        ("📋 Офіційний МОК", "mock:open"),
        ("🎓 Повний мок іспиту", "exam:open"),
        ("🧯 Мої помилки", "mistakes:open"),
        ("📅 Мій план", "plan:show"),
        ("📝 Завдання", "asgn:me"),
        ("🏆 Рейтинг класу", "lb:me"),
        ("🎁 Запросити друга", "ref:invite"),
        ("🆘 Підтримка / 💡 Ідея", "support:open"),
    ]
    for i in range(0, len(practice), 2):  # у 2 колонки — менше скролу
        kb.row(*(InlineKeyboardButton(text=t, callback_data=c) for t, c in practice[i : i + 2]))
    kb.row(InlineKeyboardButton(text="📝 Тест рівня", callback_data="placement:start"))
    return kb.as_markup()


def teacher_welcome_kb() -> InlineKeyboardMarkup:
    """Після схвалення/продовження викладача — його дії (клас, матеріали), НЕ учнівські."""
    kb = InlineKeyboardBuilder()
    kb.button(text="👥 Мій клас", callback_data="teacher:class")
    kb.button(text="📚 Матеріали та тести", callback_data="teacher:materials")
    kb.adjust(1)
    return kb.as_markup()


async def menu_kb_for(user_id: int) -> InlineKeyboardMarkup:
    """Меню за роллю: викладачу (у т.ч. view-as) — його інструмент, інакше учнівський хаб.
    Використовується у фіналах вправ, щоб превʼю-вправа не викидала викладача в учнівське меню."""
    from app.services import state as user_state
    from app.services import viewas

    st = await user_state.load(user_id)
    if viewas.role_for(await viewas.get(user_id), st.role) == "teacher":
        return teacher_menu_kb()
    return menu_kb()


def teacher_menu_kb() -> InlineKeyboardMarkup:
    """Меню викладача — живе й функціональне САМЕ для викладача: клас, матеріали,
    запрошення учнів, оплати. Без учнівського (тест рівня, урок дня, план, місії, SRS)."""
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="👥 Мій клас", callback_data="teacher:class"))  # головний CTA
    kb.row(InlineKeyboardButton(text="📚 Матеріали та тести", callback_data="teacher:materials"))
    kb.row(
        InlineKeyboardButton(text="🔗 Запросити учнів", callback_data="teacher:invite"),
        InlineKeyboardButton(text="💎 Оплати учнів", callback_data="teacher:revenue"),
    )
    kb.row(InlineKeyboardButton(text="🆘 Підтримка / звʼязок", callback_data="support:open"))
    return kb.as_markup()


def teacher_materials_kb() -> InlineKeyboardMarkup:
    """Матеріали для викладача: каталог тестів + перегляд усіх типів вправ як превʼю
    (учнівський контент, щоб знати/демонструвати/призначати; готовність не рухається)."""
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="🎓 Каталог офіційних тестів", callback_data="teacher:catalog"))
    kb.row(InlineKeyboardButton(text="🎓 Повний мок (превʼю)", callback_data="exam:open"))
    preview = [
        ("🎧 Аудіювання", "listening:start"),
        ("🎯 Тренування", "drill:start"),
        ("🧩 Зіставлення", "match:open"),
        ("🔗 Аудіо-зіставл.", "amatch:open"),
        ("✏️ Впиши форму", "fill:open"),
        ("🔄 Трансформації", "open:open"),
        ("✍️ Письмо", "writing:start"),
        ("🗣 Мовлення", "speaking:start"),
        ("🖼 Опис фото", "speaking:photo"),
        ("📚 Словник", "lex:open"),
        ("📋 Офіційний МОК", "mock:open"),
    ]
    for i in range(0, len(preview), 2):
        kb.row(*(InlineKeyboardButton(text=t, callback_data=c) for t, c in preview[i : i + 2]))
    kb.row(InlineKeyboardButton(text="⬅️ Меню викладача", callback_data="menu:home"))
    return kb.as_markup()


def drill_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для тренування (з індексом питання)."""
    return _mcq_kb(options, qidx, "dr:ans", "dr:stop")


def mock_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для офіційного МОКу."""
    return _mcq_kb(options, qidx, "mk:ans", "mk:stop")


def mistakes_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для опрацювання колоди помилок."""
    return _mcq_kb(options, qidx, "mi:ans", "mi:stop")


def exam_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для повного моку (режим іспиту — без миттєвого вердикту)."""
    return _mcq_kb(options, qidx, "ex:ans", "ex:stop")


def match_kb(n_options: int, qidx: int) -> InlineKeyboardMarkup:
    """Зіставлення: літерні кнопки A, B, C… (фрагменти показані в інтро) + вихід.

    Фрагменти бувають довгі — тому на кнопках лише літери, самі фрагменти — у списку
    вгорі. Callback сумісний із quiz.read_answer: 'ma:ans:<qidx>:<opt>'.
    """
    kb = InlineKeyboardBuilder()
    letters = [
        InlineKeyboardButton(text=chr(65 + i), callback_data=f"ma:ans:{qidx}:{i}")
        for i in range(n_options)
    ]
    for j in range(0, len(letters), 4):
        kb.row(*letters[j : j + 4])
    kb.row(InlineKeyboardButton(text="⏹ Завершити", callback_data="ma:stop"))
    return kb.as_markup()


def fill_kb(pos: int) -> InlineKeyboardMarkup:
    """Free-fill: відповідь вводиться ТЕКСТОМ; кнопки лише «не знаю» / вихід."""
    kb = InlineKeyboardBuilder()
    kb.button(text="⏭ Не знаю", callback_data=f"ff:skip:{pos}")
    kb.button(text="⏹ Завершити", callback_data="ff:stop")
    kb.adjust(2)
    return kb.as_markup()


def open_kb(pos: int) -> InlineKeyboardMarkup:
    """Open-таск (трансформація): відповідь ТЕКСТОМ; «пропустити» / вихід."""
    kb = InlineKeyboardBuilder()
    kb.button(text="⏭ Пропустити", callback_data=f"op:skip:{pos}")
    kb.button(text="⏹ Завершити", callback_data="op:stop")
    kb.adjust(2)
    return kb.as_markup()


def audiomatch_kb(n_speakers: int, selected: set[int], pos: int) -> InlineKeyboardMarkup:
    """Аудіо-зіставлення (multi-select): перемикачі осіб 1..N (✅ = обрано) + «Готово».

    Callback: 'am:tog:<pos>:<i>' (перемкнути особу i), 'am:done:<pos>', 'am:stop'.
    """
    kb = InlineKeyboardBuilder()
    btns = [
        InlineKeyboardButton(
            text=("✅ " if i in selected else "") + str(i + 1),
            callback_data=f"am:tog:{pos}:{i}",
        )
        for i in range(n_speakers)
    ]
    for j in range(0, len(btns), 4):
        kb.row(*btns[j : j + 4])
    kb.row(InlineKeyboardButton(text="✔️ Готово", callback_data=f"am:done:{pos}"))
    kb.row(InlineKeyboardButton(text="⏹ Завершити", callback_data="am:stop"))
    return kb.as_markup()


def exam_match_kb(n_options: int, qidx: int) -> InlineKeyboardMarkup:
    """Зіставлення в РЕЖИМІ ІСПИТУ — літерні кнопки (ex:ans, без вердикту) + вихід."""
    kb = InlineKeyboardBuilder()
    letters = [
        InlineKeyboardButton(text=chr(65 + i), callback_data=f"ex:ans:{qidx}:{i}")
        for i in range(n_options)
    ]
    for j in range(0, len(letters), 4):
        kb.row(*letters[j : j + 4])
    kb.row(InlineKeyboardButton(text="⏹ Завершити", callback_data="ex:stop"))
    return kb.as_markup()


def exam_audiomatch_kb(n_speakers: int, selected: set[int], pos: int) -> InlineKeyboardMarkup:
    """Multi-select аудіо-зіставлення в РЕЖИМІ ІСПИТУ — toggle осіб + «Далі» (без вердикту).

    Callback: 'ex:mtog:<pos>:<i>' (перемкнути особу i), 'ex:mdone:<pos>', 'ex:stop'.
    """
    kb = InlineKeyboardBuilder()
    btns = [
        InlineKeyboardButton(
            text=("✅ " if i in selected else "") + str(i + 1),
            callback_data=f"ex:mtog:{pos}:{i}",
        )
        for i in range(n_speakers)
    ]
    for j in range(0, len(btns), 4):
        kb.row(*btns[j : j + 4])
    kb.row(InlineKeyboardButton(text="➡️ Далі", callback_data=f"ex:mdone:{pos}"))
    kb.row(InlineKeyboardButton(text="⏹ Завершити", callback_data="ex:stop"))
    return kb.as_markup()


def exam_text_kb(pos: int) -> InlineKeyboardMarkup:
    """Текстовий крок моку (free-fill/open) — відповідь ТЕКСТОМ; пропустити / вихід."""
    kb = InlineKeyboardBuilder()
    kb.button(text="⏭ Пропустити", callback_data=f"ex:skip:{pos}")
    kb.button(text="⏹ Завершити", callback_data="ex:stop")
    kb.adjust(2)
    return kb.as_markup()


def mock_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📖 Читання (офіц.)", callback_data="mock:czytanie")
    kb.button(text="🔤 Граматика (офіц.)", callback_data="mock:gramatyka")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


def review_grade_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Знав", callback_data="rv:ok")
    kb.button(text="❌ Не знав", callback_data="rv:no")
    kb.adjust(2)
    return kb.as_markup()


def to_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


def lesson_kb() -> InlineKeyboardMarkup:
    """Після уроку/тесту: почати урок або відкрити меню."""
    kb = InlineKeyboardBuilder()
    kb.button(text="▶️ Почати урок", callback_data="lesson:start")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


def coach_kb() -> InlineKeyboardMarkup:
    """Нагадування: головний CTA — розумний автопідбір дії."""
    kb = InlineKeyboardBuilder()
    kb.button(text="⚡ Навчатись зараз", callback_data="coach:now")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()
