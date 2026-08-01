"""«🗣 Розмова з екзаменатором» — голосовий діалоговий симулятор Mówienie (Zad3).

FSM голос-по-колу: режим → сценарій → (списання квоти) → репліка екзаменатора голосом →
учень відповідає голосом → STT (Groq→локальний) → наступна репліка → … → фінальний бал
за офіц. рубрикою. Turn-based (Telegram не вміє realtime), Haiku веде діалог, Sonnet оцінює.
Гейт вартості — sim_quota (тижнева) + стеля MAX_TURNS; НЕ через limits.allow_ai (то дрилі).
"""

from __future__ import annotations

import html
import logging
import os
import tempfile

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import menu_kb_for, to_menu_kb
from app.domain.models import Module
from app.integrations import speech
from app.services import examiner, goals, sim_quota, tts_say, uxlock
from app.services import state as user_state

logger = logging.getLogger(__name__)
router = Router()

MAX_VOICE_SEC = 180
MAX_VOICE_BYTES = 10 * 1024 * 1024

_MODE_LABEL = {"exam": "📝 Іспит", "practice": "🎓 Тренування"}


class Rozmowa(StatesGroup):
    talking = State()


# ─────────────────────────── клавіатури ───────────────────────────
def _mode_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Іспит (без підказок)", callback_data="examiner:mode:exam")],
        [InlineKeyboardButton(text="🎓 Тренування (з підказками)", callback_data="examiner:mode:practice")],
        [InlineKeyboardButton(text="⬅️ У меню", callback_data="examiner:cancel")],
    ])


def _scenario_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for sc in examiner.SCENARIOS:
        reg = "🏛" if sc.register == "oficjalny" else "😊"
        kb.button(text=f"{reg} {sc.title}", callback_data=f"examiner:sc:{sc.id}")
    kb.button(text="🎲 Випадковий", callback_data="examiner:sc:random")
    kb.button(text="⬅️ У меню", callback_data="examiner:cancel")
    kb.adjust(1)
    return kb.as_markup()


