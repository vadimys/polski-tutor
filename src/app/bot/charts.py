"""Графіки прогресу (matplotlib, Agg через OO-API — без pyplot, потоко-безпечно).

matplotlib — опційна залежність (extra "viz"). Якщо не встановлено — повертаємо None,
і хендлер деградує до текстового прогресу.
"""

from __future__ import annotations

import io

# Порядок і чисті підписи (без емоджі — DejaVu Sans не має емоджі-гліфів)
_LABELS = {
    "pisanie": "Pisanie",
    "mowienie": "Mówienie",
    "sluchanie": "Słuchanie",
    "czytanie": "Czytanie",
    "gramatyka": "Gramatyka",
}
_ORDER = list(_LABELS)


def readiness_bar(readiness: dict[str, int]) -> bytes | None:
    """Горизонтальна діаграма готовності по виміряних модулях (з порогом 50%).

    None, якщо немає виміряних модулів або matplotlib недоступний.
    """
    measured = [(k, int(v)) for k, v in readiness.items() if k in _LABELS]
    if not measured:
        return None
    try:
        from matplotlib.figure import Figure
    except Exception:  # noqa: BLE001 — без matplotlib деградуємо до тексту
        return None

    measured.sort(key=lambda kv: _ORDER.index(kv[0]))
    labels = [_LABELS[k] for k, _ in measured]
    values = [v for _, v in measured]
    colors = ["#4caf50" if v >= 50 else "#ffa726" if v >= 30 else "#ef5350" for v in values]

    fig = Figure(figsize=(6, 0.62 * len(values) + 1.4), dpi=110)
    ax = fig.subplots()
    ax.barh(labels, values, color=colors)
    ax.axvline(50, color="#444", linestyle="--", linewidth=1, label="поріг 50%")
    ax.set_xlim(0, 100)
    ax.set_xlabel("Готовність, %")
    ax.set_title("Готовність за модулями")
    ax.invert_yaxis()
    for i, v in enumerate(values):
        ax.text(min(v + 2, 95), i, f"{v}%", va="center", fontsize=9)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    return buf.getvalue()
