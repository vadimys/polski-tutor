from app.bot.ui import bar
from app.services import feedback, writing


def test_sets_valid():
    ids = [s.id for s in writing.SETS]
    assert len(ids) == len(set(ids))
    assert len(writing.SETS) >= 6
    for s in writing.SETS:
        for task in (s.a, s.b):
            assert task.prompt and task.genre
            assert task.words > 0


def test_set_by_id():
    assert writing.set_by_id("t1") is not None
    assert writing.set_by_id("nope") is None


def test_known_genres_have_requirements():
    # кожен жанр із наборів має офіційні вимоги форми
    for s in writing.SETS:
        for task in (s.a, s.b):
            assert task.genre in writing.GENRE_REQ, task.genre


def test_parse_official_pisanie():
    txt = "Оцінка...\nWYNIK: wykonanie=8 środki=7 poprawność=6"
    assert feedback.parse_official_pisanie(txt) == (8, 7, 6)
    assert feedback.parse_official_pisanie("WYNIK: wykonanie=15 środki=0 poprawność=3") == (10, 0, 3)
    assert feedback.parse_official_pisanie("без оцінки") is None


def test_strip_official_line():
    out = feedback.strip_official_line("Фідбек тут.\nWYNIK: wykonanie=8 środki=7 poprawność=6")
    assert "WYNIK" not in out and "Фідбек тут." in out


def test_bar():
    assert bar(0).endswith("0%")
    assert bar(150).endswith("100%")
