"""Модуль аудіювання (Słuchanie): офіц. запис (piper TTS) → офіц. питання."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from app.bot import quiz
from app.bot.keyboards import listen_kb, menu_kb, to_menu_kb
from app.domain.models import Module
from app.integrations import tts
from app.services import listening
from app.services import state as user_state

router = Router()


class Listening(StatesGroup):
    active = State()


async def _play(message: Message, audio: str) -> None:
    data = await tts.synthesize(audio)
    if data:
        await message.answer_voice(
            BufferedInputFile(data, filename="sluchanie.ogg"),
            caption="🎧 Прослухай (можна кілька разів).",
        )
    else:
        await message.answer(f"🔇 (аудіо недоступне — прочитай)\n\n<i>{html.escape(audio)}</i>")


async def _send_q(message: Message, ex: listening.Exercise, seg: int, q: int, gstep: int) -> None:
    question = ex.segments[seg].questions[q]
    total = listening.total_questions(ex)
    await message.answer(
        f"<b>Питання {gstep + 1}/{total}</b>\n\n{html.escape(question.text)}",
        reply_markup=listen_kb(question.options, gstep),
    )


async def _start(message: Message, state: FSMContext) -> None:
    ex = listening.pick()
    await state.set_state(Listening.active)
    await state.update_data(ex_id=ex.id, seg=0, q=0, correct=0, gstep=0)
    await message.answer(
        f"🎧 <b>Аудіювання — {html.escape(ex.title)}</b> ({listening.SOURCE})\n\n{ex.intro}"
    )
    await _play(message, ex.segments[0].audio)
    await _send_q(message, ex, 0, 0, 0)


@router.message(Command("sluchanie"))
async def cmd_listening(message: Message, state: FSMContext) -> None:
    await _start(message, state)


@router.callback_query(F.data == "listening:start")
async def cb_listening(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _start(cb.message, state)


@router.callback_query(Listening.active, F.data.startswith("ls:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    ex = listening.by_id(data["ex_id"])
    seg, q, correct, gstep = data["seg"], data["q"], data["correct"], data["gstep"]
    if ex is None:
        await state.clear()
        await cb.message.answer("Запис загубився — почнімо заново.", reply_markup=menu_kb())
        await cb.answer()
        return

    chosen = await quiz.read_answer(cb, gstep)
    if chosen is None:  # стале/дубль/зіпсовано — уже оброблено
        return

    question = ex.segments[seg].questions[q]
    if await quiz.show_verdict(
        cb, chosen, question.correct, question.options, question.text, question.explain
    ):
        correct += 1

    q += 1
    gstep += 1
    if q < len(ex.segments[seg].questions):
        await state.update_data(q=q, correct=correct, gstep=gstep)
        await _send_q(cb.message, ex, seg, q, gstep)
        return
    seg += 1
    if seg < len(ex.segments):
        await state.update_data(seg=seg, q=0, correct=correct, gstep=gstep)
        await _play(cb.message, ex.segments[seg].audio)
        await _send_q(cb.message, ex, seg, 0, gstep)
    else:
        await _finalize(cb.message, cb.from_user.id, state, correct, listening.total_questions(ex))


async def _finalize(
    message: Message, user_id: int, state: FSMContext, correct: int, total: int
) -> None:
    await state.clear()
    pct = round(correct / total * 100) if total else 0
    await user_state.update_readiness(user_id, Module.SLUCHANIE.value, pct)
    emoji = "🎉" if pct >= 80 else "👍" if pct >= 50 else "💪"
    await message.answer(
        f"{emoji} <b>Аудіювання: {correct}/{total} ({pct}%)</b>\nГотовність Słuchanie оновлено.",
        reply_markup=menu_kb() if pct >= 50 else to_menu_kb(),
    )
