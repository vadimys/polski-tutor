from app.services import listening


def test_exercises_valid():
    ids = [e.id for e in listening.EXERCISES]
    assert len(ids) == len(set(ids))
    assert len(listening.EXERCISES) >= 3
    for e in listening.EXERCISES:
        assert e.title and e.intro and e.segments
        for seg in e.segments:
            assert seg.audio
            for q in seg.questions:
                assert 0 <= q.correct < len(q.options)
                assert q.text


def test_by_id():
    assert listening.by_id("willa") is not None
    assert listening.by_id("nope") is None


def test_total_questions_match_official_key():
    assert listening.total_questions(listening.by_id("u1")) == 10
    assert listening.total_questions(listening.by_id("willa")) == 8
    assert listening.total_questions(listening.by_id("muzeum")) == 5
