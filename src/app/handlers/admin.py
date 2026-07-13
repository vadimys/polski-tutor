"""Адмін: схвалення/відмова запитів на доступ + відповідь користувачу."""

from __future__ import annotations

import html
import logging
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import approved_kb, contact_admin_kb, teacher_welcome_kb
from app.config import settings
from app.services import access, admin_stats, broadcast, churn, events, resets, support, viewas
from app.services import state as user_state

router = Router()
logger = logging.getLogger(__name__)


class AdminMsg(StatesGroup):
    waiting = State()  # адмін пише повідомлення конкретному користувачу


class TicketReply(StatesGroup):
    waiting = State()  # адмін відповідає на тікет підтримки


class Broadcast(StatesGroup):
    text = State()  # адмін пише текст розсилки (сегмент уже обрано)


def _is_admin(user_id: int) -> bool:
    return bool(settings.admin_id) and user_id == settings.admin_id


# ── Адмін-консоль (/admin) — інлайн-хаб; префікс ac: (щоб не плутати з adm:) ──
def _hub_kb() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Огляд", callback_data="ac:overview")
    kb.button(text="👥 Користувачі", callback_data="ac:users:0")
    kb.button(text="🧑‍🎓 Сегменти", callback_data="ac:segments")
    kb.button(text="👩‍🏫 Викладачі", callback_data="ac:teachers")
    kb.button(text="📈 Аналітика", callback_data="ac:analytics")
    kb.button(text="🆘 Підтримка", callback_data="ac:support")
    kb.button(text="📣 Розсилка", callback_data="ac:bcast")
    kb.button(text="🧪 Режими", callback_data="ac:viewas")
    kb.button(text="🎓 Моє навчання", callback_data="ac:learn")
    kb.adjust(2)
    return kb


async def send_hub(message: Message) -> None:
    await message.answer(
        "🛠 <b>Адмін-консоль</b>\nКерування ботом, користувачі, підтримка, аналітика.\n"
        "🎓 <b>Моє навчання</b> — тренуватись як звичайний учень.",
        reply_markup=_hub_kb().as_markup(),
    )


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    await send_hub(message)


