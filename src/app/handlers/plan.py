"""Індивідуальний план підготовки: /plan + кнопка (генерується з дати + готовності)."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import to_menu_kb
from app.services import access, clock, goals, missions, plan, progress

router = Router()


async def send_plan(message: Message, user_id: int) -> None:
    inf = await access.info(user_id)
    readiness = progress.pcts(await progress.compute(user_id))  # чесна готовність (свіжо)
    g = await goals.status(user_id)
    p = plan.build(inf.exam_date, inf.confirmed, readiness, clock.today_local(), daily_min=g["goal"])
    dm = missions.daily_mission(user_id, clock.today_local().isoformat())
    tie = (
        f"\n\n🔥 Серія: <b>{g['streak']}</b> дн · ⭐ рівень <b>{g['level']}</b>\n"
        f"🎲 <b>Крок сьогодні:</b> {dm['desc']} (+{dm['xp']} XP)"
    )
    await message.answer(plan.render(p) + tie, reply_markup=to_menu_kb())


@router.message(Command("plan"))
async def cmd_plan(message: Message) -> None:
    await send_plan(message, message.from_user.id)


@router.callback_query(F.data == "plan:show")
async def cb_plan(cb: CallbackQuery) -> None:
    await cb.answer()
    await send_plan(cb.message, cb.from_user.id)
