"""Активація: чеклист перших кроків (чисті функції)."""

from app.services import activation


def _steps(*done_keys):
    return [
        {"key": k, "label": lbl, "short": sh, "cb": cb, "done": k in done_keys}
        for k, lbl, sh, cb in activation.STEPS
    ]


def test_next_step_is_first_incomplete():
    assert activation.next_step(_steps())["key"] == "placement"
    assert activation.next_step(_steps("placement"))["key"] == "exercise"
    assert activation.next_step(_steps("placement", "exercise", "word", "habit")) is None


def test_all_done():
    assert not activation.all_done(_steps("placement"))
    assert activation.all_done(_steps("placement", "exercise", "word", "habit"))


def test_render_progress_and_marks():
    t = activation.render(_steps("placement"))
    assert "(1/4)" in t
    assert "✅ Пройти стартовий тест" in t and "◻️ Зробити першу вправу" in t
