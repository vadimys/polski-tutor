"""Тренажер дієслів: SRS-повторення (Leitner) замість простих лічильників помилок.

Стан — Redis-хеш verbs:srs:<kind>:<uid> (kind: forms/rekcja), поле "gi:vi" →
"box|due" (коробка 1-5 + дата наступного повторення; інтервали рахує services/srs —
той самий рушій, що й у словнику: 1→3→7→16→35 днів; помилка → коробка 1).
Підбір сесії: спершу «доспілі» (due ≤ сьогодні), тоді нові (ще не бачені), тоді
найближчі майбутні. Прогрес B1 не рухає — це навчальний тренажер.
"""

from __future__ import annotations

import random
from datetime import date

from redis.asyncio import Redis

from app import verbs
from app.config import settings
from app.services import clock, srs

_redis: Redis | None = None
DRILL_SIZE = 5

PAST_RATIO = 0.35  # частка питань у минулому часі (де парадигма доступна)
FUTURE_RATIO = 0.25  # частка питань у майбутньому складеному (będę + inf)


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(uid: int, kind: str = "forms") -> str:
    return f"verbs:srs:{kind}:{uid}"


def _legacy_key(uid: int, kind: str = "forms") -> str:
    return f"verbs:wrong:{kind}:{uid}"  # старі лічильники помилок (до SRS)


def _parse_field(f: str) -> tuple[int, int] | None:
    try:
        gi, vi = str(f).split(":")
        return int(gi), int(vi)
    except ValueError:
        return None


async def _migrate_legacy(uid: int, kind: str) -> None:
    """Одноразово: старі лічильники помилок → коробка 1, доспіло сьогодні."""
    old = await _r().hgetall(_legacy_key(uid, kind))
    if not old:
        return
    today = clock.today_local().isoformat()
    for f in old:
        if _parse_field(str(f)) is not None:
            await _r().hset(_key(uid, kind), str(f), f"1|{today}")
    await _r().delete(_legacy_key(uid, kind))


async def srs_state(uid: int, kind: str = "forms") -> dict[tuple[int, int], tuple[int, str]]:
    """{(gi, vi): (box, due)} — стан SRS користувача для тренажера kind."""
    await _migrate_legacy(uid, kind)
    raw = await _r().hgetall(_key(uid, kind))
    out: dict[tuple[int, int], tuple[int, str]] = {}
    for f, v in raw.items():
        coords = _parse_field(str(f))
        if coords is None:
            continue
        box_s, _, due = str(v).partition("|")
        try:
            out[coords] = (int(box_s), due)
        except ValueError:
            continue
    return out


async def record_answer(uid: int, gi: int, vi: int, ok: bool, kind: str = "forms") -> None:
    """Оновити SRS: правильно → коробка вище (довший інтервал), помилка → коробка 1."""
    state = await srs_state(uid, kind)
    box = state.get((gi, vi), (0, ""))[0]
    new_box = srs.on_correct(box) if ok else srs.on_wrong(box)
    due = srs.next_due(new_box, clock.today_local())
    await _r().hset(_key(uid, kind), f"{gi}:{vi}", f"{new_box}|{due}")


def due_count(state: dict[tuple[int, int], tuple[int, str]], today: date) -> int:
    """Скільки дієслів доспіло до повторення (чиста функція)."""
    return sum(1 for _box, due in state.values() if srs.is_due(due, today))


def pick_srs(
    coords: list[tuple[int, int]],
    state: dict[tuple[int, int], tuple[int, str]],
    today: date,
    k: int = DRILL_SIZE,
    rng: random.Random | None = None,
) -> list[tuple[int, int, int]]:
    """Сесія за SRS-пріоритетом: доспілі → нові (не бачені) → найближчі майбутні.

    Дієслова не повторюються; особа (0-5) — випадкова. Чиста функція (rng у тестах).
    """
    rng = rng or random.Random()
    due = [c for c in coords if c in state and srs.is_due(state[c][1], today)]
    new = [c for c in coords if c not in state]
    ahead = sorted(
        (c for c in coords if c in state and not srs.is_due(state[c][1], today)),
        key=lambda c: state[c][1],  # найближчі за датою — першими
    )
    rng.shuffle(due)
    rng.shuffle(new)
    chosen = (due + new + ahead)[:k]
    return [(gi, vi, rng.randrange(6)) for gi, vi in chosen]


def with_tenses(
    queue: list[tuple[int, int, int]], rng: random.Random | None = None
) -> list[tuple[int, int, int, int]]:
    """Додати час до питань: (gi, vi, person, tense). 0=теперішній, 1=минулий, 2=майбутній.

    Минулий — лише де past_paradigm парситься (слоти ja-ч/ja-ж/on/ona/oni/one);
    майбутній складений регулярний для всіх. Чиста функція (rng інʼєктиться в тестах).
    """
    rng = rng or random.Random()
    out: list[tuple[int, int, int, int]] = []
    for gi, vi, person in queue:
        v = verbs.verb_at(gi, vi)
        can_past = v is not None and verbs.past_paradigm(v.past) is not None
        roll = rng.random()
        if can_past and roll < PAST_RATIO:
            tense = 1
        elif roll < PAST_RATIO + FUTURE_RATIO:
            tense = 2
        else:
            tense = 0
        out.append((gi, vi, person, tense))
    return out


async def build_drill(uid: int) -> list[tuple[int, int, int, int]]:
    coords = [(gi, vi) for gi, vi, _ in verbs.all_verbs()]
    state = await srs_state(uid)
    return with_tenses(pick_srs(coords, state, clock.today_local()))


async def due_counts(uid: int) -> tuple[int, int]:
    """(доспіло у формах, доспіло в rekcji) — для хаба «на повторення сьогодні»."""
    today = clock.today_local()
    forms = due_count(await srs_state(uid, "forms"), today)
    rekcja = due_count(await srs_state(uid, "rekcja"), today)
    return forms, rekcja


# ── тренажер rekcji («який відмінок після X?») ────────────────────────────────
def rekcja_pool() -> list[str]:
    """Усі різні канонічні відповіді rekcja_q — пул для дистракторів."""
    return sorted({v.rekcja_q for _, _, v in verbs.all_verbs() if v.rekcja_q})


def rekcja_options(correct: str, pool: list[str], rng: random.Random | None = None) -> list[str]:
    """4 варіанти: правильна + 3 дистрактори з пулу (перемішано). Чиста функція."""
    rng = rng or random.Random()
    distractors = [p for p in pool if p != correct]
    rng.shuffle(distractors)
    opts = [correct, *distractors[:3]]
    rng.shuffle(opts)
    return opts


async def build_rekcja_drill(uid: int) -> list[tuple[int, int, int]]:
    """Сесія rekcja-тренажера: лише дієслова з rekcja_q; той самий SRS-підбір.

    person у тріаді не використовується (лишаємо як є) — формат сумісний із формами.
    """
    coords = [(gi, vi) for gi, vi, v in verbs.all_verbs() if v.rekcja_q]
    state = await srs_state(uid, "rekcja")
    return pick_srs(coords, state, clock.today_local())
