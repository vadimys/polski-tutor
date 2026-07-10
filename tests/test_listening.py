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


def test_2023_02_listening_present():
    assert listening.total_questions(listening.by_id("s2302_1")) == 14
    assert listening.total_questions(listening.by_id("s2302_2")) == 8  # 2023: 8 діалогів
    assert listening.total_questions(listening.by_id("s2302_3")) == 5
    assert listening.total_questions(listening.by_id("s2302_4")) == 5  # 2023: 5 TAK/NIE
    z1 = [s.questions[0].correct for s in listening.by_id("s2302_1").segments]
    assert z1 == [2, 1, 0, 2, 0, 2, 0, 1, 1, 2, 0, 0, 1, 2]


def test_2023_04_listening_present():
    assert listening.total_questions(listening.by_id("s2304_1")) == 14
    assert listening.total_questions(listening.by_id("s2304_2")) == 8
    assert listening.total_questions(listening.by_id("s2304_3")) == 5
    assert listening.total_questions(listening.by_id("s2304_4")) == 5
    z1 = [s.questions[0].correct for s in listening.by_id("s2304_1").segments]
    assert z1 == [2, 1, 2, 1, 0, 2, 0, 2, 1, 1, 0, 2, 1, 2]


def test_2023_06_listening_present():
    assert listening.total_questions(listening.by_id("s2306_1")) == 14
    assert listening.total_questions(listening.by_id("s2306_2")) == 8
    assert listening.total_questions(listening.by_id("s2306_3")) == 5
    assert listening.total_questions(listening.by_id("s2306_4")) == 5
    z1 = [s.questions[0].correct for s in listening.by_id("s2306_1").segments]
    assert z1 == [0, 2, 0, 1, 0, 2, 1, 0, 2, 1, 1, 2, 0, 1]


def test_2023_11_listening_present():
    assert listening.total_questions(listening.by_id("s2311_1")) == 14
    assert listening.total_questions(listening.by_id("s2311_2")) == 6
    assert listening.total_questions(listening.by_id("s2311_3")) == 5
    assert listening.total_questions(listening.by_id("s2311_4")) == 6
    z1 = [s.questions[0].correct for s in listening.by_id("s2311_1").segments]
    assert z1 == [1, 2, 0, 2, 1, 2, 0, 1, 2, 2, 1, 0, 1, 2]


def test_2022_02_listening_present():
    assert listening.total_questions(listening.by_id("s2202_1")) == 14
    assert listening.total_questions(listening.by_id("s2202_2")) == 8
    assert listening.total_questions(listening.by_id("s2202_3")) == 5
    assert listening.total_questions(listening.by_id("s2202_4")) == 5
    z1 = [s.questions[0].correct for s in listening.by_id("s2202_1").segments]
    assert z1 == [1, 1, 2, 0, 2, 1, 2, 1, 0, 1, 2, 0, 2, 0]


def test_2022_11_listening_present():
    assert listening.total_questions(listening.by_id("s2211_1")) == 14
    assert listening.total_questions(listening.by_id("s2211_2")) == 8
    assert listening.total_questions(listening.by_id("s2211_3")) == 5
    assert listening.total_questions(listening.by_id("s2211_4")) == 5
    z1 = [s.questions[0].correct for s in listening.by_id("s2211_1").segments]
    assert z1 == [0, 1, 0, 2, 2, 1, 0, 2, 1, 2, 1, 0, 2, 0]  # klucz a,b,a,c,c,b,a,c,b,c,b,a,c,a
    # Zad III — MCQ-інтерв'ю; Zad IV — TAK/NIE
    assert len(listening.by_id("s2211_3").segments[0].questions[0].options) == 3
    for q in listening.by_id("s2211_4").segments[0].questions:
        assert q.options == ["TAK", "NIE"]


