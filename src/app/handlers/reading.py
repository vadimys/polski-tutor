"""📖 «Читалочка» — СЕКРЕТНИЙ адмін-режим (для дитини, що вчиться читати польською).

Адмін шле фото сторінки → OCR (Claude vision) → інтерактивне читання:
• 🔊 слухати весь текст (зі сповільненням — кнопка 🐢 під голосовим);
• 📖 по реченнях: одне речення на екран + тап на БУДЬ-ЯКЕ слово → вимова + переклад;
• 🔤 словничок: усі слова тексту з українським перекладом.

Гейт — адмін + `settings.reading_allowed_ids` (фіча прихована: нема в меню/COMMANDS,
доступ лише тим, хто знає команду /czytanka й є в списку). Реюз озвучення:
повний текст і речення йдуть через наявні `say:`-кнопки (вже мають перемикач швидкості),
окремі слова — через reading-специфічні `rd:w`/`rd:ws` (щоб тримати переклад у підписі).
"""

from __future__ import annotations

import base64
import html
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings
from app.integrations import ai
from app.services import reading, tts_say, uxlock

router = Router()

_MAX_WORD_BTNS = 30  # стеля кнопок-слів на речення (сторінка-речення коротка)
_TEXT_CAP = 3500  # ліміт показу тексту в картці (озвучення бере повний)


def _reading_ids() -> set[int]:
    """Кому дозволено «Читалочку»: адмін + конфігуровані user_id (settings.reading_allowed_ids)."""
    ids = {settings.admin_id}
    for part in settings.reading_allowed_ids.split(","):
        part = part.strip()
        if part.isdigit():
            ids.add(int(part))
    return ids


def _allowed(uid: int | None) -> bool:
    return uid in _reading_ids()


# ---------- рендери ----------


def _card(obj: dict, rid: str, full_sid: str) -> tuple[str, InlineKeyboardMarkup]:
    title = html.escape(obj.get("title", "Текст"))
    text = obj["text"]
    shown = html.escape(text[:_TEXT_CAP] + ("…" if len(text) > _TEXT_CAP else ""))
    body = (
        f"📖 <b>{title}</b>\n\n{shown}\n\n"
        "Як читаємо? 👇"
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="🔊 Слухати весь текст", callback_data=f"say:{full_sid}")
    kb.button(text="📖 Читати по реченнях", callback_data=f"rd:sent:{rid}:0")
    kb.button(text="🔤 Словничок (переклад)", callback_data=f"rd:gloss:{rid}")
    kb.adjust(1)
    return body, kb.as_markup()


