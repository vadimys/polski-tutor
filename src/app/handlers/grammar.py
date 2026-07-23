"""Розділ «Граматика» — окремий курс польської з нуля (не повʼязаний із B1).

UX: карта модулів → уроки → КАРТКИ по одній (◀️ ▶️, редагуються на місці, без полотна)
→ міні-практика → ✅ пройдено → наступний урок. Кожне повідомлення — логічний блок зі
своїми кнопками (правило проєкту). Навчання не рухає B1-готовність — це чистий курс.
"""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import grammar
from app.services import grammar as gp

router = Router()

# коротка «дорожня карта» майбутніх модулів (щоб учень бачив шлях)
_ROADMAP = (
    "🎓 <i>Повний базовий курс: від алфавіту до складання речень. Проходь по порядку "
    "або обирай тему. Курс поповнюватимемо новими вправами й темами.</i>"
)


# ── карта модулів ────────────────────────────────────────────────────────────
def _map_text(done: set[str]) -> str:
    lines = [
        "📚 <b>Граматика польської</b>",
        "<i>Окремий курс — вивчай мову з нуля, крок за кроком. Не повʼязано з підготовкою "
        "до іспиту.</i>",
        "",
        f"📈 Пройдено: <b>{gp.overall_pct(done)}%</b>",
        "",
    ]
    for m in grammar.all_modules():
        got, total = gp.module_progress(done, m)
        tick = " ✅" if got == total and total else ""
        lines.append(f"{m.icon} <b>{html.escape(m.title)}</b> · {got}/{total}{tick}")
    lines += ["", _ROADMAP]
    return "\n".join(lines)


