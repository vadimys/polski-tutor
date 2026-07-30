"""Підписка через Telegram Stars (XTR).

Флоу: /subskrypcja або кнопка → send_invoice(XTR) → pre_checkout(ok) →
successful_payment → продовжуємо доступ (billing.apply_subscription) + сповіщаємо
учня й (якщо приведений) викладача. Хендлери — ПОЗА access-гейтом (платити може
й той, у кого trial завершився).
"""

from __future__ import annotations

import logging
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards import approved_kb, to_menu_kb
from app.config import settings
from app.services import access, billing, experiments, referrals, viewas

router = Router()
logger = logging.getLogger(__name__)


async def _is_referred(user_id: int) -> bool:
    if (await billing.referrer_of(user_id)) > 0:
        return True
    return (await viewas.get(user_id)) == "referred"  # view-as: тест знижки реферала


async def _access_line(user_id: int) -> str:
    """Рядок стану доступу: trial до X · підписка до Y · завершився. '' якщо нема даних."""
    from datetime import date

    from app.services import clock

    inf = await access.info(user_id)
    if inf.status != "approved" or not inf.until:
        return ""
    try:
        left = (date.fromisoformat(inf.until) - clock.today_local()).days
    except ValueError:
        return ""
    if left < 0:
        return "⏳ Твій доступ завершився — прогрес збережено, продовжимо з того ж місця.\n\n"
    what = "Підписка активна" if await billing.has_payments(user_id) else "Пробний період"
    return f"✅ {what} до <b>{inf.until}</b> (ще {left} дн). Оформити можна будь-коли — дні додаються, не згорають.\n\n"


async def _offer(message: Message, user_id: int) -> None:
    referred = await _is_referred(user_id)
    m_stars = billing.discounted(settings.sub_stars, referred)
    y_stars = billing.discounted(settings.sub_year_stars, referred)
    kb = InlineKeyboardBuilder()
    kb.button(text=f"📅 Місяць — {m_stars} ⭐", callback_data="pay:m")
    kb.button(text=f"🗓 Рік — {y_stars} ⭐ (−{100 - round(y_stars / 12 / m_stars * 100)}%)", callback_data="pay:y")
    kb.button(text="🎁 Запросити друга (+7 днів)", callback_data="ref:invite")
    kb.adjust(1)
    gift = (
        f"\n🎁 Тебе привів викладач — знижка <b>−{settings.referral_discount_pct}%</b> вже врахована!\n"
        if referred else ""
    )
    await message.answer(
        "💎 <b>Підписка Polski B1 Coach</b>\n\n"
        + await _access_line(user_id)
        + "Повний доступ до всіх 5 модулів іспиту: 🎧 аудіювання · 📖 читання · 🔤 граматика "
        "· ✍️ письмо і 🗣 мовлення з AI-перевіркою за офіційними критеріями.\n\n"
        f"📅 Місяць — <b>{m_stars} ⭐</b> (≈25 zł)\n"
        f"🗓 Рік — <b>{y_stars} ⭐</b> (≈{y_stars // 12} ⭐/міс — і голова не болить до самого іспиту)"
        f"\n{gift}\n"
        "💛 <b>За що оплата?</b> Кожна перевірка твого письма чи мовлення — це робота "
        "штучного інтелекту, озвучення — нейро-голос, і все це крутиться на серверах. "
        "Підписка покриває ці витрати й дає змогу розвивати бота далі — нові іспити, "
        "нові функції. Дякую, що підтримуєш ❤️\n\n"
        f"🎁 <b>Реферальна програма:</b> запроси друга — він отримає <b>{settings.trial_days} днів "
        f"безкоштовно</b>, а ти <b>+{settings.referral_reward_days} днів</b> доступу, щойно він "
        "оформить підписку.\n\n"
        "Оплата — через Telegram Stars (⭐), прямо в застосунку. Автосписань немає: "
        "закінчиться — просто нагадаю.\n\n"
        "<i>⭐ Зірки купуються за хвилину прямо в Telegram із телефона. З компʼютера — "
        "через офіційний @PremiumBot.</i>",
        reply_markup=kb.as_markup(),
    )


async def _send_invoice(message: Message, user_id: int, kind: str) -> None:
    base_stars, days = billing.plan_base(kind)
    stars = billing.discounted(base_stars, await _is_referred(user_id))
    label = "рік доступу" if kind == "y" else "місяць доступу"
    await message.answer_invoice(
        title="Підписка Polski B1 Coach",
        description=f"Повний доступ до всіх 5 модулів на {days} днів: аудіо, читання, "
        "граматика, письмо й мовлення з фідбеком.",
        payload=f"sub:{kind}",
        currency="XTR",  # Telegram Stars
        prices=[LabeledPrice(label=label, amount=stars)],
    )


@router.message(Command("subskrypcja"))
async def cmd_subscribe(message: Message) -> None:
    await _offer(message, message.from_user.id)


@router.message(Command("testpay"))
async def cmd_testpay(message: Message) -> None:
    """Адмін-перевірка платіжного флоу: інвойс на 1⭐ (той самий шлях, що й бойовий).
    Після оплати повернути через /refund <charge_id>."""
    if message.from_user.id != settings.admin_id:
        return
    await message.answer_invoice(
        title="ТЕСТ оплати (1 ⭐)",
        description="Технічна перевірка платіжного флоу. Після оплати можна повернути через /refund.",
        payload="sub:m",
        currency="XTR",
        prices=[LabeledPrice(label="тест — 1 зірка", amount=1)],
    )


