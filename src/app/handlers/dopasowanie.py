"""Зіставлення (dopasowanie) — офіційний тип завдання Czytanie Zad III/IV.

Вставити фрагменти в текст або добрати заголовок до абзацу. Опорні фрагменти
показуємо ОДИН раз (список A–H), далі по одному пропуску з літерними кнопками +
миттєвий вердикт (тренувальний режим). Це РЕАЛЬНЕ екзам-завдання → рухає готовність
(на відміну від керованої практики). У повний мок /egzamin інтегрується окремо.
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
from app.bot.keyboards import match_kb, menu_kb_for, to_menu_kb
from app.bot.ui import emph
from app.services import goals
from app.services import state as user_state

_SEP = "➖➖➖➖➖"

router = Router()

_LABEL = {"czytanie": "📖 Читання", "gramatyka": "🔤 Граматика"}


class Match(StatesGroup):
    active = State()


async def _intro(message: Message) -> None:
    tasks = content.all_match_tasks()
    if not tasks:
        await message.answer("Завдання на зіставлення поки недоступні.", reply_markup=to_menu_kb())
        return
    b = InlineKeyboardBuilder()
    for i, t in enumerate(tasks):
        b.button(text=t.title, callback_data=f"match:begin:{i}")
    b.button(text="⬅️ Меню", callback_data="menu:home")
    b.adjust(1)
    await message.answer(
        "🧩 <b>Зіставлення (dopasowanie)</b>\n"
        "Офіційний тип завдання: вставити фрагменти в текст або добрати заголовки. "
        "Фрагменти показую списком (A, B, C…), ти обираєш літеру на кожен пропуск.\n\n"
        "Обери завдання:",
        reply_markup=b.as_markup(),
    )


def _frag_block(title: str, intro: str, options: list[str]) -> str:
    """Шапка «дошки»: заголовок + інтро + список фрагментів (референс завжди зверху)."""
    opts = "\n".join(f"<b>{chr(65 + i)})</b> {html.escape(o)}" for i, o in enumerate(options))
    return f"🧩 <b>{html.escape(title)}</b>\n\n{intro}\n\n🔤 <b>Фрагменти:</b>\n{opts}"


def _verdict_line(pos: int, chosen: int, correct: int, options: list[str], explain: str) -> str:
    """Короткий вердикт попереднього пропуску (лишається у «дошці» над наступним питанням)."""
    cl = chr(65 + correct)
    if chosen == correct:
        head = f"✅ Пропуск {pos + 1}: <b>правильно</b> ({cl})"
    else:
        yl = chr(65 + chosen) if 0 <= chosen < len(options) else "—"
        head = f"❌ Пропуск {pos + 1}: ти обрав {yl}, правильно <b>{cl}</b>"
    return head + (f"\n💡 {emph(explain)}" if explain else "")


def _board(title: str, intro: str, options: list[str], prompts: list[str], pos: int, verdict: str) -> str:
    """Повний текст «дошки»: фрагменти + (опц.) вердикт попереднього + поточне питання.

    Уся вправа — ОДНЕ повідомлення, що редагується на місці: немає окремого питання
    «під згином», чат не засмічується, кнопки лишаються там само між пропусками.
    """
    s = _frag_block(title, intro, options)
    if verdict:
        s += f"\n\n{_SEP}\n{verdict}"
    s += (
        f"\n\n{_SEP}\n🧩 Пропуск <b>{pos + 1}/{len(prompts)}</b>\n\n"
        f"{html.escape(prompts[pos])}\n\nОбери фрагмент (літера):"
    )
    return s


@router.message(Command("dopasowanie"))
async def cmd_match(message: Message) -> None:
    await _intro(message)


@router.callback_query(F.data == "match:open")
async def cb_open(cb: CallbackQuery) -> None:
    await cb.answer()
    await _intro(cb.message)


@router.callback_query(F.data.startswith("match:begin:"))
async def cb_begin(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    idx = int(cb.data.split(":")[2])
    tasks = content.all_match_tasks()
    if idx >= len(tasks):
        await cb.message.answer("Завдання недоступне.", reply_markup=to_menu_kb())
        return
    t = tasks[idx]
    await state.set_state(Match.active)
    await state.update_data(
        section=t.section, title=t.title, intro=t.intro,
        options=list(t.options), prompts=list(t.prompts),
        key=list(t.key), explains=list(t.explain), pos=0, correct=0,
    )
    # уся вправа — ОДНЕ повідомлення-«дошка» (фрагменти + питання), редагується на місці
    await cb.message.answer(
        _board(t.title, t.intro, t.options, t.prompts, 0, ""),
        reply_markup=match_kb(len(t.options), 0),
    )


@router.callback_query(Match.active, F.data == "ma:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "⏹ Зіставлення завершено — <b>без оцінки</b> (готовність рухає лише пройдене повністю).",
        reply_markup=await menu_kb_for(cb.from_user.id),
    )


@router.callback_query(Match.active, F.data.startswith("ma:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    prompts, options, key, explains = (
        data["prompts"], data["options"], data["key"], data["explains"],
    )
    pos, correct, section = data["pos"], data["correct"], data["section"]
    title, intro = data["title"], data["intro"]

    chosen = await quiz.read_answer(cb, pos)
    if chosen is None:  # стале/дубль/зіпсовано
        return

    ok = chosen == key[pos]
    if ok:
        correct += 1
    await cb.answer("✔️" if ok else "❌")
    verdict = _verdict_line(pos, chosen, key[pos], options, explains[pos])
    pos += 1
    await state.update_data(pos=pos, correct=correct)
    if pos < len(prompts):  # редагуємо ТУ САМУ дошку → наступне питання (без нового повідомлення)
        with suppress(Exception):
            await cb.message.edit_text(
                _board(title, intro, options, prompts, pos, verdict),
                reply_markup=match_kb(len(options), pos),
            )
    else:
        with suppress(Exception):
            await cb.message.edit_text(
                _frag_block(title, intro, options) + f"\n\n{_SEP}\n{verdict}\n\n✅ Усі пропуски пройдено.",
                reply_markup=None,
            )
        await _finalize(cb.message, cb.from_user.id, state, correct, len(prompts), section)


async def _finalize(
    message: Message, user_id: int, state: FSMContext, correct: int, total: int, section: str
) -> None:
    await state.clear()
    score = round(correct / total * 100) if total else 0
    await user_state.update_readiness(user_id, section, score)  # рухає готовність + час/XP
    emoji = "🎉" if score >= 80 else "👍" if score >= 50 else "💪"
    await message.answer(
        f"{emoji} <b>Зіставлення: {correct}/{total} ({score}%)</b>\n"
        f"Готовність {_LABEL.get(section, section)} оновлено.",
        reply_markup=(await menu_kb_for(user_id)) if score >= 50 else to_menu_kb(),
    )
    if c := await goals.pop_celebration(user_id):
        await message.answer(c)
