"""A/B: детерміноване bucketing + звіт (чисті функції)."""

from app.services import experiments as ab


def test_variant_deterministic_and_stable():
    # той самий (test,user) → завжди той самий варіант
    assert ab.variant("paywall_expiry", 12345) == ab.variant("paywall_expiry", 12345)
    # різні тести можуть дати різні бакети тому самому юзеру
    assert isinstance(ab.variant("paywall_expiry", 1), int)


def test_split_is_roughly_even():
    buckets = [ab._bucket("t", uid, 2) for uid in range(2000)]
    ones = sum(buckets)
    assert 850 < ones < 1150  # ~50/50 у межах шуму


def test_render_preliminary_gate_below_min_sample():
    rows = [
        {"variant": 0, "name": "A", "exposed": 5, "converted": 2, "rate": 40.0},
        {"variant": 1, "name": "B", "exposed": 4, "converted": 3, "rate": 75.0},
    ]
    t = ab.render_report("paywall_expiry", rows)
    assert "Попередньо" in t and "Гіпотеза" in t  # не оголошуємо переможця зарано


def test_render_declares_leader_when_enough_data():
    rows = [
        {"variant": 0, "name": "A", "exposed": 40, "converted": 8, "rate": 20.0},
        {"variant": 1, "name": "B", "exposed": 40, "converted": 14, "rate": 35.0},
    ]
    t = ab.render_report("paywall_expiry", rows)
    assert "Лідирує" in t and "B" in t
