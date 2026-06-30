"""Модуль аудіювання (Słuchanie): TTS-аудіо → питання формату іспиту."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from app.bot.keyboards import listen_kb, menu_kb, to_menu_kb
from app.domain.models import Module
from app.integrations import tts
from app.services import listening
from app.services import state as user_state

router = Router()


class Listening(StatesGroup):
    active = State()


async def _send_question(message: Message, item: listening.ListeningItem, n: int) -> None:
    q = item.questions[n]
    await message.answer(
        f"<b>Питання {n + 1}/{len(item.questions)}</b>\n\n{html.escape(q.text)}",
        reply_markup=listen_kb(q.options),
    )


async def _start(message: Message, state: FSMContext) -> None:
    item = listening.pick()
    await message.answer("🎧 <b>Аудіювання</b> — готую запис…")
    audio = await tts.synthesize(item.text)
    if audio:
        await message.answer_voice(
            BufferedInputFile(audio, filename="sluchanie.ogg"),
            caption="🎧 Прослухай (можна кілька разів) і відповідай на питання.",
        )
    else:
        # фолбек: TTS недоступний → показуємо текст
        await message.answer(
            f"🔇 (аудіо недоступне — прочитай)\n\n<i>{html.escape(item.text)}</i>"
        )
    await state.set_state(Listening.active)
    await state.update_data(item_id=item.id, idx=0, correct=0)
    await _send_question(message, item, 0)


@router.message(Command("sluchanie"))
async def cmd_listening(message: Message, state: FSMContext) -> None:
    await _start(message, state)


@router.callback_query(F.data == "listening:start")
async def cb_listening(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _start(cb.message, state)


@router.callback_query(Listening.active, F.data.startswith("ls:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    chosen = int(cb.data.rsplit(":", 1)[1])
    data = await state.get_data()
    item = listening.by_id(data["item_id"])
    idx = data["idx"]
    correct = data["correct"]
    if item is None:
        await state.clear()
        await cb.message.answer("Запис загубився — почнімо заново.", reply_markup=menu_kb())
        await cb.answer()
        return

    q = item.questions[idx]
    ok = chosen == q.correct
    if ok:
        correct += 1
        verdict = "✔️ <b>Правильно!</b>"
    else:
        verdict = f"❌ Правильно: <b>{html.escape(q.options[q.correct])}</b>"
    await cb.message.edit_text(f"{html.escape(q.text)}\n\n{verdict}\n💡 {html.escape(q.explain)}")
    await cb.answer("✔️" if ok else "❌")

    idx += 1
    await state.update_data(idx=idx, correct=correct)
    if idx < len(item.questions):
        await _send_question(cb.message, item, idx)
    else:
        await _finalize(cb.message, cb.from_user.id, state, correct, len(item.questions))


async def _finalize(
    message: Message, user_id: int, state: FSMContext, correct: int, total: int
) -> None:
    await state.clear()
    score = round(correct / total * 100) if total else 0
    st = await user_state.load(user_id)
    old = st.readiness.get(Module.SLUCHANIE.value, score)
    st.readiness[Module.SLUCHANIE.value] = round((old + score) / 2)
    await user_state.save(st)
    emoji = "🎉" if score >= 80 else "👍" if score >= 50 else "💪"
    await message.answer(
        f"{emoji} <b>Аудіювання: {correct}/{total} ({score}%)</b>\nГотовність Słuchanie оновлено.",
        reply_markup=menu_kb() if score >= 50 else to_menu_kb(),
    )
