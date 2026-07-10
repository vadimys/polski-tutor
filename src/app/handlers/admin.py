"""Адмін: схвалення/відмова запитів на доступ + відповідь користувачу."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import approved_kb, contact_admin_kb
from app.config import settings
from app.services import access

router = Router()


def _is_admin(user_id: int) -> bool:
    return bool(settings.admin_id) and user_id == settings.admin_id


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
                f"<b>{settings.trial_days} днів</b>, а ти зможеш стежити за його прогресом. "
                "Ділись посиланням зі своїм класом! 🚀",
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
