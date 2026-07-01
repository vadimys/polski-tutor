from app.domain.models import Module
from app.services import badges


def test_no_badges_when_empty():
    assert badges.earned({}, 0, 0) == []


def test_first_steps_after_one_session():
    assert "🎯 Перші кроки" in badges.earned({}, 0, 1)


def test_streaks_and_sessions():
    out = badges.earned({}, 7, 100)
    assert any("Тиждень" in x for x in out)
    assert any("100" in x for x in out)


def test_all_modules_passed_badge():
    r = {m.value: 60 for m in Module}
    out = badges.earned(r, 0, 30)
    assert any("готовий" in x.lower() for x in out)
    assert any("5/5" in x for x in out)
