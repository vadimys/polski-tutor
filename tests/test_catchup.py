"""Вечірній catch-up-нудж: делікатне «ще трохи» лише кому денна ціль не закрита.

Головний важіль — loss aversion на серію (streak). Тестуємо: текст-гілки
(_catchup_text) + маршрутизацію _catchup_due (година / роль / lesson_hour≥catchup /
дедуп / uid≤0).
"""

from __future__ import annotations

import pytest

from app import scheduler
from app.services import goals


class _FakeBot:
    def __init__(self):
        self.sent: list[tuple[int, str]] = []

    async def send_message(self, uid, text, reply_markup=None):
        self.sent.append((uid, text))


# ─────────────────────────── _catchup_text гілки ───────────────────────────
@pytest.fixture
def _goals(monkeypatch):
    state = {"goal": 15, "done": 0, "streak": 0}

    async def _goal(uid):
        return state["goal"]

    async def _done(uid):
        return state["done"]

    async def _streak(uid):
        return state["streak"]

    monkeypatch.setattr(goals, "get_goal", _goal)
    monkeypatch.setattr(goals, "today_minutes", _done)
    monkeypatch.setattr(goals, "current_streak", _streak)
    return state


async def test_text_empty_when_goal_met(_goals):
    _goals.update(goal=15, done=15, streak=5)
    assert await scheduler._catchup_text(1) == ""


async def test_text_streak_loss_aversion(_goals):
    _goals.update(goal=15, done=5, streak=7)
    t = await scheduler._catchup_text(1)
    assert "серія — 7 дн" in t and "~10 хв" in t


async def test_text_finish_when_started_no_streak(_goals):
    _goals.update(goal=15, done=8, streak=0)
    t = await scheduler._catchup_text(1)
    assert "вже почав" in t and "~7 хв" in t


async def test_text_empty_when_idle_no_streak(_goals):
    """streak=0 і нічого не робив → ранковий нудж уже був, не нагадуємо вдруге."""
    _goals.update(goal=15, done=0, streak=0)
    assert await scheduler._catchup_text(1) == ""


# ─────────────────────────── _catchup_due маршрутизація ───────────────────────────
@pytest.fixture
def _wired(monkeypatch):
    # uid: (lesson_hour, role); 3 має lesson_hour=20≥catchup (пропуск), 4 teacher (пропуск)
    hours = {1: 8, 2: 8, 3: 20, 4: 8}
    roles = {1: "student", 2: "student", 3: "student", 4: "teacher"}

    async def ids():
        return [-999, *hours]  # -999 синтетичний → пропуск

    async def load(uid):
        return type("S", (), {"lesson_hour": hours[uid], "role": roles[uid]})()

    async def allowed(uid, admin_id):
        return True

    async def text(uid):
        return "ще трохи" if uid in (1, 2) else ""  # 2 має текст теж

    monkeypatch.setattr(scheduler.state, "all_user_ids", ids)
    monkeypatch.setattr(scheduler.state, "load", load)
    monkeypatch.setattr(scheduler.access, "is_allowed", allowed)
    monkeypatch.setattr(scheduler, "_catchup_text", text)

    marks: set[str] = set()
    monkeypatch.setattr(scheduler, "_already_catchup", lambda u, d: _in(marks, u, d))
    monkeypatch.setattr(scheduler, "_mark_catchup", lambda u, d: _add(marks, u, d))
    return marks


async def _in(marks, uid, today):
    return f"{uid}:{today}" in marks


async def _add(marks, uid, today):
    marks.add(f"{uid}:{today}")


async def test_catchup_wrong_hour_noop(_wired):
    bot = _FakeBot()
    assert await scheduler._catchup_due(bot, hour=8, today="2026-08-01") == 0
    assert bot.sent == []


async def test_catchup_fires_for_eligible_only(_wired):
    bot = _FakeBot()
    n = await scheduler._catchup_due(bot, hour=20, today="2026-08-01")
    # 1,2 підходять (student, lesson_hour<20, є текст); 3 (lesson_hour=20) і 4 (teacher) і -999 — ні
    assert n == 2 and sorted(u for u, _ in bot.sent) == [1, 2]


async def test_catchup_dedupe_same_day(_wired):
    bot = _FakeBot()
    await scheduler._catchup_due(bot, hour=20, today="2026-08-01")
    n2 = await scheduler._catchup_due(bot, hour=20, today="2026-08-01")
    assert n2 == 0  # той самий день — не шлемо вдруге