@router.callback_query(F.data == "ac:hub")
async def cb_hub(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    await send_hub(cb.message)


@router.callback_query(F.data == "ac:learn")
async def cb_learn(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Стартовий тест", callback_data="placement:start")
    kb.button(text="📋 Меню навчання", callback_data="menu:home")
    kb.button(text="♻️ Почати з нуля", callback_data=f"ac:resetask:{cb.from_user.id}")
    kb.button(text="🛠 Назад у панель", callback_data="ac:hub")
    kb.adjust(1)
    await cb.message.answer(
        "🎓 <b>Режим навчання</b> — тут ти звичайний учень (прогрес зараховується).\n"
        "Почни зі стартового тесту або відкрий меню. Можеш обнулити прогрес і почати з нуля 👇\n"
        "<i>Повернутись у панель будь-коли: /admin</i>",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data == "ac:overview")
async def cb_overview(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    d = await admin_stats.overview()
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Хаб", callback_data="ac:hub")
    await cb.message.answer(admin_stats.render_overview(d), reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("ac:users:"))
async def cb_users(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    offset = int(cb.data.split(":")[2])
    rows, total = await admin_stats.list_users(offset)
    kb = InlineKeyboardBuilder()
    for r in rows:
        kb.button(
            text=f"{admin_stats.role_emoji(r['role'])} {r['name']} · {r['overall']}% · {r['status']}",
            callback_data=f"ac:user:{r['id']}",
        )
    kb.adjust(1)
    nav = InlineKeyboardBuilder()
    if offset > 0:
        nav.button(text="⬅️", callback_data=f"ac:users:{max(0, offset - admin_stats.PAGE)}")
    if offset + admin_stats.PAGE < total:
        nav.button(text="➡️", callback_data=f"ac:users:{offset + admin_stats.PAGE}")
    nav.button(text="🛠 Хаб", callback_data="ac:hub")
    kb.attach(nav)
    shown = f"{offset + 1}–{min(offset + admin_stats.PAGE, total)}" if total else "0"
    await cb.message.answer(
        f"👥 <b>Користувачі</b> {shown} з <b>{total}</b>\nОбери, щоб відкрити картку:",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data == "ac:segments")
async def cb_segments(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    d = await admin_stats.segments()
    kb = InlineKeyboardBuilder()
    kb.button(text="🛠 Хаб", callback_data="ac:hub")
    await cb.message.answer(admin_stats.render_segments(d), reply_markup=kb.as_markup())


@router.callback_query(F.data == "ac:teachers")
async def cb_teachers(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    rows = await admin_stats.teachers()
    kb = InlineKeyboardBuilder()
    for t in rows:
        kb.button(
            text=f"👩‍🏫 {t['name']} · {t['n_students']} учнів · 💎{t['n_paying']}",
            callback_data=f"ac:group:{t['id']}",
        )
    kb.button(text="🛠 Хаб", callback_data="ac:hub")
    kb.adjust(1)
    head = f"👩‍🏫 <b>Викладачі</b> — {len(rows)}\nОбери, щоб побачити групу:" if rows else "👩‍🏫 Викладачів поки немає."
    await cb.message.answer(head, reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("ac:group:"))
async def cb_group(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    tid = int(cb.data.split(":")[2])
    d = await admin_stats.teacher_group(tid)
    if d is None:
        await cb.message.answer("Викладача не знайдено.")
        return
    kb = InlineKeyboardBuilder()
    for st in d["students"]:
        kb.button(text=f"👤 {st['name']} · {st['overall']}%", callback_data=f"ac:user:{st['id']}")
    kb.button(text="⬅️ Викладачі", callback_data="ac:teachers")
    kb.adjust(1)
    await cb.message.answer(admin_stats.render_group(d), reply_markup=kb.as_markup())


@router.callback_query(F.data == "ac:analytics")
async def cb_analytics(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    kb = InlineKeyboardBuilder()
    kb.button(text="📈 Фічі (увага)", callback_data="ac:an:feat")
    kb.button(text="🔻 Воронка", callback_data="ac:an:funnel")
    kb.button(text="🙅 Причини відмов", callback_data="ac:an:churn")
    kb.button(text="📉 Складність модулів", callback_data="ac:an:mods")
    kb.button(text="🛠 Хаб", callback_data="ac:hub")
    kb.adjust(1)
    await cb.message.answer(
        "📈 <b>Аналітика використання</b>\nЩо обрати:", reply_markup=kb.as_markup()
    )


@router.callback_query(F.data.startswith("ac:an:"))
async def cb_analytics_view(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    what = cb.data.split(":")[2]
    if what == "feat":
        text = admin_stats.render_features(await events.feature_report())
    elif what == "funnel":
        text = admin_stats.render_funnel(await admin_stats.funnel())
    elif what == "churn":
        text = admin_stats.render_churn(await churn.reasons_report())
    else:  # mods
        text = admin_stats.render_mods(await admin_stats.module_difficulty())
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Аналітика", callback_data="ac:analytics")
    await cb.message.answer(text, reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("ac:user:"))
async def cb_user_card(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    uid = int(cb.data.split(":")[2])
    d = await admin_stats.user_detail(uid)
    if d is None:
        await cb.message.answer("Користувача не знайдено.")
        return
    kb = InlineKeyboardBuilder()
    kb.button(text="✉️ Написати", callback_data=f"ac:msg:{uid}")
    kb.button(text="🔓 Продовжити доступ", callback_data=f"adm:extend:{uid}")
    kb.button(text="♻️ Reset прогресу", callback_data=f"ac:resetask:{uid}")
    kb.button(text="❌ Відмовити", callback_data=f"adm:no:{uid}")
    kb.button(text="⬅️ Список", callback_data="ac:users:0")
    kb.adjust(1)
    await cb.message.answer(admin_stats.render_user(d), reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("ac:msg:"))
async def cb_msg_start(cb: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    uid = int(cb.data.split(":")[2])
    await state.set_state(AdminMsg.waiting)
    await state.update_data(target=uid)
    await cb.answer()
    await cb.message.answer(f"✍️ Напиши повідомлення для користувача <code>{uid}</code> (одним повідомленням):")


@router.message(AdminMsg.waiting, F.text)
async def on_admin_msg(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        await state.clear()
        return
    data = await state.get_data()
    await state.clear()
    uid = int(data.get("target", 0))
    try:
        await message.bot.send_message(uid, f"✉️ <b>Адмін:</b> {html.escape(message.text or '')}")
        await message.answer("Надіслано ✅")
    except Exception:  # noqa: BLE001
        await message.answer("Не вдалося надіслати (користувач міг не активувати бота).")


@router.callback_query(F.data.startswith("adm:"))
async def cb_decision(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    try:
        _, action, suid = cb.data.split(":")
        uid = int(suid)
    except (ValueError, IndexError):
        await cb.answer()
        return

    if action == "teacher":
        until = await access.approve_teacher(uid)
        me = await cb.bot.get_me()
        link = f"https://t.me/{me.username}?start=t{uid}"
        await cb.message.edit_text(f"{cb.message.html_text}\n\n👩‍🏫 Схвалено як викладача (до {until}).")
        try:
            await cb.bot.send_message(
                uid,
                "👩‍🏫 <b>Вітаємо — ти партнер-викладач!</b>\n"
                f"Безкоштовний доступ активний до <b>{until}</b>.\n\n"
                "🔗 <b>Твоє реферальне посилання для учнів:</b>\n"
                f"<code>{link}</code>\n\n"
                "Учень, який зайде за ним, одразу отримає безкоштовний доступ на "
                f"<b>{settings.trial_days} днів</b>, а ти бачитимеш його прогрес у "
                "<b>/uczniowie</b> (твій клас). Ділись посиланням зі своїм класом! 🚀",
                reply_markup=teacher_welcome_kb(),
            )
        except Exception:  # noqa: BLE001
            pass
    elif action == "extend":
        until = await access.approve(uid)  # продовження: повне вікно (6 міс / до іспиту)
        inf = await access.info(uid)
        kb = teacher_welcome_kb() if inf.role == "teacher" else approved_kb()
        await cb.message.edit_text(f"{cb.message.html_text}\n\n🔓 Продовжено (до {until}).")
        try:
            await cb.bot.send_message(
                uid,
                f"🔓 <b>Доступ продовжено</b> до <b>{until}</b>! Продовжуймо підготовку 👇",
                reply_markup=kb,
            )
        except Exception:  # noqa: BLE001
            pass
    elif action == "ok":
        until = await access.approve(uid)
        await cb.message.edit_text(f"{cb.message.html_text}\n\n✅ Схвалено (доступ до {until}).")
        try:
            await cb.bot.send_message(
                uid,
                f"✅ <b>Доступ відкрито</b> до <b>{until}</b>! Починаймо 👇",
                reply_markup=approved_kb(),
            )
        except Exception:  # noqa: BLE001
            pass
    else:
        await access.deny(uid)
        await cb.message.edit_text(f"{cb.message.html_text}\n\n❌ Відмовлено.")
        try:
            await cb.bot.send_message(
                uid,
                "🚫 На жаль, у доступі відмовлено. Можеш написати адміну.",
                reply_markup=contact_admin_kb(),
            )
        except Exception:  # noqa: BLE001
            pass
    await cb.answer()


@router.message(Command("status"))
async def cmd_status(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    from sqlalchemy import func, select

    from app.db.base import session_factory
    from app.db.models import Session, User
    from app.integrations import speech, tts

    db_ok, users, sessions = True, 0, 0
    try:
        async with session_factory()() as s:
            users = (await s.execute(select(func.count()).select_from(User))).scalar() or 0
            sessions = (await s.execute(select(func.count()).select_from(Session))).scalar() or 0
    except Exception:  # noqa: BLE001
        db_ok = False
    await message.answer(
        "🩺 <b>Стан системи</b>\n"
        f"• PostgreSQL: {'✅' if db_ok else '❌'}\n"
        f"• Користувачів: <b>{users}</b> · вправ: <b>{sessions}</b>\n"
        f"• Whisper (голос): {'✅' if speech.available() else '❌'}\n"
        f"• Piper TTS (аудіо): {'✅' if tts.available() else '❌'}"
    )


@router.message(Command("reply"))
async def cmd_reply(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    parts = (message.text or "").split(maxsplit=2)
    if len(parts) < 3 or not parts[1].isdigit():
        await message.answer("Формат: <code>/reply &lt;id&gt; текст</code>")
        return
    uid, text = int(parts[1]), parts[2]
    try:
        await message.bot.send_message(uid, f"✉️ <b>Адмін:</b> {html.escape(text)}")
        await message.answer("Надіслано ✅")
    except Exception:  # noqa: BLE001
        await message.answer("Не вдалося надіслати (можливо, користувач не активний).")


# ── Повний reset прогресу — виконує ЛИШЕ адмін (за запитом користувача або з картки) ──
@router.callback_query(F.data.startswith("ac:resetask:"))
async def cb_reset_ask(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    uid = int(cb.data.split(":")[2])
    req = await resets.get(uid)
    reason = f"\nПричина: {html.escape(req[1])}" if req else ""
    who = "ТВІЙ прогрес" if uid == cb.from_user.id else f"прогрес користувача <code>{uid}</code>"
    kb = InlineKeyboardBuilder()
    kb.button(text="♻️ Так, обнулити", callback_data=f"ac:resetdo:{uid}")
    kb.button(text="↩️ Ні", callback_data="ac:hub")
    kb.adjust(1)
    await cb.message.answer(
        f"♻️ Обнулити {who}? Це <b>незворотно</b> (вправи/готовність/XP/помилки/слова)."
        f"{reason}",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("ac:resetdo:"))
async def cb_reset_do(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer("Обнулено")
    uid = int(cb.data.split(":")[2])
    await user_state.full_reset(uid)
    await resets.clear(uid)
    logger.info("full_reset by admin for uid=%s", uid)
    if uid == cb.from_user.id:  # адмін обнулив себе
        await cb.message.answer(
            "♻️ <b>Твій прогрес обнулено.</b> Починаємо з чистого аркуша — стартовий тест 👇",
            reply_markup=approved_kb(),
        )
    else:  # обнулили користувача за запитом
        try:
            await cb.bot.send_message(
                uid,
                "♻️ <b>Твій прогрес обнулено</b> за твоїм запитом. Починаємо з чистого аркуша!\n"
                "Почни зі стартового тесту (/test) 👇",
                reply_markup=approved_kb(),
            )
        except Exception:  # noqa: BLE001
            pass
        await cb.message.answer(f"♻️ Прогрес користувача <code>{uid}</code> обнулено.")


@router.callback_query(F.data.startswith("ac:resetno:"))
async def cb_reset_no(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer("Відхилено")
    uid = int(cb.data.split(":")[2])
    await resets.clear(uid)
    logger.info("reset request declined for uid=%s", uid)
    with suppress(Exception):
        await cb.bot.send_message(
            uid, "ℹ️ Запит на повне обнулення прогресу відхилено. Якщо потрібно — напиши адміну."
        )
    with suppress(Exception):
        await cb.message.edit_text(f"{cb.message.html_text}\n\n❌ Відхилено.")


# ── Support-inbox: черга звернень + відповідь у 1 тап ────────────────────────
@router.callback_query(F.data == "ac:support")
async def cb_support(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    tickets = await support.all_tickets(open_only=True)
    kb = InlineKeyboardBuilder()
    for tid, t in tickets[:20]:
        kb.button(
            text=f"🎫 #{tid} {support.cat_label(t['cat']).split()[0]} · {t['name']}",
            callback_data=f"ac:ticket:{tid}",
        )
    kb.button(text="🛠 Хаб", callback_data="ac:hub")
    kb.adjust(1)
    head = f"🆘 <b>Відкриті звернення</b> — {len(tickets)}\nОбери тікет:" if tickets else "🆘 Відкритих звернень немає ✅"
    await cb.message.answer(head, reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("ac:ticket:"))
async def cb_ticket(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    tid = int(cb.data.split(":")[2])
    t = await support.get(tid)
    if t is None:
        await cb.message.answer("Тікет не знайдено.")
        return
    kb = InlineKeyboardBuilder()
    kb.button(text="✉️ Відповісти", callback_data=f"ac:treply:{tid}")
    kb.button(text="☑️ Закрити", callback_data=f"ac:tclose:{tid}")
    kb.button(text="⬅️ Звернення", callback_data="ac:support")
    kb.adjust(1)
    await cb.message.answer(support.render_ticket(tid, t), reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("ac:treply:"))
async def cb_ticket_reply(cb: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    tid = int(cb.data.split(":")[2])
    await state.set_state(TicketReply.waiting)
    await state.update_data(tid=tid)
    await cb.answer()
    await cb.message.answer(f"✍️ Відповідь на тікет #{tid} (одним повідомленням):")


@router.message(TicketReply.waiting, F.text)
async def on_ticket_reply(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        await state.clear()
        return
    data = await state.get_data()
    await state.clear()
    tid = int(data.get("tid", 0))
    t = await support.get(tid)
    if not t:
        await message.answer("Тікет не знайдено.")
        return
    try:
        await message.bot.send_message(
            int(t["uid"]),
            f"✉️ <b>Відповідь підтримки</b> (звернення #{tid}):\n{html.escape(message.text or '')}",
        )
        await support.set_status(tid, "closed")
        await message.answer(f"Надіслано ✅ Тікет #{tid} закрито.")
    except Exception:  # noqa: BLE001
        await message.answer("Не вдалося надіслати (користувач міг не активувати бота).")


@router.callback_query(F.data.startswith("ac:tclose:"))
async def cb_ticket_close(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    tid = int(cb.data.split(":")[2])
    await support.set_status(tid, "closed")
    await cb.answer("Закрито")
    with suppress(Exception):
        await cb.message.edit_text(f"{cb.message.html_text}\n\n☑️ Закрито.")


# ── View-as: тестові режими (учень/викладач/референс) ────────────────────────
_VA_LABELS = {"student": "🎓 учень", "teacher": "👩‍🏫 викладач", "referred": "🎁 референс-учень"}


@router.callback_query(F.data == "ac:viewas")
async def cb_viewas(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    cur = await viewas.get(cb.from_user.id)
    now = f"Зараз: <b>{_VA_LABELS.get(cur, '—')}</b>" if cur else "Зараз: <b>адмін</b>"
    kb = InlineKeyboardBuilder()
    kb.button(text="🎓 Як учень", callback_data="ac:va:student")
    kb.button(text="👩‍🏫 Як викладач", callback_data="ac:va:teacher")
    kb.button(text="🎁 Як референс-учень", callback_data="ac:va:referred")
    kb.button(text="⏹ Вийти в адміна", callback_data="ac:va:off")
    kb.button(text="🛠 Хаб", callback_data="ac:hub")
    kb.adjust(1)
    await cb.message.answer(
        "🧪 <b>Тестові режими (view-as)</b>\n"
        f"{now}\n\n"
        "Перемикає, як бот <b>виглядає й поводиться</b> для тебе (меню, /start, /uczniowie, "
        "знижка реферала). Обери роль — далі тисни /start.\n"
        "<i>⚠️ Прогрес у тебе один: це тест UX/флоу, не окремі дані. Для ізольованих "
        "історій навчання — заведи вторинний Telegram-акаунт і зайди звичайним користувачем.</i>",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("ac:va:"))
async def cb_viewas_set(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    mode = cb.data.split(":")[2]
    if mode == "off":
        await viewas.clear(cb.from_user.id)
        await cb.answer("Вихід у адміна")
        await cb.message.answer("⏹ Режим перегляду вимкнено. Ти знову адмін — /admin.")
        return
    await viewas.set_mode(cb.from_user.id, mode)
    await cb.answer()
    await cb.message.answer(
        f"👁 Увімкнено режим: <b>{_VA_LABELS.get(mode, mode)}</b>.\n"
        "Тисни <b>/start</b>, щоб побачити досвід цієї ролі. Вийти — /admin → 🧪 Режими → «Вийти»."
    )


# ── Розсилка/оголошення по сегментах ─────────────────────────────────────────
@router.callback_query(F.data == "ac:bcast")
async def cb_bcast(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    kb = InlineKeyboardBuilder()
    for seg, lbl in broadcast.SEGMENTS.items():
        kb.button(text=lbl, callback_data=f"ac:bcseg:{seg}")
    kb.button(text="🛠 Хаб", callback_data="ac:hub")
    kb.adjust(2)
    await cb.message.answer(
        "📣 <b>Розсилка / оголошення</b>\nОбери кому надіслати:", reply_markup=kb.as_markup()
    )


@router.callback_query(F.data.startswith("ac:bcseg:"))
async def cb_bcast_seg(cb: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    seg = cb.data.split(":")[2]
    await state.set_state(Broadcast.text)
    await state.update_data(seg=seg)
    await cb.answer()
    await cb.message.answer(
        f"✍️ Напиши текст розсилки для «<b>{broadcast.label(seg)}</b>» (HTML можна). "
        "Надішли одним повідомленням — покажу прев'ю."
    )


@router.message(Broadcast.text, F.text)
async def on_bcast_text(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        await state.clear()
        return
    data = await state.get_data()
    seg = data.get("seg", "all")
    text = message.text or ""
    ids = await broadcast.recipients(seg)
    await state.update_data(text=text)  # сегмент уже є
    kb = InlineKeyboardBuilder()
    kb.button(text=f"✅ Надіслати ({len(ids)})", callback_data="ac:bcgo")
    kb.button(text="↩️ Скасувати", callback_data="ac:hub")
    kb.adjust(1)
    await message.answer(
        f"📣 <b>Прев'ю</b> · сегмент «{broadcast.label(seg)}» · отримувачів: <b>{len(ids)}</b>\n\n"
        f"{text}",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(Broadcast.text, F.data == "ac:bcgo")
async def cb_bcast_go(cb: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    data = await state.get_data()
    await state.clear()
    seg, text = data.get("seg", "all"), data.get("text", "")
    ids = await broadcast.recipients(seg)
    await cb.answer("Надсилаю…")
    sent, failed = await broadcast.send(cb.bot, ids, text)
    logger.info("broadcast seg=%s sent=%s failed=%s", seg, sent, failed)
    await cb.message.answer(f"📣 Готово: доставлено <b>{sent}</b> · не вдалося {failed}.")
