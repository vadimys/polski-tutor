"""Онбординг + контроль доступу: /start, вибір дати, запит доступу, зв'язок з адміном."""

from __future__ import annotations

import html
from contextlib import suppress

from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import (
    activation_kb,
    admin_extend_kb,
    admin_teacher_kb,
    approved_kb,
    churn_survey_kb,
    contact_admin_kb,
    exam_dates_kb,
    exam_result_kb,
    extend_request_kb,
    role_choice_kb,
    send_request_kb,
    to_menu_kb,
)
from app.config import settings
from app.handlers.privacy import PRIVACY_SHORT
from app.services import (
    access,
    activation,
    attribution,
    churn,
    clock,
    exam_dates,
    experiments,
    groups,
    referrals,
    viewas,
    vocab,
)

router = Router()


class Onb(StatesGroup):
    contact = State()
    teacher_app = State()  # очікуємо текст заявки викладача


def _fmt(iso: str, confirmed: bool) -> str:
    return exam_dates.label(iso) if (confirmed and iso) else "ще не підтверджена"


def _date_kb():
    return exam_dates_kb(exam_dates.upcoming(clock.today_local()), "onb:date", with_unconfirmed=True)


def _trial_disclosure() -> str:
    """Єдине джерело чесного дисклеймера про підписку після trial (money/legal — без дрейфу)."""
    return (
        f"<i>Далі, щоб продовжити, — підписка {settings.sub_stars} ⭐ / {settings.sub_days} дн. "
        "Нічого не спишеться автоматично.</i>"
    )


def _days_line(inf) -> str:
    """Рядок про іспит з урахуванням фази (майбутнє/сьогодні/минув)."""
    d = exam_dates.days_left(inf.exam_date, clock.today_local()) if inf.confirmed else None
    if d is None:
        return "Дату іспиту ще не підтверджено — познач її в меню."
    if d > 0:
        return f"До іспиту <b>{d}</b> днів."
    if d == 0:
        return "🍀 Сьогодні твій іспит — powodzenia!"
    return "Іспит уже позаду. Признач нову дату, якщо готуєшся знову."


async def _approved_welcome(message: Message, user_id: int) -> None:
    inf = await access.info(user_id)
    mode = await viewas.get(user_id)
    role = viewas.role_for(mode, inf.role)
    banner = f"👁 <i>Режим перегляду: {mode}. Вийти — /admin.</i>\n\n" if mode else ""
    if role == "teacher":
        me = await message.bot.get_me()
        link = f"https://t.me/{me.username}?start=t{user_id}"
        await message.answer(
            f"{banner}👩‍🏫 <b>Вітаю, викладачу!</b> Доступ активний.\n\n"
            "🔗 Твоє посилання для учнів:\n"
            f"<code>{link}</code>\n\n"
            "👥 Прогрес класу — <b>/uczniowie</b>\n"
            "<i>Вправи можеш проходити сам як превʼю — вони не зараховуються як підготовка.</i>",
            reply_markup=to_menu_kb(),
        )
        return
    await vocab.seed_if_empty(user_id, clock.today_local())
    # іспит минув, а результат ще не зафіксовано → питаємо «як пройшло?»
    if not mode and exam_dates.status(inf.exam_date, inf.confirmed, clock.today_local()) == "past" \
            and inf.exam_result in ("", "pending"):
        await message.answer(
            "📅 Твій іспит уже позаду. <b>Як пройшло?</b>", reply_markup=exam_result_kb()
        )
        return
    steps = await activation.checklist(user_id)
    if activation.all_done(steps):  # уже освоївся (aha!) → меню
        # word-of-mouth-тригер лише ОРГАНІЧНИМ учням — щоб не розмивати teacher-атрибуцію
        ref_hint = (
            f"\n\n🎁 <i>Подобається? Запроси друга («🎁 Запросити друга» в меню) — він отримає "
            f"trial, а ти +{settings.referral_reward_days} днів, коли він оформить підписку.</i>"
            if not inf.referred_by
            else ""
        )
        await message.answer(
            f"{banner}Cześć! 👋 Доступ активний. {_days_line(inf)}\nОбери дію в меню 👇{ref_hint}",
            reply_markup=approved_kb(),
        )
    else:  # веду до наступного кроку з видимим прогресом (one goal per session)
        nxt = activation.next_step(steps)
        await message.answer(
            f"{banner}Cześć! 👋 Доступ активний. {_days_line(inf)}\n\n"
            f"{activation.render(steps)}\n\nПочнемо з наступного 👇",
            reply_markup=activation_kb(nxt["cb"], nxt["short"]),
        )


