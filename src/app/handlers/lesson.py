"""Щоденний урок: структурований мікро-урок під найслабший модуль (через AI).

UI: одне повідомлення-картка — шапка + кнопки розділів (Тема/Граматика/Слова/
Завдання); тап відкриває розділ у ТОМУ Ж повідомленні (⬅️ Назад). Наприкінці —
кнопка «✍️ Виконати й здати», що запускає реальну (оцінювану) вправу модуля.
Матеріал уроку сам по собі НЕ оцінюється — прогрес рухає лише виконане завдання.
"""

from __future__ import annotations

import asyncio
import html
import json
import logging
import re
from contextlib import suppress
from datetime import timedelta

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis.asyncio import Redis

from app.config import settings
from app.domain.models import MODULE_LABELS, Module
from app.integrations import ai, tts
from app.services import clock, goals, limits, tts_say, vocab
from app.services import state as user_state

logger = logging.getLogger(__name__)

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def _cache_get(user_id: int) -> dict | None:
    """Урок дня з кешу (той самий день → не перегенеровуємо)."""
    v = await _r().get(f"polski:lesson:{user_id}:{clock.today_local().isoformat()}")
    return json.loads(v) if v else None


async def _cache_set(user_id: int, lesson: dict) -> None:
    await _r().set(
        f"polski:lesson:{user_id}:{clock.today_local().isoformat()}",
        json.dumps(lesson, ensure_ascii=False),
        ex=26 * 3600,
    )
router = Router()

# Кнопка «Виконати й здати» веде до реальної (оцінюваної) вправи модуля
_EXERCISE_CB = {
    "pisanie": "writing:start",
    "mowienie": "speaking:start",
    "sluchanie": "listening:start",
    "czytanie": "drill:start",
    "gramatyka": "drill:start",
}

_FRAMES = [
    "📖 Збираю тему дня…",
    "📐 Добираю граматику…",
    "🔤 Готую нові слова…",
    "✍️ Формую завдання…",
]

_SYSTEM = (
    "Ти — терплячий персональний тренер польської мови для україномовного учня, "
    "який готується до державного іспиту B1 (egzamin certyfikatowy). "
    "Пояснюй УКРАЇНСЬКОЮ, дуже просто, з прикладами. Цільова мова — польська. "
    "Спирайся на схожість української й польської, але ЗАВЖДИ підсвічуй «фальшивих друзів». "
    "Теми — з реального життя: резиденція, громадянство, urząd, praca, побут. "
    "У текстових полях лише теги <b>...</b> та емодзі, БЕЗ markdown (*, _, #)."
)


def _prompt(module: Module, level: str) -> str:
    return (
        f"Згенеруй короткий урок (~10–15 хв) із фокусом на модуль «{MODULE_LABELS[module]}», "
        f"рівень учня {level}. Поверни СТРОГО JSON (без ```-огортки) з полями:\n"
        '• "topic" — рядок: одне життєве речення-вступ (можна <b>).\n'
        '• "grammar" — рядок: ОДНЕ правило (назва простими словами → чому так → '
        "шаблон/закінчення → контраст з українською → приклад; <b> дозволено).\n"
        '• "vocab" — масив 5–7 обʼєктів {"pl","ua","example"}: pl=польське слово; '
        "ua=стислий український переклад (БЕЗ тегів і приміток); example=ОДНЕ коротке речення "
        "ЛИШЕ польською з цим словом (без перекладу, без HTML-тегів).\n"
        '• "task" — рядок: коротке завдання САМЕ цього модуля з життєвою ситуацією (без markdown).\n'
        "Тільки валідний JSON, нічого поза ним."
    )


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", str(s)).strip()


def _clean_pl(s: str) -> str:
    """Лишити ЧИСТЕ польське речення: без HTML і без укр. перекладу/приміток після «—»."""
    s = _strip_tags(s)
    s = re.split(r"\s[—–-]\s|⚠", s, maxsplit=1)[0]  # AI часто криє переклад/примітку після тире
    return s.strip()


