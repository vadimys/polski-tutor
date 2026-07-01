"""Стартовий тест (FSM) — офіційні питання (services/mock), результат по модулях."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot import quiz
from app.bot.keyboards import lesson_kb, question_kb
from app.bot.ui import bar
from app.domain.models import MODULE_LABELS, Module
from app.services import mock, placement
from app.services import state as user_state  # aiogram інжектить FSM у параметр `state`

router = Router()


class Placement(StatesGroup):
    active = State()


async def _send_question(message: Message, pairs: list, pos: int) -> None:
    section, idx = pairs[pos]
    it = mock.section_items(section)[idx]
    ctx = f"<i>{html.escape(it.context)}</i>\n\n" if it.context else ""
    await message.answer(
        f"<b>Питання {pos + 1}/{len(pairs)}</b>\n\n{ctx}{html.escape(it.question)}",
        reply_markup=question_kb(it.options, pos),
    )


async def _start(message: Message, state: FSMContext) -> None:
    pairs = placement.build_test()  # щоразу різна вибірка з офіц. банку
    await state.set_state(Placement.active)
    await state.update_data(pairs=pairs, pos=0, chosen=[])
    await message.answer(
        f"📝 <b>Стартовий тест</b> — {len(pairs)} офіційних питань (граматика + читання). "
        "Щоразу різні!\nВідповідай чесно — це діагностика. Поїхали!"
    )
    await _send_question(message, pairs, 0)


@router.message(Command("test"))
async def cmd_test(message: Message, state: FSMContext) -> None:
    await _start(message, state)


@router.callback_query(F.data == "placement:start")
async def cb_start(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _start(cb.message, state)


@router.callback_query(Placement.active, F.data.startswith("pl:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    ans = quiz.parse_answer(cb.data)
    if ans is None:
        await cb.answer()
        return
    qidx, choice = ans
    data = await state.get_data()
    pos = data["pos"]
    pairs = data["pairs"]
    chosen = data["chosen"]

    if qidx != pos:  # дубль/стале
        await cb.answer("Це питання вже пройдено 🙂")
        try:
            await cb.message.edit_reply_markup(reply_markup=None)
        except Exception:  # noqa: BLE001
            pass
        return

    chosen.append(choice)
    pos += 1
    await state.update_data(pos=pos, chosen=chosen)
    await cb.answer()
    try:
        await cb.message.edit_reply_markup(reply_markup=None)
    except Exception:  # noqa: BLE001
        pass

    if pos < len(pairs):
        await _send_question(cb.message, pairs, pos)
    else:
        await _finalize(cb.message, cb.from_user.id, state, pairs, chosen)


async def _finalize(
    message: Message, user_id: int, state: FSMContext, pairs: list, chosen: list
) -> None:
    await state.clear()
    result = placement.score([tuple(p) for p in pairs], chosen)

    st = await user_state.load(user_id)
    st.placement_done = True
    st.level = result.level
    st.readiness = result.per_module  # лише виміряні (gramatyka/czytanie)
    await user_state.save(st)

    lines = [
        f"✅ <b>Тест пройдено!</b> {result.correct}/{result.total} правильних.",
        f"📊 Рівень (за граматикою+читанням): <b>{result.level}</b>\n",
        "<b>Готовність за модулями:</b>",
    ]
    for m in Module:
        if m.value in result.per_module:
            lines.append(f"{MODULE_LABELS[m]}\n  {bar(result.per_module[m.value])}")
        else:
            lines.append(f"{MODULE_LABELS[m]}\n  ❔ ще не виміряно — зроби вправу цього модуля")

    # розбір помилок (макс. 5)
    wrong = []
    for (section, idx), ch in zip(pairs, chosen, strict=False):
        it = mock.section_items(section)[idx]
        if ch != it.correct:
            wrong.append(it)
    if wrong:
        lines.append("\n<b>Розбір помилок:</b>")
        for it in wrong[:5]:
            lines.append(
                f"• {html.escape(it.question)}\n  ✔️ <b>{html.escape(it.options[it.correct])}</b>"
                f" — {html.escape(it.explain)}"
            )

    lines.append(f"\n🎯 Почнемо з: <b>{MODULE_LABELS[st.weakest_module()]}</b>. Готовий до уроку?")
    await message.answer("\n".join(lines), reply_markup=lesson_kb())

    # одразу будуємо індивідуальний план (за датою іспиту + слабкими модулями)
    from app.handlers.plan import send_plan

    await send_plan(message, user_id)
