from datetime import date, timedelta

from app.services.access import (
    SIX_MONTHS_DAYS,
    AccessInfo,
    compute_access_until,
    extend_until,
    is_expired,
    parse_group,
    parse_referral,
)

TODAY = date(2026, 7, 1)
SIX = TODAY + timedelta(days=SIX_MONTHS_DAYS)


def test_unconfirmed_gives_six_months():
    assert compute_access_until("", False, TODAY) == SIX


def test_confirmed_but_within_six_months_gives_min_six():
    # іспит через ~2 місяці → мінімум 6 місяців
    assert compute_access_until("2026-09-01", True, TODAY) == SIX


def test_confirmed_beyond_six_months_gives_exam_date():
    assert compute_access_until("2027-06-01", True, TODAY) == date(2027, 6, 1)


def test_confirmed_exactly_uses_max():
    # рівно на межі 6 міс → не менше 6 міс
    assert compute_access_until(SIX.isoformat(), True, TODAY) == SIX


def test_invalid_date_falls_back_to_six_months():
    assert compute_access_until("не-дата", True, TODAY) == SIX


def test_extend_until_prolongs_to_later_exam():
    # доступ до 2026-12-30 (6 міс), зареєструвався на пізніший іспит → подовжуємо
    assert extend_until("2026-12-30", "2027-06-01") == "2027-06-01"


def test_extend_until_keeps_window_if_exam_earlier():
    assert extend_until("2027-06-01", "2026-12-05") == "2027-06-01"


def test_extend_until_no_exam_keeps_current():
    assert extend_until("2026-12-30", "") == "2026-12-30"


def test_parse_referral():
    assert parse_referral("t367724841") == 367724841
    assert parse_referral(" t42 ") == 42
    assert parse_referral("") is None
    assert parse_referral("abc") is None
    assert parse_referral("t") is None  # без цифр
    assert parse_referral("t12x") is None


def test_referral_keyboards_callbacks():
    from app.bot.keyboards import admin_teacher_kb, role_choice_kb

    role_cbs = [b.callback_data for row in role_choice_kb().inline_keyboard for b in row]
    assert role_cbs == ["onb:role:student", "onb:role:teacher"]
    adm_cbs = [b.callback_data for row in admin_teacher_kb(99).inline_keyboard for b in row]
    assert adm_cbs == ["adm:teacher:99", "adm:no:99"]


def _inf(status, until):
    return AccessInfo(status, until, "", False, "")


def test_is_expired():
    today = date(2026, 7, 10)
    assert is_expired(_inf("approved", "2026-07-01"), today) is True  # минув
    assert is_expired(_inf("approved", "2026-07-10"), today) is False  # сьогодні ще діє
    assert is_expired(_inf("approved", "2026-12-01"), today) is False  # активний
    assert is_expired(_inf("approved", ""), today) is False  # без терміну = безстроково
    assert is_expired(_inf("pending", "2026-07-01"), today) is False  # не approved


def test_extend_keyboards_callbacks():
    from app.bot.keyboards import admin_extend_kb, extend_request_kb

    ext = [b.callback_data for row in extend_request_kb().inline_keyboard for b in row]
    assert ext == ["pay:start", "onb:contact"]  # підписка Stars — головний CTA після trial
    adm = [b.callback_data for row in admin_extend_kb(7).inline_keyboard for b in row]
    assert adm == ["adm:extend:7", "adm:no:7"]


def test_parse_group():
    assert parse_group("g5")==5
    assert parse_group("g367724841")==367724841
    assert parse_group("t5") is None
    assert parse_group("") is None
    assert parse_group("g") is None
