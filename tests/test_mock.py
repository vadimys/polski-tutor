from app.services import mock


def test_sections_populated():
    r = mock.section_items("czytanie")
    g = mock.section_items("gramatyka")
    assert len(r) >= 10
    assert len(g) >= 20
    assert len(r) + len(g) == len(mock.ITEMS)


def test_all_items_valid():
    for it in mock.ITEMS:
        assert it.section in ("czytanie", "gramatyka")
        assert 0 <= it.correct < len(it.options)
        assert len(it.options) >= 2
        assert it.question and it.explain


def test_no_mixed_cyrillic_in_polish_prompt():
    # «Wybierz poprawną formę» має бути латиницею (регрес: був змішаний «формę»)
    for it in mock.ITEMS:
        assert "формę" not in it.question
