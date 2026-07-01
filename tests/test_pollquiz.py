from app.services import pollquiz


def test_fits_short_items():
    items = [{"q": "2+2=?", "opts": ["3", "4", "5"], "correct": 1, "explain": "бо так"}]
    assert pollquiz.fits(items)


def test_rejects_long_question():
    items = [{"q": "x" * 400, "opts": ["a", "b"], "correct": 0}]
    assert not pollquiz.fits(items)


def test_rejects_long_option():
    items = [{"q": "Q?", "opts": ["a", "b" * 150], "correct": 0}]
    assert not pollquiz.fits(items)


def test_rejects_bad_option_count():
    assert not pollquiz.fits([{"q": "Q?", "opts": ["only"], "correct": 0}])  # <2
    assert not pollquiz.fits([{"q": "Q?", "opts": [str(i) for i in range(11)], "correct": 0}])  # >10


def test_rejects_correct_out_of_range():
    assert not pollquiz.fits([{"q": "Q?", "opts": ["a", "b"], "correct": 5}])
