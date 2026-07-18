"""Хмарний TTS (Azure): екранування SSML + прапорець доступності."""

from app import config
from app.integrations import cloud_tts


def test_escape_ssml_special_chars():
    assert cloud_tts._escape("a & b < c > \"d\"") == "a &amp; b &lt; c &gt; &quot;d&quot;"
    assert cloud_tts._escape("skóra") == "skóra"


def test_ssml_normal_has_no_prosody():
    out = cloud_tts._ssml("Dzień dobry", slow=False)
    assert "prosody" not in out
    assert "Dzień dobry" in out


def test_ssml_slow_wraps_prosody_rate():
    out = cloud_tts._ssml("Dzień dobry", slow=True)
    assert f"<prosody rate='{cloud_tts._SLOW_RATE}'>" in out
    assert "</prosody>" in out


def test_available_reflects_config(monkeypatch):
    monkeypatch.setattr(config.settings, "azure_tts_key", "")
    monkeypatch.setattr(config.settings, "azure_tts_region", "")
    assert not cloud_tts.available()
    monkeypatch.setattr(config.settings, "azure_tts_key", "k")
    monkeypatch.setattr(config.settings, "azure_tts_region", "westeurope")
    assert cloud_tts.available()
