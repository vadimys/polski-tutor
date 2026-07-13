"""Тематичний словник: цілісність підтем + парсер (чисті частини)."""

from app.services import lexicon


def test_every_topic_has_subtopics():
    for key, _ in lexicon.TOPICS:
        subs = lexicon.subtopics(key)
        assert subs, f"тема {key} без підтем"
        keys = [s for s, _ in subs]
        assert len(keys) == len(set(keys)), f"дублі підтем у {key}"
        assert all(lbl for _, lbl in subs)


def test_labels_and_fallback():
    assert lexicon.topic_label("jedzenie").startswith("🍽")
    assert "Овоч" in lexicon.sub_label("jedzenie", "owoce")
    assert lexicon.sub_label("jedzenie", "nope") == "nope"  # фолбек
    assert lexicon.topic_label("nope") == "nope"


def test_parse_dedups_and_sorts_by_level():
    raw = """[
      {"pl":"trudny","ua":"важкий","example":"","level":3},
      {"pl":"dom","ua":"дім","example":"To jest dom.","level":1},
      {"pl":"dom","ua":"дубль","example":"","level":1},
      {"pl":"okno","ua":"вікно","example":"","level":2}
    ]"""
    words = lexicon._parse(raw)
    assert [w.pl for w in words] == ["dom", "okno", "trudny"]  # дедуп + сорт за level


def test_parse_handles_codefence_and_junk():
    assert lexicon._parse("```json\n[]\n```") == []
    assert lexicon._parse("not json") == []


def test_apply_edit_changes_ua_and_example():
    arr = [{"pl": "pomidorek", "ua": "помідор", "example": "", "level": 1}]
    assert lexicon._apply_edit(arr, "pomidorek", "помідорчик", "To pomidorek.") is True
    assert arr[0]["ua"] == "помідорчик" and arr[0]["example"] == "To pomidorek."
    assert lexicon._apply_edit(arr, "brak", "x", None) is False  # нема слова


def test_apply_edit_keeps_example_when_none():
    arr = [{"pl": "dom", "ua": "дім", "example": "stary", "level": 1}]
    lexicon._apply_edit(arr, "dom", "будинок", None)
    assert arr[0]["ua"] == "будинок" and arr[0]["example"] == "stary"  # приклад не чіпаємо


def test_apply_remove():
    arr = [{"pl": "a", "ua": "1"}, {"pl": "b", "ua": "2"}]
    assert [o["pl"] for o in lexicon._apply_remove(arr, "a")] == ["b"]
