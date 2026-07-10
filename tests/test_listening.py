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


def test_2024_listening_present_and_sized():
    # реальний іспит лютий-2024: Zad I=14, II=6, III=5, IV=6 (офіц. ключ)
    assert listening.total_questions(listening.by_id("s2024_1")) == 14
    assert listening.total_questions(listening.by_id("s2024_2")) == 6
    assert listening.total_questions(listening.by_id("s2024_3")) == 5
    z4 = listening.by_id("s2024_4")
    assert listening.total_questions(z4) == 6
    for q in z4.segments[0].questions:
        assert q.options == ["TAK", "NIE"]
    # Zad III — одне довге аудіо (інтерв'ю) з 5 питаннями
    assert len(listening.by_id("s2024_3").segments) == 1


def test_2024_04_listening_present():
    # квітень-2024: Zad I=14, II=6, III=5, IV=6
    assert listening.total_questions(listening.by_id("s2404_1")) == 14
    assert listening.total_questions(listening.by_id("s2404_2")) == 6
    assert listening.total_questions(listening.by_id("s2404_3")) == 5
    assert listening.total_questions(listening.by_id("s2404_4")) == 6
    for q in listening.by_id("s2404_4").segments[0].questions:
        assert q.options == ["TAK", "NIE"]
    # Zad I key звірено з klucz: b,c,c,a,c,a,b,b,c,a,b,c,a,b
    z1 = [s.questions[0].correct for s in listening.by_id("s2404_1").segments]
    assert z1 == [1, 2, 2, 0, 2, 0, 1, 1, 2, 0, 1, 2, 0, 1]


def test_2024_06_listening_present():
    assert listening.total_questions(listening.by_id("s2406_1")) == 14
    assert listening.total_questions(listening.by_id("s2406_2")) == 6
    assert listening.total_questions(listening.by_id("s2406_3")) == 5
    assert listening.total_questions(listening.by_id("s2406_4")) == 6
    z1 = [s.questions[0].correct for s in listening.by_id("s2406_1").segments]
    assert z1 == [0, 2, 1, 2, 0, 1, 2, 1, 0, 2, 1, 2, 1, 0]  # klucz a,c,b,c,a,b,c,b,a,c,b,c,b,a
    for q in listening.by_id("s2406_4").segments[0].questions:
        assert q.options == ["TAK", "NIE"]


def test_2020_zad5_matching_as_mcq():
    z5 = listening.by_id("s2020_5")
    assert listening.total_questions(z5) == 5
    seg = z5.segments[0]
    # 6 спільних описів-опцій, ключ E,D,B,F,A (індекси 4,3,1,5,0), C(2) — дистрактор
    assert [q.correct for q in seg.questions] == [4, 3, 1, 5, 0]
    for q in seg.questions:
        assert len(q.options) == 6
    assert 2 not in [q.correct for q in seg.questions]  # C ніколи не правильний
