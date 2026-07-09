"""Колода помилок: /pomylki → повторно опрацювати свої неправильні відповіді.

Правильно відповів тут → помилка виходить із колоди. Не рухає готовність (це
тренування закріплення), але прибирає прогалини, які видно з реальних вправ.
"""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot import quiz
from app.bot.keyboards import mistakes_kb, to_menu_kb
from app.services import mistakes

router = Router()


class Mist(StatesGroup):
    active = State()


async def _send_intro(message: Message, user_id: int) -> None:
    n = await mistakes.count(user_id)
    if n == 0:
        await message.answer(
            "🎉 <b>Колода помилок порожня!</b>\nПомилки з тренувань/МОКу зʼявляться тут — "
            "щоб потім їх цілеспрямовано закрити.",
            reply_markup=to_menu_kb(),
        )
        return
    kb = InlineKeyboardBuilder()
    kb.button(text=f"▶️ Опрацювати ({n})", callback_data="mist:start")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    await message.answer(
        f"🧯 <b>Робота над помилками</b>\nУ колоді <b>{n}</b> питань, де ти помилявся. "
        "Розберемо їх ще раз — правильна відповідь прибирає питання з колоди.",
        reply_markup=kb.as_markup(),
    )


@router.message(Command("pomylki"))
async def cmd_mistakes(message: Message) -> None:
    await _send_intro(message, message.from_user.id)


@router.callback_query(F.data == "mistakes:open")
async def cb_open(cb: CallbackQuery) -> None:
    await cb.answer()
    await _send_intro(cb.message, cb.from_user.id)


async def _send_q(message: Message, items: list, pos: int) -> None:
    it = items[pos]
    await message.answer(
        f"🧯 <b>Помилка {pos + 1}/{len(items)}</b>\n\n{html.escape(it['q'])}",
        reply_markup=mistakes_kb(it["opts"], pos),
    )


@router.callback_query(F.data == "mist:start")
async def cb_start(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    items = await mistakes.all_items(cb.from_user.id)
    if not items:
        await cb.message.answer("Колода вже порожня 🎉", reply_markup=to_menu_kb())
        return
    await state.set_state(Mist.active)
    await state.update_data(items=items, pos=0, fixed=0)
    await _send_q(cb.message, items, 0)


@router.callback_query(Mist.active, F.data == "mi:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    await cb.message.answer("⏹ Роботу над помилками зупинено.", reply_markup=to_menu_kb())


@router.callback_query(Mist.active, F.data.startswith("mi:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    items, pos, fixed = data["items"], data["pos"], data["fixed"]
    chosen = await quiz.read_answer(cb, pos)
    if chosen is None:
        return
    it = items[pos]
    ok = await quiz.show_verdict(cb, chosen, it["correct"], it["opts"], it["q"], it["explain"])
    if ok:  # закрив помилку — прибираємо з колоди
        await mistakes.resolve(cb.from_user.id, it["h"])
        fixed += 1

    pos += 1
    await state.update_data(pos=pos, fixed=fixed)
    if pos < len(items):
        await _send_q(cb.message, items, pos)
        return
    await state.clear()
    left = await mistakes.count(cb.from_user.id)
    await cb.message.answer(
        f"🏁 <b>Готово!</b> Закрито помилок: <b>{fixed}</b>. У колоді лишилось: <b>{left}</b>.\n"
        "Помилки, де знову схибив, лишаються — повернемось до них.",
        reply_markup=to_menu_kb(),
    )
