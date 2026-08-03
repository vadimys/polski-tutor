"""Мікро-перемоги: видимий приріст готовності модуля після вправи (retention-механіка).

Логіка в єдиному funnel state.update_readiness → наявний celeb-буфер (goals.push_celebration),
який усі ~11 хендлерів уже зливають після вердикту. Тестуємо детерміновано: чисту
_microwin_line + гілки (позитивна дельта / celebrate=False / teacher-превʼю).
"""

from __future__ import annotations

import pytest

from app.db.base import session_factory
from app.db.models import User
from app.services import access, assignments, goals, progress, viewas
from app.services import state as user_state


def test_microwin_line_valid_module():
    line = user_state._microwin_line("sluchanie", 50, 55)
    assert line == "🎧 Słuchanie: 50% → <b>55%</b> (+5%) 📈"


def test_microwin_line_non_module_is_empty():
    assert user_state._microwin_line("nonsense", 50, 55) == ""


@pytest.fixture
def _stub(monkeypatch):
    """Ізолювати update_readiness від Redis-колаборантів; контролювати old/new pct."""
    pushed: list[str] = []

    async def _cap(uid, text):
        pushed.append(text)

    async def _noop(*a, **k):
        return None

    async def _no_assign(uid):
        return []

    async def _viewas_get(uid):
        return None

    monkeypatch.setattr(goals, "push_celebration", _cap)
    monkeypatch.setattr(goals, "record_module", _noop)
    monkeypatch.setattr(assignments, "on_session", _no_assign)
    monkeypatch.setattr(viewas, "get", _viewas_get)
    monkeypatch.setattr(access, "anchor_trial", _noop)  # не про anchoring — ізолюємо від Redis

    async def _compute(uid):
        return {}

    monkeypatch.setattr(progress, "compute", _compute)
    return pushed


async def _seed(uid, *, readiness, role="student"):
    async with session_factory()() as s:
        s.add(User(id=uid, role=role, readiness=readiness))
        await s.commit()


async def test_positive_delta_pushes_microwin(db, _stub, monkeypatch):
    monkeypatch.setattr(progress, "pcts", lambda stats: {"sluchanie": 55})
    await _seed(-8001, readiness={"sluchanie": 50})
    await user_state.update_readiness(-8001, "sluchanie", 80)
    wins = [t for t in _stub if "📈" in t]
    assert wins == ["🎧 Słuchanie: 50% → <b>55%</b> (+5%) 📈"]


async def test_flat_delta_no_microwin(db, _stub, monkeypatch):
    monkeypatch.setattr(progress, "pcts", lambda stats: {"sluchanie": 50})  # без приросту
    await _seed(-8002, readiness={"sluchanie": 50})
    await user_state.update_readiness(-8002, "sluchanie", 40)
    assert not [t for t in _stub if "📈" in t]


async def test_negative_delta_no_microwin(db, _stub, monkeypatch):
    monkeypatch.setattr(progress, "pcts", lambda stats: {"sluchanie": 44})  # свіжість опустила
    await _seed(-8003, readiness={"sluchanie": 50})
    await user_state.update_readiness(-8003, "sluchanie", 30)
    assert not [t for t in _stub if "📈" in t]


async def test_celebrate_false_suppresses(db, _stub, monkeypatch):
    """placement/мок передають celebrate=False — жодної мікро-перемоги."""
    monkeypatch.setattr(progress, "pcts", lambda stats: {"sluchanie": 55})
    await _seed(-8004, readiness={"sluchanie": 50})
    await user_state.update_readiness(-8004, "sluchanie", 80, celebrate=False)
    assert not [t for t in _stub if "📈" in t]


async def test_teacher_preview_no_microwin(db, _stub, monkeypatch):
    """Викладач/превʼю — рання гілка, тільки нотатка про непарахування, без «+N%»."""
    monkeypatch.setattr(progress, "pcts", lambda stats: {"sluchanie": 55})
    await _seed(-8005, readiness={"sluchanie": 50}, role="teacher")
    await user_state.update_readiness(-8005, "sluchanie", 80)
    assert not [t for t in _stub if "📈" in t]
    assert any("Превʼю" in t for t in _stub)


async def test_first_ever_exercise_from_zero(db, _stub, monkeypatch):
    """Перша вправа (немає рядка/готовності): old=0 → показуємо повний бар як перемогу."""
    monkeypatch.setattr(progress, "pcts", lambda stats: {"gramatyka": 40})
    await user_state.update_readiness(-8006, "gramatyka", 40)  # користувача ще нема в БД
    wins = [t for t in _stub if "📈" in t]
    assert len(wins) == 1 and "+40%" in wins[0] and "Gramatyka" in wins[0]
