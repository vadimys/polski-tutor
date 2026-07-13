"""Churn-prevention: причини exit-survey (чисті частини)."""

from app.services import churn


def test_reasons_order_and_labels():
    assert [k for k, _ in churn.REASONS] == ["price", "notime", "unsure", "noneed"]
    assert churn.reason_label("notime").startswith("⏳")
    assert churn.reason_label("невідомо") == "невідомо"  # fallback
