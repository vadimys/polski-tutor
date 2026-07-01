from app.services import listening


def test_items_valid():
    ids = [it.id for it in listening.ITEMS]
    assert len(ids) == len(set(ids))
    assert len(listening.ITEMS) >= 4
    qids: list[str] = []
    for it in listening.ITEMS:
        assert it.text and it.title
        assert len(it.questions) >= 1
        for q in it.questions:
            assert 0 <= q.correct < len(q.options)
            qids.append(q.id)
    assert len(qids) == len(set(qids)), "id питань мають бути унікальні"


def test_by_id():
    assert listening.by_id("pogoda") is not None
    assert listening.by_id("nope") is None
