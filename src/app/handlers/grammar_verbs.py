"""Розділ «Дієслова» — довідник + тренажер (окремо від B1, не рухає готовність).

UX (за best-practices ConjuGato/Cooljugator + наші фішки): хаб → тематичні групи →
картка дієслова (таблиця, минулий, видова пара, rekcja, приклад, 🔊 вимова всієї
парадигми через TTS) → адаптивний тренажер (частіше питає «болючі» дієслова).
Кожне повідомлення — логічний блок зі своїми кнопками; браузер редагується на місці.
"""

from __future__ import annotations

import html
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import verbs
from app.services import tts_say
from app.services import verbs as vdrill

router = Router()


class VFind(StatesGroup):
    waiting = State()  # чекаємо текст для пошуку дієслова


class VDrill(StatesGroup):
    active = State()  # сесія тренажера форм


class RDrill(StatesGroup):
    active = State()  # сесія тренажера rekcji (який відмінок після дієслова)


# ── хаб ──────────────────────────────────────────────────────────────────────
_HUB = (
    "🔀 <b>Дієслова</b>\n"
    "<i>Довідник найуживаніших дієслів: відмінювання, видова пара, керування "
    "відмінком (rekcja) і вимова. Плюс тренажер, який запамʼятовує твої помилки.</i>\n\n"
    "Обери групу, тренуйся або знайди дієслово 👇"
)


def _hub_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for gi, g in enumerate(verbs.all_groups()):
        kb.button(text=f"{g.icon} {g.title}", callback_data=f"vb:g:{gi}")
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text="🏋️ Тренажер відмінювання", callback_data="vb:drill"))
    kb.row(InlineKeyboardButton(text="🎯 Тренажер rekcji (відмінок після дієслова)", callback_data="vb:rdrill"))
    kb.row(InlineKeyboardButton(text="🔍 Знайти дієслово", callback_data="vb:find"))
    kb.row(InlineKeyboardButton(text="⬅️ Меню", callback_data="menu:home"))
    return kb.as_markup()


@router.message(Command("czasowniki"))
async def cmd_verbs(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(_HUB, reply_markup=_hub_kb())


@router.callback_query(F.data == "verbs:home")
async def cb_open(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await state.clear()
    await cb.message.answer(_HUB, reply_markup=_hub_kb())


@router.callback_query(F.data == "vb:home")
async def cb_home(cb: CallbackQuery, state: FSMContext) -> None:
    """Повернення в хаб — редагуємо те саме повідомлення."""
    await cb.answer()
    await state.clear()
    await _edit(cb, _HUB, _hub_kb())


# ── група → список дієслів ───────────────────────────────────────────────────
@router.callback_query(F.data.startswith("vb:g:"))
async def cb_group(cb: CallbackQuery) -> None:
    await cb.answer()
    gi = int(cb.data.split(":")[2])
    g = verbs.group_at(gi)
    if not g:
        return
    kb = InlineKeyboardBuilder()
    for vi, v in enumerate(g.verbs):
        kb.button(text=f"{v.inf} — {v.uk}", callback_data=f"vb:c:{gi}:{vi}")
    kb.button(text="⬅️ До груп", callback_data="vb:home")
    kb.adjust(1)
    await _edit(
        cb,
        f"{g.icon} <b>{html.escape(g.title)}</b>\n<i>{html.escape(g.subtitle)}</i>\n\n"
        "Обери дієслово 👇",
        kb.as_markup(),
    )


# ── картка дієслова ──────────────────────────────────────────────────────────
def _card_text(v: verbs.Verb) -> str:
    parts = [f"🔀 <code>{html.escape(v.inf)}</code> — <b>{html.escape(v.uk)}</b>"]
    if v.pair:
        parts.append(
            f"🎬 недоконаний · пара: <code>{html.escape(v.pair)}</code>"
            + (f" (майб.: <code>{html.escape(v.pair_hint)}</code>)" if v.pair_hint else "")
        )
    else:
        parts.append("🎬 видової пари нема (або вживається одна форма)")
    if v.group:
        parts.append(f"📐 Модель: {html.escape(v.group)}")
    p = v.present
    parts.append(
        "\n🕐 <b>Теперішній час:</b>\n"
        f"ja <code>{p[0]}</code> · ty <code>{p[1]}</code> · on/ona <code>{p[2]}</code>\n"
        f"my <code>{p[3]}</code> · wy <code>{p[4]}</code> · oni <code>{p[5]}</code>"
    )
    if v.past:
        parts.append(f"🕰 <b>Минулий:</b> <code>{html.escape(v.past)}</code>")
    if v.rekcja:
        parts.append(f"🎯 <b>Керування:</b> {html.escape(v.rekcja)}")
    for pl, uk in v.examples:
        parts.append(f"📝 <code>{html.escape(pl)}</code> — {html.escape(uk)}")
    return "\n\n".join(parts)


async def _card_kb(v: verbs.Verb, gi: int, vi: int) -> InlineKeyboardMarkup:
    # 🔊 — озвучити всю парадигму (реюз say-механізму з кешем file_id)
    sid = await tts_say.stash(f"{v.inf}. " + ", ".join(v.present))
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="🔊 Вимова", callback_data=f"say:{sid}"),
        InlineKeyboardButton(text="🏋️ Тренувати", callback_data=f"vb:tr:{gi}:{vi}"),
    )
    kb.row(InlineKeyboardButton(text="⬅️ До групи", callback_data=f"vb:g:{gi}"))
    return kb.as_markup()


