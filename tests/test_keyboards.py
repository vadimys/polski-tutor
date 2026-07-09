"""Регрес: кнопки відповідей містять індекс питання (захист від дубль-тапів) + вихід."""

from app.bot.keyboards import drill_kb, mock_kb, question_kb


def _datas(markup):
    return [b.callback_data for row in markup.inline_keyboard for b in row]


def test_answer_kb_embeds_qidx_and_exit():
    cases = [
        (question_kb, "pl:ans", "pl:stop"),
        (drill_kb, "dr:ans", "dr:stop"),
        (mock_kb, "mk:ans", "mk:stop"),
    ]
    for fn, prefix, stop in cases:
        datas = _datas(fn(["a", "b", "c"], 3))
        # варіанти з індексом питання
        assert datas[:3] == [f"{prefix}:3:0", f"{prefix}:3:1", f"{prefix}:3:2"]
        # кнопка дострокового виходу — окремий callback, не плутається з :ans:
        assert datas[-1] == stop
