"""Тренування — 5 ОФІЦІЙНИХ питань (з services/mock), миттєвий фідбек, готовність."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import drill_kb, menu_kb, to_menu_kb
from app.domain.models import MODULE_LABELS, Module
from app.services import drills, mock
from app.services import state as user_state

router = Router()
SESSION_SIZE = 5


class Drill(StatesGroup):
    active = State()


def _target_module(st) -> Module:
    """Найслабший із дрильованих модулів (граматика/читання)."""
    return min(drills.DRILLABLE, key=lambda m: st.readiness.get(m.value, 0))


async def _send_q(message: Message, section: str, idxs: list[int], pos: int) -> None:
    it = mock.section_items(section)[idxs[pos]]
    ctx = f"<i>{html.escape(it.context)}</i>\n\n" if it.context else ""
    await message.answer(
        f"<b>{pos + 1}/{len(idxs)}</b> · {MODULE_LABELS[Module(section)]}\n\n{ctx}{html.escape(it.question)}",
        reply_markup=drill_kb(it.options, pos),
    )


async def _start(message: Message, user_id: int, state: FSMContext) -> None:
    st = await user_state.load(user_id)
    module = _target_module(st)
    idxs = drills.session_indices(module.value, SESSION_SIZE)
    await state.set_state(Drill.active)
    await state.update_data(section=module.value, idxs=idxs, pos=0, correct=0)
    await message.answer(
        f"🎯 <b>Тренування</b> — {len(idxs)} офіційних питань, фокус: {MODULE_LABELS[module]}.\n"
        "Тисни варіант — одразу скажу, правильно чи ні, з поясненням."
    )
    await _send_q(message, module.value, idxs, 0)


@router.message(Command("trening"))
async def cmd_drill(message: Message, state: FSMContext) -> None:
    await _start(message, message.from_user.id, state)


@router.callback_query(F.data == "drill:start")
async def cb_drill(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _start(cb.message, cb.from_user.id, state)


@router.callback_query(Drill.active, F.data.startswith("dr:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    parts = cb.data.split(":")  # dr:ans:<qidx>:<option>
    if len(parts) != 4:
        await cb.answer()
        return
    qidx, chosen = int(parts[2]), int(parts[3])
    data = await state.get_data()
    section, idxs, pos, correct = data["section"], data["idxs"], data["pos"], data["correct"]

    if qidx != pos:  # дубль/стале питання
        await cb.answer("Це питання вже пройдено 🙂")
        try:
            await cb.message.edit_reply_markup(reply_markup=None)
        except Exception:  # noqa: BLE001
            pass
        return

    it = mock.section_items(section)[idxs[pos]]
    ok = chosen == it.correct
    if ok:
        correct += 1
        verdict = "✔️ <b>Dobrze!</b>"
    else:
        verdict = f"❌ Poprawnie: <b>{html.escape(it.options[it.correct])}</b>"
    await cb.message.edit_text(f"{html.escape(it.question)}\n\n{verdict}\n💡 {html.escape(it.explain)}")
    await cb.answer("✔️" if ok else "❌")

    pos += 1
    await state.update_data(pos=pos, correct=correct)
    if pos < len(idxs):
        await _send_q(cb.message, section, idxs, pos)
    else:
        await _finalize(cb.message, cb.from_user.id, state, correct, len(idxs), section)


async def _finalize(
    message: Message, user_id: int, state: FSMContext, correct: int, total: int, section: str
) -> None:
    await state.clear()
    score = round(correct / total * 100) if total else 0
    st = await user_state.load(user_id)
    old = st.readiness.get(section, score)
    st.readiness[section] = round((old + score) / 2)
    await user_state.save(st)
    emoji = "🎉" if score >= 80 else "👍" if score >= 50 else "💪"
    await message.answer(
        f"{emoji} <b>Результат: {correct}/{total} ({score}%)</b>\n"
        f"Готовність {MODULE_LABELS[Module(section)]} оновлено.",
        reply_markup=menu_kb() if score >= 50 else to_menu_kb(),
    )
