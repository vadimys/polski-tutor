import importlib.util

from app.bot import charts

_HAS_MPL = importlib.util.find_spec("matplotlib") is not None


def test_empty_readiness_returns_none():
    assert charts.readiness_bar({}) is None
    assert charts.readiness_bar({"unknown": 50}) is None


def test_graceful_without_matplotlib():
    # Без matplotlib має повертати None, не падати (перевіряємо лише коли його справді нема)
    if not _HAS_MPL:
        assert charts.readiness_bar({"pisanie": 40}) is None


def test_renders_png_when_matplotlib_present():
    if not _HAS_MPL:
        return
    png = charts.readiness_bar({"pisanie": 40, "gramatyka": 70})
    assert png is not None and png[:8] == b"\x89PNG\r\n\x1a\n"  # PNG-сигнатура