def _vocab_html(items: list) -> str:
    lines: list[str] = []
    for w in items[:7]:
        if not isinstance(w, dict):
            continue
        pl, ua, ex = _strip_tags(w.get("pl", "")), _strip_tags(w.get("ua", "")), _clean_pl(w.get("example", ""))
        # урок = перше знайомство → переклад ВІДКРИТИЙ (спойлер лишається для /powtorki, /slownik)
        lines.append(f"🔑 <b>{html.escape(pl)}</b> — {html.escape(ua)}")
        if ex:
            lines.append(f"📌 <i>{html.escape(ex)}</i>")
    return "\n".join(lines)


def _parse_lesson(raw: str, module: Module) -> dict | None:
    s = raw.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\s*", "", s).rstrip("`").strip()
    i, j = s.find("{"), s.rfind("}")
    if i < 0 or j < 0:
        return None
    try:
        obj = json.loads(s[i : j + 1])
    except (ValueError, TypeError):
        return None
    if not all(k in obj for k in ("topic", "grammar", "vocab", "task")):
        return None
    voc = obj["vocab"] if isinstance(obj["vocab"], list) else []
    return {
        "module": module.value,
        "label": MODULE_LABELS[module],
        "topic": str(obj["topic"]),
        "grammar": str(obj["grammar"]),
        "vocab": _vocab_html(voc),
        "vocab_n": len(voc),
        "vocab_say": _vocab_say(voc),  # [мітка, текст «слово. приклад»] для кнопок 🔊
        "task": html.escape(str(obj["task"])),
    }


def _vocab_say(items: list) -> list[list[str]]:
    """Пари [мітка-слово, текст-для-озвучення] — слово + ЧИСТИЙ польський приклад.

    Тільки польська (без укр. перекладу/тегів/приміток) — інакше 🔊 читає кашу.
    """
    out: list[list[str]] = []
    for w in items[:7]:
        if not isinstance(w, dict) or not w.get("pl"):
            continue
        pl = _strip_tags(w["pl"])
        ex = _clean_pl(w.get("example", ""))
        out.append([pl, f"{pl}. {ex}" if ex else pl])
    return out


def _fallback_lesson(module: Module) -> dict:
    return {
        "module": module.value,
        "label": MODULE_LABELS[module],
        "topic": "AI тимчасово недоступний — базовий тренувальний урок цього модуля.",
        "grammar": (
            "<b>Минулий час</b>: до основи додаємо <b>-łem</b> (чол.) / <b>-łam</b> (жін.).\n"
            "czytać → czytałem/czytałam. В українській «читав/читала» — схоже, але закінчення інші."
        ),
        "vocab": (
            "🔑 <b>wniosek</b> — заява\n📌 Złożyłem wniosek.\n"
            "🔑 <b>urząd</b> — установа\n📌 Idę do urzędu.\n"
            "🔑 <b>sprawa</b> — справа\n📌 Poznaj stan sprawy."
        ),
        "vocab_n": 3,
        "vocab_say": [
            ["wniosek", "wniosek. Złożyłem wniosek."],
            ["urząd", "urząd. Idę do urzędu."],
            ["sprawa", "sprawa. Poznaj stan sprawy."],
        ],
        "task": "Перепиши польською у минулому часі: 1) Czytam książkę 2) Idę do sklepu 3) Ona pracuje.",
    }


def _bump_streak(st) -> None:
    today = clock.today_local().isoformat()
    if st.last_lesson == today:
        return
    yesterday = (clock.today_local() - timedelta(days=1)).isoformat()
    st.streak = st.streak + 1 if st.last_lesson == yesterday else 1
    st.last_lesson = today


def _header(st) -> str:
    # відлік до іспиту показуємо в меню/прогресі/вітанні (там особиста дата);
    # у картці уроку — лише стрік, щоб не дублювати й не плутати джерела.
    return f"🔥 Стрік <b>{st.streak}</b>\n🇵🇱 <b>Урок польської</b> · ~10–15 хв"


def _menu_kb(lesson: dict, due_n: int) -> object:
    kb = InlineKeyboardBuilder()
    kb.button(text="📌 Тема дня", callback_data="les:sec:topic")
    kb.button(text="📐 Граматика", callback_data="les:sec:grammar")
    kb.button(text=f"🔤 Слова · {lesson['vocab_n']}", callback_data="les:sec:vocab")
    kb.button(text="✍️ Завдання", callback_data="les:sec:task")
    if due_n:
        kb.button(text=f"🔁 Повторити слова · {due_n}", callback_data="review:start")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(2, 2, 1, 1)
    return kb.as_markup()


def _menu_text(lesson: dict, st) -> str:
    return (
        f"{_header(st)}\n\n"
        f"Модуль сьогодні: <b>{lesson['label']}</b>\n"
        "📖 Обери розділ, щоб вивчити. Коли будеш готовий — «✍️ Завдання» → «Виконати й здати»."
    )


async def _animate(msg: Message) -> None:
    i = 0
    with suppress(asyncio.CancelledError):
        while True:
            await asyncio.sleep(1.3)
            i = (i + 1) % len(_FRAMES)
            with suppress(Exception):
                await msg.edit_text(_FRAMES[i])


async def _show(msg: Message, user_id: int, fsm: FSMContext, lesson: dict, st, edit: bool) -> None:
    await vocab.seed_if_empty(user_id, clock.today_local())
    _, due_n = await vocab.counts(user_id, clock.today_local())
    await fsm.update_data(lesson=lesson)
    text, kb = _menu_text(lesson, st), _menu_kb(lesson, due_n)
    with suppress(Exception):
        await (msg.edit_text(text, reply_markup=kb) if edit else msg.answer(text, reply_markup=kb))


async def _generate(user_id: int, st) -> dict:
    module = st.weakest_module()
    lesson: dict | None = None
    if ai.enabled() and await limits.allow_ai(user_id):
        # 2500 — запас над реальними ~1300–1600 токенами уроку (кирилиця дорога),
        # щоб JSON не обривався по max_tokens і не падав у fallback.
        raw = await ai.ask(
            _SYSTEM, _prompt(module, st.level), strong=True, max_tokens=2500, cache=True, label="lekcja"
        )
        if raw:
            lesson = _parse_lesson(raw, module)
            if lesson is None:
                logger.warning(
                    "Урок: AI відповів (%d симв.), але JSON не розпарсився — fallback (модуль=%s)",
                    len(raw),
                    module.value,
                )
        if not raw or lesson is None:
            await limits.refund_ai(user_id)  # виклик не вдався/невалідний — не палимо квоту
    return lesson if lesson is not None else _fallback_lesson(module)


async def _deliver(status: Message, user_id: int, fsm: FSMContext) -> None:
    """Згенерувати новий урок дня (перший раз за день), закешувати, показати."""
    st = await user_state.load(user_id)
    lesson = await _generate(user_id, st)
    await _cache_set(user_id, lesson)
    _bump_streak(st)
    await user_state.save(st)
    # урок — ПІДГОТОВКА: 0 хвилин у денну ціль (хвилини рухає лише виконана вправа),
    # але XP + зарахування місії «пройди урок» раз на день
    await goals.add(user_id, 0, goals.XP_LESSON, kind="lesson")
    await _show(status, user_id, fsm, lesson, st, edit=True)
    if c := await goals.pop_celebration(user_id):
        await status.answer(c)


async def _open(message: Message, user_id: int, state: FSMContext) -> None:
    cached = await _cache_get(user_id)
    if cached is not None:  # той самий день — миттєво з кешу, без AI/анімації/повторного нарахування
        st = await user_state.load(user_id)
        await _show(message, user_id, state, cached, st, edit=False)
        return
    status = await message.answer(_FRAMES[0])
    task = asyncio.create_task(_animate(status))
    try:
        await _deliver(status, user_id, state)
    finally:
        task.cancel()


@router.message(Command("lekcja", "lesson"))
async def cmd_lesson(message: Message, state: FSMContext) -> None:
    await _open(message, message.from_user.id, state)


@router.callback_query(F.data == "lesson:start")
async def cb_lesson(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _open(cb.message, cb.from_user.id, state)


_SECTION_TITLE = {
    "topic": "📌 <b>Тема дня</b>",
    "grammar": "📐 <b>Граматика</b>",
    "vocab": "🔤 <b>Нові слова</b>",
    "task": "✍️ <b>Завдання</b>",
}


def _section_kb(
    section: str, module_value: str, say_items: list[tuple[str, str]] | None = None
) -> object:
    kb = InlineKeyboardBuilder()
    if say_items:  # розділ «Слова» — кнопка 🔊 на кожне слово (по 2 в ряд)
        row: list[InlineKeyboardButton] = []
        for word, sid in say_items:
            row.append(InlineKeyboardButton(text=f"🔊 {word}", callback_data=f"say:{sid}"))
            if len(row) == 2:
                kb.row(*row)
                row = []
        if row:
            kb.row(*row)
    nav = [InlineKeyboardButton(text="⬅️ Назад", callback_data="les:menu")]
    if section == "task":
        exec_cb = _EXERCISE_CB.get(module_value, "menu:home")
        nav.append(InlineKeyboardButton(text="✍️ Виконати й здати", callback_data=exec_cb))
    else:
        nav.append(InlineKeyboardButton(text="✍️ До завдання", callback_data="les:sec:task"))
    kb.row(*nav)
    return kb.as_markup()


@router.callback_query(F.data.startswith("les:sec:"))
async def cb_section(cb: CallbackQuery, state: FSMContext) -> None:
    section = cb.data.split(":", 2)[2]
    lesson = (await state.get_data()).get("lesson")
    await cb.answer()
    if not lesson or section not in _SECTION_TITLE:
        await cb.message.edit_text("Урок застарів — згенеруй новий: /lekcja")
        return

    body = lesson.get(section, "")
    text = f"🇵🇱 <b>Урок — {lesson['label']}</b>\n➖➖➖➖➖\n{_SECTION_TITLE[section]}\n\n{body}"
    say_items: list[tuple[str, str]] | None = None
    if section == "vocab" and tts.available():  # кнопки 🔊 для кожного слова
        say_items = [
            (label, await tts_say.stash(text)) for label, text in lesson.get("vocab_say", []) if text
        ]
        if say_items:
            text += "\n\n🔊 Тисни слово, щоб почути вимову."
    if section == "task":
        text += (
            "\n\nℹ️ <i>Матеріал уроку сам по собі не оцінюється. Тисни «Виконати й здати» — я дам "
            "офіційне завдання цього модуля, перевірю за критеріями Держкомісії, і це піде у твій "
            "прогрес готовності.</i>"
        )
    with suppress(Exception):
        await cb.message.edit_text(
            text, reply_markup=_section_kb(section, lesson["module"], say_items)
        )


@router.callback_query(F.data == "les:menu")
async def cb_menu(cb: CallbackQuery, state: FSMContext) -> None:
    lesson = (await state.get_data()).get("lesson")
    await cb.answer()
    if not lesson:
        await cb.message.edit_text("Урок застарів — згенеруй новий: /lekcja")
        return
    st = await user_state.load(cb.from_user.id)
    _, due_n = await vocab.counts(cb.from_user.id, clock.today_local())
    with suppress(Exception):
        await cb.message.edit_text(_menu_text(lesson, st), reply_markup=_menu_kb(lesson, due_n))
