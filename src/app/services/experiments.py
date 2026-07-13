"""A/B-тести копії в боті (skill ab-testing).

Server-side, ДЕТЕРМІНОВАНЕ бакетування за hash(test:user) — користувач завжди бачить
той самий варіант (без flicker, стабільно між рестартами, без Math.random). Метрики —
унікальні exposed/converted у Redis. Первинна метрика: trial→оплата. Конверсію
рахуємо ЛИШЕ для тих, хто реально бачив варіант (чиста воронка exposed→converted).
Анти-peeking: доки вибірка мала — звіт чесно позначає «попередньо».
"""

from __future__ import annotations

import hashlib

from redis.asyncio import Redis

from app.config import settings

MIN_SAMPLE = 30  # доки менше на варіант — не робимо висновків (сумлінність, не значущість)

# Реєстр активних тестів. Одна змінна на тест (skill: test one thing).
TESTS: dict[str, dict] = {
    "paywall_expiry": {
        "label": "Копія екрана завершення trial",
        "hypothesis": (
            "Оскільки часта причина відмов — вагання цінності, втратно-термінове "
            "формулювання (B) підніме конверсію trial→оплата проти підсумку-досягнень (A)."
        ),
        "primary": "trial→оплата (унікальні)",
        "variants": ["A · підсумок-цінності", "B · втрата+дедлайн"],
    },
}

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _bucket(test_key: str, user_id: int, n: int) -> int:
    """Детермінований бакет 0..n-1 (стабільний на користувача й перезапуск)."""
    h = hashlib.sha256(f"{test_key}:{user_id}".encode()).hexdigest()
    return int(h[:8], 16) % max(1, n)


def variant(test_key: str, user_id: int) -> int:
    n = len(TESTS[test_key]["variants"]) if test_key in TESTS else 2
    return _bucket(test_key, user_id, n)


async def expose(test_key: str, user_id: int) -> int:
    """Зафіксувати показ варіанту (унікальний користувач) і повернути його індекс."""
    v = variant(test_key, user_id)
    await _r().sadd(f"ab:{test_key}:exp:{v}", str(user_id))
    return v


async def convert(test_key: str, user_id: int) -> None:
    """Зафіксувати конверсію — лише якщо користувач реально бачив цей варіант."""
    v = variant(test_key, user_id)
    if await _r().sismember(f"ab:{test_key}:exp:{v}", str(user_id)):
        await _r().sadd(f"ab:{test_key}:conv:{v}", str(user_id))


async def report(test_key: str) -> list[dict]:
    t = TESTS.get(test_key)
    if not t:
        return []
    out: list[dict] = []
    for i, name in enumerate(t["variants"]):
        exposed = int(await _r().scard(f"ab:{test_key}:exp:{i}") or 0)
        converted = int(await _r().scard(f"ab:{test_key}:conv:{i}") or 0)
        out.append(
            {
                "variant": i,
                "name": name,
                "exposed": exposed,
                "converted": converted,
                "rate": round(converted / exposed * 100, 1) if exposed else 0.0,
            }
        )
    return out


def render_report(test_key: str, rows: list[dict]) -> str:
    t = TESTS.get(test_key, {})
    lines = [
        f"🧪 <b>{t.get('label', test_key)}</b>",
        f"<i>Гіпотеза:</i> {t.get('hypothesis', '')}",
        f"<i>Метрика:</i> {t.get('primary', '')}\n",
    ]
    for r in rows:
        lines.append(f"{r['name']}: 👁 {r['exposed']} · 💎 {r['converted']} · <b>{r['rate']}%</b>")
    ready = rows and all(r["exposed"] >= MIN_SAMPLE for r in rows)
    if not rows or not any(r["exposed"] for r in rows):
        lines.append("\n<i>Ще немає показів.</i>")
    elif ready:
        best = max(rows, key=lambda r: r["rate"])
        lines.append(f"\n✅ Лідирує <b>{best['name']}</b> ({best['rate']}%). Достатньо даних для рішення.")
    else:
        need = MIN_SAMPLE
        lines.append(
            f"\n⏳ <b>Попередньо</b> — замало даних (треба ≥{need} показів на варіант). "
            "Не роби висновків і не зупиняй тест зарано."
        )
    return "\n".join(lines)