def _map_kb(done: set[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for m in grammar.all_modules():
        got, total = gp.module_progress(done, m)
        mark = "✅" if got == total and total else ("▶️" if got else "○")
        kb.button(text=f"{mark} {m.icon} {m.title}", callback_data=f"gr:mod:{m.id}")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    return kb.as_markup()


# ── список уроків модуля ─────────────────────────────────────────────────────
def _module_text(module: grammar.Module) -> str:
    return (
        f"{module.icon} <b>{html.escape(module.title)}</b>\n"
        f"<i>{html.escape(module.subtitle)}</i>\n\n"
        "Обери урок 👇"
    )


def _module_kb(module: grammar.Module, done: set[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for ls in module.lessons:
        mark = "✅" if ls.id in done else "○"
        kb.button(text=f"{mark} {ls.title}", callback_data=f"gr:les:{ls.id}")
    kb.button(text="⬅️ До курсу", callback_data="grammar:home")
    kb.adjust(1)
    return kb.as_markup()


# ── одна картка уроку ────────────────────────────────────────────────────────
def _card_text(module: grammar.Module, lesson: grammar.Lesson, idx: int) -> str:
    c = lesson.cards[idx]
    parts = [
        f"{module.icon} <b>{html.escape(module.title)}</b>",
        f"<i>{html.escape(lesson.title)}</i> · картка {idx + 1}/{len(lesson.cards)}",
        "➖➖➖➖➖",
        f"<b>{c.title}</b>",
        "",
        c.body,
    ]
    if c.examples:
        parts.append("\n📝 <b>Приклади:</b>")
        for pl, uk in c.examples:
            parts.append(f"• <b>{html.escape(pl)}</b>" + (f" — {html.escape(uk)}" if uk else ""))
    if c.tip:
        parts.append(f"\n💡 <i>{c.tip}</i>")
    return "\n".join(parts)


def _card_kb(module: grammar.Module, lesson: grammar.Lesson, idx: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    last = idx == len(lesson.cards) - 1
    row = []
    if idx > 0:
        row.append(("◀️", f"gr:c:{lesson.id}:{idx - 1}"))
    if not last:
        row.append(("Далі ▶️", f"gr:c:{lesson.id}:{idx + 1}"))
    elif lesson.quiz:
        row.append(("🎯 Перевірити себе", f"gr:quiz:{lesson.id}:0"))
    else:
        row.append(("✅ Пройдено", f"gr:done:{lesson.id}"))
    kb.row(*(_btn(t, c) for t, c in row))
    kb.row(_btn("☰ До уроків", f"gr:mod:{module.id}"))
    return kb.as_markup()


def _btn(text: str, cb: str):
    from aiogram.types import InlineKeyboardButton

    return InlineKeyboardButton(text=text, callback_data=cb)


# ── міні-практика ────────────────────────────────────────────────────────────
def _quiz_text(lesson: grammar.Lesson, qi: int) -> str:
    q = lesson.quiz[qi]
    return (
        f"🎯 <b>Міні-практика</b> · {qi + 1}/{len(lesson.quiz)}\n"
        f"<i>{html.escape(lesson.title)}</i>\n\n"
        f"❓ {html.escape(q.q)}"
    )


def _quiz_kb(lesson: grammar.Lesson, qi: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i, opt in enumerate(lesson.quiz[qi].options):
        kb.button(text=opt, callback_data=f"gr:qa:{lesson.id}:{qi}:{i}")
    kb.adjust(1)
    return kb.as_markup()


def _quiz_verdict(lesson: grammar.Lesson, qi: int, chosen: int) -> tuple[str, InlineKeyboardMarkup]:
    q = lesson.quiz[qi]
    ok = chosen == q.correct
    yours = html.escape(q.options[chosen]) if 0 <= chosen < len(q.options) else "—"
    body = (
        f"🔵 Твоя відповідь: <b>{yours}</b>\n\n✔️ <b>Правильно!</b>"
        if ok
        else f"🔵 Твоя відповідь: <b>{yours}</b>  ❌\n\n✅ Правильно: <b>{html.escape(q.options[q.correct])}</b>"
    )
    exp = f"\n\n💡 {html.escape(q.explain)}" if q.explain else ""
    text = f"❓ {html.escape(q.q)}\n\n{body}{exp}"
    kb = InlineKeyboardBuilder()
    if qi + 1 < len(lesson.quiz):
        kb.button(text="Далі ▶️", callback_data=f"gr:quiz:{lesson.id}:{qi + 1}")
    else:
        kb.button(text="✅ Завершити урок", callback_data=f"gr:done:{lesson.id}")
    return text, kb.as_markup()


# ── фінал уроку ──────────────────────────────────────────────────────────────
def _done_text(lesson: grammar.Lesson, done: set[str], nxt: grammar.Lesson | None) -> str:
    lines = [f"✅ <b>Урок пройдено!</b>\n<i>{html.escape(lesson.title)}</i>\n",
             f"📈 Курс пройдено на <b>{gp.overall_pct(done)}%</b>."]
    if nxt:
        lines.append(f"\nНаступний урок: <b>{html.escape(nxt.title)}</b> 👇")
    else:
        lines.append("\n🎉 Ти пройшов усі доступні уроки! Нові модулі — скоро.")
    return "\n".join(lines)


def _done_kb(module: grammar.Module, nxt: grammar.Lesson | None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if nxt:
        kb.button(text=f"▶️ Далі: {nxt.title}", callback_data=f"gr:les:{nxt.id}")
    kb.button(text="☰ До уроків", callback_data=f"gr:mod:{module.id}")
    kb.button(text="⬅️ До курсу", callback_data="grammar:home")
    kb.adjust(1)
    return kb.as_markup()


# ── хендлери ─────────────────────────────────────────────────────────────────
@router.message(Command("gramatyka"))
async def cmd_grammar(message: Message) -> None:
    done = await gp.done_set(message.from_user.id)
    await message.answer(_map_text(done), reply_markup=_map_kb(done))


@router.callback_query(F.data == "grammar:home")
async def cb_home(cb: CallbackQuery) -> None:
    await cb.answer()
    done = await gp.done_set(cb.from_user.id)
    await _edit(cb, _map_text(done), _map_kb(done))


@router.callback_query(F.data.startswith("gr:mod:"))
async def cb_module(cb: CallbackQuery) -> None:
    await cb.answer()
    m = grammar.module_by_id(cb.data.split(":", 2)[2])
    if not m:
        return
    done = await gp.done_set(cb.from_user.id)
    await _edit(cb, _module_text(m), _module_kb(m, done))


@router.callback_query(F.data.startswith("gr:les:"))
async def cb_lesson(cb: CallbackQuery) -> None:
    await cb.answer()
    await _show_card(cb, cb.data.split(":", 2)[2], 0)


@router.callback_query(F.data.startswith("gr:c:"))
async def cb_card(cb: CallbackQuery) -> None:
    await cb.answer()
    _, _, lid, idx = cb.data.split(":", 3)
    await _show_card(cb, lid, int(idx))


async def _show_card(cb: CallbackQuery, lid: str, idx: int) -> None:
    lesson = grammar.lesson_by_id(lid)
    module = grammar.module_of(lid)
    if not lesson or not module or not (0 <= idx < len(lesson.cards)):
        return
    await _edit(cb, _card_text(module, lesson, idx), _card_kb(module, lesson, idx))


@router.callback_query(F.data.startswith("gr:quiz:"))
async def cb_quiz(cb: CallbackQuery) -> None:
    await cb.answer()
    _, _, lid, qi = cb.data.split(":", 3)
    lesson = grammar.lesson_by_id(lid)
    if not lesson or not lesson.quiz or not (0 <= int(qi) < len(lesson.quiz)):
        return
    await _edit(cb, _quiz_text(lesson, int(qi)), _quiz_kb(lesson, int(qi)))


@router.callback_query(F.data.startswith("gr:qa:"))
async def cb_quiz_answer(cb: CallbackQuery) -> None:
    await cb.answer()
    _, _, lid, qi, opt = cb.data.split(":", 4)
    lesson = grammar.lesson_by_id(lid)
    if not lesson or not lesson.quiz or not (0 <= int(qi) < len(lesson.quiz)):
        return
    text, kb = _quiz_verdict(lesson, int(qi), int(opt))
    await _edit(cb, text, kb)


@router.callback_query(F.data.startswith("gr:done:"))
async def cb_done(cb: CallbackQuery) -> None:
    lid = cb.data.split(":", 2)[2]
    lesson = grammar.lesson_by_id(lid)
    module = grammar.module_of(lid)
    if not lesson or not module:
        return
    await gp.mark_done(cb.from_user.id, lid)
    await cb.answer("✅ Урок пройдено!")
    done = await gp.done_set(cb.from_user.id)
    nxt = grammar.next_lesson(lid)
    await _edit(cb, _done_text(lesson, done, nxt), _done_kb(module, nxt))


async def _edit(cb: CallbackQuery, text: str, kb: InlineKeyboardMarkup) -> None:
    from contextlib import suppress

    with suppress(Exception):  # редагуємо те саме повідомлення → чистий браузер курсу
        await cb.message.edit_text(text, reply_markup=kb)
