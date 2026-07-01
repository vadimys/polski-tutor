"""Гейміфікація: бейджі-досягнення (чиста функція від стану — легко тестувати)."""

from __future__ import annotations

from app.domain.models import Module


def earned(readiness: dict[str, int], streak: int, total_sessions: int) -> list[str]:
    """Список зароблених бейджів за поточним станом."""
    b: list[str] = []
    if total_sessions >= 1:
        b.append("🎯 Перші кроки")
    if total_sessions >= 25:
        b.append("📚 25 вправ")
    if total_sessions >= 100:
        b.append("🏋️ 100 вправ")
    if streak >= 3:
        b.append("🔥 Стрік 3+")
    if streak >= 7:
        b.append("🔥🔥 Тиждень поспіль")
    passed = sum(1 for m in Module if readiness.get(m.value, 0) >= 50)
    if passed >= 1:
        b.append(f"✅ Модулів ≥50%: {passed}/5")
    if passed == 5:
        b.append("🏆 Усі 5 модулів ≥50% — готовий до іспиту!")
    return b
