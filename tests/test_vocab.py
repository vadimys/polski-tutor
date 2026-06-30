from app.services import vocab


def test_starter_valid():
    pls = [pl for pl, _ in vocab.STARTER]
    assert len(pls) == len(set(pls)), "польські слова мають бути унікальні"
    assert len(vocab.STARTER) >= 20
    for pl, uk in vocab.STARTER:
        assert pl and uk


def test_starter_has_residency_theme():
    pls = {pl for pl, _ in vocab.STARTER}
    # ключові слова під резиденцію/громадянство
    for word in ("obywatelstwo", "karta pobytu", "urząd", "cudzoziemiec"):
        assert word in pls


def test_dump_roundtrip():
    import json

    raw = vocab._dump("дім", 3, "2026-07-07")
    d = json.loads(raw)
    assert d == {"uk": "дім", "box": 3, "due": "2026-07-07"}
