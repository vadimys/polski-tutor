"""Тренування — 5 ОФІЦІЙНИХ питань (з services/mock), миттєвий фідбек, готовність."""

from __future__ import annotations

from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot import quiz
from app.bot.keyboards import drill_kb, menu_kb_for, to_menu_kb
from app.bot.ui import emph
from app.domain.models import MODULE_LABELS, Module
from app.services import drills, goals, mistakes, mock, pollquiz
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
    ctx = f"<i>{emph(it.context)}</i>\n\n" if it.context else ""
    await message.answer(
        f"<b>{pos + 1}/{len(idxs)}</b> · {MODULE_LABELS[Module(section)]}\n\n{ctx}{emph(it.question)}",
        reply_markup=drill_kb(it.options, pos),
    )


async def _start(message: Message, user_id: int, state: FSMContext) -> None:
    st = await user_state.load(user_id)
    module = _target_module(st)
    idxs = drills.session_indices(module.value, SESSION_SIZE)

    # Короткий контент (граматика) → нативний quiz-poll; довгі тексти (читання) → інлайн
    items = []
    for i in idxs:
        it = mock.section_items(module.value)[i]
        q = f"{it.context}\n\n{it.question}" if it.context else it.question
        items.append({"q": q, "opts": list(it.options), "correct": it.correct, "explain": it.explain})
    if pollquiz.fits(items):
        await message.answer(
            f"🎯 <b>Тренування</b> — {len(items)} офіційних питань, фокус: {MODULE_LABELS[module]}.\n"
            "Відповідай у quiz-опитуваннях нижче 👇"
        )
        await pollquiz.start(
            message.bot, chat_id=message.chat.id, user_id=user_id, kind="readiness",
            items=items, module=module.value, title="🔤 Тренування",
        )
        return

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


@router.callback_query(Drill.active, F.data == "dr:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "⏹ Тренування завершено — <b>без оцінки</b> (готовність рухає лише повністю пройдена серія).",
        reply_markup=await menu_kb_for(cb.from_user.id),
    )


@router.callback_query(Drill.active, F.data.startswith("dr:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    section, idxs, pos, correct = data["section"], data["idxs"], data["pos"], data["correct"]

    chosen = await quiz.read_answer(cb, pos)
    if chosen is None:  # стале/дубль/зіпсовано — уже оброблено
        return

    it = mock.section_items(section)[idxs[pos]]
    if await quiz.show_verdict(cb, chosen, it.correct, it.options, it.question, it.explain):
        correct += 1
    else:
        await mistakes.add(cb.from_user.id, section, it.question, list(it.options), it.correct, it.explain)

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
    await user_state.update_readiness(user_id, section, score)
    emoji = "🎉" if score >= 80 else "👍" if score >= 50 else "💪"
    await message.answer(
        f"{emoji} <b>Результат: {correct}/{total} ({score}%)</b>\n"
        f"Готовність {MODULE_LABELS[Module(section)]} оновлено.",
        reply_markup=(await menu_kb_for(user_id)) if score >= 50 else to_menu_kb(),
    )
    if c := await goals.pop_celebration(user_id):
        await message.answer(c)
