"""Tier-1 стійкість: семафор AI + поріг денного бюджету (детерміновані частини)."""

from app import config
from app.integrations import ai
from app.services import aicost


def test_ai_semaphore_singleton_and_size():
    ai._sem = None  # скидаємо лінивий singleton
    s = ai._semaphore()
    assert s is ai._semaphore()  # той самий обʼєкт
    assert s._value == config.settings.ai_max_concurrency


def test_over_budget_threshold():
    assert aicost._over_budget(6_000_000, 5.0) == 6.0  # $6 ≥ $5 → спрацьовує
    assert aicost._over_budget(4_000_000, 5.0) is None  # $4 < $5
    assert aicost._over_budget(9_000_000, 0.0) is None  # поріг 0 → вимкнено
