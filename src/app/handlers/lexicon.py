"""Вільний словник за темами: мікро-навчання будь-де (флеш-картки, легше→важче).

Пресінгу немає: не рухає готовність/ціль. «➕ У мій словник» додає слово в SRS
(потім у /powtorki). 🔊 — вимова (спільний say-хендлер).
"""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.integrations import tts
from app.services import clock, lexicon, tts_say, vocab

router = Router()


class Lexicon(StatesGroup):
    browsing = State()


def _topics_kb() -> object:
    kb = InlineKeyboardBuilder()
    for key, lbl in lexicon.TOPICS:
        kb.button(text=lbl, callback_data=f"lex:t:{key}")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


async def _send_topics(message: Message) -> None:
    await message.answer(
        "📚 <b>Вільний словник</b> — вчи слова коли є хвилинка (у черзі, на лавці…).\n"
        "Обери тему (слова йдуть від найлегших до найважчих):",
        reply_markup=_topics_kb(),
    )


@router.message(Command("slownik"))
async def cmd_lexicon(message: Message) -> None:
    await _send_topics(message)


@router.callback_query(F.data == "lex:topics")
async def cb_topics(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await _send_topics(cb.message)


@router.callback_query(F.data.startswith("lex:t:"))
async def cb_topic(cb: CallbackQuery, state: FSMContext) -> None:
    topic = cb.data.split(":", 2)[2]
    await cb.answer()
    status = await cb.message.answer("⏳ Готую слова теми…")
    words = await lexicon.words_for(topic)
    if not words:
        await status.edit_text(
            "😔 Не вдалося завантажити слова. Спробуй пізніше.", reply_markup=_topics_kb()
        )
        return
    await state.set_state(Lexicon.browsing)
    await state.update_data(topic=topic, words=[w.__dict__ for w in words], idx=0)
    await _render_card(status, state, reveal=False)


async def _render_card(msg: Message, state: FSMContext, reveal: bool) -> None:
    await tts_say.forget_voice(msg.bot, msg.chat.id)  # прибрати голосове попереднього слова
    data = await state.get_data()
    words, idx, topic = data["words"], data["idx"], data["topic"]
    w = words[idx]
    stars = "★" * w["level"] + "☆" * (3 - w["level"])
    head = f"📚 <b>{lexicon.label(topic)}</b> · {idx + 1}/{len(words)} · {stars}"
    kb = InlineKeyboardBuilder()
    if tts.available():
        kb.button(text="🔊 Вимова", callback_data=f"say:{await tts_say.stash(w['pl'])}")
    if reveal:
        body = f"🇵🇱 <b>{html.escape(w['pl'])}</b> — {html.escape(w['ua'])}"
        if w["example"]:
            body += f"\n📌 <i>{html.escape(w['example'])}</i>"
        body += "\n\nЗнаєш це слово? <b>➕ Додай у словник</b>, щоб повторити пізніше, або <b>➡️ Далі</b>."
        kb.button(text="➕ У мій словник", callback_data="lex:add")
        kb.button(text="➡️ Далі", callback_data="lex:next")
    else:
        body = (
            f"🇵🇱 <b>{html.escape(w['pl'])}</b>\n\n"
            "🧠 Згадай переклад у голові, послухай вимову — тоді тисни "
            "<b>👁 Показати переклад</b>, щоб перевірити себе."
        )
        kb.button(text="👁 Показати переклад", callback_data="lex:show")
        kb.button(text="➡️ Далі", callback_data="lex:next")
    kb.button(text="⬅️ Теми", callback_data="lex:topics")
    kb.adjust(1)
    await msg.edit_text(f"{head}\n\n{body}", reply_markup=kb.as_markup())


@router.callback_query(Lexicon.browsing, F.data == "lex:show")
async def cb_show(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _render_card(cb.message, state, reveal=True)


async def _advance(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    idx = data["idx"] + 1
    if idx >= len(data["words"]):
        await state.clear()
        kb = InlineKeyboardBuilder()
        kb.button(text="🔁 Спочатку", callback_data=f"lex:t:{data['topic']}")
        kb.button(text="⬅️ Теми", callback_data="lex:topics")
        kb.button(text="⬅️ Меню", callback_data="menu:home")
        kb.adjust(1)
        await cb.message.edit_text(
            "🎉 <b>Тему пройдено!</b> Додані слова чекають на тебе у /powtorki 🔁",
            reply_markup=kb.as_markup(),
        )
        return
    await state.update_data(idx=idx)
    await _render_card(cb.message, state, reveal=False)


@router.callback_query(Lexicon.browsing, F.data == "lex:next")
async def cb_next(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _advance(cb, state)


@router.callback_query(Lexicon.browsing, F.data == "lex:add")
async def cb_add(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    w = data["words"][data["idx"]]
    added = await vocab.add(cb.from_user.id, w["pl"], w["ua"], clock.today_local())
    await cb.answer("Додано в словник ✅" if added else "Вже у твоєму словнику 🙂")
    await _advance(cb, state)


@router.callback_query(F.data == "lex:open")  # вхід із меню
async def cb_open(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await _send_topics(cb.message)
