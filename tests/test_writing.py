from app.bot.ui import bar
from app.services import writing


def test_tasks_valid():
    ids = [t.id for t in writing.TASKS]
    assert len(ids) == len(set(ids))
    for t in writing.TASKS:
        assert t.prompt and t.genre
        assert t.min_words > 0


def test_task_by_id():
    assert writing.task_by_id("email_priv") is not None
    assert writing.task_by_id("nope") is None


def test_parse_score():
    assert writing.parse_score("Świetnie!\nWYNIK: 72") == 72
    assert writing.parse_score("WYNIK: 0") == 0
    assert writing.parse_score("WYNIK: 250") == 100  # clamp
    assert writing.parse_score("без оцінки") is None


def test_strip_score_line():
    txt = "Фідбек тут.\nWYNIK: 60"
    out = writing.strip_score_line(txt)
    assert "WYNIK" not in out
    assert "Фідбек тут." in out


def test_bar():
    assert bar(0).endswith("0%")
    assert bar(100).endswith("100%")
    assert bar(150).endswith("100%")  # clamp
    assert "▰" in bar(60)
