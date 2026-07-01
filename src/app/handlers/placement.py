"""Стартовий placement-тест (FSM): питання по черзі → результат по модулях."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import lesson_kb, question_kb
from app.bot.ui import bar
from app.domain.models import MODULE_LABELS, Module
from app.services import placement
from app.services import state as user_state  # aiogram інжектить FSM у параметр `state`

router = Router()


class Placement(StatesGroup):
    active = State()


async def _send_question(message: Message, idx: int) -> None:
    q = placement.QUESTIONS[idx]
    await message.answer(
        f"<b>Питання {idx + 1}/{len(placement.QUESTIONS)}</b>\n\n{html.escape(q.text)}",
        reply_markup=question_kb(q.options, idx),
    )


async def _start(message: Message, state: FSMContext) -> None:
    await state.set_state(Placement.active)
    await state.update_data(idx=0, answers={})
    await message.answer(
        "📝 <b>Стартовий тест</b> — близько 18 питань (граматика, читання, лексика).\n"
        "Відповідай чесно, без гугла — це лише діагностика, щоб скласти план. Поїхали!"
    )
    await _send_question(message, 0)


@router.message(Command("test"))
async def cmd_test(message: Message, state: FSMContext) -> None:
    await _start(message, state)


@router.callback_query(F.data == "placement:start")
async def cb_start(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()  # одразу гасимо «спінер» (інакше повільний старт → подвійні тапи)
    await _start(cb.message, state)


@router.callback_query(Placement.active, F.data.startswith("pl:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    parts = cb.data.split(":")  # pl:ans:<qidx>:<option>
    if len(parts) != 4:  # старий формат кнопки (з минулої сесії) — ігноруємо
        await cb.answer()
        return
    qidx, chosen = int(parts[2]), int(parts[3])
    data = await state.get_data()
    idx = data["idx"]
    answers = data["answers"]

    # тап по НЕ поточному питанню (дубль/стале) — ігноруємо, прибираємо кнопки
    if qidx != idx:
        await cb.answer("Це питання вже пройдено 🙂")
        try:
            await cb.message.edit_reply_markup(reply_markup=None)
        except Exception:  # noqa: BLE001
            pass
        return

    q = placement.QUESTIONS[idx]
    answers[q.id] = chosen
    idx += 1
    await state.update_data(idx=idx, answers=answers)
    await cb.answer()
    # прибираємо кнопки з відповіданого питання
    try:
        await cb.message.edit_reply_markup(reply_markup=None)
    except Exception:  # noqa: BLE001
        pass

    if idx < len(placement.QUESTIONS):
        await _send_question(cb.message, idx)
    else:
        # cb.from_user — реальний користувач (cb.message.from_user — це бот!)
        await _finalize(cb.message, cb.from_user.id, state, answers)


async def _finalize(
    message: Message, user_id: int, state: FSMContext, answers: dict[str, int]
) -> None:
    await state.clear()
    result = placement.score(answers)

    st = await user_state.load(user_id)
    st.placement_done = True
    st.level = result.level
    st.readiness = result.per_module
    await user_state.save(st)

    lines = [
        f"✅ <b>Тест пройдено!</b> {result.correct}/{result.total} правильних.",
        f"📊 Орієнтовний рівень: <b>{result.level}</b>\n",
        "<b>Готовність за модулями</b> (попередньо):",
    ]
    for mod in Module:
        pct = result.per_module.get(mod.value, 0)
        lines.append(f"{MODULE_LABELS[mod]}\n  {bar(pct)}")

    wrong = [
        q for q in placement.QUESTIONS if q.id in answers and answers[q.id] != q.correct
    ]
    if wrong:
        lines.append("\n<b>Розбір помилок:</b>")
        for q in wrong[:5]:
            correct_opt = html.escape(q.options[q.correct])
            lines.append(
                f"• {html.escape(q.text)}\n  ✔️ <b>{correct_opt}</b> — {html.escape(q.explain)}"
            )

    weakest = MODULE_LABELS[Module(min(result.per_module, key=lambda k: result.per_module[k]))]
    lines.append(f"\n🎯 Почнемо з найслабшого: <b>{weakest}</b>. Готовий до уроку?")

    await message.answer("\n".join(lines), reply_markup=lesson_kb())