@router.callback_query(F.data.startswith("vb:c:"))
async def cb_card(cb: CallbackQuery) -> None:
    await cb.answer()
    _, _, gi, vi = cb.data.split(":")
    v = verbs.verb_at(int(gi), int(vi))
    if not v:
        return
    await _edit(cb, _card_text(v), await _card_kb(v, int(gi), int(vi)))


# ── тренажер ─────────────────────────────────────────────────────────────────
def _q_item(queue: list, pos: int) -> tuple[int, int, int, int]:
    """(gi, vi, person, tense); старі 3-елементні сесії з Redis → теперішній час."""
    item = queue[pos]
    return (*item, 0) if len(item) == 3 else tuple(item)  # type: ignore[return-value]


def _drill_forms(v: verbs.Verb, tense: int) -> tuple[list[str], list[str]] | None:
    """(форми, мітки осіб) для питання: теперішній або минулий (з парадигми past)."""
    if tense == 0:
        return v.present, verbs.PERSONS
    paradigm = verbs.past_paradigm(v.past)
    return (paradigm, verbs.PAST_PERSONS) if paradigm else None


def _drill_q_text(v: verbs.Verb, person: int, tense: int, pos: int, total: int) -> str:
    persons = verbs.PAST_PERSONS if tense else verbs.PERSONS
    tense_label = "🕰 Минулий час" if tense else "🕐 Теперішній час"
    return (
        f"🏋️ <b>Тренажер</b> · {pos + 1}/{total}\n\n"
        f"❓ <code>{html.escape(v.inf)}</code> ({html.escape(v.uk)})\n"
        f"{tense_label} · форма для <b>«{persons[person]}»</b>?"
    )


def _drill_q_kb(forms: list[str], pos: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i, form in enumerate(forms):
        kb.button(text=form, callback_data=f"vd:a:{pos}:{i}")
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text="⏹ Завершити", callback_data="vd:stop"))
    return kb.as_markup()


