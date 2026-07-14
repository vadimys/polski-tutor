"""Спостережність AI-витрат: токени й орієнтовна вартість по фічах (skill context-optimization).

«Виміряй перед оптимізацією» — доти ми не бачили, куди йдуть токени/гроші. Лічильники в
Redis (label→calls/in/out/cache_read/мікродолари). Ціни — з тарифів Anthropic (за 1М токенів);
cache-read ~0.1×, cache-write ~1.25× вхідної ціни. Рендер — чиста функція (тестується).
"""

from __future__ import annotations

from redis.asyncio import Redis

from app.config import settings

# $/токен за тіром (Sonnet 4.6: 3/15; Haiku 4.5: 1/5 за 1М)
_PRICE = {
    "strong": {"in": 3e-6, "out": 15e-6},
    "cheap": {"in": 1e-6, "out": 5e-6},
}

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def cost_micro(tier: str, inp: int, out: int, cache_read: int = 0, cache_write: int = 0) -> int:
    """Орієнтовна вартість у мікродоларах (для акумуляції цілими числами)."""
    p = _PRICE.get(tier, _PRICE["cheap"])
    usd = inp * p["in"] + out * p["out"] + cache_read * p["in"] * 0.1 + cache_write * p["in"] * 1.25
    return int(round(usd * 1_000_000))


async def record(label: str, tier: str, usage) -> None:  # noqa: ANN001 — anthropic Usage
    """Залогувати витрати одного AI-виклику (best-effort, не валить основний потік)."""
    inp = int(getattr(usage, "input_tokens", 0) or 0)
    out = int(getattr(usage, "output_tokens", 0) or 0)
    cread = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    cwrite = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)
    micro = cost_micro(tier, inp, out, cread, cwrite)
    r = _r()
    await r.hincrby("aicost:calls", label, 1)
    await r.hincrby("aicost:in", label, inp + cread + cwrite)
    await r.hincrby("aicost:out", label, out)
    await r.hincrby("aicost:cread", label, cread)
    await r.hincrby("aicost:micro", label, micro)


async def report() -> list[dict]:
    r = _r()
    calls = await r.hgetall("aicost:calls")
    ins = await r.hgetall("aicost:in")
    outs = await r.hgetall("aicost:out")
    creads = await r.hgetall("aicost:cread")
    micros = await r.hgetall("aicost:micro")
    rows = []
    for label in calls:
        rows.append(
            {
                "label": label,
                "calls": int(calls.get(label, 0)),
                "in": int(ins.get(label, 0)),
                "out": int(outs.get(label, 0)),
                "cread": int(creads.get(label, 0)),
                "usd": int(micros.get(label, 0)) / 1_000_000,
            }
        )
    return sorted(rows, key=lambda x: x["usd"], reverse=True)


def render_report(rows: list[dict]) -> str:
    if not rows:
        return "💰 <b>AI-витрати</b>\nПоки немає даних."
    lines = ["💰 <b>AI-витрати по фічах</b>\n"]
    total_usd = 0.0
    for r in rows:
        total_usd += r["usd"]
        hit = f" · кеш {round(r['cread'] / r['in'] * 100)}%" if r["in"] else ""
        lines.append(
            f"<b>{r['label']}</b>: {r['calls']} викл · {r['in']}→{r['out']} ток · "
            f"${r['usd']:.4f}{hit}"
        )
    lines.append(f"\n<b>Разом: ${total_usd:.4f}</b>")
    lines.append("<i>Орієнтовно (тарифи Anthropic). Кеш% = частка вхідних токенів із кешу.</i>")
    return "\n".join(lines)
