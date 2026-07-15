"""TTS: підготовка тексту (крапка для повного закриття синтезу piper)."""

from app.integrations.tts import _prep


def test_prep_adds_period_to_bare_word():
    assert _prep("skóra") == "skóra."
    assert _prep("  skóra  ") == "skóra."


def test_prep_keeps_existing_terminal_punctuation():
    assert _prep("To jest skóra.") == "To jest skóra."
    assert _prep("Naprawdę?") == "Naprawdę?"
    assert _prep("Uwaga!") == "Uwaga!"
