"""Повний мок іспиту (/egzamin) — усі авто-оцінювані секції ПОСЛІДОВНО, режим іспиту.

Відмінність від /mok (окремі секції з миттєвим фідбеком): тут — без підказок і
вердиктів під час; відповіді фіксуються, результат у балах — у кінці. Це найближче
до реальних умов. Записує складання моку (гейт готовності) і помилки в колоду.
Продуктивні модулі (письмо/мовлення) — окремо (їх не можна авто-оцінити тут).
"""

from __future__ import annotations

import html
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import content
from app.bot import quiz
from app.bot.keyboards import exam_kb, menu_kb, to_menu_kb
from app.services import exam_scale, goals, mistakes, progress
from app.services import state as user_state

router = Router()

_LABEL = {"sluchanie": "🎧 Аудіювання", "czytanie": "📖 Читання", "gramatyka": "🔤 Граматика"}


class Exam(StatesGroup):
    active = State()


def _build_seq(exam_id: str) -> list[list]:
    seq: list[list] = []
    for sec in content.exam_sections(exam_id):
        for i in range(len(content.exam_items(exam_id, sec))):
            seq.append([sec, i])
    return seq


@router.message(Command("egzamin"))
async def cmd_exam(message: Message) -> None:
    await _intro(message)


@router.callback_query(F.data == "exam:open")
async def cb_open(cb: CallbackQuery) -> None:
    await cb.answer()
    await _intro(cb.message)


async def _intro(message: Message) -> None:
    exam = content.latest()  # тренуємось на найновішому офіційному тесті
    seq = _build_seq(exam.id)
    if not seq:
        await message.answer("Повний мок тимчасово недоступний.", reply_markup=to_menu_kb())
        return
    labels = " → ".join(_LABEL[s] for s in content.exam_sections(exam.id))
    b = InlineKeyboardBuilder()
    b.button(text="▶️ Почати мок", callback_data=f"exam:begin:{exam.id}")
    b.button(text="⬅️ Меню", callback_data="menu:home")
    b.adjust(1)
    await message.answer(
        f"🎓 <b>Повний мок іспиту</b>\nТест: <b>{exam.label}</b>\n\n"
        f"Секції поспіль: {labels} — <b>{len(seq)}</b> питань.\n"
        "⏱ Режим іспиту: <b>без підказок і вердиктів</b>, результат у балах — у кінці. "
        "Виділи ~40–60 хв і не відволікайся.\n"
        "<i>Письмо й мовлення оцінюються окремо (/pisanie, /mowienie).</i>",
        reply_markup=b.as_markup(),
    )


async def _send_q(message: Message, exam_id: str, seq: list, pos: int) -> None:
    sec, idx = seq[pos]
    it = content.exam_items(exam_id, sec)[idx]
    ctx = f"<i>{html.escape(it.context)}</i>\n\n" if it.context else ""
    await message.answer(
        f"🎓 <b>Мок · {_LABEL[sec]}</b> · питання {pos + 1}/{len(seq)}\n\n{ctx}{html.escape(it.question)}",
        reply_markup=exam_kb(it.options, pos),
    )


@router.callback_query(F.data.startswith("exam:begin:"))
async def cb_begin(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    exam_id = cb.data.split(":", 2)[2]
    seq = _build_seq(exam_id)
    await state.set_state(Exam.active)
    await state.update_data(exam_id=exam_id, seq=seq, pos=0, correct={})
    await _send_q(cb.message, exam_id, seq, 0)


@router.callback_query(Exam.active, F.data == "ex:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Мок припинено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "⏹ Мок припинено достроково — <b>без оцінки</b> (повний мок рахується лише цілком).",
        reply_markup=to_menu_kb(),
    )


@router.callback_query(Exam.active, F.data.startswith("ex:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    exam_id, seq, pos, correct = data["exam_id"], data["seq"], data["pos"], data["correct"]
    chosen = await quiz.read_answer(cb, pos)
    if chosen is None:
        return
    sec, idx = seq[pos]
    it = content.exam_items(exam_id, sec)[idx]
    if chosen == it.correct:
        correct[sec] = correct.get(sec, 0) + 1
    else:  # режим іспиту — вердикт не показуємо, лише в колоду
        await mistakes.add(cb.from_user.id, sec, it.question, list(it.options), it.correct, it.explain)

    pos += 1
    await state.update_data(pos=pos, correct=correct)
    await cb.answer()
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    if pos < len(seq):
        await _send_q(cb.message, exam_id, seq, pos)
    else:
        await _finalize(cb.message, cb.from_user.id, state, seq, correct)


async def _finalize(
    message: Message, user_id: int, state: FSMContext, seq: list, correct: dict
) -> None:
    await state.clear()
    sections = [s for s in _LABEL if any(x[0] == s for x in seq)]  # секції цього моку
    totals = {s: sum(1 for x in seq if x[0] == s) for s in sections}
    lines = ["🏁 <b>Повний мок — результат</b>\n"]
    all_pass = True
    for sec in sections:
        got, tot = correct.get(sec, 0), totals[sec]
        pct = round(got / tot * 100) if tot else 0
        await user_state.update_readiness(user_id, sec, pct)
        await progress.record_mock_pass(user_id, sec, pct)
        if pct < 50:
            all_pass = False
        lines.append(f"{_LABEL[sec]}: <b>{got}/{tot}</b> ({pct}%) · {exam_scale.module_line(sec, pct)}")

    verdict = (
        "🏆 <b>Усі секції — вище порога!</b> Так тримати — і продуктивні модулі не забувай."
        if all_pass
        else "💪 Є секції нижче 50% — попрацюй над ними (див. 🧯 помилки) і повтори мок."
    )
    lines.append(f"\n{verdict}\n<i>Письмо й мовлення — окремо (/pisanie, /mowienie).</i>")
    await message.answer("\n".join(lines), reply_markup=menu_kb())
    if c := await goals.pop_celebration(user_id):
        await message.answer(c)
