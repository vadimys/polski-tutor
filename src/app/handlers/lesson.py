"""Щоденний урок: мікро-урок під найслабший модуль (через AI)."""

from __future__ import annotations

import logging
from datetime import timedelta

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import to_menu_kb
from app.domain.models import MODULE_LABELS, Module
from app.integrations import ai
from app.services import clock, limits, state, vocab

logger = logging.getLogger(__name__)
router = Router()

_SYSTEM = (
    "Ти — терплячий персональний тренер польської мови для україномовного учня, "
    "який готується до державного іспиту B1 (egzamin certyfikatowy). "
    "Пояснюй УКРАЇНСЬКОЮ, дуже просто, з прикладами — так, щоб зрозуміла навіть людина "
    "без граматичних термінів. Цільова мова — польська. Спирайся на схожість української "
    "й польської, але ЗАВЖДИ підсвічуй «фальшивих друзів» і місця, де мови різняться. "
    "На іспиті треба ≥50% у КОЖНОМУ з 5 модулів окремо. "
    "Теми наближай до реального життя учня: резиденція, громадянство, urząd, praca, побут. "
    "Форматуй для Telegram: лише теги <b>...</b> та емодзі, БЕЗ markdown (*, _, #)."
)


def _prompt(module: Module, level: str) -> str:
    return (
        f"Згенеруй короткий урок (~10–15 хв) із фокусом на модуль «{MODULE_LABELS[module]}». "
        f"Рівень учня: {level}. Структура:\n"
        "1. <b>Тема дня</b> — одне життєве речення-вступ.\n"
        "2. <b>Граматика дня</b> — ОДНЕ правило: назва простими словами → чому так → "
        "шаблон/закінчення → контраст з українською → приклад.\n"
        "3. <b>Нові слова</b> — 5–7 слів за темою: польською — українською + приклад речення.\n"
        "4. <b>Завдання</b> — коротка вправа саме цього модуля (для Pisanie — попроси написати "
        "короткий текст; для Czytanie — дай міні-текст і 2 питання; для Gramatyki — 3 речення "
        "на перетворення тощо). Учень відповість наступним повідомленням."
    )


def _fallback(module: Module) -> str:
    return (
        f"📚 <b>Урок дня</b> — фокус: {MODULE_LABELS[module]}\n\n"
        "AI тимчасово недоступний (не задано ключ). Базова вправа:\n\n"
        "Перепиши польською 3 речення у минулому часі:\n"
        "1. Czytam książkę. → ___\n"
        "2. Idę do sklepu. → ___\n"
        "3. Ona pracuje. → ___\n\n"
        "Відповідь надішли повідомленням — щойно AI під'єднають, перевірю."
    )


def _bump_streak(st) -> None:
    today = clock.today_local().isoformat()
    if st.last_lesson == today:
        return  # вже сьогодні займались
    yesterday = (clock.today_local() - timedelta(days=1)).isoformat()
    st.streak = st.streak + 1 if st.last_lesson == yesterday else 1
    st.last_lesson = today


async def _deliver(message: Message, user_id: int) -> None:
    st = await state.load(user_id)
    module = st.weakest_module()

    text = ""
    if ai.enabled() and await limits.allow_ai(user_id):
        text = await ai.ask(_SYSTEM, _prompt(module, st.level), strong=True, max_tokens=1500)
    if not text:
        text = _fallback(module)

    _bump_streak(st)
    await state.save(st)

    await vocab.seed_if_empty(user_id, clock.today_local())
    _, due_n = await vocab.counts(user_id, clock.today_local())
    review_note = f"\n\n🔁 На повторення сьогодні: <b>{due_n}</b> слів — /powtorki" if due_n else ""

    header = f"🔥 Стрік: <b>{st.streak}</b> · до іспиту <b>{clock.days_to_exam()}</b> днів\n\n"
    await message.answer(header + text + review_note, reply_markup=to_menu_kb())


@router.message(Command("lekcja", "lesson"))
async def cmd_lesson(message: Message) -> None:
    await message.answer("✍️ Готую урок…")
    await _deliver(message, message.from_user.id)


@router.callback_query(F.data == "lesson:start")
async def cb_lesson(cb: CallbackQuery) -> None:
    await cb.answer()
    await cb.message.answer("✍️ Готую урок…")
    await _deliver(cb.message, cb.from_user.id)
