"""Денна ціль: константи + рендер рядка прогресу (без Redis — це перевіряється наживо)."""

from app.handlers.menu import _goal_line
from app.services import goals


def test_goal_constants_sane():
    assert goals.DEFAULT_GOAL > 0
    assert goals.GOAL_CHOICES and all(m > 0 for m in goals.GOAL_CHOICES)
    assert goals.MODULE_MIN["pisanie"] > 0 and goals.MODULE_MIN["mowienie"] > 0
    assert goals.LESSON_MIN > 0 and goals.REVIEW_MIN > 0


def test_goal_line_done_shows_check_and_streak():
    s = _goal_line({"today": 20, "goal": 15, "done": True, "streak": 3})
    assert "20/15" in s and "виконано" in s and "3" in s


def test_goal_line_not_done_no_check():
    s = _goal_line({"today": 5, "goal": 15, "done": False, "streak": 0})
    assert "5/15" in s and "виконано" not in s
