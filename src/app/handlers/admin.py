"""Адмін: схвалення/відмова запитів на доступ + відповідь користувачу."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import approved_kb, contact_admin_kb
from app.config import settings
from app.services import access, admin_stats

router = Router()


class AdminMsg(StatesGroup):
    waiting = State()  # адмін пише повідомлення конкретному користувачу


def _is_admin(user_id: int) -> bool:
    return bool(settings.admin_id) and user_id == settings.admin_id


# ── Адмін-консоль (/admin) — інлайн-хаб; префікс ac: (щоб не плутати з adm:) ──
def _hub_kb() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Огляд", callback_data="ac:overview")
    kb.button(text="👥 Користувачі", callback_data="ac:users:0")
    kb.adjust(2)
    return kb


async def _send_hub(message: Message) -> None:
    kb = _hub_kb()
    kb.row()  # (наступні розділи — сегменти/аналітика/підтримка/режими — додаються інкрементами)
    await message.answer(
        "🛠 <b>Адмін-консоль</b>\nКерування ботом, користувачі та підтримка.\n"
        "<i>Далі зʼявляться: сегменти, аналітика використання, підтримка, тест-режими.</i>",
        reply_markup=kb.as_markup(),
    )


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    await _send_hub(message)


@router.callback_query(F.data == "ac:hub")
async def cb_hub(cb: CallbackQuery) -> None:
    if not _is_admin(cb.from_user.id):
        await cb.answer("Лише адмін.", show_alert=True)
        return
    await cb.answer()
    await _send_hub(cb.message)


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
                reply_markup=approved_kb(),
            )
        except Exception:  # noqa: BLE001
            pass
    elif action == "extend":
        until = await access.approve(uid)  # продовження: повне вікно (6 міс / до іспиту)
        await cb.message.edit_text(f"{cb.message.html_text}\n\n🔓 Продовжено (до {until}).")
        try:
            await cb.bot.send_message(
                uid,
                f"🔓 <b>Доступ продовжено</b> до <b>{until}</b>! Продовжуймо підготовку 👇",
                reply_markup=approved_kb(),
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
