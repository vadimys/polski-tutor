"""Трекінг фіч: нормалізація події + рендери аналітики."""

from app.services import admin_stats
from app.services.events import feature_of


def test_feature_of_commands_and_callbacks():
    assert feature_of("/lekcja") == "cmd:lekcja"
    assert feature_of("/egzamin@polski_bot start") == "cmd:egzamin"
    assert feature_of("lesson:start") == "cb:lesson"
    assert feature_of("coach:now") == "cb:coach"


def test_feature_of_ignores_admin_and_empty():
    assert feature_of("ac:overview") is None
    assert feature_of("adm:ok:5") is None
    assert feature_of("") is None
    assert feature_of("   ") is None


def test_render_funnel_drop():
    d = {"total": 100, "approved": 80, "placement": 60, "did_ex": 45, "paid": 6}
    t = admin_stats.render_funnel(d)
    assert "Старт (усього)" in t and "<b>100</b>" in t
    assert "−20" in t and "−15" in t  # спад approved(-20) і placement→did_ex(-15)
    assert "6</b> · 6%" in t


def test_render_mods_sorted_hardest_first():
    rows = [("gramatyka", 100, 45), ("czytanie", 80, 72)]
    t = admin_stats.render_mods(rows)
    assert "gramatyka: <b>45%</b>" in t and "czytanie: <b>72%</b>" in t
    # порядок: gramatyka (45) перед czytanie (72)
    assert t.index("gramatyka") < t.index("czytanie")


def test_render_features_top_and_bottom():
    rows = [(f"cb:f{i}", 100 - i, 10 - i % 3) for i in range(15)]
    t = admin_stats.render_features(rows)
    assert "Найпопулярніші:" in t and "cb:f0" in t
    assert "Найрідше вживані:" in t  # >8 фіч → зʼявляється анти-топ


def test_render_features_empty():
    assert "Ще немає даних" in admin_stats.render_features([])