async def _grant_referral(message: Message, uid: int, teacher_id: int, group_id: int, group_name: str) -> None:
    """Відкрити trial приведеному учню + сповістити викладача (з назвою групи, якщо є)."""
    until = await access.grant_trial(
        uid, message.from_user.username or "", teacher_id, settings.trial_days, group_id=group_id
    )
    await vocab.seed_if_empty(uid, clock.today_local())
    grp = f" (група «{html.escape(group_name)}»)" if group_name else ""
    await message.answer(
        f"Cześć! 👋 Тебе запросив викладач{grp} — тобі відкрито <b>безкоштовний доступ на "
        f"{settings.trial_days} днів</b> (до <b>{until}</b>).\n"
        "<i>Твій викладач бачитиме твій прогрес, щоб допомагати.</i>\n"
        f"{_trial_disclosure()}\n\n"
        "Почнемо зі стартового тесту 👇",
        reply_markup=approved_kb(),
    )
    name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
    with suppress(Exception):
        where = f" у групу «{html.escape(group_name)}»" if group_name else " за твоїм посиланням"
        await message.bot.send_message(teacher_id, f"🎉 Новий учень долучився{where}: {html.escape(name)}")


async def _try_referral(message: Message, uid: int, payload: str) -> bool:
    """Учень за посиланням викладача (t<teacher>) або групи (g<group>) → авто-trial."""
    gid = access.parse_group(payload)
    if gid is not None:
        g = await groups.get(gid)
        if not g or g["teacher_id"] == uid or not await access.is_teacher(g["teacher_id"]):
            return False
        await _grant_referral(message, uid, g["teacher_id"], gid, g["name"])
        return True
    teacher_id = access.parse_referral(payload)
    if teacher_id is not None and teacher_id != uid and await access.is_teacher(teacher_id):
        await _grant_referral(message, uid, teacher_id, 0, "")
        return True
    friend = referrals.parse(payload)  # учень→друг (word-of-mouth)
    if friend is not None and friend != uid:
        await _grant_friend(message, uid, friend)
        return True
    return False


async def _grant_friend(message: Message, uid: int, referrer: int) -> None:
    """Друг за посиланням учня → trial + фіксація реферала (винагорода — на оплаті друга)."""
    until = await access.grant_trial(uid, message.from_user.username or "", 0, settings.trial_days)
    await vocab.seed_if_empty(uid, clock.today_local())
    await referrals.record_invite(uid, referrer)
    await message.answer(
        f"Cześć! 👋 Тебе запросив друг — тобі відкрито <b>безкоштовний доступ на "
        f"{settings.trial_days} днів</b> (до <b>{until}</b>).\n"
        f"{_trial_disclosure()}\n\nПочнемо зі стартового тесту 👇",
        reply_markup=approved_kb(),
    )
    with suppress(Exception):  # підбадьорити запрошувача (petля живіша)
        await message.bot.send_message(
            referrer,
            f"🎉 Твій друг долучився за твоїм посиланням! Щойно він оформить підписку — "
            f"ти отримаєш <b>+{settings.referral_reward_days} днів</b> доступу. Дякуємо, що ділишся 🙌",
        )


