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


def test_2020_listening_present_and_sized():
    # Zad I=12, Zad II=7, Zad III=5 (офіц. ключ тесту 2020)
    assert listening.total_questions(listening.by_id("s2020_1")) == 12
    assert listening.total_questions(listening.by_id("s2020_2")) == 7
    assert listening.total_questions(listening.by_id("s2020_3")) == 5
    # Zad III — одне довге аудіо (інтерв'ю) з 5 питаннями TAK/NIE
    z3 = listening.by_id("s2020_3")
    assert len(z3.segments) == 1 and len(z3.segments[0].questions) == 5
    for q in z3.segments[0].questions:
        assert q.options == ["TAK", "NIE"]
