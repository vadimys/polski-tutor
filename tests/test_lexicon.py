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
