from app.bot import quiz


def test_parse_answer_valid():
    assert quiz.parse_answer("pl:ans:3:1") == (3, 1)
    assert quiz.parse_answer("dr:ans:0:2") == (0, 2)
    assert quiz.parse_answer("ls:ans:5:0") == (5, 0)


def test_parse_answer_rejects_bad():
    assert quiz.parse_answer("pl:ans:0") is None  # старий формат (3 частини)
    assert quiz.parse_answer("garbage") is None
    assert quiz.parse_answer("pl:ans:x:y") is None


def test_verdict_card_correct():
    out = quiz.verdict_card("Pytanie?", 1, 1, ["a", "b", "c"], "бо так")
    assert "Dobrze" in out and "бо так" in out and "Pytanie?" in out


def test_verdict_card_wrong_shows_answer():
    out = quiz.verdict_card("Pytanie?", 0, 2, ["a", "b", "c"], "")
    assert "Poprawnie" in out and "c" in out
