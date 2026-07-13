"""Спільний рушій MCQ-вікторин (placement/drills/mock/listening).

Прибирає дублювання двох повторюваних кроків:
  • read_answer — парсинг callback + guard проти стале/дубльованої кнопки (усі 4);
  • show_verdict — «картка розбору» + фідбек ✔️/❌ (drills/mock/listening; placement
    без миттєвого вердикту — лише діагностика).
Кожен хендлер лишає власну логіку просування/фіналізації.
Callback формат: '<prefix>:ans:<qidx>:<option>'.
"""

from __future__ import annotations

import html
from contextlib import suppress

from aiogram.types import CallbackQuery, ReactionTypeEmoji


def parse_answer(data: str) -> tuple[int, int] | None:
    """'<prefix>:ans:<qidx>:<opt>' → (qidx, opt); None, якщо формат не той (стара кнопка)."""
    parts = data.split(":")
    if len(parts) != 4:
        return None
    try:
        return int(parts[2]), int(parts[3])
    except ValueError:
        return None


def verdict_card(question: str, chosen: int, correct: int, options: list[str], explain: str) -> str:
    """Текст питання, що перетворюється на «розібрану картку» після відповіді.
    Завжди показує ОБРАНУ відповідь (щоб учень бачив свій вибір), тоді вердикт."""
    yours = html.escape(options[chosen]) if 0 <= chosen < len(options) else "—"
    if chosen == correct:
        body = f"🔵 Твій вибір: <b>{yours}</b> — ✔️ <b>Dobrze!</b>"
    else:
        body = (
            f"🔵 Твій вибір: <b>{yours}</b> — ❌\n"
            f"✅ Poprawnie: <b>{html.escape(options[correct])}</b>"
        )
    exp = f"\n💡 {html.escape(explain)}" if explain else ""
    return f"{html.escape(question)}\n\n{body}{exp}"


async def show_choice(cb: CallbackQuery, opt_idx: int) -> None:
    """Показати ОБРАНУ відповідь у флоу БЕЗ вердикту (стартовий тест / повний мок) і
    прибрати клавіатуру. Текст опції беремо з кнопки повідомлення — універсально."""
    chosen = ""
    mk = getattr(cb.message, "reply_markup", None)
    if mk and mk.inline_keyboard and 0 <= opt_idx < len(mk.inline_keyboard) and mk.inline_keyboard[opt_idx]:
        chosen = mk.inline_keyboard[opt_idx][0].text
    with suppress(Exception):
        base = cb.message.html_text or ""
        tail = f"\n\n🔵 Твій вибір: <b>{html.escape(chosen)}</b>" if chosen else ""
        await cb.message.edit_text(base + tail, reply_markup=None)


async def read_answer(cb: CallbackQuery, current_pos: int) -> int | None:
    """Парсить callback і перевіряє актуальність питання.

    Повертає обрану опцію (int), якщо на неї можна реагувати; None — якщо кнопка
    стара/дубльована/зіпсована (у цьому разі cb.answer уже викликано — хендлер має return).
    """
    ans = parse_answer(cb.data or "")
    if ans is None:
        await cb.answer()
        return None
    qidx, chosen = ans
    if qidx != current_pos:  # дубль/стале питання (напр., подвійний тап по старій кнопці)
        await cb.answer("Це питання вже пройдено 🙂")
        with suppress(Exception):
            await cb.message.edit_reply_markup(reply_markup=None)
        return None
    return chosen


async def show_verdict(
    cb: CallbackQuery, chosen: int, correct: int, options: list[str], question: str, explain: str
) -> bool:
    """Перетворює питання на картку розбору + фідбек ✔️/❌. Повертає, чи правильно."""
    ok = chosen == correct
    await cb.message.edit_text(verdict_card(question, chosen, correct, options, explain))
    await cb.answer("✔️" if ok else "❌")
    if ok:  # маленька гейміфікація — реакція на правильну відповідь
        with suppress(Exception):
            await cb.bot.set_message_reaction(
                cb.message.chat.id, cb.message.message_id, [ReactionTypeEmoji(emoji="🔥")]
            )
    return ok
