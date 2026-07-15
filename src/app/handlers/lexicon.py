"""Тематичний словник: тема → підтема → огляд / флешкарти / гуртом у SRS + пошук.

Пресінгу немає: не рухає готовність/ціль. «➕ У словник» додає в SRS (потім /powtorki).
🔊 — вимова (спільний say-хендлер). Слова AI-генеруються на підтему й кешуються.
"""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings
from app.integrations import tts
from app.services import clock, lexicon, tts_say, uxlock, vocab

router = Router()

_OV_PAGE = 12  # слів на сторінку огляду


class Lexicon(StatesGroup):
    browsing = State()  # флешкарти


class LexEdit(StatesGroup):
    waiting = State()  # адмін вводить виправлений переклад (topic/sub/pl/idx у data)


def _is_admin(chat_id: int) -> bool:
    return bool(settings.admin_id) and chat_id == settings.admin_id


# ---------- теми ----------


async def _send_topics(message: Message) -> None:
    kb = InlineKeyboardBuilder()
    for key, lbl in lexicon.TOPICS:
        kb.button(text=f"{lbl} ({len(lexicon.subtopics(key))})", callback_data=f"lex:t:{key}")
    kb.button(text="🔎 Пошук слова", callback_data="lex:searchhint")
    kb.button(text="⬅️ Меню", callback_data="menu:home")
    kb.adjust(1)
    await message.answer(
        "📚 <b>Словник за темами</b> — вчи слова коли є хвилинка (у черзі, на лавці…).\n"
        "12 тем · сотні слів. Обери тему, тоді підтему.\n"
        "🔎 Або знайди слово: <code>/szukaj &lt;слово&gt;</code>",
        reply_markup=kb.as_markup(),
    )


@router.message(Command("slownik"))
async def cmd_lexicon(message: Message, state: FSMContext) -> None:
    await state.clear()
    await _send_topics(message)


