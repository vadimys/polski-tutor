"""Аналітика: воронка з конверсіями + автопозначення діри; причини відмов."""

from app.services import admin_stats


def test_funnel_conversion_and_biggest_hole():
    d = {"total": 100, "approved": 90, "placement": 30, "did_ex": 25, "paid": 10}
    t = admin_stats.render_funnel(d)
    assert "конв." in t  # показуємо конверсію між кроками
    # найбільша діра — approved→placement (30/90 = 33%)
    assert "Головна діра" in t and "Пройшли placement" in t


def test_funnel_low_data():
    d = {"total": 0, "approved": 0, "placement": 0, "did_ex": 0, "paid": 0}
    assert "Замало даних" in admin_stats.render_funnel(d)


def test_render_churn_distribution_and_empty():
    assert "немає даних" in admin_stats.render_churn({})
    t = admin_stats.render_churn({"price": 3, "notime": 1})
    assert "усього 4" in t and "💸 Дорого" in t and "75%" in t
