"""Переклад % готовності в офіційні бали B1 (реальні максимуми Держкомісії)."""

from app.domain.models import Module
from app.services import exam_scale


def test_module_max_matches_official():
    assert exam_scale.MODULE_MAX[Module.MOWIENIE.value] == 40  # мовлення — 40 б
    assert exam_scale.MODULE_MAX[Module.GRAMATYKA.value] == 30
    assert exam_scale.TOTAL_MAX == 160


def test_points_and_threshold():
    assert exam_scale.module_points(Module.GRAMATYKA.value, 100) == (30, 30, 15)
    assert exam_scale.module_points(Module.GRAMATYKA.value, 50) == (15, 30, 15)
    assert exam_scale.module_points(Module.MOWIENIE.value, 100) == (40, 40, 20)
    assert exam_scale.module_points(Module.MOWIENIE.value, 0) == (0, 40, 20)


def test_total_points_full():
    got, mx = exam_scale.total_points({m.value: 100 for m in Module})
    assert (got, mx) == (160, 160)


def test_module_line_marks_pass():
    assert "✅" in exam_scale.module_line(Module.CZYTANIE.value, 80)
    assert "🔸" in exam_scale.module_line(Module.CZYTANIE.value, 30)