def test_2022_03_listening_present():
    assert listening.total_questions(listening.by_id("s2203_1")) == 14
    assert listening.total_questions(listening.by_id("s2203_2")) == 8
    assert listening.total_questions(listening.by_id("s2203_3")) == 5
    assert listening.total_questions(listening.by_id("s2203_4")) == 5
    z1 = [s.questions[0].correct for s in listening.by_id("s2203_1").segments]
    assert z1 == [2, 1, 0, 0, 1, 2, 1, 2, 0, 2, 2, 1, 0, 1]


def test_2022_06_listening_present():
    assert listening.total_questions(listening.by_id("s2206_1")) == 14
    assert listening.total_questions(listening.by_id("s2206_2")) == 8
    assert listening.total_questions(listening.by_id("s2206_3")) == 5
    assert listening.total_questions(listening.by_id("s2206_4")) == 5
    # Zad III тут TAK/NIE, Zad IV — a/b/c
    for q in listening.by_id("s2206_3").segments[0].questions:
        assert q.options == ["TAK", "NIE"]
    assert len(listening.by_id("s2206_4").segments[0].questions[0].options) == 3


def test_match_audio_wellformed():
    assert listening.MATCH_AUDIO, "має бути хоча б одне аудіо-зіставлення"
    for m in listening.MATCH_AUDIO:
        n = len(m.speakers)
        assert n >= 2 and m.title and m.intro
        assert len(m.prompts) == len(m.key) == len(m.explain)
        for ks in m.key:
            assert ks, "кожен опис стосується хоча б однієї особи"
            assert len(set(ks)) == len(ks)  # без повторів у межах опису
            assert all(0 <= k < n for k in ks)  # індекси в межах мовців
    assert listening.match_audio_by_id("am2020_4") is not None
    assert listening.match_audio_by_id("nope") is None


def test_match_audio_keys_official():
    # ключі звірено з офіц. klucz (0-based індекси мовців)
    expected = {
        "am2020_4": [[2], [0, 3], [1, 3], [3], [1]],  # A=3,B=1&4,C=2&4,D=4,E=2
        "am2402_5": [[0, 3], [4], [0, 2], [1]],  # A=1&4,B=5,C=1&3,D=2
        "am2404_5": [[1, 3], [2], [0], [3], [2]],  # A=2&4,B=3,C=1,D=4,E=3
        "am2406_5": [[4], [1, 3], [0, 2], [0]],  # A=5,B=2&4,C=1&3,D=1
        "am2302_5": [[2], [0, 2], [3], [1]],  # A=3,B=1&3,C=4,D=2
        "am2304_5": [[1], [0, 2], [3], [2]],  # A=2,B=1&3,C=4,D=3
        "am2306_5": [[2, 3], [3], [1], [0]],  # A=3&4,B=4,C=2,D=1
        "am2311_5": [[1], [0, 3], [2], [1], [0]],  # A=2,B=1&4,C=3,D=2,E=1
        "am2211_5": [[3], [1, 2], [0], [2]],  # A=4,B=2&3,C=1,D=3
    }
    for mid, key in expected.items():
        m = listening.match_audio_by_id(mid)
        assert m is not None and m.key == key
        assert len(m.prompts) == len(m.key) == len(m.explain)


def test_content_listening_ids_all_resolve():
    """Звʼязок «тест → аудіо» (content._LISTENING) не має одруків — кожен id існує."""
    from app import content

    for e in content.EXAMS:
        for lid in e.listening_ids:
            assert listening.by_id(lid) is not None, f"{e.id}: неіснуючий audio-id {lid}"
    assert content.latest().listening_ids  # найновіший повний тест має аудіо


def test_2020_zad5_matching_as_mcq():
    z5 = listening.by_id("s2020_5")
    assert listening.total_questions(z5) == 5
    seg = z5.segments[0]
    # 6 спільних описів-опцій, ключ E,D,B,F,A (індекси 4,3,1,5,0), C(2) — дистрактор
    assert [q.correct for q in seg.questions] == [4, 3, 1, 5, 0]
    for q in seg.questions:
        assert len(q.options) == 6
    assert 2 not in [q.correct for q in seg.questions]  # C ніколи не правильний