async def _expired_paywall(uid: int, inf, variant: int = 0) -> str:  # noqa: ANN001
    """Paywall завершеного trial (A/B — skill ab-testing). Обидва варіанти спираються
    на РЕАЛЬНИЙ прогрес; різниться ЛИШЕ формулювання (одна змінна):
    A — підсумок-досягнень + ціль; B — втрата+терміновість (дедлайн)."""
    from app.services import progress, quest
    from app.services import state as user_state

    st = await user_state.load(uid)
    total_sessions, _ = await progress.counts(uid)
    words = await vocab.count(uid)
    overall = quest.overall_pct(st.readiness or {})
    days = (
        exam_dates.days_left(inf.exam_date, clock.today_local())
        if inf.confirmed and inf.exam_date
        else None
    )
    cta = (
        "повний доступ до всіх 5 модулів (з фідбеком письма й мовлення від AI) — "
        f"<b>{settings.sub_stars} ⭐ / {settings.sub_days} днів</b>."
    )

    if variant == 1:  # B — втрата + терміновість
        lines = ["⏳ <b>Твій безкоштовний період завершився.</b>\n"]
        if total_sessions:
            stat = [f"🏁 готовність {overall}%"]
            if st.streak:
                stat.append(f"🔥 серія {st.streak} дн")
            if words:
                stat.append(f"📚 {words} слів")
            lines.append(
                "⚠️ Без практики польська швидко тане. Ти вже наробив: "
                + " · ".join(stat)
                + " — не даймо цьому згаснути."
            )
        if days is not None and days >= 0:
            lines.append(f"\n⏰ До іспиту <b>{days} днів</b> — час працює або на тебе, або проти.")
        lines.append(f"\nВідкрий {cta}")
        return "\n".join(lines)

    # A — підсумок-досягнень + ціль (контроль)
    lines = ["⏳ <b>Твій безкоштовний період завершився.</b>\n"]
    if total_sessions:
        acc = [f"🏋️ вправ пройдено: <b>{total_sessions}</b>", f"🏁 готовність до B1: <b>{overall}%</b>"]
        if words:
            acc.append(f"📚 слів у памʼяті: <b>{words}</b>")
        if st.streak:
            acc.append(f"🔥 серія: <b>{st.streak}</b> дн")
        lines.append("За цей час ти вже:\n• " + "\n• ".join(acc) + "\n")
    if days is not None and days >= 0:
        lines.append(f"⏰ До іспиту <b>{days} днів</b> — шкода спинятися на пів-дорозі.")
    lines.append(f"Щоб не втратити прогрес і <b>довести справу до складеного B1</b>, відкрий {cta}")
    return "\n".join(lines)