@router.callback_query(F.data == "lex:open")
@router.callback_query(F.data == "lex:topics")
async def cb_topics(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await _send_topics(cb.message)


# ---------- підтеми (з прогресом) ----------


async def _send_subtopics(message: Message, user_id: int, topic: str) -> None:
    kb = InlineKeyboardBuilder()
    for sub_key, sub_lbl in lexicon.subtopics(topic):
        words = await lexicon.cached_words(topic, sub_key)  # без генерації
        suffix = ""
        if words:
            in_deck = len(await vocab.has_words(user_id, [w.pl for w in words]))
            suffix = f" · 📥 {in_deck}/{len(words)}"
        kb.button(text=f"{sub_lbl}{suffix}", callback_data=f"lex:s:{topic}:{sub_key}")
    kb.button(text="⬅️ Теми", callback_data="lex:topics")
    kb.adjust(1)
    await message.answer(
        f"📚 <b>{lexicon.topic_label(topic)}</b>\nОбери підтему (📥 — скільки вже у твоєму словнику):",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("lex:t:"))
async def cb_topic(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await _send_subtopics(cb.message, cb.from_user.id, cb.data.split(":", 2)[2])


# ---------- підтема: вибір режиму ----------


async def _send_subtopic(message: Message, user_id: int, topic: str, sub: str) -> None:
    status = await message.answer("⏳ Готую слова…")
    async with uxlock.typing(message.bot, message.chat.id):
        words = await lexicon.words_for(topic, sub)
    if not words:
        await status.edit_text(
            "😔 Не вдалося завантажити слова. Спробуй пізніше.",
            reply_markup=_back_kb(f"lex:t:{topic}", "⬅️ Підтеми"),
        )
        return
    in_deck = len(await vocab.has_words(user_id, [w.pl for w in words]))
    kb = InlineKeyboardBuilder()
    kb.button(text="📖 Огляд (список)", callback_data=f"lex:ov:{topic}:{sub}:0")
    kb.button(text="🎴 Флешкарти", callback_data=f"lex:fc:{topic}:{sub}")
    kb.button(text=f"➕ Додати всі {len(words)} у словник", callback_data=f"lex:aa:{topic}:{sub}")
    kb.button(text="⬅️ Підтеми", callback_data=f"lex:t:{topic}")
    kb.adjust(1)
    await status.edit_text(
        f"📚 <b>{lexicon.topic_label(topic)} · {lexicon.sub_label(topic, sub)}</b>\n"
        f"📊 {len(words)} слів · 📥 {in_deck} вже у твоєму словнику\n\nЯк вчимо?",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("lex:s:"))
async def cb_subtopic(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    _, _, topic, sub = cb.data.split(":")
    await _send_subtopic(cb.message, cb.from_user.id, topic, sub)


# ---------- огляд (список із перекладами, сторінками) ----------


@router.callback_query(F.data.startswith("lex:ov:"))
async def cb_overview(cb: CallbackQuery) -> None:
    await cb.answer()
    _, _, topic, sub, page_s = cb.data.split(":")
    page = int(page_s)
    words = await lexicon.words_for(topic, sub)
    if not words:
        return
    pages = (len(words) + _OV_PAGE - 1) // _OV_PAGE
    page = max(0, min(page, pages - 1))
    chunk = words[page * _OV_PAGE : (page + 1) * _OV_PAGE]
    lines = [f"📖 <b>{lexicon.sub_label(topic, sub)}</b> · стор. {page + 1}/{pages}\n"]
    for i, w in enumerate(chunk, start=page * _OV_PAGE + 1):
        ex = f"\n   <i>{html.escape(w.example)}</i>" if w.example else ""
        lines.append(f"{i}. 🇵🇱 <b>{html.escape(w.pl)}</b> — {html.escape(w.ua)}{ex}")
    kb = InlineKeyboardBuilder()
    if page > 0:
        kb.button(text="◀️", callback_data=f"lex:ov:{topic}:{sub}:{page - 1}")
    if page < pages - 1:
        kb.button(text="▶️", callback_data=f"lex:ov:{topic}:{sub}:{page + 1}")
    kb.button(text="➕ Додати всі у словник", callback_data=f"lex:aa:{topic}:{sub}")
    kb.button(text="🎴 Флешкарти", callback_data=f"lex:fc:{topic}:{sub}")
    kb.button(text="⬅️ Підтема", callback_data=f"lex:s:{topic}:{sub}")
    kb.adjust(2, 1, 1, 1)
    with _suppress():
        await cb.message.edit_text("\n".join(lines), reply_markup=kb.as_markup())


# ---------- гуртове додавання ----------


@router.callback_query(F.data.startswith("lex:aa:"))
async def cb_add_all(cb: CallbackQuery) -> None:
    _, _, topic, sub = cb.data.split(":")
    words = await lexicon.words_for(topic, sub)
    added = await vocab.add_many(
        cb.from_user.id, [(w.pl, w.ua) for w in words], clock.today_local()
    )
    await cb.answer(
        f"➕ Додано {added} нових слів у словник!" if added else "Усі слова вже у твоєму словнику 🙂",
        show_alert=True,
    )


# ---------- флешкарти ----------


@router.callback_query(F.data.startswith("lex:fc:"))
async def cb_flashcards(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    _, _, topic, sub = cb.data.split(":")
    words = await lexicon.words_for(topic, sub)
    if not words:
        return
    await state.set_state(Lexicon.browsing)
    await state.update_data(topic=topic, sub=sub, words=[w.__dict__ for w in words], idx=0)
    await _render_card(cb.message, state, reveal=False, fresh=True)


async def _render_card(msg: Message, state: FSMContext, reveal: bool, fresh: bool = False) -> None:
    await tts_say.forget_voice(msg.bot, msg.chat.id)
    data = await state.get_data()
    words, idx, topic, sub = data["words"], data["idx"], data["topic"], data["sub"]
    w = words[idx]
    stars = "★" * w["level"] + "☆" * (3 - w["level"])
    head = f"🎴 <b>{lexicon.sub_label(topic, sub)}</b> · {idx + 1}/{len(words)} · {stars}"
    kb = InlineKeyboardBuilder()
    if tts.available():
        kb.button(text="🔊 Вимова", callback_data=f"say:{await tts_say.stash(w['pl'])}")
    if reveal:
        body = f"🇵🇱 <b>{html.escape(w['pl'])}</b> — {html.escape(w['ua'])}"
        if w["example"]:
            body += f"\n📌 <i>{html.escape(w['example'])}</i>"
        body += "\n\n<b>➕ Додай у словник</b>, щоб повторити пізніше, або <b>➡️ Далі</b>."
        kb.button(text="➕ У мій словник", callback_data="lex:add")
        kb.button(text="➡️ Далі", callback_data="lex:next")
        if _is_admin(msg.chat.id):  # адмін-редагування AI-перекладу прямо з картки
            kb.button(text="✏️ Виправити", callback_data="lex:edit")
            kb.button(text="🗑 Прибрати", callback_data="lex:del")
    else:
        body = (
            f"🇵🇱 <b>{html.escape(w['pl'])}</b>\n\n"
            "🧠 Згадай переклад, послухай вимову — тоді <b>👁 Показати переклад</b>."
        )
        kb.button(text="👁 Показати переклад", callback_data="lex:show")
        kb.button(text="➡️ Далі", callback_data="lex:next")
    kb.button(text="⬅️ Підтема", callback_data=f"lex:s:{topic}:{sub}")
    kb.adjust(1)
    text = f"{head}\n\n{body}"
    if fresh:
        await msg.answer(text, reply_markup=kb.as_markup())
    else:
        with _suppress():
            await msg.edit_text(text, reply_markup=kb.as_markup())


@router.callback_query(Lexicon.browsing, F.data == "lex:show")
async def cb_show(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _render_card(cb.message, state, reveal=True)


async def _advance(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    idx = data["idx"] + 1
    if idx >= len(data["words"]):
        await state.clear()
        kb = InlineKeyboardBuilder()
        kb.button(text="➕ Додати всю підтему", callback_data=f"lex:aa:{data['topic']}:{data['sub']}")
        kb.button(text="🔁 Спочатку", callback_data=f"lex:fc:{data['topic']}:{data['sub']}")
        kb.button(text="⬅️ Підтеми", callback_data=f"lex:t:{data['topic']}")
        kb.adjust(1)
        with _suppress():
            await cb.message.edit_text(
                "🎉 <b>Підтему пройдено!</b> Додані слова чекають у /powtorki 🔁",
                reply_markup=kb.as_markup(),
            )
        return
    await state.update_data(idx=idx)
    await _render_card(cb.message, state, reveal=False)


@router.callback_query(Lexicon.browsing, F.data == "lex:next")
async def cb_next(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    await _advance(cb, state)


@router.callback_query(Lexicon.browsing, F.data == "lex:add")
async def cb_add(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    w = data["words"][data["idx"]]
    added = await vocab.add(cb.from_user.id, w["pl"], w["ua"], clock.today_local())
    await cb.answer("Додано в словник ✅" if added else "Вже у твоєму словнику 🙂")
    await _advance(cb, state)


# ---------- адмін: виправлення / видалення слова (правки AI-перекладу) ----------


@router.callback_query(Lexicon.browsing, F.data == "lex:edit")
async def cb_edit(cb: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише для адміна", show_alert=True)
        return
    data = await state.get_data()
    w = data["words"][data["idx"]]
    await state.set_state(LexEdit.waiting)
    await state.update_data(edit_pl=w["pl"])  # решта (topic/sub/words/idx) лишається в data
    await cb.answer()
    await cb.message.answer(
        f"✏️ Виправлення «<b>{html.escape(w['pl'])}</b>» (зараз: {html.escape(w['ua'])}).\n"
        "Надішли новий переклад. Можна з прикладом через <code>|</code>:\n"
        "<code>переклад | приклад польською</code>\n<i>/anuluj — скасувати.</i>"
    )


@router.message(LexEdit.waiting, F.text, ~F.text.startswith("/"))
async def on_edit_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    topic, sub, pl = data["topic"], data["sub"], data["edit_pl"]
    parts = [p.strip() for p in (message.text or "").split("|", 1)]
    ua = parts[0]
    example = parts[1] if len(parts) == 2 else None
    ok = await lexicon.edit_word(topic, sub, pl, ua, example)
    if ok:  # оновити й знімок у FSM, щоб картка одразу показала нове
        words = data["words"]
        for wd in words:
            if wd["pl"] == pl:
                wd["ua"] = ua
                if example is not None:
                    wd["example"] = example
                break
        await state.update_data(words=words)
    await state.set_state(Lexicon.browsing)
    await message.answer("✅ Виправлено." if ok else "😔 Слово не знайдено в кеші.")
    await _render_card(message, state, reveal=True, fresh=True)


@router.callback_query(Lexicon.browsing, F.data == "lex:del")
async def cb_del(cb: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише для адміна", show_alert=True)
        return
    data = await state.get_data()
    idx, words = data["idx"], data["words"]
    w = words[idx]
    await lexicon.remove_word(data["topic"], data["sub"], w["pl"])
    words.pop(idx)
    await cb.answer("🗑 Прибрано")
    if not words:
        await state.clear()
        with _suppress():
            await cb.message.edit_text("Слів у підтемі не лишилось.", reply_markup=_back_kb(
                f"lex:t:{data['topic']}", "⬅️ Підтеми"))
        return
    await state.update_data(words=words, idx=min(idx, len(words) - 1))
    await _render_card(cb.message, state, reveal=False)


# ---------- пошук ----------


@router.callback_query(F.data == "lex:searchhint")
async def cb_search_hint(cb: CallbackQuery) -> None:
    await cb.answer(
        "Надішли: /szukaj <слово> — знайду серед уже відкритих тем 🔎", show_alert=True
    )


@router.message(Command("szukaj"))
async def cmd_search(message: Message, command: CommandObject) -> None:
    query = (command.args or "").strip()
    if len(query) < 2:
        await message.answer("🔎 Приклад: <code>/szukaj książka</code> або <code>/szukaj книга</code>")
        return
    results = await lexicon.search(query)
    if not results:
        await message.answer(
            "😔 Нічого не знайшов серед уже відкритих тем. Пошук працює по темах, які ти вже "
            "відкривав — спершу зайди у кілька тем, щоб наповнити словник.",
        )
        return
    lines = [f"🔎 <b>Знайдено ({len(results)})</b> за «{html.escape(query)}»:\n"]
    for w, topic, sub in results:
        lines.append(
            f"🇵🇱 <b>{html.escape(w.pl)}</b> — {html.escape(w.ua)}  "
            f"<i>({lexicon.topic_label(topic)} · {lexicon.sub_label(topic, sub)})</i>"
        )
    await message.answer("\n".join(lines))


# ---------- утиліти ----------


def _back_kb(cb_data: str, label: str) -> object:
    kb = InlineKeyboardBuilder()
    kb.button(text=label, callback_data=cb_data)
    kb.adjust(1)
    return kb.as_markup()


def _suppress():  # noqa: ANN202 — контекст-менеджер придушення «message not modified» тощо
    from contextlib import suppress

    return suppress(Exception)
