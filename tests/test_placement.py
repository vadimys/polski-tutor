from app.domain.models import Module
from app.services import placement
from app.services.placement import QUESTIONS, build_test, score


def test_questions_valid():
    ids = [q.id for q in QUESTIONS]
    assert len(ids) == len(set(ids)), "id питань мають бути унікальні"
    for q in QUESTIONS:
        assert 0 <= q.correct < len(q.options)
        assert len(q.options) >= 2


def test_all_correct_only_measured_modules():
    answers = {q.id: q.correct for q in QUESTIONS}
    r = score(answers)
    assert r.correct == r.total == len(QUESTIONS)
    assert r.overall_pct == 100
    # ЛИШЕ реально виміряні модулі — без вигаданих Pisanie/Mówienie/Słuchanie
    assert set(r.per_module) == {Module.GRAMATYKA.value, Module.CZYTANIE.value}
    assert Module.PISANIE.value not in r.per_module
    assert Module.MOWIENIE.value not in r.per_module
    assert Module.SLUCHANIE.value not in r.per_module


def test_all_wrong():
    answers = {q.id: (q.correct + 1) % len(q.options) for q in QUESTIONS}
    r = score(answers)
    assert r.overall_pct == 0
    assert r.level == "A1"


def test_build_test_balanced_and_from_big_bank():
    t = build_test()
    ids = [q.id for q in t]
    assert len(ids) == len(set(ids))  # без дублів у тесті
    assert sum(q.module == Module.GRAMATYKA for q in t) == 12
    assert sum(q.module == Module.CZYTANIE for q in t) == 6
    # банк достатньо великий, щоб вибірки різнились між проходженнями
    assert len([q for q in QUESTIONS if q.module == Module.GRAMATYKA]) >= 20
    assert len([q for q in QUESTIONS if q.module == Module.CZYTANIE]) >= 10


def test_by_id():
    assert placement.by_id("g1") is not None
    assert placement.by_id("nope") is None
