"""Вільний словник: парсинг слів + сортування легше→важче."""

from app.services import lexicon


def test_topics_nonempty_and_labeled():
    assert lexicon.TOPICS
    key = lexicon.TOPICS[0][0]
    assert lexicon.label(key) == lexicon.TOPICS[0][1]


def test_parse_sorts_by_level_and_keeps_fields():
    raw = (
        '[{"pl":"trudny","ua":"складний","example":"To trudny test.","level":3},'
        '{"pl":"dom","ua":"дім","example":"Mam dom.","level":1},'
        '{"pl":"praca","ua":"робота","example":"Idę do pracy.","level":2}]'
    )
    words = lexicon._parse(raw)
    assert [w.level for w in words] == [1, 2, 3]  # від найлегших до найважчих
    assert words[0].pl == "dom" and words[0].example.startswith("Mam")


def test_parse_handles_code_fence_and_bad_items():
    raw = '```json\n[{"pl":"kot","ua":"кіт","level":1},{"bad":"x"}]\n```'
    words = lexicon._parse(raw)
    assert len(words) == 1 and words[0].pl == "kot"


def test_parse_garbage_returns_empty():
    assert lexicon._parse("no json here") == []