@router.callback_query(F.data.startswith("churn:reason:"))
async def cb_churn_reason(cb: CallbackQuery) -> None:
    """Exit-survey: причина відмови → адресний save-offer (skill churn-prevention)."""
    await cb.answer()
    uid = cb.from_user.id
    # захист: survey лише для тих, у кого доступ реально сплив (callback підроблюваний)
    if not access.is_expired(await access.info(uid), clock.today_local()):
        return
    reason = cb.data.split(":")[2]
    await churn.record_reason(reason)

    # «не встиг» → разова реактивація +N днів (атомарний claim проти подвійного кліку)
    if reason == "notime" and await churn.claim_reoffer(uid):
        until = await access.extend_days(uid, settings.winback_extend_days)
        await cb.message.answer(
            f"🎁 <b>Ще {settings.winback_extend_days} дні безкоштовно</b> — щоб ти встиг відчути "
            f"користь. Доступ відкрито до <b>{until}</b>. Тисни /menu і продовжуй 👇\n"
            "<i>Далі — підписка, щоб довести підготовку до складеного B1.</i>",
            reply_markup=to_menu_kb(),
        )
        return

    if reason == "price":  # → якір на річний план (не глибока знижка — не привчаємо кидати)
        text = (
            "💸 Розумію. Дивись: <b>річний</b> план — "
            f"<b>{settings.sub_year_stars}⭐</b> проти ~{settings.sub_stars * 12}⭐ за 12 місяців "
            f"окремо (≈{settings.sub_year_stars // 12}⭐/міс). Менше за одну каву на місяць — "
            "за підготовку до державного іспиту."
        )
    elif reason == "unsure":  # → реасюр цінності + запросити фідбек
        text = (
            "🤔 Чесно: бот тренує всі <b>5 модулів</b> іспиту на <b>офіційних</b> завданнях "
            "Держкомісії й дає AI-фідбек письма та мовлення за держ-критеріями — це найближче "
            "до реального іспиту, що є. Напиши «Написати адміну», чого бракує, — врахую."
        )
    elif reason == "noneed":  # → грейсфул, без тиску (respect the no)
        await cb.message.answer(
            "Дякую за чесність! 🙌 Твій прогрес збережено — повертайся будь-коли (/start). "
            "Успіхів на іспиті! 🍀"
        )
        return
    else:  # «не встиг», але реактивацію вже використано
        text = (
            "Ти вже пробував бота в ділі 💪 Щоб не втратити прогрес — оформи підписку "
            "й дійдемо до складеного B1 разом."
        )
    await cb.message.answer(text, reply_markup=extend_request_kb())


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, command: CommandObject) -> None:
    await state.clear()
    uid = message.from_user.id
    payload = (command.args or "").strip()
    if payload:  # мітка кампанії (?start=fb_wielun…) — first-touch, no-op для рефералів/адміна
        await attribution.record(uid, payload)
    inf = await access.info(uid)
    if uid == settings.admin_id:
        if await viewas.get(uid):  # у режимі перегляду — рендеримо досвід обраної ролі
            await _approved_welcome(message, uid)
        else:
            from app.handlers.admin import send_hub  # адмін → одразу панель керування
            await send_hub(message)
    elif access.is_expired(inf, clock.today_local()) and inf.role == "teacher":
        # викладачам доступ безкоштовний — НЕ показуємо учнівський paywall/churn-survey
        await message.answer(
            "👩‍🏫 <b>Термін твого викладацького доступу минув.</b>\n"
            "Напиши адміну, щоб продовжити — доступ для викладачів безкоштовний.",
            reply_markup=contact_admin_kb(),
        )
    elif access.is_expired(inf, clock.today_local()):
        v = await experiments.expose("paywall_expiry", uid)  # A/B копії paywall
        await message.answer(await _expired_paywall(uid, inf, v), reply_markup=churn_survey_kb())
    elif inf.status == "approved":
        await _approved_welcome(message, uid)
    elif inf.status == "pending":
        await message.answer(
            "⏳ Твій запит на розгляді. Щойно адмін вирішить — сповіщу.",
            reply_markup=contact_admin_kb(),
        )
    elif inf.status == "denied":
        await message.answer(
            "🚫 На жаль, доступ відхилено. Можеш написати адміну.",
            reply_markup=contact_admin_kb(),
        )
    elif await _try_referral(message, uid, (command.args or "").strip()):
        return  # новий учень за реферальним посиланням — доступ уже відкрито
    else:  # новий без реферала → розвилка ролі
        await message.answer(
            "Cześć! 👋 Я тренер польської до державного іспиту <b>B1</b>.\n\n"
            "Хто ти?\n"
            "🎓 <b>Учень</b> — готуєшся до іспиту (персональний план, усі 5 модулів).\n"
            "👩‍🏫 <b>Викладач</b> — навчаєш учнів (безкоштовний доступ + запросиш свій клас).\n\n"
            f"{PRIVACY_SHORT}",
            reply_markup=role_choice_kb(),
        )


