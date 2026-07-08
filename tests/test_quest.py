"""Квест-мапа: чистий рендер прогресу-подорожі."""

from app.domain.models import Module
from app.services import quest


def _all(v: int) -> dict[str, int]:
    return {m.value: v for m in Module}


def test_overall_pct_scales_to_ready_threshold():
    assert quest.overall_pct(_all(0)) == 0
    assert quest.overall_pct(_all(70)) == 100  # усі на порозі готовності → 100% шляху
    assert quest.overall_pct(_all(35)) == 50


def test_render_has_stations_and_locked_boss():
    txt = quest.render(_all(30), days_left=150, level=2, streak=4)
    assert "Похід до B1" in txt
    assert "150" in txt and "станці" in txt.lower()
    assert "🔒" in txt and "Бос" in txt  # бос замкнений (модулі <50%)
    assert "🚶" in txt  # маркер позиції на стежці/станції


def test_render_unlocks_boss_when_all_pass():
    txt = quest.render(_all(60), days_left=None, level=5, streak=10)
    assert "/mok" in txt  # усі ≥50% → бос відкритий


def test_render_ready_celebration():
    txt = quest.render(_all(75), days_left=10, level=8, streak=20)
    assert "готовий до B1" in txt