def _sentence_view(obj: dict, rid: str, i: int, sent_sid: str) -> tuple[str, InlineKeyboardMarkup]:
    sents = obj["sentences"]
    i = max(0, min(i, len(sents) - 1))
    sentence = sents[i]
    body = (
        f"📖 Речення <b>{i + 1}/{len(sents)}</b>\n\n"
        f"{html.escape(sentence)}\n\n"
        "👇 Тисни слово — почуєш вимову й переклад"
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="🔊 Слухати речення", callback_data=f"say:{sent_sid}")
    tokens = reading.word_tokens(sentence)
    word_btns = 0
    for wi, tok in enumerate(tokens):
        if not reading.norm(tok):  # чиста пунктуація — не кнопка
            continue
        kb.button(text=tok, callback_data=f"rd:w:{rid}:{i}:{wi}")
        word_btns += 1
        if word_btns >= _MAX_WORD_BTNS:
            break
    nav: list[InlineKeyboardButton] = []
    if i > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"rd:sent:{rid}:{i - 1}"))
    if i < len(sents) - 1:
        nav.append(InlineKeyboardButton(text="Далі ➡️", callback_data=f"rd:sent:{rid}:{i + 1}"))
    home = InlineKeyboardButton(text="📖 Весь текст", callback_data=f"rd:card:{rid}")
    # 1 (слухати) + рядки слів по 4 + навігація + додому
    kb.adjust(1, *([4] * ((word_btns + 3) // 4)))
    m = kb.as_markup()
    rows = list(m.inline_keyboard)
    if nav:
        rows.append(nav)
    rows.append([home])
    return body, InlineKeyboardMarkup(inline_keyboard=rows)


def _word_speed_kb(rid: str, si: int, wi: int, *, slow: bool) -> InlineKeyboardMarkup:
    if slow:
        btn = InlineKeyboardButton(text="🐇 Звичайна швидкість", callback_data=f"rd:w:{rid}:{si}:{wi}")
    else:
        btn = InlineKeyboardButton(text="🐢 Повільніше", callback_data=f"rd:ws:{rid}:{si}:{wi}")
    return InlineKeyboardMarkup(inline_keyboard=[[btn]])


def _gloss_view(obj: dict, rid: str) -> tuple[str, InlineKeyboardMarkup]:
    lines = ["🔤 <b>Словничок</b> <i>(слово — переклад)</i>\n"]
    for it in obj.get("glossary", []):
        lines.append(f"• <b>{html.escape(it['pl'])}</b> — {html.escape(it['uk'])}")
    if len(lines) == 1:
        lines.append("<i>Порожньо.</i>")
    body = "\n".join(lines)[:4096]
    kb = InlineKeyboardBuilder()
    kb.button(text="📖 Читати по реченнях", callback_data=f"rd:sent:{rid}:0")
    kb.button(text="📖 Весь текст", callback_data=f"rd:card:{rid}")
    kb.adjust(1)
    return body, kb.as_markup()


# ---------- вхід: фото + /czytanka ----------


@router.message(Command("czytanka"))
async def cmd_czytanka(message: Message) -> None:
    if not _allowed(message.from_user.id):
        return
    await message.answer(
        "📖 <b>Читалочка</b> (секретний режим)\n\n"
        "Надішли <b>фото сторінки</b> з польським текстом — я розпізнаю його й підготую до "
        "читання: слухати весь текст або по реченнях, тапати кожне слово (вимова + переклад), "
        "словничок. Скрізь є кнопка 🐢 <b>Повільніше</b>.\n\n"
        "💡 Для найточнішого розпізнавання шли фото <b>як «Файл»</b> (📎 → Файл) — без стиснення."
    )


@router.message(F.photo)
async def on_photo(message: Message) -> None:
    if not _allowed(message.from_user.id):
        return  # секретна фіча — мовчки ігноруємо чужі фото
    await _process_image(message, message.photo[-1].file_id, "image/jpeg")


@router.message(F.document.mime_type.startswith("image/"))
async def on_image_document(message: Message) -> None:
    if not _allowed(message.from_user.id):
        return
    # фото як «Файл» — без стиснення, найкраще для OCR
    await _process_image(message, message.document.file_id, message.document.mime_type or "image/jpeg")


async def _process_image(message: Message, file_id: str, media_type: str) -> None:
    if not ai.enabled():
        await message.answer("🔒 Розпізнавання недоступне (AI вимкнено).")
        return
    note = await message.answer("🔍 Читаю сторінку… (кілька секунд)")
    try:
        buf = await message.bot.download(file_id)
        b64 = base64.b64encode(buf.read()).decode()
        async with uxlock.typing(message.bot, message.chat.id):
            obj = await reading.extract(b64, media_type)
    except Exception:  # noqa: BLE001
        obj = None
    with suppress(Exception):
        await note.delete()
    if not obj:
        await message.answer(
            "😔 Не вдалося розпізнати текст. Спробуй чіткіше фото (рівно, добре освітлення)."
        )
        return
    full_sid = await tts_say.stash(obj["text"])
    rid = await reading.stash(obj)
    body, kb = _card(obj, rid, full_sid)
    await message.answer(body, reply_markup=kb)


# ---------- навігація ----------


async def _load_or_warn(cb: CallbackQuery, rid: str) -> dict | None:
    obj = await reading.load(rid)
    if not obj:
        await cb.answer("Читанка застаріла — надішли фото ще раз 🙂", show_alert=True)
        return None
    return obj


@router.callback_query(F.data.startswith("rd:card:"))
async def cb_card(cb: CallbackQuery) -> None:
    if not _allowed(cb.from_user.id):
        return
    rid = cb.data.split(":")[2]
    obj = await _load_or_warn(cb, rid)
    if not obj:
        return
    await cb.answer()
    full_sid = await tts_say.stash(obj["text"])
    body, kb = _card(obj, rid, full_sid)
    with suppress(Exception):
        await cb.message.edit_text(body, reply_markup=kb)


@router.callback_query(F.data.startswith("rd:sent:"))
async def cb_sentence(cb: CallbackQuery) -> None:
    if not _allowed(cb.from_user.id):
        return
    _, _, rid, si = cb.data.split(":")
    obj = await _load_or_warn(cb, rid)
    if not obj:
        return
    await cb.answer()
    i = max(0, min(int(si), len(obj["sentences"]) - 1))
    sent_sid = await tts_say.stash(obj["sentences"][i])
    body, kb = _sentence_view(obj, rid, i, sent_sid)
    with suppress(Exception):
        await cb.message.edit_text(body, reply_markup=kb)


@router.callback_query(F.data.startswith("rd:gloss:"))
async def cb_gloss(cb: CallbackQuery) -> None:
    if not _allowed(cb.from_user.id):
        return
    rid = cb.data.split(":")[2]
    obj = await _load_or_warn(cb, rid)
    if not obj:
        return
    await cb.answer()
    body, kb = _gloss_view(obj, rid)
    with suppress(Exception):
        await cb.message.edit_text(body, reply_markup=kb)


@router.callback_query(F.data.startswith("rd:ws:"))
async def cb_word_slow(cb: CallbackQuery) -> None:
    await _say_word(cb, slow=True)


@router.callback_query(F.data.startswith("rd:w:"))
async def cb_word(cb: CallbackQuery) -> None:
    await _say_word(cb, slow=False)


async def _say_word(cb: CallbackQuery, *, slow: bool) -> None:
    if not _allowed(cb.from_user.id):
        return
    parts = cb.data.split(":")  # rd:w:<rid>:<si>:<wi>  або rd:ws:<rid>:<si>:<wi>
    rid, si, wi = parts[2], int(parts[3]), int(parts[4])
    obj = await reading.load(rid)
    if not obj:
        await cb.answer("Читанка застаріла — надішли фото ще раз 🙂", show_alert=True)
        return
    sents = obj["sentences"]
    if si >= len(sents):
        await cb.answer()
        return
    tokens = reading.word_tokens(sents[si])
    token = tokens[wi] if wi < len(tokens) else ""
    clean = reading.norm(token)
    if not clean:
        await cb.answer()
        return
    uk = reading.translate(obj, token) or "—"
    await cb.answer(f"{token} — {uk}")  # миттєвий тост із перекладом
    with suppress(Exception):
        await cb.bot.send_chat_action(cb.message.chat.id, "upload_voice")
    await tts_say.forget_voice(cb.bot, cb.message.chat.id)  # одне слово-голосове за раз
    msg = await tts_say.send_voice(
        cb.bot, cb.message.chat.id, clean,
        caption=f"🔊 <b>{html.escape(token)}</b> — {html.escape(uk)}",
        filename="slowo.ogg", slow=slow,
        reply_markup=_word_speed_kb(rid, si, wi, slow=slow),
    )
    if msg is None:
        await cb.message.answer("Не вдалось озвучити 😔")
        return
    await tts_say.remember_voice(cb.message.chat.id, msg.message_id)
