"""Відкриті завдання (трансформація) — офіційний тип Gramatyka Zad VI.

Студент перетворює речення текстом (обов'язково вживши задане слово). Однозначного
ключа нема → оцінює AI, ЗАЗЕМЛЕНА офіційним зразком (1 виклик на все завдання). Якщо
AI вимкнено/збій → self-check: показуємо офіц. зразки, готовність НЕ рухаємо (чесно).
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
from app.bot.keyboards import menu_kb_for, open_kb, to_menu_kb
from app.integrations import ai
from app.services import goals, limits, opencheck, uxlock
from app.services import state as user_state

router = Router()

_LABEL = {"czytanie": "📖 Читання", "gramatyka": "🔤 Граматика"}


class Open(StatesGroup):
    active = State()


async def _intro(message: Message) -> None:
    tasks = content.all_open_tasks()
    if not tasks:
        await message.answer("Відкриті завдання поки недоступні.", reply_markup=to_menu_kb())
        return
    b = InlineKeyboardBuilder()
    for i, t in enumerate(tasks):
        b.button(text=t.title, callback_data=f"open:begin:{i}")
    b.button(text="⬅️ Меню", callback_data="menu:home")
    b.adjust(1)
    await message.answer(
        "🔄 <b>Трансформація речень</b>\n"
        "Офіційний тип завдання: перепиши речення, зберігаючи сенс і вживши задане "
        "слово. Пишеш <b>текстом</b>; наприкінці — оцінка з поясненням.\n"
        "💡 Порада: вимкни автовиправлення/T9 у клавіатурі — воно псує польські слова.\n"
        "\nОбери завдання:",
        reply_markup=b.as_markup(),
    )


async def _send_prompt(
    message: Message, prompts: list[str], words: list[str], pos: int
) -> None:
    await message.answer(
        f"🔄 <b>Речення {pos + 1}/{len(prompts)}</b>\n\n"
        f"❓ {html.escape(prompts[pos])}\n\n"
        f"🔑 Обов'язково вжий: <b>{html.escape(words[pos])}</b>\n\n"
        "👇 <i>Напиши перетворене речення:</i>",
        reply_markup=open_kb(pos),
    )


@router.message(Command("transformacje"))
async def cmd_open(message: Message) -> None:
    await _intro(message)


@router.callback_query(F.data == "open:open")
async def cb_open(cb: CallbackQuery) -> None:
    await cb.answer()
    await _intro(cb.message)


@router.callback_query(F.data.startswith("open:begin:"))
async def cb_begin(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    idx = int(cb.data.split(":")[2])
    tasks = content.all_open_tasks()
    if idx >= len(tasks):
        await cb.message.answer("Завдання недоступне.", reply_markup=to_menu_kb())
        return
    t = tasks[idx]
    await state.set_state(Open.active)
    await state.update_data(
        section=t.section, title=t.title, prompts=list(t.prompts), words=list(t.words),
        models=[list(m) for m in t.models], pos=0, answers=[],
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="▶️ Розпочати", callback_data="open:go")
    kb.button(text="⬅️ Меню", callback_data="op:stop")
    kb.adjust(1)
    await cb.message.answer(
        f"🔄 <b>{html.escape(t.title)}</b>\n\n{t.intro}", reply_markup=kb.as_markup()
    )


@router.callback_query(Open.active, F.data == "open:go")
async def cb_go(cb: CallbackQuery, state: FSMContext) -> None:
    """Старт: прибрати кнопки з інтро → перше завдання (шлеться у відповідь на тап → скролиться)."""
    await cb.answer()
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    await _send_prompt(cb.message, data["prompts"], data["words"], 0)


@router.callback_query(Open.active, F.data == "op:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "⏹ Завдання завершено достроково — <b>без оцінки</b> (оцінюємо лише повністю).",
        reply_markup=await menu_kb_for(cb.from_user.id),
    )


async def _record(message: Message, user_id: int, state: FSMContext, answer: str) -> None:
    data = await state.get_data()
    answers = [*data["answers"], answer]
    pos = data["pos"] + 1
    await state.update_data(answers=answers, pos=pos)
    if pos < len(data["prompts"]):
        await _send_prompt(message, data["prompts"], data["words"], pos)
    else:
        await _finalize(message, user_id, state)


@router.callback_query(Open.active, F.data.startswith("op:skip:"))
async def cb_skip(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    if int(cb.data.split(":")[2]) != data["pos"]:  # стала кнопка / дубль
        await cb.answer("Це речення вже пройдено 🙂")
        return
    await cb.answer()
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await _record(cb.message, cb.from_user.id, state, "")


@router.message(Open.active, F.text)
async def on_answer(message: Message, state: FSMContext) -> None:
    txt = (message.text or "").strip()
    if len(txt) > 500:  # трансформація — одне речення
        await message.answer("Це має бути одне речення. Напиши коротше ✍️")
        return
    await _record(message, message.from_user.id, state, txt)


async def _finalize(message: Message, user_id: int, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    prompts, words, models, answers = (
        data["prompts"], data["words"], data["models"], data["answers"],
    )
    section, total = data["section"], len(prompts)

    graded = None
    if ai.enabled() and await limits.allow_ai(user_id):
        items = [
            {"n": i + 1, "original": prompts[i], "word": words[i],
             "models": models[i], "answer": answers[i]}
            for i in range(total)
        ]
        async with uxlock.typing(message.bot, message.chat.id):
            graded = await opencheck.grade(items)
        if graded is None:  # AI не спрацював — не палимо квоту
            await limits.refund_ai(user_id)

    if graded is not None:
        await _show_graded(message, user_id, prompts, models, answers, graded, section)
    else:
        await _show_selfcheck(message, prompts, models, answers)


async def _show_graded(
    message: Message, user_id: int, prompts: list[str], models: list[list[str]],
    answers: list[str], graded: list[dict], section: str,
) -> None:
    correct = sum(1 for g in graded if g["ok"])
    total = len(prompts)
    lines = ["🔄 <b>Результат (оцінка AI за офіц. зразком)</b>\n"]
    for i, g in enumerate(graded):
        mark = "✔️" if g["ok"] else "❌"
        ans = html.escape(answers[i]) if answers[i] else "<i>(порожньо)</i>"
        lines.append(
            f"{mark} <b>#{i + 1}</b> {ans}\n"
            f"✅ Зразок: <i>{html.escape(models[i][0])}</i>"
            + (f"\n💡 {html.escape(g['feedback'])}" if g["feedback"] else "")
        )
    score = round(correct / total * 100) if total else 0
    await user_state.update_readiness(user_id, section, score)  # рухає готовність + час/XP
    emoji = "🎉" if score >= 80 else "👍" if score >= 50 else "💪"
    lines.append(
        f"\n{emoji} <b>{correct}/{total} ({score}%)</b> · готовність "
        f"{_LABEL.get(section, section)} оновлено."
    )
    await message.answer(
        "\n\n".join(lines), reply_markup=(await menu_kb_for(user_id)) if score >= 50 else to_menu_kb()
    )
    if c := await goals.pop_celebration(user_id):
        await message.answer(c)


async def _show_selfcheck(
    message: Message, prompts: list[str], models: list[list[str]], answers: list[str]
) -> None:
    lines = ["🔄 <b>Самоперевірка</b> <i>(AI недоступний — порівняй сам)</i>\n"]
    for i in range(len(prompts)):
        ans = html.escape(answers[i]) if answers[i] else "<i>(порожньо)</i>"
        official = " / ".join(html.escape(m) for m in models[i])
        lines.append(f"<b>#{i + 1}</b> Твоя: {ans}\n✅ Зразок: <i>{official}</i>")
    lines.append(
        "\nℹ️ Це самоперевірка — <b>готовність не змінюємо</b>. Порівняй свої речення "
        "зі зразками (можливі й інші правильні варіанти)."
    )
    await message.answer("\n\n".join(lines), reply_markup=to_menu_kb())
