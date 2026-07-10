"""Персональна година нагадувань: тік поважає lesson_hour + дедуплікація в межах доби."""

import pytest

from app import scheduler


class _FakeBot:
    def __init__(self):
        self.sent: list[int] = []

    async def send_message(self, uid, text, reply_markup=None):
        self.sent.append(uid)


@pytest.fixture
def wired(monkeypatch):
    """Троє учнів із різними годинами; усі схвалені; нейтральний текст нагадування."""
    hours = {1: 8, 2: 8, 3: 20}

    async def fake_ids():
        return list(hours)

    async def fake_load(uid):
        return type("S", (), {"lesson_hour": hours[uid]})()

    async def fake_allowed(uid, admin_id):
        return True

    async def fake_nudge(uid):
        return "поштовх"

    monkeypatch.setattr(scheduler.state, "all_user_ids", fake_ids)
    monkeypatch.setattr(scheduler.state, "load", fake_load)
    monkeypatch.setattr(scheduler.access, "is_allowed", fake_allowed)
    monkeypatch.setattr(scheduler, "_personal_nudge", fake_nudge)
    return hours


async def test_nudge_only_matching_hour(wired):
    bot = _FakeBot()
    sent_on: dict[int, str] = {}
    n = await scheduler._nudge_due(bot, hour=8, today="2026-07-10", sent_on=sent_on)
    assert n == 2 and sorted(bot.sent) == [1, 2]  # лише ті, у кого 08:00
    # о 20:00 — третій
    bot2 = _FakeBot()
    await scheduler._nudge_due(bot2, hour=20, today="2026-07-10", sent_on={})
    assert bot2.sent == [3]


async def test_nudge_dedupe_same_day(wired):
    bot = _FakeBot()
    sent_on: dict[int, str] = {}
    await scheduler._nudge_due(bot, hour=8, today="2026-07-10", sent_on=sent_on)
    # повторний тік тієї ж години того ж дня — нічого не шле (дедуплікація)
    n2 = await scheduler._nudge_due(bot, hour=8, today="2026-07-10", sent_on=sent_on)
    assert n2 == 0 and sorted(bot.sent) == [1, 2]
    # наступний день — знову шле
    n3 = await scheduler._nudge_due(bot, hour=8, today="2026-07-11", sent_on=sent_on)
    assert n3 == 2


async def test_seconds_until_next_hour_in_range():
    s = await scheduler._seconds_until_next_hour()
    assert 0 < s <= 3600
