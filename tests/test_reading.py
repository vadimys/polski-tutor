"""Читалочка: чисті хелпери (нормалізація/токени/переклад/поділ речень)."""

from app.services import reading


def test_norm_strips_punct_and_lowercases():
    assert reading.norm("Dźwięk,") == "dźwięk"
    assert reading.norm("«łabędź»") == "łabędź"
    assert reading.norm("...") == ""
    assert reading.norm("  Znajdź!  ") == "znajdź"


def test_word_tokens_keeps_words_as_in_text():
    toks = reading.word_tokens("Zła wiedźma – ukradła dźwięki.")
    assert toks == ["Zła", "wiedźma", "–", "ukradła", "dźwięki."]


def test_split_sentences_fallback():
    out = reading.split_sentences("Kot pije mleko. Pies śpi!\nPtak lata?")
    assert out == ["Kot pije mleko.", "Pies śpi!", "Ptak lata?"]


def test_translate_matches_normalized_token():
    obj = {"glossary": [{"pl": "wiedźma", "uk": "відьма"}, {"pl": "dźwięki", "uk": "звуки"}]}
    assert reading.translate(obj, "Wiedźma,") == "відьма"  # регістр+пунктуація не заважають
    assert reading.translate(obj, "dźwięki") == "звуки"
    assert reading.translate(obj, "kot") is None


def test_gloss_map_dedupes_first_wins():
    obj = {"glossary": [
        {"pl": "z", "uk": "з"},
        {"pl": "Z", "uk": "інше"},  # той самий нормалізований ключ → перший лишається
    ]}
    assert reading.gloss_map(obj) == {"z": "з"}
