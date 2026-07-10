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
    """Учні (student) з різними годинами + викладач (teacher, id 4, 08:00, нудж НЕ шлемо)."""
    hours = {1: 8, 2: 8, 3: 20, 4: 8}
    roles = {1: "student", 2: "student", 3: "student", 4: "teacher"}

    async def fake_ids():
        return list(hours)

    async def fake_load(uid):
        return type("S", (), {"lesson_hour": hours[uid], "role": roles[uid]})()

    async def fake_allowed(uid, admin_id):
        return True

    async def fake_nudge(uid):
        return "поштовх"

    monkeypatch.setattr(scheduler.state, "all_user_ids", fake_ids)
    monkeypatch.setattr(scheduler.state, "load", fake_load)
    monkeypatch.setattr(scheduler.access, "is_allowed", fake_allowed)
    monkeypatch.setattr(scheduler, "_personal_nudge", fake_nudge)

    # дедуп-мітка в памʼяті (замість Redis) — імітує persistence між тіками/рестартами
    marks: set[str] = set()

    async def fake_already(uid, today):
        return f"{uid}:{today}" in marks

    async def fake_mark(uid, today):
        marks.add(f"{uid}:{today}")

    monkeypatch.setattr(scheduler, "_already_nudged", fake_already)
    monkeypatch.setattr(scheduler, "_mark_nudged", fake_mark)
    return hours


async def test_nudge_only_matching_hour(wired):
    bot = _FakeBot()
    n = await scheduler._nudge_due(bot, hour=8, today="2026-07-10")
    # лише учні о 08:00 (1,2); викладач (4, teacher) — пропущено
    assert n == 2 and sorted(bot.sent) == [1, 2]
    # о 20:00 — третій
    bot2 = _FakeBot()
    await scheduler._nudge_due(bot2, hour=20, today="2026-07-10")
    assert bot2.sent == [3]


async def test_nudge_dedupe_same_day(wired):
    bot = _FakeBot()
    await scheduler._nudge_due(bot, hour=8, today="2026-07-10")
    # повторний тік тієї ж години того ж дня — нічого не шле (дедуп переживає й рестарт)
    n2 = await scheduler._nudge_due(bot, hour=8, today="2026-07-10")
    assert n2 == 0 and sorted(bot.sent) == [1, 2]
    # наступний день — знову шле
    n3 = await scheduler._nudge_due(bot, hour=8, today="2026-07-11")
    assert n3 == 2


async def test_seconds_until_next_hour_in_range():
    s = await scheduler._seconds_until_next_hour()
    assert 0 < s <= 3600
