"""AI-витрати: розрахунок вартості + рендер (чисті функції)."""

from app.services import aicost


def test_cost_micro_tiers_and_cache():
    # strong: 1000 in @ $3/1M + 200 out @ $15/1M = 0.003 + 0.003 = $0.006
    assert aicost.cost_micro("strong", 1000, 200) == 6000
    # cheap: 1000 in @ $1/1M + 100 out @ $5/1M = 0.001 + 0.0005 = $0.0015
    assert aicost.cost_micro("cheap", 1000, 100) == 1500
    # cache_read дешевший за повний вхід (0.1×)
    full = aicost.cost_micro("strong", 1000, 0)
    cached = aicost.cost_micro("strong", 0, 0, cache_read=1000)
    assert cached < full


def test_render_report_totals_and_cache_pct():
    rows = [
        {"label": "pisanie", "calls": 3, "in": 1000, "out": 400, "cread": 500, "usd": 0.012},
        {"label": "eval", "calls": 1, "in": 200, "out": 50, "cread": 0, "usd": 0.001},
    ]
    t = aicost.render_report(rows)
    assert "pisanie" in t and "50%" in t  # cread/in = 500/1000
    assert "Разом: $0.0130" in t
    assert "немає даних" in aicost.render_report([])