def _again_kb(remaining: int) -> InlineKeyboardMarkup:
    rows = []
    if remaining > 0:
        rows.append([InlineKeyboardButton(text="🔁 Ще одна розмова", callback_data="examiner:start")])
    rows.append([InlineKeyboardButton(text="⬅️ У меню", callback_data="menu:home")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ─────────────────────────── вхід ───────────────────────────
async def _open(message: Message, uid: int) -> None:
    left = await sim_quota.remaining(uid)
    if left <= 0:
        from app.services import billing

        extra = (
            "\n\n💎 З підпискою — 3 розмови на тиждень. /subskrypcja"
            if not await billing.has_payments(uid)
            else "\n\nНаступного тижня квота оновиться 🙂"
        )
        await message.answer(
            "🗣 <b>Розмова з екзаменатором</b>\n\nНа цей тиждень ліміт розмов вичерпано." + extra,
            reply_markup=to_menu_kb(),
        )
        return
    await message.answer(
        "🗣 <b>Розмова з екзаменатором</b>\n\n"
        "Змоделюємо усну частину іспиту (Zadanie 3): ти говориш голосом, я граю "
        "співрозмовника й реагую як на справжньому іспиті. Наприкінці — бал за офіційними "
        "критеріями.\n\n"
        f"Розмов цього тижня лишилось: <b>{left}</b>.\n\nОбери режим:",
        reply_markup=_mode_kb(),
    )


@router.message(Command("rozmowa"))
async def cmd_rozmowa(message: Message, state: FSMContext) -> None:
    await state.clear()
    await _open(message, message.from_user.id)


@router.callback_query(F.data == "examiner:start")
async def cb_start(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await _open(cb.message, cb.from_user.id)
    await cb.answer()


@router.callback_query(F.data == "examiner:cancel")
async def cb_cancel(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.message.edit_text("Гаразд, повернув у меню.", reply_markup=await menu_kb_for(cb.from_user.id))
    await cb.answer()


@router.callback_query(F.data.startswith("examiner:mode:"))
async def cb_mode(cb: CallbackQuery, state: FSMContext) -> None:
    mode = cb.data.split(":")[-1]
    await state.update_data(mode=mode)
    await cb.message.edit_text(
        f"Режим: <b>{_MODE_LABEL.get(mode, mode)}</b>\n\nОбери ситуацію:",
        reply_markup=_scenario_kb(),
    )
    await cb.answer()


@router.callback_query(F.data.startswith("examiner:sc:"))
async def cb_scenario(cb: CallbackQuery, state: FSMContext) -> None:
    import random

    sid = cb.data.split(":")[-1]
    sc = random.choice(examiner.SCENARIOS) if sid == "random" else examiner.scenario_by_id(sid)
    if sc is None:
        await cb.answer("Ситуація загубилась", show_alert=True)
        return
    uid = cb.from_user.id
    if await sim_quota.remaining(uid) <= 0:  # повторна перевірка (могли витратити паралельно)
        await cb.answer("Ліміт розмов на тиждень вичерпано", show_alert=True)
        return
    await sim_quota.consume(uid)  # списуємо ОДНУ розмову на старті (не за репліку)
    data = await state.get_data()
    mode = data.get("mode", "exam")
    await state.set_data({"mode": mode, "sid": sc.id, "history": [["egzaminator", sc.opening_pl]]})
    await state.set_state(Rozmowa.talking)

    reg = "офіційний (Pan/Pani)" if sc.register == "oficjalny" else "неофіційний (ty)"
    await cb.message.edit_text(
        f"🎬 <b>Ситуація</b>\n{html.escape(sc.setup_uk)}\n\n"
        f"🎯 <b>Твоя мета:</b> {html.escape(sc.goal_uk)}\n"
        f"🗣 <b>Регістр:</b> {reg}\n\n"
        "Я вже дзвоню/починаю — <b>послухай і відповідай голосом</b> 🎤\n"
        "<i>Порада: говори 20–60 секунд, як у справжній розмові.</i>"
    )
    await tts_say.send_voice(cb.message.bot, cb.message.chat.id, sc.opening_pl, caption=f"🗣 {sc.opening_pl}")
    await cb.answer()


# ─────────────────────────── цикл розмови ───────────────────────────
async def _learner_turn(message: Message, state: FSMContext, utterance: str) -> None:
    data = await state.get_data()
    sc = examiner.scenario_by_id(data.get("sid", ""))
    if sc is None:
        await state.clear()
        await message.answer("Розмова загубилась — почнімо заново.", reply_markup=to_menu_kb())
        return
    mode = data.get("mode", "exam")
    history: list[list[str]] = data.get("history", [])
    history.append(["uczen", utterance])

    tuples = [(w, t) for w, t in history]
    async with uxlock.typing(message.bot, message.chat.id):
        reply, done = await examiner.next_reply(sc, mode, tuples)
    if reply:
        history.append(["egzaminator", reply])
        await tts_say.send_voice(message.bot, message.chat.id, reply, caption=f"🗣 {reply}")

    if done:
        await _finish(message, state, sc, history)
    else:
        await state.update_data(history=history)


async def _finish(message: Message, state: FSMContext, sc, history: list[list[str]]) -> None:
    uid = message.from_user.id
    await state.clear()
    tuples = [(w, t) for w, t in history]
    async with uxlock.typing(message.bot, message.chat.id):
        verdict = await examiner.grade(sc, tuples)
    left = await sim_quota.remaining(uid)
    if verdict is None:
        await message.answer(
            "Розмову завершено 👏 AI-оцінка тимчасово недоступна — але практика зарахована.",
            reply_markup=_again_kb(left),
        )
        return
    cel = "✅ досягнуто" if verdict.cel_osiagniety else "⚠️ не повністю"
    reg = "✅ доречний" if verdict.rejestr_ok else "⚠️ подекуди недоречний"
    await user_state.update_readiness(uid, Module.MOWIENIE.value, verdict.pct)
    await message.answer(
        "🏁 <b>Розмову завершено!</b>\n\n"
        "📊 <b>Офіційні критерії</b> (оцінюване з тексту):\n"
        f"• Wykonanie zadania: <b>{verdict.wykonanie}</b>/6\n"
        f"• Gramatyka: <b>{verdict.gramatyka}</b>/8\n"
        f"• Słownictwo i styl: <b>{verdict.slownictwo}</b>/8\n"
        f"• Комунікативна мета: {cel}\n"
        f"• Регістр: {reg}\n"
        "• Poprawność fonetyczna i płynność: лише на аудіо (чесно не оцінюємо з тексту)\n\n"
        f"💬 {html.escape(verdict.feedback)}\n\n"
        f"Розмов цього тижня лишилось: <b>{left}</b>.",
        reply_markup=_again_kb(left),
    )
    if c := await goals.pop_celebration(uid):
        await message.answer(c)


@router.message(Rozmowa.talking, F.voice)
async def on_voice(message: Message, state: FSMContext) -> None:
    if (message.voice.duration or 0) > MAX_VOICE_SEC:
        await message.answer(f"🎤 Голосове задовге (максимум {MAX_VOICE_SEC} с). Запиши коротше 🙂")
        return
    if (message.voice.file_size or 0) > MAX_VOICE_BYTES:
        await message.answer("🎤 Файл завеликий. Запиши коротше голосове.")
        return
    fd, path = tempfile.mkstemp(suffix=".oga")
    os.close(fd)
    try:
        await message.bot.download(message.voice, destination=path)
        async with uxlock.typing(message.bot, message.chat.id):
            transcript = await speech.transcribe(path)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
    if not transcript:
        await message.answer("Не вдалося розпізнати голос 😕 Спробуй ще раз, ближче до мікрофона.")
        return
    await message.answer(f"📝 <i>Почув:</i> «{html.escape(transcript)}»")
    await _learner_turn(message, state, transcript)


@router.message(Rozmowa.talking, F.text, ~F.text.startswith("/"))
async def on_text(message: Message, state: FSMContext) -> None:
    # приймаємо й текст (без мікрофона/для тесту), але це усний іспит — нагадуємо про голос
    await message.answer("🎤 <i>Краще голосом (це усний іспит), але приймаю й текст.</i>")
    await _learner_turn(message, state, message.text.strip())
