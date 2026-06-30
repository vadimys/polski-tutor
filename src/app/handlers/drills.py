"""Тренування у форматі екзамену: 5 питань, миттєвий фідбек, оновлення готовності."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import drill_kb, menu_kb, to_menu_kb
from app.domain.models import MODULE_LABELS, Module
from app.services import drills
from app.services import state as user_state

router = Router()

SESSION_SIZE = 5
# модулі, які тренує дрил (об'єктивні MCQ)
_DRILLABLE = (Module.GRAMATYKA, Module.CZYTANIE)


class Drill(StatesGroup):
    active = State()


def _target_module(st) -> Module:
    """Найслабший із дрильованих модулів (за готовністю)."""
    return min(_DRILLABLE, key=lambda m: st.readiness.get(m.value, 0))


async def _send_q(message: Message, qid: str, n: int, total: int) -> None:
    q = drills.by_id(qid)
    if q is None:
        return
    await message.answer(
        f"<b>{n}/{total}</b> · {MODULE_LABELS[q.module]}\n\n{html.escape(q.text)}",
        reply_markup=drill_kb(q.options),
    )


async def _start(message: Message, user_id: int, state: FSMContext) -> None:
    st = await user_state.load(user_id)
    module = _target_module(st)
    qs = drills.session(module, SESSION_SIZE)
    ids = [q.id for q in qs]
    await state.set_state(Drill.active)
    await state.update_data(ids=ids, idx=0, correct=0, module=module.value)
    await message.answer(
        f"🎯 <b>Тренування</b> — {len(ids)} питань, фокус: {MODULE_LABELS[module]}.\n"
        "Тисни варіант — одразу скажу, правильно чи ні, з поясненням."
    )
    await _send_q(message, ids[0], 1, len(ids))


@router.message(Command("trening"))
async def cmd_drill(message: Message, state: FSMContext) -> None:
    await _start(message, message.from_user.id, state)


@router.callback_query(F.data == "drill:start")
async def cb_drill(cb: CallbackQuery, state: FSMContext) -> None:
    await _start(cb.message, cb.from_user.id, state)
    await cb.answer()


@router.callback_query(Drill.active, F.data.startswith("dr:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    chosen = int(cb.data.rsplit(":", 1)[1])
    data = await state.get_data()
    ids = data["ids"]
    idx = data["idx"]
    correct = data["correct"]

    q = drills.by_id(ids[idx])
    ok = q is not None and chosen == q.correct
    if ok:
        correct += 1
        verdict = "✔️ <b>Правильно!</b>"
    else:
        verdict = f"❌ Правильно: <b>{html.escape(q.options[q.correct])}</b>"
    # питання → перетворюємо на «розібрану картку» (прибираємо кнопки)
    await cb.message.edit_text(
        f"{html.escape(q.text)}\n\n{verdict}\n💡 {html.escape(q.explain)}"
    )
    await cb.answer("✔️" if ok else "❌")

    idx += 1
    await state.update_data(idx=idx, correct=correct)

    if idx < len(ids):
        await _send_q(cb.message, ids[idx], idx + 1, len(ids))
    else:
        await _finalize(cb.message, cb.from_user.id, state, correct, len(ids), data["module"])


async def _finalize(
    message: Message, user_id: int, state: FSMContext, correct: int, total: int, module_value: str
) -> None:
    await state.clear()
    score = round(correct / total * 100) if total else 0

    st = await user_state.load(user_id)
    old = st.readiness.get(module_value, score)
    st.readiness[module_value] = round((old + score) / 2)  # згладжене оновлення
    await user_state.save(st)

    emoji = "🎉" if score >= 80 else "👍" if score >= 50 else "💪"
    await message.answer(
        f"{emoji} <b>Результат: {correct}/{total} ({score}%)</b>\n"
        f"Готовність {MODULE_LABELS[Module(module_value)]} оновлено.",
        reply_markup=menu_kb() if score >= 50 else to_menu_kb(),
    )