@router.message(Command("refund"))
async def cmd_refund(message: Message) -> None:
    """Адмін: повернути Stars-платіж за charge_id (собі — для тесту, або підтримка)."""
    if message.from_user.id != settings.admin_id:
        return
    parts = (message.text or "").split()
    if len(parts) < 2:
        await message.answer("Використання: <code>/refund &lt;charge_id&gt;</code> — поверне Stars тобі.")
        return
    try:
        await message.bot.refund_star_payment(
            user_id=message.from_user.id, telegram_payment_charge_id=parts[1]
        )
        await message.answer("✅ Stars повернено.")
    except Exception as e:  # noqa: BLE001
        await message.answer(f"❌ Не вдалося: <code>{type(e).__name__}: {str(e)[:200]}</code>")


@router.callback_query(F.data == "pay:start")
async def cb_subscribe(cb: CallbackQuery) -> None:
    await cb.answer()
    await _offer(cb.message, cb.from_user.id)


@router.callback_query(F.data == "ref:invite")
async def cb_ref_invite(cb: CallbackQuery) -> None:
    """Реф-посилання. ПОЗА гейтом (перенесено з menu.py) — запрошувати може й той,
    у кого trial уже завершився: винагорода +7 дн якраз поверне його в бот."""
    await cb.answer()
    from app.services import referrals

    me = await cb.bot.get_me()
    link = referrals.link(me.username or "", cb.from_user.id)
    s = await referrals.stats(cb.from_user.id)
    await cb.message.answer(
        "🎁 <b>Запроси друга — виграєте обидва</b>\n\n"
        f"Друг отримає <b>{settings.trial_days} днів</b> безкоштовно, а ти — "
        f"<b>+{settings.referral_reward_days} днів</b> доступу, щойно він оформить підписку.\n\n"
        f"🔗 Твоє посилання:\n<code>{link}</code>\n\n"
        f"👥 Запрошено: <b>{s['invited']}</b> · 🎉 винагороджено: <b>{s['rewarded']}</b>",
        reply_markup=to_menu_kb(),
    )


@router.callback_query(F.data.in_({"pay:m", "pay:y"}))
async def cb_plan(cb: CallbackQuery) -> None:
    await cb.answer()
    await _send_invoice(cb.message, cb.from_user.id, cb.data.split(":")[1])


@router.pre_checkout_query()
async def on_pre_checkout(pcq: PreCheckoutQuery) -> None:
    # для Stars-товару просто підтверджуємо; валідних сценаріїв відмови нема
    await pcq.answer(ok=True)


@router.message(F.successful_payment)
async def on_paid(message: Message) -> None:
    sp = message.successful_payment
    uid = message.from_user.id
    stars = sp.total_amount  # у Stars = скільки реально сплачено (уже зі знижкою)
    charge = sp.telegram_payment_charge_id
    kind = (sp.invoice_payload or "sub:m").split(":")[-1]  # 'm' | 'y'
    _, days = billing.plan_base(kind)
    try:
        until = await billing.apply_subscription(uid, days, stars, charge)
    except Exception:
        # оплату отримано, але доступ не продовжився — НЕ брешемо про успіх, кличемо адміна
        logger.exception("payment grant FAILED uid=%s stars=%s charge=%s", uid, stars, charge)
        await message.answer(
            "✅ Оплату отримано, але сталася технічна затримка з активацією. "
            "Уже розбираюсь — доступ відкрию найближчим часом 🙏"
        )
        if settings.admin_id:
            with suppress(Exception):
                await message.bot.send_message(
                    settings.admin_id,
                    f"🆘 <b>ОПЛАТА БЕЗ АКТИВАЦІЇ</b> uid <code>{uid}</code> · {stars}⭐ · "
                    f"charge <code>{charge}</code> — активувати вручну!",
                )
        return
    await message.answer(
        f"✅ <b>Дякуємо! Підписку активовано</b> до <b>{until}</b>.\n"
        "Повний доступ відкрито — продовжуймо підготовку 👇",
        reply_markup=approved_kb(),
    )
    logger.info("payment ok uid=%s stars=%s until=%s", uid, stars, until)
    # побічні дії ПІСЛЯ активації — best-effort: збій тут НЕ має ламати грошовий шлях
    # (інакше учень уже побачив «✅ оплачено», а далі — «щось пішло не так»)
    with suppress(Exception):
        await experiments.convert("paywall_expiry", uid)  # A/B: конверсія trial→оплата
        # word-of-mouth: якщо оплатив запрошений друг — винагородити запрошувача
        referrer = await referrals.on_subscription(uid)
        if referrer:
            r_until = await access.extend_days(referrer, settings.referral_reward_days)
            await message.bot.send_message(
                referrer,
                f"🎉 Друг, якого ти запросив, оформив підписку! Тобі <b>+"
                f"{settings.referral_reward_days} днів</b> доступу (до <b>{r_until}</b>). "
                "Дякуємо, що ділишся 🙌",
            )
    # сповістити викладача, якщо учень приведений (референс-бонус/атрибуція)
    teacher_id = await billing.referrer_of(uid)
    if teacher_id:
        name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
        try:
            await message.bot.send_message(
                teacher_id,
                f"🎉 Твій учень {name} оформив підписку — дякуємо, що приводиш клас! "
                "Деталі — у /uczniowie.",
            )
        except Exception:  # noqa: BLE001
            pass
    # сповістити адміна (облік)
    if settings.admin_id:
        try:
            await message.bot.send_message(
                settings.admin_id,
                f"💰 Оплата: uid <code>{uid}</code> · {stars} ⭐ · до {until}\n"
                f"charge <code>{charge}</code>  (повернути: /refund {charge})",
            )
        except Exception:  # noqa: BLE001
            pass
