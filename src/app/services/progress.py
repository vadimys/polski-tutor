"""Аналітика прогресу + ЧЕСНА оцінка готовності.

Готовність модуля = Результат × Впевненість × Свіжість (рахується з ІСТОРІЇ сесій,
не з ковзного середнього) — щоб «2 вдалі дні» не давали «готовий»:
  • Результат  — зважене середнє останніх балів (свіжіші важать більше);
  • Впевненість — росте від кількості вправ І кількості різних днів (анти-зубріння);
  • Свіжість   — спадає з часом простою (треба повторювати постійно).
Профіль «збалансовано»: повна впевненість ≈ 8 вправ за 3 дні; спад удвічі за 2 тижні.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from redis.asyncio import Redis
from sqlalchemy import func, select

from app.config import settings
from app.db.base import session_factory
from app.db.models import Session
from app.domain.models import MODULE_LABELS, Module
from app.services import clock

# --- калібрування «збалансовано» ---
_P_RECENCY = 0.85  # вага кожного давнішого бала (експоненційний спад)
_P_WINDOW = 10  # скільки останніх балів беремо в результат
_CONF_ATTEMPTS = 8  # вправ на повну впевненість
_GRACE_DAYS = 7  # свіжість без спаду
_HALF_LIFE = 14  # спад готовності вдвічі за стільки днів простою
_MASTERY = 70  # поріг «впевнено» для модуля
_MOCK_PASS = 60  # поріг складання повного моку секції
_MOCK_TTL = 30 * 24 * 3600  # «склав мок» дійсне (свіжість підтвердження)
_MOCK_SECTIONS = ("czytanie", "gramatyka")  # секції з повним моком

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


@dataclass
class ModuleStat:
    pct: int  # підсумкова готовність 0..100
    attempts: int  # скільки вправ модуля зроблено
    days: int  # у скількох РІЗНИХ днях практикувався
    days_since: int  # днів від останньої практики (999 якщо не було)
    mastered: bool  # pct ≥ поріг


def readiness_score(perf: float, attempts: int, days: int, days_since: int) -> int:
    """Результат × Впевненість × Свіжість → 0..100 (чиста функція, легко тестувати)."""
    conf = min(1.0, attempts / _CONF_ATTEMPTS) * (0.6 + 0.4 * min(1.0, (days - 1) / 2))
    fresh = 0.5 ** (max(0, days_since - _GRACE_DAYS) / _HALF_LIFE)
    return max(0, min(100, round(perf * conf * fresh)))


async def compute(user_id: int) -> dict[str, ModuleStat]:
    """Готовність по всіх 5 модулях із історії сесій (Результат×Впевненість×Свіжість)."""
    async with session_factory()() as s:
        rows = (
            await s.execute(
                select(Session.module, Session.score, Session.created_at)
                .where(Session.user_id == user_id)
                .order_by(Session.created_at.desc())
            )
        ).all()
    tzinfo = clock.tz()
    today = clock.today_local()
    by_mod: dict[str, list[tuple[int, date]]] = {}
    for module, score, created in rows:
        by_mod.setdefault(module, []).append((score, created.astimezone(tzinfo).date()))

    out: dict[str, ModuleStat] = {}
    for m in Module:
        recs = by_mod.get(m.value, [])  # найновіші спершу
        if not recs:
            out[m.value] = ModuleStat(0, 0, 0, 999, False)
            continue
        wsum = w = 0.0
        wt = 1.0
        for score, _d in recs[:_P_WINDOW]:  # Результат — зважене середнє останніх балів
            wsum += wt * score
            w += wt
            wt *= _P_RECENCY
        perf = wsum / w
        attempts = len(recs)
        days = len({d for _s, d in recs})
        days_since = (today - max(d for _s, d in recs)).days
        pct = readiness_score(perf, attempts, days, days_since)
        out[m.value] = ModuleStat(pct, attempts, days, days_since, pct >= _MASTERY)
    return out


def pcts(stats: dict[str, ModuleStat]) -> dict[str, int]:
    """Плоский {модуль: готовність%} для барів/квесту/плану."""
    return {k: v.pct for k, v in stats.items()}


async def record_mock_pass(user_id: int, section: str, pct: int) -> None:
    """Позначити складений повний мок секції (для гейту готовності)."""
    if pct >= _MOCK_PASS and section in _MOCK_SECTIONS:
        await _r().set(f"polski:mokpass:{user_id}:{section}", "1", ex=_MOCK_TTL)


async def mock_ok(user_id: int) -> bool:
    """Чи складено НЕЩОДАВНО повний мок обох секцій (доказ «під іспитом»)."""
    for sec in _MOCK_SECTIONS:
        if not await _r().get(f"polski:mokpass:{user_id}:{sec}"):
            return False
    return True


async def counts(user_id: int) -> tuple[int, int]:
    """(усього вправ, за останні 7 днів)."""
    async with session_factory()() as s:
        total = (
            await s.execute(
                select(func.count()).select_from(Session).where(Session.user_id == user_id)
            )
        ).scalar() or 0
        week_ago = clock.now_local() - timedelta(days=7)
        last7 = (
            await s.execute(
                select(func.count())
                .select_from(Session)
                .where(Session.user_id == user_id, Session.created_at >= week_ago)
            )
        ).scalar() or 0
        return int(total), int(last7)


async def recent_scores(user_id: int, module_value: str, limit: int = 5) -> list[int]:
    """Останні бали модуля (найновіші спершу)."""
    async with session_factory()() as s:
        rows = await s.execute(
            select(Session.score)
            .where(Session.user_id == user_id, Session.module == module_value)
            .order_by(Session.created_at.desc())
            .limit(limit)
        )
        return [r[0] for r in rows.all()]


READY_THRESHOLD = 70  # усі 5 модулів ≥ цього → «схоже, готовий до іспиту» (запас над 50%)


def verdict(stats: dict[str, ModuleStat], is_mock_ok: bool) -> tuple[str, list[Module]]:
    """Стан підготовки (жорсткий гейт — не «2 вдалі дні»):

    ('incomplete', [невиміряні])  — якийсь модуль ще без жодної вправи;
    ('gaps', [слабкі])            — виміряні, але не всі впевнені (<70 із урахуванням
                                     обсягу/днів/свіжості);
    ('almost', [])                — усі 5 впевнені, але ще не складено повний мок;
    ('ready', [])                 — усі впевнені + складено моки (обидві секції ≥60).
    """
    missing = [m for m in Module if stats[m.value].attempts == 0]
    if missing:
        return "incomplete", missing
    weak = [m for m in Module if not stats[m.value].mastered]
    if weak:
        return "gaps", weak
    if not is_mock_ok:
        return "almost", []
    return "ready", []


def trend(scores: list[int]) -> str:
    """Стрілка тренду за останніми двома балами (найновіші спершу)."""
    if len(scores) < 2:
        return "→"
    if scores[0] > scores[1]:
        return "↑"
    if scores[0] < scores[1]:
        return "↓"
    return "→"


def projection(readiness: dict[str, int], has_date: bool, days_left: int | None) -> str:
    """Чесний якісний прогноз готовності до порога ≥50% у кожному модулі."""
    below = [m for m in Module if readiness.get(m.value, 0) < 50]
    if not below:
        return "✅ Усі модулі ≥50% — тримай темп до іспиту!"
    names = ", ".join(MODULE_LABELS[m] for m in below)
    if has_date and days_left is not None:
        pace = (
            "встигаєш, якщо тримати ~1 год/день"
            if days_left >= len(below) * 14
            else "часу впритул — фокус лише на цих модулях"
        )
        return f"🔸 Нижче порога (50%): {names}.\n📈 Днів до іспиту: {days_left} — {pace}."
    return f"🔸 Нижче порога (50%): {names}. Признач дату іспиту для точнішого прогнозу."
