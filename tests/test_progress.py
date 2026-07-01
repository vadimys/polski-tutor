from app.domain.models import Module
from app.services import progress


def test_trend_arrows():
    assert progress.trend([]) == "→"
    assert progress.trend([70]) == "→"
    assert progress.trend([80, 60]) == "↑"  # найновіший 80 > попередній 60
    assert progress.trend([50, 70]) == "↓"
    assert progress.trend([60, 60]) == "→"


def test_projection_all_pass():
    r = {m.value: 60 for m in Module}
    assert "≥50%" in progress.projection(r, True, 100)


def test_projection_below_with_date():
    out = progress.projection({"czytanie": 100, "pisanie": 30}, True, 200)
    assert "Нижче порога" in out and "Днів до іспиту" in out


def test_projection_below_no_date():
    out = progress.projection({"pisanie": 30}, False, None)
    assert "Признач дату" in out
