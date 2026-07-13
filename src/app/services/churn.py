"""Churn-prevention: exit-survey на завершенні trial + save-offer + win-back.

Telegram Stars не має recurring-cancel чи card-dunning, тож наш churn = trial згорів,
а учень не оформив підписку. Ловимо його: exit-survey (причина → адресний оффер),
разовою реактивацією (+N днів для «не встиг»), win-back-нуджами (scheduler). Причини
рахуємо в Redis для аналітики. Реактивація — рівно ОДИН раз на учня (проти зловживань).
"""

from __future__ import annotations

from redis.asyncio import Redis

from app.config import settings

# причини exit-survey (skill churn-prevention: 5-8 опцій, найчастіші спершу)
REASONS: list[tuple[str, str]] = [
    ("price", "💸 Дорого"),
    ("notime", "⏳ Не встиг спробувати"),
    ("unsure", "🤔 Не впевнений, що допоможе"),
    ("noneed", "🙅 Просто не потрібно"),
]
_LABELS = dict(REASONS)


def reason_label(key: str) -> str:
    return _LABELS.get(key, key)


_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def record_reason(reason: str) -> None:
    """Рахуємо причину відмови (розподіл — для рішень про ціну/оффери)."""
    await _r().hincrby("polski:churn:reasons", reason, 1)


async def reasons_report() -> dict[str, int]:
    raw = await _r().hgetall("polski:churn:reasons")
    return {str(k): int(v) for k, v in raw.items()}


async def reoffer_available(user_id: int) -> bool:
    """Чи ще НЕ використано разову реактивацію (+N днів)."""
    return not await _r().exists(f"polski:churn:reoffered:{user_id}")


async def mark_reoffered(user_id: int) -> None:
    await _r().set(f"polski:churn:reoffered:{user_id}", "1")  # без TTL — рівно один раз
