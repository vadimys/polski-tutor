"""Індивідуальний план підготовки: /plan + кнопка (генерується з дати + готовності)."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import to_menu_kb
from app.services import access, clock, plan
from app.services import state as user_state

router = Router()


async def send_plan(message: Message, user_id: int) -> None:
    inf = await access.info(user_id)
    st = await user_state.load(user_id)
    p = plan.build(inf.exam_date, inf.confirmed, st.readiness, clock.today_local())
    await message.answer(plan.render(p), reply_markup=to_menu_kb())


@router.message(Command("plan"))
async def cmd_plan(message: Message) -> None:
    await send_plan(message, message.from_user.id)


@router.callback_query(F.data == "plan:show")
async def cb_plan(cb: CallbackQuery) -> None:
    await cb.answer()
    await send_plan(cb.message, cb.from_user.id)
