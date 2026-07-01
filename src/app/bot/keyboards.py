"""Інлайн-клавіатури бота."""

from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Пройти стартовий тест", callback_data="placement:start")
    kb.adjust(1)
    return kb.as_markup()


def onboarding_date_kb() -> InlineKeyboardMarkup:
    """Вибір дати іспиту (офіційні сесії 2026) або «не підтверджена»."""
    kb = InlineKeyboardBuilder()
    kb.button(text="📅 5 грудня 2026", callback_data="onb:date:2026-12-05")
    kb.button(text="📅 17 жовтня 2026", callback_data="onb:date:2026-10-17")
    kb.button(text="✏️ Інша дата", callback_data="onb:other")
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
    kb.button(text="📋 Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


def question_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Кнопки-варіанти (callback містить індекс питання — захист від дублів/сталих тапів)."""
    kb = InlineKeyboardBuilder()
    for i, opt in enumerate(options):
        kb.button(text=opt, callback_data=f"pl:ans:{qidx}:{i}")
    kb.adjust(1)
    return kb.as_markup()


def menu_kb() -> InlineKeyboardMarkup:
    """Головне меню."""
    kb = InlineKeyboardBuilder()
    kb.button(text="📖 Урок дня", callback_data="lesson:start")
    kb.button(text="🔁 Повторення слів", callback_data="review:start")
    kb.button(text="✍️ Письмо", callback_data="writing:start")
    kb.button(text="🗣 Мовлення", callback_data="speaking:start")
    kb.button(text="🖼 Опис фото", callback_data="speaking:photo")
    kb.button(text="🎧 Аудіювання", callback_data="listening:start")
    kb.button(text="🎯 Тренування", callback_data="drill:start")
    kb.button(text="📋 Офіційний МОК", callback_data="mock:open")
    kb.button(text="📊 Прогрес", callback_data="progress:show")
    kb.button(text="📝 Тест рівня", callback_data="placement:start")
    kb.adjust(1)
    return kb.as_markup()


def drill_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для тренування (з індексом питання)."""
    kb = InlineKeyboardBuilder()
    for i, opt in enumerate(options):
        kb.button(text=opt, callback_data=f"dr:ans:{qidx}:{i}")
    kb.adjust(1)
    return kb.as_markup()


def listen_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для аудіювання (з індексом питання)."""
    kb = InlineKeyboardBuilder()
    for i, opt in enumerate(options):
        kb.button(text=opt, callback_data=f"ls:ans:{qidx}:{i}")
    kb.adjust(1)
    return kb.as_markup()


def mock_kb(options: list[str], qidx: int) -> InlineKeyboardMarkup:
    """Варіанти відповіді для офіційного МОКу."""
    kb = InlineKeyboardBuilder()
    for i, opt in enumerate(options):
        kb.button(text=opt, callback_data=f"mk:ans:{qidx}:{i}")
    kb.adjust(1)
    return kb.as_markup()


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
