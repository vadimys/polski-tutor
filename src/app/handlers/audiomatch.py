"""Аудіо-зіставлення (przyporządkowanie) — офіц. тип Słuchanie, що НЕ лягає в
single-choice: кожен опис A–E стосується МНОЖИНИ мовців. Multi-select через
перемикачі осіб + звірка множин. Тренувальний режим (миттєвий вердикт) → рухає
готовність Słuchanie. Аудіо мовців — piper TTS (fallback транскрипт).
"""

from __future__ import annotations

import html
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import audiomatch_kb, menu_kb_for, to_menu_kb
from app.domain.models import Module
from app.integrations import tts
from app.services import goals, listening
from app.services import state as user_state

router = Router()


class AMatch(StatesGroup):
    active = State()


async def _play(message: Message, label: str, text: str) -> None:
    data = await tts.synthesize(text)
    if data:
        await message.answer_voice(
            BufferedInputFile(data, filename="osoba.ogg"), caption=f"🔊 <b>{label}</b>"
        )
    else:
        await message.answer(f"🔇 <b>{label}</b> <i>(аудіо недоступне — прочитай)</i>\n\n{html.escape(text)}")


async def _intro(message: Message) -> None:
    tasks = listening.MATCH_AUDIO
    if not tasks:
        await message.answer("Аудіо-зіставлення поки недоступні.", reply_markup=to_menu_kb())
        return
    b = InlineKeyboardBuilder()
    for m in tasks:
        b.button(text=m.title, callback_data=f"amatch:begin:{m.id}")
    b.button(text="⬅️ Меню", callback_data="menu:home")
    b.adjust(1)
    await message.answer(
        "🔗 <b>Аудіо-зіставлення (przyporządkowanie)</b>\n"
        "Офіц. тип аудіювання: слухаєш кількох мовців і зіставляєш кожен опис із тим, "
        "кого він стосується. Один опис може стосуватися <b>кількох осіб</b>.\n\nОбери завдання:",
        reply_markup=b.as_markup(),
    )


async def _send_prompt(message: Message, prompts: list[str], n_spk: int, pos: int) -> None:
    await message.answer(
        f"🔗 Опис <b>{pos + 1}/{len(prompts)}</b>\n\n{html.escape(prompts[pos])}\n\n"
        "<i>Кого це стосується? Познач усі номери, тоді «Готово».</i>",
        reply_markup=audiomatch_kb(n_spk, set(), pos),
    )


@router.message(Command("przyporzadkowanie"))
async def cmd_amatch(message: Message) -> None:
    await _intro(message)


@router.callback_query(F.data == "amatch:open")
async def cb_open(cb: CallbackQuery) -> None:
    await cb.answer()
    await _intro(cb.message)


@router.callback_query(F.data.startswith("amatch:begin:"))
async def cb_begin(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    mid = cb.data.split(":", 2)[2]
    m = listening.match_audio_by_id(mid)
    if not m:
        await cb.message.answer("Завдання недоступне.", reply_markup=to_menu_kb())
        return
    await state.set_state(AMatch.active)
    await state.update_data(
        prompts=list(m.prompts), key=[list(k) for k in m.key], explains=list(m.explain),
        n_spk=len(m.speakers), pos=0, correct=0, selected=[],
    )
    await cb.message.answer(f"🔗 <b>{html.escape(m.title)}</b>\n\n{m.intro}")
    for i, spk in enumerate(m.speakers):
        await _play(cb.message, f"Особа {i + 1}", spk)
    await _send_prompt(cb.message, m.prompts, len(m.speakers), 0)


@router.callback_query(AMatch.active, F.data == "am:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "⏹ Зіставлення завершено — <b>без оцінки</b> (готовність рухає лише пройдене повністю).",
        reply_markup=await menu_kb_for(cb.from_user.id),
    )


@router.callback_query(AMatch.active, F.data.startswith("am:tog:"))
async def cb_toggle(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    parts = (cb.data or "").split(":")
    if len(parts) != 4 or int(parts[2]) != data["pos"]:
        await cb.answer("Це вже пройдено 🙂")
        return
    i = int(parts[3])
    selected = listening.toggle_selection(data["selected"], i)
    await state.update_data(selected=selected)
    await cb.answer()
    with suppress(Exception):
        await cb.message.edit_reply_markup(
            reply_markup=audiomatch_kb(data["n_spk"], set(selected), data["pos"])
        )


@router.callback_query(AMatch.active, F.data.startswith("am:done:"))
async def cb_done(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    if int((cb.data or "am:done:0").split(":")[2]) != data["pos"]:
        await cb.answer("Це вже пройдено 🙂")
        return
    await cb.answer()
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)

    pos, prompts, key, explains = data["pos"], data["prompts"], data["key"], data["explains"]
    want = set(key[pos])
    ok = listening.match_audio_correct(data["selected"], key[pos])
    correct = data["correct"] + (1 if ok else 0)
    names = ", ".join(str(x + 1) for x in sorted(want)) or "—"
    head = "✅ <b>Правильно!</b>" if ok else f"❌ <b>Правильно: особа(и) {names}</b>"
    await cb.message.answer(f"{head}\n💡 {explains[pos]}")

    pos += 1
    await state.update_data(pos=pos, correct=correct, selected=[])
    if pos < len(prompts):
        await _send_prompt(cb.message, prompts, data["n_spk"], pos)
    else:
        await _finalize(cb.message, cb.from_user.id, state, correct, len(prompts))


async def _finalize(
    message: Message, user_id: int, state: FSMContext, correct: int, total: int
) -> None:
    await state.clear()
    score = round(correct / total * 100) if total else 0
    await user_state.update_readiness(user_id, Module.SLUCHANIE.value, score)
    emoji = "🎉" if score >= 80 else "👍" if score >= 50 else "💪"
    await message.answer(
        f"{emoji} <b>Аудіо-зіставлення: {correct}/{total} ({score}%)</b>\n"
        "Готовність 🎧 Аудіювання оновлено.",
        reply_markup=(await menu_kb_for(user_id)) if score >= 50 else to_menu_kb(),
    )
    if c := await goals.pop_celebration(user_id):
        await message.answer(c)
