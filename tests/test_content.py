"""Реєстр офіційного контенту: агрегат/за-тестом, latest, валідність ключів."""

from app import content


def test_registry_nonempty_and_latest_is_complete():
    assert len(content.EXAMS) >= 2
    lt = content.latest()
    assert content.by_id(lt.id) is lt
    assert len({it.section for it in lt.items}) >= 2  # дефолт /egzamin — повний тест


def test_all_items_aggregates_across_exams():
    r = content.all_items("czytanie")
    g = content.all_items("gramatyka")
    # 2019 (11 чит + 23 грам) + 2020 (12 чит) → пул виріс
    assert len(r) >= 23 and len(g) >= 20
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
