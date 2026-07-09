"""Реєстр офіційного контенту: агрегат/за-тестом, latest, валідність ключів."""

from app import content


def test_registry_nonempty_and_latest():
    assert content.EXAMS
    assert content.latest() is content.EXAMS[-1]
    assert content.by_id(content.latest().id) is content.latest()


def test_all_items_aggregates_sections():
    r = content.all_items("czytanie")
    g = content.all_items("gramatyka")
    assert len(r) >= 10 and len(g) >= 20
    assert len(content.all_items_flat()) == len(r) + len(g)


def test_exam_items_and_sections():
    eid = content.latest().id
    secs = content.exam_sections(eid)
    assert "czytanie" in secs and "gramatyka" in secs
    assert content.exam_items(eid, "czytanie")  # непорожньо


def test_keys_valid_everywhere():
    for it in content.all_items_flat():
        assert it.section in ("sluchanie", "czytanie", "gramatyka")
        assert 0 <= it.correct < len(it.options)
        assert len(it.options) >= 2 and it.question and it.explain


def test_deterministic_order():
    # стабільний порядок → індекси лишаються валідними між викликами
    assert content.all_items("gramatyka") == content.all_items("gramatyka")
