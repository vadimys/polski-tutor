from app.services import feedback, speaking


def test_tasks_valid():
    ids = [t.id for t in speaking.TASKS]
    assert len(ids) == len(set(ids))
    assert len(speaking.TASKS) >= 5
    for t in speaking.TASKS:
        assert t.prompt


def test_task_by_id():
    assert speaking.task_by_id("dzien") is not None
    assert speaking.task_by_id("nope") is None


def test_feedback_parse_score():
    assert feedback.parse_score("dobrze\nWYNIK: 64") == 64
    assert feedback.parse_score("WYNIK: 300") == 100
    assert feedback.parse_score("нема") is None


def test_feedback_strip():
    out = feedback.strip_score_line("Фідбек.\nWYNIK: 70")
    assert "WYNIK" not in out and "Фідбек." in out


def test_writing_reexports_score():
    # writing має лишитись сумісним (реекспорт із feedback)
    from app.services import writing

    assert writing.parse_score("WYNIK: 50") == 50
