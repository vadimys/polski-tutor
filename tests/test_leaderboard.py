"""Груповий лідерборд: рендер + порядок (стрік ↓, тоді готовність)."""

from app.services import leaderboard


def test_render_medals_and_highlight():
    rows = [
        {"id": 1, "name": "@a", "streak": 12, "overall": 70, "rank": 1},
        {"id": 2, "name": "@b", "streak": 8, "overall": 55, "rank": 2},
        {"id": 3, "name": "@c", "streak": 3, "overall": 40, "rank": 3},
        {"id": 4, "name": "@d", "streak": 1, "overall": 20, "rank": 4},
    ]
    t = leaderboard.render(rows, "Ранкова B1", highlight_id=2)
    assert "🏆" in t and "Ранкова B1" in t
    assert "🥇 @a · 🔥12 · 🏁70%" in t
    assert "🥈 @b" in t and "← ти" in t  # підсвічування себе
    assert "4. @d" in t  # поза топ-3 — номер


def test_render_empty():
    assert "немає учнів" in leaderboard.render([], "Клас")
