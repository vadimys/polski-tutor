"""Обробник відповідей на нативні quiz-poll (спільний для всіх poll-вправ)."""

from __future__ import annotations

from aiogram import Bot, Router
from aiogram.types import PollAnswer

from app.bot.keyboards import menu_kb, to_menu_kb
from app.domain.models import MODULE_LABELS, Module
from app.services import clock, pollquiz, vocab
from app.services import state as user_state

router = Router()


@router.poll_answer()
async def on_poll_answer(poll_answer: PollAnswer, bot: Bot) -> None:
    session = await pollquiz.pop(poll_answer.poll_id)
    if session is None:
        return  # стара/чужа опитувалка

    idx = session["idx"]
    item = session["items"][idx]
    chosen = poll_answer.option_ids[0] if poll_answer.option_ids else -1
    ok = chosen == int(item["correct"])

    if session["kind"] == "srs" and item.get("key"):  # повторення слів → оновити SRS
        await vocab.review(session["user_id"], item["key"], ok, clock.today_local())
    if ok:
        session["correct"] += 1

    session["idx"] = idx + 1
    if session["idx"] < len(session["items"]):
        await pollquiz.send_item(bot, session)
        return

    # фінал
    correct, total = session["correct"], len(session["items"])
    pct = round(correct / total * 100) if total else 0
    chat_id = session["chat_id"]
    if session["kind"] == "readiness" and session.get("module"):
        await user_state.update_readiness(session["user_id"], session["module"], pct)
        label = MODULE_LABELS[Module(session["module"])]
        emoji = "🎉" if pct >= 80 else "👍" if pct >= 50 else "💪"
        await bot.send_message(
            chat_id,
            f"{emoji} <b>{session.get('title') or 'Результат'}: {correct}/{total} ({pct}%)</b>\n"
            f"Готовність {label} оновлено.",
            reply_markup=menu_kb() if pct >= 50 else to_menu_kb(),
        )
    else:
        await bot.send_message(
            chat_id,
            f"🔁 <b>Повторення: {correct}/{total} правильних.</b> Так тримати! 💪",
            reply_markup=to_menu_kb(),
        )
