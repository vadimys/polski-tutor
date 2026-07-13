"""Підтримка/ідеї від користувача → тікет у чергу + алерт адміну.

Кнопка «🆘 Підтримка / 💡 Ідея» в меню. Категорія → текст → тікет (services.support).
Швидкий канал зворотного звʼязку: проблема або пропозиція покращення.
"""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import cancel_kb, support_category_kb, to_menu_kb
from app.config import settings
from app.services import clock, support

router = Router()


class Support(StatesGroup):
    waiting = State()  # очікуємо текст звернення (категорію вже обрано)


async def _open(message: Message) -> None:
    await message.answer(
        "🆘 <b>Підтримка та ідеї</b>\nНапиши мені про проблему або запропонуй покращення — "
        "я читаю кожне звернення. Обери тип:",
        reply_markup=support_category_kb(),
    )


@router.message(Command("pomoc_kontakt"))
async def cmd_support(message: Message) -> None:
    await _open(message)


@router.callback_query(F.data == "support:open")
async def cb_open(cb: CallbackQuery) -> None:
    await cb.answer()
    await _open(cb.message)


@router.callback_query(F.data.startswith("support:cat:"))
async def cb_cat(cb: CallbackQuery, state: FSMContext) -> None:
    cat = cb.data.split(":")[2]
    await state.set_state(Support.waiting)
    await state.update_data(cat=cat)
    await cb.answer()
    await cb.message.answer(
        f"✍️ Опиши {support.cat_label(cat).lower()} одним повідомленням "
        "(що сталось / що покращити). Я передам адміну.",
        reply_markup=cancel_kb(),
    )


@router.message(Support.waiting, F.text, ~F.text.startswith("/"))
async def on_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    cat = data.get("cat", "problem")
    uid = message.from_user.id
    uname = message.from_user.username
    name = f"@{uname}" if uname else (message.from_user.full_name or str(uid))
    at = clock.now_local().isoformat(timespec="minutes")
    tid = await support.create(uid, name, cat, message.text or "", at)
    await message.answer(
        "📨 <b>Дякую!</b> Звернення передано — відповім якнайшвидше 🙌",
        reply_markup=to_menu_kb(),
    )
    if settings.admin_id:
        kb = InlineKeyboardBuilder()
        kb.button(text="🎫 Відкрити тікет", callback_data=f"ac:ticket:{tid}")
        await message.bot.send_message(
            settings.admin_id,
            f"🆘 <b>Нове звернення #{tid}</b> · {support.cat_label(cat)}\n"
            f"Від: {html.escape(name)}\n\n{html.escape(message.text or '')}",
            reply_markup=kb.as_markup(),
        )
