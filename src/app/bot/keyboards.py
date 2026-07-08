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
    kb.button(text="📨 Надіслати запит адміну", callback_data="onb:send")
    kb.button(text="⬅️ Змінити дату", callback_data="onb:restart")
    kb.adjust(1)
    return kb.as_markup()


def contact_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✍️ Написати адміну", callback_data="onb:contact")
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
    kb.button(text="📋 Меню", callback_data="menu:home")
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
    if settings.webapp_url:  # хаб прогресу — вгорі, коли Mini App увімкнено
        kb.row(InlineKeyboardButton(text="📱 Панель прогресу", web_app=WebAppInfo(url=settings.webapp_url)))
    kb.row(InlineKeyboardButton(text="📖 Урок дня", callback_data="lesson:start"))
    practice = [
        ("🔁 Повторення слів", "review:start"),
        ("📚 Словник за темами", "lex:open"),
        ("✍️ Письмо", "writing:start"),
        ("🗣 Мовлення", "speaking:start"),
        ("🖼 Опис фото", "speaking:photo"),
        ("🎧 Аудіювання", "listening:start"),
        ("🎯 Тренування", "drill:start"),
        ("📋 Офіційний МОК", "mock:open"),
        ("📅 Мій план", "plan:show"),
    ]
    for i in range(0, len(practice), 2):  # у 2 колонки — менше скролу
        kb.row(*(InlineKeyboardButton(text=t, callback_data=c) for t, c in practice[i : i + 2]))
    kb.row(InlineKeyboardButton(text="📝 Тест рівня", callback_data="placement:start"))
    return kb.as_markup()


def drill_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для тренування (з індексом питання)."""
    return _mcq_kb(options, qidx, "dr:ans", "dr:stop")


def listen_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для аудіювання (з індексом питання)."""
    return _mcq_kb(options, qidx, "ls:ans", "ls:stop")


def mock_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для офіційного МОКу."""
    return _mcq_kb(options, qidx, "mk:ans", "mk:stop")


def mock_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📖 Читання (офіц.)", callback_data="mock:czytanie")
    kb.button(text="🔤 Граматика (офіц.)", callback_data="mock:gramatyka")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


def review_show_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="👁 Показати переклад", callback_data="rv:show")
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
