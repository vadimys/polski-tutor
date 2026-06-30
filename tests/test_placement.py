from app.services.placement import QUESTIONS, score


def test_questions_valid():
    ids = [q.id for q in QUESTIONS]
    assert len(ids) == len(set(ids)), "id питань мають бути унікальні"
    for q in QUESTIONS:
        assert 0 <= q.correct < len(q.options)
        assert len(q.options) >= 2


def test_all_correct():
    answers = {q.id: q.correct for q in QUESTIONS}
    r = score(answers)
    assert r.correct == r.total == len(QUESTIONS)
    assert r.overall_pct == 100
    assert "B1" in r.level
    assert len(r.per_module) == 5  # усі 5 модулів мають готовність


def test_all_wrong():
    answers = {q.id: (q.correct + 1) % len(q.options) for q in QUESTIONS}
    r = score(answers)
    assert r.overall_pct == 0
    assert r.level == "A1"
    assert len(r.per_module) == 5


def test_partial_only_measured_modules_real():
    # відповідаємо лише на перші 5 правильно, решта пропущена → total=5
    answers = {q.id: q.correct for q in QUESTIONS[:5]}
    r = score(answers)
    assert r.total == 5
    assert r.correct == 5