async def _send_drill_q(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    queue, pos = data["queue"], data["pos"]
    gi, vi, person, tense = _q_item(queue, pos)
    v = verbs.verb_at(gi, vi)
    fp = _drill_forms(v, tense) if v else None
    if not v or fp is None:  # дані змінились між релізами — завершуємо коректно
        await state.clear()
        return
    forms, _ = fp
    await message.answer(
        _drill_q_text(v, person, tense, pos, len(queue)), reply_markup=_drill_q_kb(forms, pos)
    )


async def _start_drill(
    cb: CallbackQuery, state: FSMContext, queue: list[tuple[int, int, int, int]]
) -> None:
    await state.set_state(VDrill.active)
    await state.update_data(queue=queue, pos=0, correct=0)
    await _send_drill_q(cb.message, state)


@router.callback_query(F.data == "vb:drill")
async def cb_drill(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _start_drill(cb, state, await vdrill.build_drill(cb.from_user.id))


@router.callback_query(F.data.startswith("vb:tr:"))
async def cb_train_one(cb: CallbackQuery, state: FSMContext) -> None:
    """Тренувати конкретне дієслово: 3 різні особи (мікс часів) + 2 випадкові інші."""
    await cb.answer()
    _, _, gi, vi = cb.data.split(":")
    gi, vi = int(gi), int(vi)
    if not verbs.verb_at(gi, vi):
        return
    import random

    persons = random.sample(range(6), 3)
    focus = vdrill.with_tenses([(gi, vi, p) for p in persons])
    rest = [q for q in await vdrill.build_drill(cb.from_user.id) if (q[0], q[1]) != (gi, vi)][:2]
    await _start_drill(cb, state, focus + rest)


@router.callback_query(VDrill.active, F.data == "vd:stop")
async def cb_drill_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer("⏹ Тренажер закрито.", reply_markup=_hub_kb())


@router.callback_query(VDrill.active, F.data.startswith("vd:a:"))
async def cb_drill_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    queue, pos, correct = data["queue"], data["pos"], data["correct"]
    _, _, qpos, opt = cb.data.split(":")
    if int(qpos) != pos:  # стала кнопка / подвійний тап
        await cb.answer("Це питання вже пройдено 🙂")
        return
    gi, vi, person, tense = _q_item(queue, pos)
    v = verbs.verb_at(gi, vi)
    fp = _drill_forms(v, tense) if v else None
    if not v or fp is None:
        await state.clear()
        return
    forms, persons = fp
    chosen = int(opt)
    ok = chosen == person  # правильна форма = форма цієї особи
    await vdrill.record_answer(cb.from_user.id, gi, vi, ok)
    await cb.answer("✔️" if ok else "❌")
    yours = forms[chosen] if 0 <= chosen < 6 else "—"
    verdict = (
        f"🔵 Твоя відповідь: <code>{yours}</code>\n\n✔️ <b>Dobrze!</b>"
        if ok
        else f"🔵 Твоя відповідь: <code>{yours}</code>  ❌\n\n"
        f"✅ Правильно: <b>{persons[person]}</b> <code>{forms[person]}</code>"
    )
    with suppress(Exception):
        await cb.message.edit_text(
            f"❓ <code>{html.escape(v.inf)}</code> — «{persons[person]}»\n\n{verdict}"
        )
    correct += ok
    pos += 1
    await state.update_data(pos=pos, correct=correct)
    if pos < len(queue):
        await _send_drill_q(cb.message, state)
    else:
        await state.clear()
        total = len(queue)
        emoji = "🎉" if correct == total else "👍" if correct >= total - 1 else "💪"
        await cb.message.answer(
            f"{emoji} <b>Результат: {correct}/{total}</b>\n"
            "<i>Тренажер запамʼятовує помилки й питатиме ці дієслова частіше.</i>",
            reply_markup=_hub_kb(),
        )


# ── тренажер rekcji ──────────────────────────────────────────────────────────
def _rekcja_q_text(v: verbs.Verb, pos: int, total: int) -> str:
    return (
        f"🎯 <b>Тренажер rekcji</b> · {pos + 1}/{total}\n\n"
        f"❓ <code>{html.escape(v.inf)}</code> ({html.escape(v.uk)})\n"
        "З яким відмінком/прийменником це працює?"
    )


async def _send_rekcja_q(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    queue, pos = data["queue"], data["pos"]
    gi, vi, _ = queue[pos]
    v = verbs.verb_at(gi, vi)
    if not v or not v.rekcja_q:
        await state.clear()
        return
    opts = vdrill.rekcja_options(v.rekcja_q, vdrill.rekcja_pool())
    await state.update_data(opts=opts)  # варіанти фіксуємо в FSM (стабільні між тапами)
    kb = InlineKeyboardBuilder()
    for i, o in enumerate(opts):
        kb.button(text=o, callback_data=f"vr:a:{pos}:{i}")
    kb.adjust(1)
    kb.row(InlineKeyboardButton(text="⏹ Завершити", callback_data="vr:stop"))
    await message.answer(_rekcja_q_text(v, pos, len(queue)), reply_markup=kb.as_markup())


@router.callback_query(F.data == "vb:rdrill")
async def cb_rdrill(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    queue = await vdrill.build_rekcja_drill(cb.from_user.id)
    if not queue:
        return
    await state.set_state(RDrill.active)
    await state.update_data(queue=queue, pos=0, correct=0)
    await _send_rekcja_q(cb.message, state)


@router.callback_query(RDrill.active, F.data == "vr:stop")
async def cb_rdrill_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Завершено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer("⏹ Тренажер закрито.", reply_markup=_hub_kb())


@router.callback_query(RDrill.active, F.data.startswith("vr:a:"))
async def cb_rdrill_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    queue, pos, correct, opts = data["queue"], data["pos"], data["correct"], data["opts"]
    _, _, qpos, oi = cb.data.split(":")
    if int(qpos) != pos:
        await cb.answer("Це питання вже пройдено 🙂")
        return
    gi, vi, _ = queue[pos]
    v = verbs.verb_at(gi, vi)
    if not v:
        await state.clear()
        return
    chosen = opts[int(oi)] if 0 <= int(oi) < len(opts) else "—"
    ok = chosen == v.rekcja_q
    await vdrill.record_answer(cb.from_user.id, gi, vi, ok, kind="rekcja")
    await cb.answer("✔️" if ok else "❌")
    verdict = (
        f"🔵 Твоя відповідь: <b>{html.escape(chosen)}</b>\n\n✔️ <b>Dobrze!</b>"
        if ok
        else f"🔵 Твоя відповідь: <b>{html.escape(chosen)}</b>  ❌\n\n"
        f"✅ Правильно: <b>{html.escape(v.rekcja_q)}</b>"
    )
    exp = f"\n\n💡 {html.escape(v.rekcja)}" if v.rekcja else ""
    with suppress(Exception):
        await cb.message.edit_text(f"❓ <code>{html.escape(v.inf)}</code>\n\n{verdict}{exp}")
    correct += ok
    pos += 1
    await state.update_data(pos=pos, correct=correct)
    if pos < len(queue):
        await _send_rekcja_q(cb.message, state)
    else:
        await state.clear()
        total = len(queue)
        emoji = "🎉" if correct == total else "👍" if correct >= total - 1 else "💪"
        await cb.message.answer(
            f"{emoji} <b>Результат: {correct}/{total}</b>\n"
            "<i>Rekcja — найчастіше джерело помилок. Тренажер повертатиме складні "
            "дієслова, доки не закріпиш.</i>",
            reply_markup=_hub_kb(),
        )


# ── пошук ────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "vb:find")
async def cb_find(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await state.set_state(VFind.waiting)
    await cb.message.answer(
        "🔍 Напиши дієслово <b>одним повідомленням</b> — польською (<code>robić</code>) "
        "або українською («робити»):"
    )


@router.message(VFind.waiting, F.text, ~F.text.startswith("/"))
async def on_find(message: Message, state: FSMContext) -> None:
    await state.clear()
    hits = verbs.search(message.text or "")
    if not hits:
        kb = InlineKeyboardBuilder()
        kb.button(text="🔍 Спробувати ще", callback_data="vb:find")
        kb.button(text="⬅️ До дієслів", callback_data="verbs:home")
        kb.adjust(1)
        await message.answer(
            "Не знайшов такого дієслова 😔 У довіднику — 60 найуживаніших; "
            "список зростатиме.",
            reply_markup=kb.as_markup(),
        )
        return
    kb = InlineKeyboardBuilder()
    for gi, vi, v in hits:
        kb.button(text=f"{v.inf} — {v.uk}", callback_data=f"vb:c:{gi}:{vi}")
    kb.button(text="⬅️ До дієслів", callback_data="verbs:home")
    kb.adjust(1)
    await message.answer("Ось що знайшов 👇", reply_markup=kb.as_markup())


async def _edit(cb: CallbackQuery, text: str, kb: InlineKeyboardMarkup) -> None:
    with suppress(Exception):
        await cb.message.edit_text(text, reply_markup=kb)
