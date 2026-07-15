"""TTS: підготовка тексту й детект одиночного слова (для режиму контекст+виріз)."""

from app.integrations.tts import _is_single_word, _norm, _prep


def test_prep_adds_period_to_bare_word():
    assert _prep("skóra") == "skóra."
    assert _prep("  skóra  ") == "skóra."


def test_prep_keeps_existing_terminal_punctuation():
    assert _prep("To jest skóra.") == "To jest skóra."
    assert _prep("Naprawdę?") == "Naprawdę?"


def test_is_single_word():
    assert _is_single_word("skóra")
    assert _is_single_word("  dwadzieścia-cztery  ")  # дефіс — усе ще одне «слово»
    assert not _is_single_word("To jest skóra")
    assert not _is_single_word("")


def test_norm_strips_punct_and_case():
    assert _norm("Skóra.") == "skóra"
    assert _norm("«skóra»") == "skóra"
