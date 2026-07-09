"""Інтервальне повторення слів (SRS): показ слова → самооцінка → оновлення коробки."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import menu_kb, review_grade_kb, to_menu_kb
from app.integrations import tts
from app.services import clock, goals, pollquiz, tts_say, vocab

router = Router()

SESSION_CAP = 20  # максимум слів за одну сесію


class Review(StatesGroup):
    active = State()


async def _send_word(message: Message, pl: str, n: int, total: int) -> None:
    kb = InlineKeyboardBuilder()
    if tts.available():  # 🔊 послухати вимову слова
        kb.button(text="🔊 Послухати", callback_data=f"say:{await tts_say.stash(pl)}")
    kb.button(text="👁 Показати переклад", callback_data="rv:show")
    kb.adjust(1)
    await message.answer(
        f"🔁 <b>Повторення {n}/{total}</b>\n\n"
        f"🇵🇱 <b>{html.escape(pl)}</b>\n\nЗгадай переклад 👇",
        reply_markup=kb.as_markup(),
    )


async def _start(message: Message, user_id: int, state: FSMContext) -> None:
    today = clock.today_local()
    await vocab.seed_if_empty(user_id, today)
    items = await vocab.due(user_id, today)
    if not items:
        await message.answer(
            "🎉 Слів на повторення сьогодні немає. Повертайся завтра або зроби урок!",
            reply_markup=menu_kb(),
        )
        return
    due_pairs = [(it.pl, it.uk) for it in items][:SESSION_CAP]
    pool = await vocab.all_pairs(user_id)
    quiz = vocab.quiz_items(due_pairs, pool)
    if quiz and pollquiz.fits(quiz):  # вікторина «обери переклад» (нативні quiz-poll)
        await message.answer(
            f"🔁 <b>Повторення</b> — {len(quiz)} слів. Обери правильний переклад у quiz нижче 👇"
        )
        await pollquiz.start(
            message.bot, chat_id=message.chat.id, user_id=user_id, kind="srs",
            items=quiz, title="🔁 Повторення",
        )
        return

    # fallback: старий flashcard (замало слів для дистракторів)
    words = [pl for pl, _ in due_pairs]
    await state.set_state(Review.active)
    await state.update_data(words=words, idx=0, known=0)
    await _send_word(message, words[0], 1, len(words))


@router.message(Command("powtorki"))
async def cmd_review(message: Message, state: FSMContext) -> None:
    await _start(message, message.from_user.id, state)


@router.callback_query(F.data == "review:start")
async def cb_review(cb: CallbackQuery, state: FSMContext) -> None:
    await _start(cb.message, cb.from_user.id, state)
    await cb.answer()


@router.callback_query(Review.active, F.data == "rv:show")
async def cb_show(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    pl = data["words"][data["idx"]]
    item = await vocab.get(cb.from_user.id, pl)
    uk = item.uk if item else "—"
    await cb.message.edit_text(
        f"🇵🇱 <b>{html.escape(pl)}</b> — {html.escape(uk)}\n\nЗнав?",
        reply_markup=review_grade_kb(),
    )
    await cb.answer()


@router.callback_query(Review.active, F.data.in_({"rv:ok", "rv:no"}))
async def cb_grade(cb: CallbackQuery, state: FSMContext) -> None:
    correct = cb.data == "rv:ok"
    data = await state.get_data()
    words = data["words"]
    idx = data["idx"]
    known = data["known"] + (1 if correct else 0)

    pl = words[idx]
    await vocab.review(cb.from_user.id, pl, correct, clock.today_local())
    await cb.message.edit_text(
        f"🇵🇱 <b>{html.escape(pl)}</b> — {'✅ знав' if correct else '❌ повторимо скоро'}"
    )
    await cb.answer()

    idx += 1
    await state.update_data(idx=idx, known=known)
    if idx < len(words):
        await _send_word(cb.message, words[idx], idx + 1, len(words))
    else:
        await state.clear()
        await goals.add(cb.from_user.id, goals.REVIEW_MIN, goals.XP_REVIEW, kind="review")
        await cb.message.answer(
            f"🏁 <b>Готово!</b> Повторено {len(words)} слів, знав {known}. "
            "Слова повернуться за графіком SRS. 🔥",
            reply_markup=to_menu_kb(),
        )
        if c := await goals.pop_celebration(cb.from_user.id):
            await cb.message.answer(c)
