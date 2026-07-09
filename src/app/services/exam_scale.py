"""Переклад готовності (%) в ОФІЦІЙНІ бали іспиту B1 (Держкомісія).

Реальні максимуми (test przykładowy B1): Słuchanie/Czytanie/Gramatyka/Pisanie —
30 б, Mówienie — 40 б. Поріг складання — ≥50% У КОЖНОМУ модулі. Разом 160 б.
Не вигадуємо — цифри з офіційного пробного тесту ([[polski-b1-exam-official]]).
"""

from __future__ import annotations

from app.domain.models import Module

# офіційні максимуми балів по модулях
MODULE_MAX: dict[str, int] = {
    Module.SLUCHANIE.value: 30,
    Module.CZYTANIE.value: 30,
    Module.GRAMATYKA.value: 30,
    Module.PISANIE.value: 30,
    Module.MOWIENIE.value: 40,
}
TOTAL_MAX = sum(MODULE_MAX.values())  # 160


def module_points(module_value: str, pct: int) -> tuple[int, int, int]:
    """(бали, максимум, поріг=50%) для модуля за готовністю у %."""
    mx = MODULE_MAX.get(module_value, 30)
    return round(pct / 100 * mx), mx, mx // 2


def module_line(module_value: str, pct: int) -> str:
    """«≈22/30 · поріг 15 ✅/🔸» — приписка до бару модуля."""
    pts, mx, thr = module_points(module_value, pct)
    mark = "✅" if pts >= thr else "🔸"
    return f"≈{pts}/{mx} б · поріг {thr} {mark}"


def total_points(readiness: dict[str, int]) -> tuple[int, int]:
    """(сума орієнтовних балів, максимум 160) за готовністю всіх модулів."""
    got = sum(module_points(m.value, readiness.get(m.value, 0))[0] for m in Module)
    return got, TOTAL_MAX
