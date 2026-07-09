"""Open-таски: парсинг AI-відповіді + валідність даних завдань."""

from app import content
from app.services import opencheck


def test_parse_valid_json():
    raw = '[{"ok": true, "feedback": "добре"}, {"ok": false, "feedback": "не той відмінок"}]'
    out = opencheck._parse(raw, 2)
    assert out == [
        {"ok": True, "feedback": "добре"},
        {"ok": False, "feedback": "не той відмінок"},
    ]


def test_parse_with_prose_around_json():
    raw = 'Ось оцінка:\n[{"ok": true, "feedback": "ок"}]\nсподіваюсь допомогло'
    out = opencheck._parse(raw, 1)
    assert out and out[0]["ok"] is True


def test_parse_wrong_length_is_none():
    raw = '[{"ok": true, "feedback": "x"}]'
    assert opencheck._parse(raw, 3) is None  # очікували 3 пункти


def test_parse_garbage_is_none():
    assert opencheck._parse("вибачте, не можу", 1) is None
    assert opencheck._parse("", 1) is None


def test_parse_coerces_types():
    raw = '[{"ok": 1, "feedback": 123}]'
    out = opencheck._parse(raw, 1)
    assert out == [{"ok": True, "feedback": "123"}]


def test_build_prompt_contains_grounding():
    p = opencheck._build_prompt(
        [{"n": 1, "original": "A lubi B.", "word": "interesuje się",
          "models": ["A interesuje się B."], "answer": "A interesuje się B."}]
    )
    assert "Офіційний зразок" in p and "interesuje się" in p and "Відповідь студента" in p


def test_open_tasks_wellformed():
    tasks = content.all_open_tasks()
    assert tasks, "має бути хоча б одне відкрите завдання"
    for t in tasks:
        assert len(t.prompts) == len(t.words) == len(t.models)
        for m in t.models:
            assert m and all(isinstance(x, str) and x.strip() for x in m)
        assert t.section in ("czytanie", "gramatyka")
        assert t.title and t.intro and t.criterion


def test_open_section_filter():
    assert content.all_open_tasks("gramatyka")  # 2020 Zad VI
    assert content.all_open_tasks("czytanie") == []
    assert content.exam_open_tasks("2020")
