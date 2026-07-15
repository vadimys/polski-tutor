"""Хмарний TTS (Azure): екранування SSML + прапорець доступності."""

from app import config
from app.integrations import cloud_tts


def test_escape_ssml_special_chars():
    assert cloud_tts._escape("a & b < c > \"d\"") == "a &amp; b &lt; c &gt; &quot;d&quot;"
    assert cloud_tts._escape("skóra") == "skóra"


def test_available_reflects_config(monkeypatch):
    monkeypatch.setattr(config.settings, "azure_tts_key", "")
    monkeypatch.setattr(config.settings, "azure_tts_region", "")
    assert not cloud_tts.available()
    monkeypatch.setattr(config.settings, "azure_tts_key", "k")
    monkeypatch.setattr(config.settings, "azure_tts_region", "westeurope")
    assert cloud_tts.available()
