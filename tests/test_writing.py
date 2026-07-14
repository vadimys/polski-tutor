from app.bot.ui import bar
from app.services import writing


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


def test_bar():
    assert bar(0).endswith("0%")
    assert bar(150).endswith("100%")
