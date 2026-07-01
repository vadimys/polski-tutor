"""Регрес: кнопки відповідей містять індекс питання (захист від дубль-тапів)."""

from app.bot.keyboards import drill_kb, listen_kb, question_kb


def _datas(markup):
    return [b.callback_data for row in markup.inline_keyboard for b in row]


def test_answer_kb_embeds_qidx():
    for fn, prefix in [(question_kb, "pl:ans"), (drill_kb, "dr:ans"), (listen_kb, "ls:ans")]:
        markup = fn(["a", "b", "c"], 3)
        assert _datas(markup) == [f"{prefix}:3:0", f"{prefix}:3:1", f"{prefix}:3:2"]
