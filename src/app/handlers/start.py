"""/start — привітання, мета, лічильник днів до іспиту."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.keyboards import lesson_kb, start_kb
from app.domain.models import MODULE_LABELS
from app.services import clock, state, vocab

router = Router()


def _intro_text() -> str:
    days = clock.days_to_exam()
    modules = "\n".join(f"  {label}" for label in MODULE_LABELS.values())
    return (
        "Cześć! 👋 Я твій <b>тренер польської до іспиту B1</b>.\n\n"
        f"🎯 Ціль: скласти <b>egzamin certyfikatowy B1</b>.\n"
        f"📅 Іспит: <b>5 грудня 2026</b> — лишилось <b>{days}</b> днів.\n\n"
        "Готуємо всі 5 модулів (на іспиті треба <b>≥50% у кожному</b>):\n"
        f"{modules}\n\n"
        "Почнемо зі стартового тесту — я визначу твій рівень і слабкі місця, "
        "щоб скласти план саме під тебе. 👇"
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    st = await state.load(message.from_user.id)
    await state.save(st)  # реєструємо користувача (для нагадувань)
    await vocab.seed_if_empty(message.from_user.id, clock.today_local())  # стартовий банк слів
    if st.placement_done:
        await message.answer(
            f"Z powrotem! 💪 Рівень: <b>{st.level}</b>, стрік: <b>{st.streak}</b> 🔥\n"
            f"До іспиту <b>{clock.days_to_exam()}</b> днів. Почнемо урок?",
            reply_markup=lesson_kb(),
        )
        return
    await message.answer(_intro_text(), reply_markup=start_kb())


@router.message(Command("pomoc", "help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "📚 <b>Команди</b>\n"
        "/menu — головне меню\n"
        "/lekcja — сьогоднішній урок\n"
        "/powtorki — повторення слів\n"
        "/pisanie — письмо з фідбеком\n"
        "/mowienie — мовлення (голосове)\n"
        "/sluchanie — аудіювання\n"
        "/trening — тренування\n"
        "/postep — мій прогрес\n"
        "/test — стартовий тест ще раз\n"
        "/pomoc — ця довідка"
    )
