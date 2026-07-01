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


def test_guided_speak_steps_all_kinds():
    assert guidance.guided_speak_n("sytuacja") == 5
    assert guidance.guided_speak_n("monolog") == 4
    assert guidance.guided_speak_n("opis") == 5
    assert guidance.guided_available("sytuacja") and not guidance.guided_available("nope")
    first = guidance.guided_speak_step("sytuacja", 0)
    assert "Крок 1/5" in first and "фрази" in first.lower()
    assert "Крок 4/4" in guidance.guided_speak_step("monolog", 3)


def test_guided_writing_steps():
    assert guidance.WRITING_STEPS_N == 4
    assert "Крок 1/4" in guidance.writing_step(0)
    assert "Крок 4/4" in guidance.writing_step(3)
