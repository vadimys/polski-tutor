"""Авто-оцінка open-tasks: робастна нормалізація structured output."""

from app.services import opencheck


def test_normalize_valid():
    data = {"results": [{"ok": True, "feedback": "добре"}, {"ok": False, "feedback": "виправ час"}]}
    out = opencheck._normalize(data, 2)
    assert out == [{"ok": True, "feedback": "добре"}, {"ok": False, "feedback": "виправ час"}]


def test_normalize_count_mismatch():
    assert opencheck._normalize({"results": [{"ok": True, "feedback": "x"}]}, 2) is None


def test_normalize_bad_shapes():
    assert opencheck._normalize({}, 1) is None
    assert opencheck._normalize([], 1) is None
    assert opencheck._normalize({"results": "nope"}, 1) is None


def test_normalize_coerces_and_truncates():
    out = opencheck._normalize({"results": [{"ok": 1, "feedback": "x" * 500}]}, 1)
    assert out[0]["ok"] is True and len(out[0]["feedback"]) == 300


def test_schema_is_object_with_results_array():
    s = opencheck._SCHEMA
    assert s["type"] == "object" and "results" in s["properties"]
    assert s["properties"]["results"]["items"]["additionalProperties"] is False


def test_build_prompt_contains_grounding():
    p = opencheck._build_prompt(
        [{"n": 1, "original": "A lubi B.", "word": "interesuje się",
          "models": ["A interesuje się B."], "answer": "A interesuje się B."}]
    )
    assert "Офіційний зразок" in p and "interesuje się" in p and "Відповідь студента" in p
