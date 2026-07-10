"""Дашборд викладача: форматування рядка класу (_row) + активність."""

from app.handlers.teacher import _activity, _row


def test_activity():
    assert _activity(0) == " · активн. сьогодні"
    assert _activity(3) == " · 3 дн тому"
    assert _activity(999) == ""


def _d(**kw):
    base = {
        "name": "@ola", "overall": 62, "passed": 3, "started": True,
        "weak_label": "✍️ Pisanie", "weak_pct": 40, "streak": 5,
        "days_since": 0, "expired": False,
    }
    base.update(kw)
    return base


def test_row_active_student():
    r = _row(_d())
    assert "@ola" in r and "🏁 62%" in r and "3/5 ≥50%" in r
    assert "✍️ Pisanie 40%" in r and "🔥 5" in r and "активн. сьогодні" in r
    assert "trial завершився" not in r


def test_row_not_started():
    r = _row(_d(started=False))
    assert "ще не проходив вправ" in r
    assert "📉" not in r  # без модуля, бо ще не міряно


def test_row_expired_marker_and_no_streak():
    r = _row(_d(expired=True, streak=0))
    assert "⚠️ trial завершився" in r
    assert "🔥" not in r  # серії немає — не показуємо
