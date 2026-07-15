"""Модуль аудіювання (Słuchanie): офіц. запис (piper TTS) → офіц. питання (quiz-poll).

Питання — нативні quiz-poll; аудіо сегмента програється перед його першим питанням
(через pollquiz.send_item, поле 'audio'). Оцінювання — у спільному poll_answer-хендлері.
"""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.domain.models import Module
from app.services import listening, pollquiz, uxlock

router = Router()


async def _start(message: Message, user_id: int) -> None:
    # антидубль: доки готуємо вправу (синтез аудіо кілька секунд), другий старт ігноруємо
    if not await uxlock.acquire(f"listen:{user_id}", 40):
        await message.answer("⏳ Уже готую вправу — секунду…")
        return
    try:
        ex = listening.pick()
        items: list[dict] = []
        for seg in ex.segments:
            for qi, q in enumerate(seg.questions):
                item = {"q": q.text, "opts": list(q.options), "correct": q.correct, "explain": q.explain}
                if qi == 0:
                    item["audio"] = seg.audio  # програти запис перед першим питанням сегмента
                items.append(item)
        await message.answer(f"🎧 <b>Аудіювання — {ex.title}</b> ({listening.SOURCE})\n\n{ex.intro}")
        await pollquiz.start(
            message.bot, chat_id=message.chat.id, user_id=user_id, kind="readiness",
            items=items, module=Module.SLUCHANIE.value, title="🎧 Аудіювання",
        )
    finally:
        await uxlock.release(f"listen:{user_id}")


@router.message(Command("sluchanie"))
async def cmd_listening(message: Message) -> None:
    await _start(message, message.from_user.id)


@router.callback_query(F.data == "listening:start")
async def cb_listening(cb: CallbackQuery) -> None:
    await cb.answer()
    await _start(cb.message, cb.from_user.id)
