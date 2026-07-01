"""Довідка (/pomoc). /start — в онбордингу (app.handlers.onboarding)."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("pomoc", "help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "📚 <b>Команди</b>\n"
        "/start — головна / запит доступу\n"
        "/menu — головне меню\n"
        "/lekcja — сьогоднішній урок\n"
        "/powtorki — повторення слів\n"
        "/pisanie — письмо · /opis — опис фото · /mowienie — мовлення\n"
        "/sluchanie — аудіювання · /mok — офіційний МОК · /trening — тренування\n"
        "/postep — прогрес · /plan — мій план · /test — стартовий тест"
    )
