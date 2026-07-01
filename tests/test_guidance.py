from app.services import guidance


def test_speaking_instruction_all_kinds():
    for kind in ("sytuacja", "monolog", "opis"):
        out = guidance.speaking_instruction(kind)
        assert "Що зробити" in out
        assert "Як будувати" in out
        assert "Корисні фрази" in out
        assert "оцінюю" in out


def test_speaking_example_present():
    for kind in ("sytuacja", "monolog", "opis"):
        assert len(guidance.speaking_example(kind)) > 50


def test_speaking_unknown_kind_safe():
    assert guidance.speaking_instruction("нема") == ""
    assert "недоступний" in guidance.speaking_example("нема")


def test_writing_instruction_shows_genre_elements():
    out = guidance.writing_instruction(
        "ogłoszenie", "хто; мета; предмет; контакт", 30, "list prywatny", "дата; звертання", 170
    )
    assert "ogłoszenie" in out and "list prywatny" in out
    assert "контакт" in out and "звертання" in out
    assert "0-30" in out or "поріг 15" in out


def test_writing_example_present():
    assert "OGŁOSZENIE" in guidance.writing_example()
