"""Довідка (/pomoc). /start — в онбордингу (app.handlers.onboarding)."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.keyboards import to_menu_kb
from app.services import access, viewas

router = Router()


@router.message(Command("pomoc", "help"))
async def cmd_help(message: Message) -> None:
    inf = await access.info(message.from_user.id)
    if viewas.role_for(await viewas.get(message.from_user.id), inf.role) == "teacher":
        await message.answer(
            "👩‍🏫 <b>Команди викладача</b>\n"
            "/menu — меню викладача\n"
            "/uczniowie — твій клас: групи, 🏆 лідерборд, 📝 завдання, 📣 розсилка\n"
            "📚 Матеріали й усі офіційні тести — меню → «Матеріали та тести» (превʼю)\n"
            "/pomoc — ця довідка\n"
            "/prywatnosc · /moidane · /zapomnij — приватність і дані",
            reply_markup=to_menu_kb(),
        )
        return
    await message.answer(
        "📚 <b>Команди</b>\n"
        "/start — головна / запит доступу\n"
        "/menu — головне меню\n"
        "/lekcja — сьогоднішній урок\n"
        "/powtorki — повторення слів · /slownik — вільний словник за темами\n"
        "/pisanie — письмо · /opis — опис фото · /mowienie — мовлення\n"
        "/sluchanie — аудіювання · /mok — офіційний МОК · /trening — тренування\n"
        "/quest — похід до B1 · /misje — місії · /cel — денна ціль\n"
        "/postep — прогрес · /plan — мій план · /test — стартовий тест\n"
        "/reset — почати навчання заново · /anuluj — скасувати завдання\n"
        "/prywatnosc — приватність · /moidane — мої дані · /zapomnij — видалити дані",
        reply_markup=to_menu_kb(),
    )
