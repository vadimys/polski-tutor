"""Повний мок іспиту (/egzamin) — усі авто-оцінювані завдання ПОСЛІДОВНО, режим іспиту.

Відмінність від /mok (окремі секції з миттєвим фідбеком): тут — без підказок і
вердиктів під час; відповіді фіксуються, результат у балах — у кінці. Найближче до
реальних умов. Включає ВСІ типи завдань офіційного тесту:
  • MCQ (a/b/c, TAK/NIE, luki) — вибір кнопкою;
  • matching (dopasowanie) — літерні кнопки (фрагменти показані раз);
  • free-fill (впиши форму) — відповідь текстом;
  • open (трансформація) — відповідь текстом, оцінює AI за офіц. зразком (self-check,
    якщо AI недоступний → поза балами).
Записує складання моку (гейт готовності) і помилки в колоду. Продуктивні модулі
(письмо/мовлення) — окремо.
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
from app.bot.keyboards import exam_kb, exam_match_kb, exam_text_kb, menu_kb, to_menu_kb
from app.integrations import ai, tts
from app.services import (
    exam_scale,
    freefill,
    goals,
    limits,
    listening,
    mistakes,
    opencheck,
    progress,
)
from app.services import state as user_state

router = Router()

_LABEL = {"sluchanie": "🎧 Аудіювання", "czytanie": "📖 Читання", "gramatyka": "🔤 Граматика"}
_TEXT_STEPS = ("fill", "open")  # кроки з текстовим вводом


class Exam(StatesGroup):
    active = State()


# ── побудова послідовності кроків ────────────────────────────────────────
def _build_seq(exam_id: str) -> list[dict]:
    """Кроки моку: спершу аудіювання (Słuchanie), тоді MCQ по секціях, далі таски."""
    seq: list[dict] = []
    # аудіювання першим — як у реальному іспиті (Rozumienie ze słuchu — модуль 1)
    for ex_id in content.exam_listening_ids(exam_id):
        ex = listening.by_id(ex_id)
        if not ex:
            continue
        for si, seg in enumerate(ex.segments):
            for qi in range(len(seg.questions)):
                seq.append({"t": "listen", "sec": "sluchanie", "ex": ex_id, "si": si, "qi": qi})
    for sec in content.exam_sections(exam_id):
        for i in range(len(content.exam_items(exam_id, sec))):
            seq.append({"t": "mcq", "sec": sec, "i": i})
    for ti, t in enumerate(content.exam_match_tasks(exam_id)):
        for gi in range(len(t.prompts)):
            seq.append({"t": "match", "sec": t.section, "ti": ti, "gi": gi})
    for ti, t in enumerate(content.exam_fill_tasks(exam_id)):
        for gi in range(len(t.prompts)):
            seq.append({"t": "fill", "sec": t.section, "ti": ti, "gi": gi})
    for ti, t in enumerate(content.exam_open_tasks(exam_id)):
        for gi in range(len(t.prompts)):
            seq.append({"t": "open", "sec": t.section, "ti": ti, "gi": gi})
    return seq


def _seq_sections(seq: list[dict]) -> list[str]:
    out: list[str] = []
    for step in seq:
        if step["sec"] not in out:
            out.append(step["sec"])
    return out


# ── інтро ────────────────────────────────────────────────────────────────
@router.message(Command("egzamin"))
async def cmd_exam(message: Message) -> None:
    await _intro(message)


@router.callback_query(F.data == "exam:open")
async def cb_open(cb: CallbackQuery) -> None:
    await cb.answer()
    await _intro(cb.message)


async def _intro(message: Message) -> None:
    exam = content.latest()  # тренуємось на найновішому повному офіційному тесті
    seq = _build_seq(exam.id)
    if not seq:
        await message.answer("Повний мок тимчасово недоступний.", reply_markup=to_menu_kb())
        return
    labels = " → ".join(_LABEL[s] for s in _seq_sections(seq))
    b = InlineKeyboardBuilder()
    b.button(text=f"▶️ Почати ({exam.label})", callback_data=f"exam:begin:{exam.id}")
    if len(content.all_exams()) > 1:
        b.button(text="📚 Обрати інший тест", callback_data="exam:pick")
    b.button(text="⬅️ Меню", callback_data="menu:home")
    b.adjust(1)
    await message.answer(
        f"🎓 <b>Повний мок іспиту</b>\nЗа замовчуванням — найновіший: <b>{exam.label}</b>\n\n"
        f"Секції: {labels} — <b>{len(seq)}</b> завдань (усі типи: 🎧 аудіо-записи, вибір, "
        "зіставлення, форми, трансформації).\n"
        "⏱ Режим іспиту: <b>без підказок і вердиктів</b>, результат у балах — у кінці. "
        "Виділи ~90–120 хв і не відволікайся.\n"
        "<i>Письмо й мовлення оцінюються окремо (/pisanie, /mowienie).</i>",
        reply_markup=b.as_markup(),
    )


@router.callback_query(F.data == "exam:pick")
async def cb_pick(cb: CallbackQuery) -> None:
    await cb.answer()
    b = InlineKeyboardBuilder()
    for e in content.all_exams():  # найновіші спершу
        n = len(_build_seq(e.id))
        secs = "".join(_LABEL[s].split()[0] for s in _seq_sections(_build_seq(e.id)))  # емодзі секцій
        b.button(text=f"{e.label} · {n} зав. {secs}", callback_data=f"exam:begin:{e.id}")
    b.button(text="⬅️ Меню", callback_data="menu:home")
    b.adjust(1)
    await cb.message.answer(
        "📚 <b>Обери тест для повного моку</b>\n"
        "Кожен — окремий офіційний тест Держкомісії. Тренуватись корисно на всіх.",
        reply_markup=b.as_markup(),
    )


@router.callback_query(F.data.startswith("exam:begin:"))
async def cb_begin(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()
    exam_id = cb.data.split(":", 2)[2]
    seq = _build_seq(exam_id)
    if not seq:
        await cb.message.answer("Цей тест тимчасово недоступний.", reply_markup=to_menu_kb())
        return
    await state.set_state(Exam.active)
    await state.update_data(exam_id=exam_id, seq=seq, pos=0, answers={})
    await _send_step(cb.message, exam_id, seq, 0)


# ── аудіо-запис сегмента (piper TTS) ─────────────────────────────────────────
async def _play_audio(message: Message, text: str) -> None:
    """Озвучує запис сегмента; якщо TTS недоступний — показує транскрипт (деградація)."""
    from aiogram.types import BufferedInputFile

    data = await tts.synthesize(text)
    if data:
        await message.answer_voice(
            BufferedInputFile(data, filename="egzamin.ogg"),
            caption="🎧 Прослухай запис, тоді відповідай на питання нижче.",
        )
    else:
        await message.answer(f"🔇 <i>(аудіо недоступне — прочитай транскрипт)</i>\n\n{html.escape(text)}")


# ── показ кроку ────────────────────────────────────────────────────────────
async def _send_step(message: Message, exam_id: str, seq: list[dict], pos: int) -> None:
    step = seq[pos]
    sec, head = step["sec"], f"🎓 <b>Мок · {_LABEL[step['sec']]}</b> · {pos + 1}/{len(seq)}"

    # преамбула аудіо-вправи (назва/інструкція — раз) + запис перед першим питанням сегмента
    if step["t"] == "listen":
        ex = listening.by_id(step["ex"])
        if ex and step["si"] == 0 and step["qi"] == 0:
            await message.answer(f"🎧 <b>{html.escape(ex.title)}</b>\n\n{ex.intro}")
        if ex and step["qi"] == 0:
            await _play_audio(message, ex.segments[step["si"]].audio)

    # преамбула на початку структурованого таска (показуємо опору один раз)
    if step["t"] == "match" and step["gi"] == 0:
        t = content.exam_match_tasks(exam_id)[step["ti"]]
        opts = "\n".join(f"<b>{chr(65 + i)})</b> {html.escape(o)}" for i, o in enumerate(t.options))
        await message.answer(f"🧩 <b>{html.escape(t.title)}</b>\n\n{t.intro}\n\n🔤 <b>Фрагменти:</b>\n{opts}")
    elif step["t"] in _TEXT_STEPS and step["gi"] == 0:
        tasks = content.exam_fill_tasks(exam_id) if step["t"] == "fill" else content.exam_open_tasks(exam_id)
        t = tasks[step["ti"]]
        icon = "✏️" if step["t"] == "fill" else "🔄"
        await message.answer(f"{icon} <b>{html.escape(t.title)}</b>\n\n{t.intro}")

    if step["t"] == "listen":
        q = listening.by_id(step["ex"]).segments[step["si"]].questions[step["qi"]]
        await message.answer(f"{head}\n\n🎧 {html.escape(q.text)}", reply_markup=exam_kb(q.options, pos))
    elif step["t"] == "mcq":
        it = content.exam_items(exam_id, sec)[step["i"]]
        ctx = f"<i>{html.escape(it.context)}</i>\n\n" if it.context else ""
        await message.answer(f"{head}\n\n{ctx}{html.escape(it.question)}", reply_markup=exam_kb(it.options, pos))
    elif step["t"] == "match":
        t = content.exam_match_tasks(exam_id)[step["ti"]]
        await message.answer(
            f"{head}\n\n🧩 {html.escape(t.prompts[step['gi']])}\n\n<i>Обери фрагмент (літера):</i>",
            reply_markup=exam_match_kb(len(t.options), pos),
        )
    elif step["t"] == "fill":
        t = content.exam_fill_tasks(exam_id)[step["ti"]]
        await message.answer(
            f"{head}\n\n✏️ {html.escape(t.prompts[step['gi']])}\n\n<i>Напиши форму текстом:</i>",
            reply_markup=exam_text_kb(pos),
        )
    else:  # open
        t = content.exam_open_tasks(exam_id)[step["ti"]]
        gi = step["gi"]
        await message.answer(
            f"{head}\n\n🔄 {html.escape(t.prompts[gi])}\n🔑 Вжий: <b>{html.escape(t.words[gi])}</b>\n\n"
            "<i>Напиши перетворене речення:</i>",
            reply_markup=exam_text_kb(pos),
        )


# ── ввід відповідей ────────────────────────────────────────────────────────
async def _advance(message: Message, user_id: int, state: FSMContext) -> None:
    data = await state.get_data()
    pos = data["pos"] + 1
    await state.update_data(pos=pos)
    if pos < len(data["seq"]):
        await _send_step(message, data["exam_id"], data["seq"], pos)
    else:
        await _finalize(message, user_id, state)


@router.callback_query(Exam.active, F.data == "ex:stop")
async def cb_stop(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer("Мок припинено")
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "⏹ Мок припинено достроково — <b>без оцінки</b> (повний мок рахується лише цілком).",
        reply_markup=to_menu_kb(),
    )


@router.callback_query(Exam.active, F.data.startswith("ex:ans:"))
async def cb_answer(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    pos, seq = data["pos"], data["seq"]
    parts = (cb.data or "").split(":")
    if len(parts) != 4 or not parts[3].isdigit() or int(parts[2]) != pos:
        await cb.answer("Це питання вже пройдено 🙂")
        with suppress(Exception):
            await cb.message.edit_reply_markup(reply_markup=None)
        return
    if seq[pos]["t"] in _TEXT_STEPS:  # тут очікуємо текст, не кнопку
        await cb.answer("Тут напиши відповідь текстом ✍️")
        return
    answers = data["answers"]
    answers[str(pos)] = int(parts[3])
    await state.update_data(answers=answers)
    await cb.answer()
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    await _advance(cb.message, cb.from_user.id, state)


@router.callback_query(Exam.active, F.data.startswith("ex:skip:"))
async def cb_skip(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    if int((cb.data or "0:0:0").split(":")[2]) != data["pos"]:
        await cb.answer("Це питання вже пройдено 🙂")
        return
    await cb.answer()
    with suppress(Exception):
        await cb.message.edit_reply_markup(reply_markup=None)
    answers = data["answers"]
    answers[str(data["pos"])] = ""  # пропущено
    await state.update_data(answers=answers)
    await _advance(cb.message, cb.from_user.id, state)


@router.message(Exam.active, F.text)
async def on_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    pos, seq = data["pos"], data["seq"]
    if seq[pos]["t"] not in _TEXT_STEPS:  # тут очікуємо вибір кнопкою
        await message.answer("На це питання обери варіант кнопкою вище 👆")
        return
    answers = data["answers"]
    answers[str(pos)] = (message.text or "").strip()
    await state.update_data(answers=answers)
    await _advance(message, message.from_user.id, state)


# ── підрахунок і звіт ──────────────────────────────────────────────────────
async def _finalize(message: Message, user_id: int, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    exam_id, seq, answers = data["exam_id"], data["seq"], data["answers"]

    correct: dict[str, int] = {}
    total: dict[str, int] = {}
    open_note = False

    # спершу оцінюємо open-таски пакетно (1 виклик AI на таск)
    open_ok = await _grade_open(user_id, exam_id, seq, answers)
    if open_ok is None and any(s["t"] == "open" for s in seq):
        open_note = True  # AI недоступний → open поза балами

    for pos, step in enumerate(seq):
        sec = step["sec"]
        ans = answers.get(str(pos))
        if step["t"] == "open":
            if open_ok is None:
                continue  # не рахуємо (поза балами)
            total[sec] = total.get(sec, 0) + 1
            if open_ok.get(pos):
                correct[sec] = correct.get(sec, 0) + 1
            continue
        total[sec] = total.get(sec, 0) + 1
        ok = _grade_closed(exam_id, step, ans)
        if ok:
            correct[sec] = correct.get(sec, 0) + 1
        else:
            await _record_mistake(user_id, exam_id, step)

    lines = ["🏁 <b>Повний мок — результат</b>\n"]
    all_pass = True
    for sec in _seq_sections(seq):
        tot = total.get(sec, 0)
        if not tot:
            continue
        got = correct.get(sec, 0)
        pct = round(got / tot * 100)
        await user_state.update_readiness(user_id, sec, pct)
        await progress.record_mock_pass(user_id, sec, pct)
        if pct < 50:
            all_pass = False
        lines.append(f"{_LABEL[sec]}: <b>{got}/{tot}</b> ({pct}%) · {exam_scale.module_line(sec, pct)}")

    verdict = (
        "🏆 <b>Усі секції — вище порога!</b> Так тримати — і продуктивні модулі не забувай."
        if all_pass
        else "💪 Є секції нижче 50% — попрацюй над ними (див. 🧯 помилки) і повтори мок."
    )
    lines.append(f"\n{verdict}")
    if open_note:
        lines.append("<i>ℹ️ Трансформації (open) не оцінено — AI недоступний. Порівняй зі зразком у /transformacje.</i>")
    lines.append("<i>Письмо й мовлення — окремо (/pisanie, /mowienie).</i>")
    await message.answer("\n".join(lines), reply_markup=menu_kb())
    if c := await goals.pop_celebration(user_id):
        await message.answer(c)


def _grade_closed(exam_id: str, step: dict, ans) -> bool:
    """Оцінка закритого кроку (listen/mcq/match/fill)."""
    if step["t"] == "listen":
        q = listening.by_id(step["ex"]).segments[step["si"]].questions[step["qi"]]
        return ans == q.correct
    if step["t"] == "mcq":
        it = content.exam_items(exam_id, step["sec"])[step["i"]]
        return ans == it.correct
    if step["t"] == "match":
        t = content.exam_match_tasks(exam_id)[step["ti"]]
        return ans == t.key[step["gi"]]
    if step["t"] == "fill":
        t = content.exam_fill_tasks(exam_id)[step["ti"]]
        return freefill.is_correct(ans or "", t.accepted[step["gi"]])
    return False


async def _grade_open(user_id: int, exam_id: str, seq: list[dict], answers: dict) -> dict | None:
    """Пакетна AI-оцінка всіх open-кроків. → {pos: ok} або None (AI недоступний/збій)."""
    open_steps = [(pos, s) for pos, s in enumerate(seq) if s["t"] == "open"]
    if not open_steps:
        return {}
    if not (ai.enabled() and await limits.allow_ai(user_id)):
        return None
    result: dict[int, bool] = {}
    ok_any = False
    by_task: dict[int, list[tuple[int, int]]] = {}  # ti → [(pos, gi)]
    for pos, s in open_steps:
        by_task.setdefault(s["ti"], []).append((pos, s["gi"]))
    for ti, entries in by_task.items():
        t = content.exam_open_tasks(exam_id)[ti]
        items = [
            {"n": gi + 1, "original": t.prompts[gi], "word": t.words[gi],
             "models": t.models[gi], "answer": answers.get(str(pos), "")}
            for pos, gi in entries
        ]
        graded = await opencheck.grade(items)
        if graded is None:
            continue  # цей таск не оцінено
        ok_any = True
        for (pos, _gi), g in zip(entries, graded, strict=False):
            result[pos] = g["ok"]
    if not ok_any:
        await limits.refund_ai(user_id)
        return None
    return result


async def _record_mistake(user_id: int, exam_id: str, step: dict) -> None:
    """Логуємо неправильні закриті питання в колоду (open/пропуски — без опцій — пропускаємо)."""
    if step["t"] == "listen":
        q = listening.by_id(step["ex"]).segments[step["si"]].questions[step["qi"]]
        await mistakes.add(user_id, step["sec"], q.text, list(q.options), q.correct, q.explain)
    elif step["t"] == "mcq":
        it = content.exam_items(exam_id, step["sec"])[step["i"]]
        await mistakes.add(user_id, step["sec"], it.question, list(it.options), it.correct, it.explain)
    elif step["t"] == "match":
        t = content.exam_match_tasks(exam_id)[step["ti"]]
        gi = step["gi"]
        await mistakes.add(
            user_id, step["sec"], t.prompts[gi], list(t.options), t.key[gi], t.explain[gi]
        )
