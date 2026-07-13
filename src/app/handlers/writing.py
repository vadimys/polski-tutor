"""Модуль письма (Pisanie): офіційний набір (a+b) → фідбек за офіційною шкалою /30."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import cancel_kb, menu_kb_for, to_menu_kb
from app.domain.models import Module
from app.services import goals, guidance, limits, writing
from app.services import state as user_state

router = Router()

MIN_WORDS = 5  # захист від «.» замість тексту
MAX_CHARS = 4000  # захист від cost-abuse: обсяг B1 ~30–175 слів, 4000 символів — з великим запасом


class Writing(StatesGroup):
    await_a = State()
    await_b = State()


class GuidedW(StatesGroup):
    active = State()  # керована практика письма (офіційний лист крок-за-кроком)


async def _give_set(message: Message, state: FSMContext) -> None:
    ws = writing.pick_set()
    await state.set_state(Writing.await_a)
    await state.update_data(set_id=ws.id, text_a="")
    await message.answer(
        f"✍️ <b>Письмо — набір ({writing.SOURCE})</b>\n\n"
        f"Як на іспиті: <b>два завдання</b>, обидва з цього набору.\n\n"
        f"<b>Завдання a</b> ({ws.a.genre}, ~{ws.a.words} слів):\n{html.escape(ws.a.prompt)}\n\n"
        f"<b>Завдання b</b> ({ws.b.genre}, ~{ws.b.words} слів):\n{html.escape(ws.b.prompt)}"
    )
    a_req = writing.GENRE_REQ.get(ws.a.genre, "—")
    b_req = writing.GENRE_REQ.get(ws.b.genre, "—")
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Показати зразок", callback_data="guide:wr")
    kb.button(text="🪜 Пройти по кроках", callback_data="guidew:start")
    kb.button(text="🚫 Скасувати", callback_data="nav:cancel")
    kb.adjust(1)
    await message.answer(
        guidance.writing_instruction(ws.a.genre, a_req, ws.a.words, ws.b.genre, b_req, ws.b.words)
        + "\n\n💡 Порада: вимкни автовиправлення/T9 — воно псує польські слова."
        + "\n✍️ Спершу напиши польською <b>завдання a</b> одним повідомленням.",
        reply_markup=kb.as_markup(),
    )


@router.message(Command("pisanie"))
async def cmd_writing(message: Message, state: FSMContext) -> None:
    await _give_set(message, state)


@router.callback_query(F.data == "writing:start")
async def cb_writing(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _give_set(cb.message, state)


@router.callback_query(F.data == "guide:wr")
async def cb_example(cb: CallbackQuery) -> None:
    await cb.answer()
    await cb.message.answer(guidance.writing_example())


# --- Керована практика письма (офіційний лист крок-за-кроком) ---


@router.callback_query(F.data == "guidew:start")
async def cb_guided_start(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await state.set_state(GuidedW.active)
    await state.update_data(gw_step=0, gw_lines=[])
    await cb.message.answer(
        "🪜 <b>Керована практика — офіційний лист</b>\n"
        "Складемо лист по частинах, а потім виконаєш справжнє завдання на оцінку."
    )
    await cb.message.answer(guidance.writing_step(0), reply_markup=cancel_kb())


@router.message(GuidedW.active, F.text, ~F.text.startswith("/"))
async def on_guided_step(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    step = int(data.get("gw_step", 0))
    lines = list(data.get("gw_lines", []))
    if len(message.text.strip()) < 2:
        await message.answer("Напиши, будь ласка, цю частину польською 🙂", reply_markup=cancel_kb())
        return
    lines.append(message.text.strip())
    step += 1
    if step < guidance.WRITING_STEPS_N:
        await state.update_data(gw_step=step, gw_lines=lines)
        await message.answer("✅ Прийнято.")
        await message.answer(guidance.writing_step(step), reply_markup=cancel_kb())
        return

    await state.clear()
    letter = "\n".join(html.escape(ln) for ln in lines)
    kb = InlineKeyboardBuilder()
    kb.button(text="✍️ Виконати офіційне завдання й здати", callback_data="writing:start")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    await message.answer(
        "🎉 <b>Готово!</b> Ось твій лист із 4 частин:\n\n"
        f"{letter}\n\n"
        "ℹ️ Це <b>тренування</b> — у готовність не зараховується. Щоб підняти готовність — "
        "виконай <b>офіційне завдання</b> модуля Pisanie й здай на перевірку 👇",
        reply_markup=kb.as_markup(),
    )


@router.message(Writing.await_a, F.text, ~F.text.startswith("/"))
async def on_task_a(message: Message, state: FSMContext) -> None:
    if len(message.text.split()) < MIN_WORDS:
        await message.answer(
            "Напиши, будь ласка, повноцінний текст завдання a 🙂", reply_markup=cancel_kb()
        )
        return
    if len(message.text) > MAX_CHARS:
        await message.answer(
            f"Текст задовгий (>{MAX_CHARS} символів). На іспиті B1 обсяг невеликий — скороти 🙂",
            reply_markup=cancel_kb(),
        )
        return
    await state.update_data(text_a=message.text)
    await state.set_state(Writing.await_b)
    data = await state.get_data()
    ws = writing.set_by_id(data["set_id"])
    b = ws.b if ws else None
    hint = f"({b.genre}, ~{b.words} слів)" if b else ""
    await message.answer(
        f"✅ Прийнято. Тепер напиши <b>завдання b</b> {hint}.", reply_markup=cancel_kb()
    )


@router.message(Writing.await_b, F.text, ~F.text.startswith("/"))
async def on_task_b(message: Message, state: FSMContext) -> None:
    if len(message.text.split()) < MIN_WORDS:
        await message.answer(
            "Напиши, будь ласка, повноцінний текст завдання b 🙂", reply_markup=cancel_kb()
        )
        return
    if len(message.text) > MAX_CHARS:
        await message.answer(
            f"Текст задовгий (>{MAX_CHARS} символів). На іспиті B1 обсяг невеликий — скороти 🙂",
            reply_markup=cancel_kb(),
        )
        return
    data = await state.get_data()
    ws = writing.set_by_id(data["set_id"])
    text_a = data.get("text_a", "")
    await state.clear()
    if ws is None:
        await message.answer("Набір загубився — почнімо заново.", reply_markup=await menu_kb_for(message.from_user.id))
        return
    if not await limits.allow_ai(message.from_user.id):
        await message.answer(
            "🚫 Денний ліміт AI-фідбеку вичерпано. Тренування/МОК/повторення — без ліміту 👍 "
            "Письмо — завтра.",
            reply_markup=to_menu_kb(),
        )
        return

    await message.answer("🔍 Оцінюю за офіційними критеріями (wykonanie / środki / poprawność)…")
    fb, scores = await writing.feedback(ws, text_a, message.text)
    if not fb:
        await limits.refund_ai(message.from_user.id)  # виклик не вдався — не палимо квоту
        await message.answer("AI тимчасово недоступний — спробуй пізніше.", reply_markup=to_menu_kb())
        return

    header = ""
    if scores is not None:
        wyk, sr, popr = scores
        total = wyk + sr + popr
        passed = "✅ склав би" if total >= 15 else "❌ поки нижче порога"
        header = (
            "📊 <b>Офіційна шкала (0-30):</b>\n"
            f"• Wykonanie zadania: <b>{wyk}</b>/10\n"
            f"• Środki językowe: <b>{sr}</b>/10\n"
            f"• Poprawność językowa: <b>{popr}</b>/10\n"
            f"• <b>Разом: {total}/30</b> — поріг 15/30 ({passed})\n\n"
        )
        pct = round(total / 30 * 100)
        await user_state.update_readiness(message.from_user.id, Module.PISANIE.value, pct)

    await message.answer(header + fb, reply_markup=to_menu_kb())
    if c := await goals.pop_celebration(message.from_user.id):
        await message.answer(c)
