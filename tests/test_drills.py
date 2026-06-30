from app.domain.models import Module
from app.services import drills


def test_bank_valid():
    ids = [q.id for q in drills.DRILLS]
    assert len(ids) == len(set(ids))
    for q in drills.DRILLS:
        assert 0 <= q.correct < len(q.options)
        assert len(q.options) >= 2
        assert q.explain


def test_by_id():
    assert drills.by_id("dg1") is not None
    assert drills.by_id("zzz") is None


def test_session_size_and_filter():
    s = drills.session(Module.GRAMATYKA, 5)
    assert len(s) == 5
    assert all(q.module == Module.GRAMATYKA for q in s)


def test_session_falls_back_when_pool_small():
    # просимо більше, ніж є у модулі читання → добираємо із загального банку
    s = drills.session(Module.CZYTANIE, 100)
    assert len(s) == len(drills.DRILLS)