@router.callback_query(F.data == "onb:role:student")
async def cb_role_student(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await cb.message.answer(
        "🎓 Чудово! Спершу скажи, <b>коли твій іспит</b> (лише офіційні сесії Держкомісії) — "
        "щоб скласти план і надіслати запит на доступ:",
        reply_markup=_date_kb(),
    )


@router.callback_query(F.data == "onb:role:teacher")
async def cb_role_teacher(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Onb.teacher_app)
    await cb.answer()
    await cb.message.answer(
        "👩‍🏫 <b>Заявка викладача</b>\n\n"
        "Розкажи коротко про себе <b>одним повідомленням</b>:\n"
        "• ім'я;\n"
        "• де навчаєш (школа / платформа, напр. Preply/iTalki, або лінк на профіль);\n"
        "• скількох учнів готуєш до B1.\n\n"
        "Після схвалення відкрию безкоштовний доступ і дам твоє <b>реферальне посилання</b> для учнів.",
    )


@router.message(Onb.teacher_app, F.text, ~F.text.startswith("/"))
async def on_teacher_app(message: Message, state: FSMContext) -> None:
    await state.clear()
    uid = message.from_user.id
    username = message.from_user.username or ""
    await access.request_teacher(uid, username)
    await message.answer(
        "✅ Заявку надіслано! Щойно адмін підтвердить — відкрию доступ і дам твоє "
        "реферальне посилання для учнів.",
        reply_markup=contact_admin_kb(),
    )
    if settings.admin_id:
        name = f"@{username}" if username else (message.from_user.full_name or str(uid))
        await message.bot.send_message(
            settings.admin_id,
            f"👩‍🏫 <b>Заявка ВИКЛАДАЧА</b>\nКористувач: {html.escape(name)} (id <code>{uid}</code>)\n\n"
            f"{html.escape(message.text)}",
            reply_markup=admin_teacher_kb(uid),
        )


@router.callback_query(F.data == "onb:restart")
async def cb_restart(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.answer()
    await cb.message.answer("Коли твій іспит?", reply_markup=_date_kb())


async def _confirm(message: Message, iso: str, confirmed: bool) -> None:
    await message.answer(
        f"📅 Дата іспиту: <b>{_fmt(iso, confirmed)}</b>\n\n"
        f"Відкрию тобі <b>{settings.organic_trial_days} днів безкоштовно</b> — почнемо?",
        reply_markup=send_request_kb(),
    )


@router.callback_query(F.data.startswith("onb:date:"))
async def cb_date(cb: CallbackQuery, state: FSMContext) -> None:
    iso = cb.data.split(":", 2)[2]
    if not exam_dates.is_official(iso):  # захист: лише офіційні дати
        await cb.answer("Оберіть офіційну дату зі списку.", show_alert=True)
        return
    await state.update_data(exam_date=iso, confirmed=True)
    await cb.answer()
    await _confirm(cb.message, iso, True)


@router.callback_query(F.data == "onb:unconfirmed")
async def cb_unconfirmed(cb: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(exam_date="", confirmed=False)
    await cb.answer()
    await cb.message.answer(
        f"❔ Дату вкажеш пізніше. Відкрию тобі <b>{settings.organic_trial_days} днів "
        "безкоштовно</b> — за цей час зареєструйся на іспит і познач дату "
        "(«📅 Вказати дату іспиту»). Почнемо?",
        reply_markup=send_request_kb(),
    )


# --- Оновлення/підтвердження дати іспиту (для схвалених) ---
@router.callback_query(F.data == "onb:setdate")
async def cb_setdate(cb: CallbackQuery) -> None:
    await cb.answer()
    await cb.message.answer(
        "Обери офіційну дату свого іспиту:",
        reply_markup=exam_dates_kb(exam_dates.upcoming(clock.today_local()), "onb:exam"),
    )


@router.callback_query(F.data.startswith("onb:exam:"))
async def cb_examdate(cb: CallbackQuery) -> None:
    iso = cb.data.split(":", 2)[2]
    if not exam_dates.is_official(iso):
        await cb.answer("Оберіть офіційну дату зі списку.", show_alert=True)
        return
    until = await access.set_exam_date(cb.from_user.id, iso)
    await cb.answer()
    await cb.message.answer(
        f"✅ Дату іспиту збережено: <b>{exam_dates.label(iso)}</b>."
        + (f"\nДоступ активний до <b>{until}</b>." if until else ""),
        reply_markup=to_menu_kb(),
    )


# --- Post-exam: результат іспиту (питання шле scheduler, коли дата минула) ---
@router.callback_query(F.data == "exam:res:passed")
async def cb_exam_passed(cb: CallbackQuery) -> None:
    await access.set_exam_result(cb.from_user.id, "passed")
    await cb.answer("🎉")
    await cb.message.answer(
        "🎉 <b>Вітаю зі складанням іспиту B1!</b> Це велика робота — ти дійшов до мети! 🇵🇱\n\n"
        "Якщо бот був корисний — <b>порекомендуй його друзям</b>, хто теж готується. "
        "Дякую, що був з нами! 💚",
        reply_markup=to_menu_kb(),
    )


@router.callback_query(F.data == "exam:res:failed")
async def cb_exam_failed(cb: CallbackQuery) -> None:
    await access.set_exam_result(cb.from_user.id, "failed")
    await cb.answer()
    await cb.message.answer(
        "Нічого страшного — це досвід, і ти вже близько. Обери <b>наступну сесію</b>, "
        "і ми підтягнемо слабкі місця (весь прогрес зберігається):",
        reply_markup=exam_dates_kb(exam_dates.upcoming(clock.today_local()), "onb:exam"),
    )


@router.callback_query(F.data == "exam:res:wait")
async def cb_exam_wait(cb: CallbackQuery) -> None:
    await cb.answer()
    await cb.message.answer(
        "🤞 Тримаю кулаки! Коли дізнаєшся результат — познач його: /start → як пройшло, "
        "або зміни дату (📅), якщо перескладатимеш.",
        reply_markup=to_menu_kb(),
    )


@router.callback_query(F.data == "onb:send")
async def cb_send(cb: CallbackQuery, state: FSMContext) -> None:
    """Органічний учень → авто-trial БЕЗ черги (self-serve freemium). Адмін лише інформується."""
    data = await state.get_data()
    exam_date = data.get("exam_date", "")
    confirmed = bool(data.get("confirmed", False))
    uid = cb.from_user.id
    username = cb.from_user.username or ""
    until = await access.grant_trial(
        uid, username, 0, settings.organic_trial_days, exam_date, confirmed
    )
    await vocab.seed_if_empty(uid, clock.today_local())
    await state.clear()
    await cb.answer()
    await cb.message.answer(
        f"🚀 <b>Доступ відкрито — {settings.organic_trial_days} днів безкоштовно!</b> "
        f"(до <b>{until}</b>)\n"
        f"{_trial_disclosure()}\n"
        "Почнемо зі стартового тесту 👇",
        reply_markup=approved_kb(),
    )
    if settings.admin_id:  # інформуємо (без схвалення — доступ уже відкрито)
        name = f"@{username}" if username else (cb.from_user.full_name or str(uid))
        await cb.bot.send_message(
            settings.admin_id,
            f"🆕 <b>Новий учень (self-serve trial)</b>: {html.escape(name)} "
            f"(id <code>{uid}</code>) · дата: <b>{_fmt(exam_date, confirmed)}</b> · до {until}",
        )


@router.callback_query(F.data == "onb:extend")
async def cb_extend(cb: CallbackQuery) -> None:
    """Учень просить продовження після trial → у чергу до адміна (місток до підписки)."""
    await cb.answer()
    uid = cb.from_user.id
    username = cb.from_user.username or ""
    await cb.message.answer("📨 Запит на продовження надіслано. Щойно вирішу — сповіщу 🙂")
    if settings.admin_id:
        name = f"@{username}" if username else (cb.from_user.full_name or str(uid))
        await cb.bot.send_message(
            settings.admin_id,
            f"🔓 <b>Запит на ПРОДОВЖЕННЯ</b> (trial вичерпано)\n{html.escape(name)} "
            f"(id <code>{uid}</code>)",
            reply_markup=admin_extend_kb(uid),
        )


@router.callback_query(F.data == "onb:contact")
async def cb_contact(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Onb.contact)
    await cb.answer()
    await cb.message.answer("✍️ Напиши повідомлення для адміна одним повідомленням:")


@router.message(Onb.contact, F.text, ~F.text.startswith("/"))
async def on_contact(message: Message, state: FSMContext) -> None:
    await state.clear()
    uid = message.from_user.id
    username = message.from_user.username or ""
    name = f"@{username}" if username else (message.from_user.full_name or str(uid))
    if settings.admin_id:
        await message.bot.send_message(
            settings.admin_id,
            f"✉️ <b>Повідомлення від</b> {html.escape(name)} (id <code>{uid}</code>):\n"
            f"{html.escape(message.text)}\n\n<i>Відповісти: /reply {uid} текст</i>",
        )
    await message.answer("📨 Надіслано адміну. Дякую!")
