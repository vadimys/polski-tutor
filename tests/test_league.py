"""Тижнева ліга XP: sorted-set рейтинг, анонімні аліаси, позиція, forget, рендер."""

from __future__ import annotations

from app.services import league


# ─────────────────────────── аліаси (чисті) ───────────────────────────
def test_alias_stable_and_anonymous():
    a1, a2 = league.alias(12345), league.alias(12345)
    assert a1 == a2  # стабільний
    assert "12345" not in a1 and "@" not in a1  # без PII/username
    assert " " in a1  # «Прикметник Тварина»


def test_alias_varies_by_uid():
    assert league.alias(1) != league.alias(2)


def test_days_to_reset_range():
    assert 1 <= league.days_to_reset() <= 7


# ─────────────────────────── sorted-set (fakeredis) ───────────────────────────
async def test_add_xp_and_top_order(fake_redis):
    await league.add_xp(101, 30)
    await league.add_xp(102, 50)
    await league.add_xp(103, 10)
    await league.add_xp(101, 25)  # 101 → 55 (сумується)
    top = await league.top()
    assert top == [(101, 55), (102, 50), (103, 10)]


async def test_add_xp_ignores_nonpositive(fake_redis):
    await league.add_xp(201, 0)
    await league.add_xp(201, -5)
    assert await league.top() == []


async def test_rank_of(fake_redis):
    await league.add_xp(301, 100)
    await league.add_xp(302, 40)
    assert await league.rank_of(301) == (1, 100)
    assert await league.rank_of(302) == (2, 40)
    assert await league.rank_of(999) == (None, 0)  # ще без XP


async def test_forget_removes_member(fake_redis):
    await league.add_xp(401, 70)
    assert (await league.rank_of(401))[0] == 1
    await league.forget(401)
    assert await league.rank_of(401) == (None, 0)


# ─────────────────────────── рендер ───────────────────────────
def test_render_empty():
    assert "ще ніхто не набрав" in league.render([], 1, None, 0)


def test_render_marks_me_in_top():
    rows = [(101, 90), (102, 50), (103, 20)]
    out = league.render(rows, 102, 2, 50)
    assert "← ти" in out and league.alias(102) in out and "🥈" in out


def test_render_shows_me_outside_top():
    rows = [(i, 100 - i) for i in range(1, 11)]  # топ-10 без мене
    out = league.render(rows, 555, 42, 7)
    assert "…" in out and "42." in out and "← ти" in out
