"""Інтеграційні тести тренажера дієслів на in-memory Redis (fakeredis fixture).

Перевіряють Redis-шлях SRS наскрізь — той самий, що canary проганяє у проді:
правильна відповідь підіймає коробку Leitner, помилка скидає в 1, стан читається
назад. Раніше SRS-логіка юніт-тестами покривалась лише як чисті функції — тут ще й
реальний запис/читання Redis-хеша.
"""

from __future__ import annotations

from datetime import timedelta

from app import verbs
from app.services import clock
from app.services import verbs as vdrill


async def test_correct_answer_advances_box(fake_redis):
    gi, vi, _v = verbs.all_verbs()[0]
    uid = -7001
    before = await vdrill.srs_state(uid, "forms")
    assert (gi, vi) not in before  # чистий старт
    await vdrill.record_answer(uid, gi, vi, ok=True, kind="forms")
    after = await vdrill.srs_state(uid, "forms")
    box, due = after[(gi, vi)]
    assert box == 1  # 0 → 1 (літерал, не round-trip srs.on_correct)
    assert due == (clock.today_local() + timedelta(days=1)).isoformat()  # box1 → +1 день


async def test_two_corrects_advance_progressively(fake_redis):
    """Наскрізна прогресія 0→1→2 (ловить cap-на-1 / off-by-one у on_correct)."""
    gi, vi, _v = verbs.all_verbs()[0]
    uid = -7005
    await vdrill.record_answer(uid, gi, vi, ok=True, kind="forms")
    assert (await vdrill.srs_state(uid, "forms"))[(gi, vi)][0] == 1
    await vdrill.record_answer(uid, gi, vi, ok=True, kind="forms")
    assert (await vdrill.srs_state(uid, "forms"))[(gi, vi)][0] == 2


async def test_wrong_answer_resets_to_box_one(fake_redis):
    gi, vi, _v = verbs.all_verbs()[0]
    uid = -7002
    # підняти до коробки 3
    for _ in range(3):
        await vdrill.record_answer(uid, gi, vi, ok=True, kind="forms")
    assert (await vdrill.srs_state(uid, "forms"))[(gi, vi)][0] == 3
    await vdrill.record_answer(uid, gi, vi, ok=False, kind="forms")
    assert (await vdrill.srs_state(uid, "forms"))[(gi, vi)][0] == 1  # помилка → коробка 1 (літерал)


async def test_forms_and_rekcja_states_are_separate(fake_redis):
    gi, vi, _v = verbs.all_verbs()[0]
    uid = -7003
    await vdrill.record_answer(uid, gi, vi, ok=True, kind="forms")
    assert (gi, vi) in await vdrill.srs_state(uid, "forms")
    assert (gi, vi) not in await vdrill.srs_state(uid, "rekcja")  # інший kind — інший ключ


async def test_legacy_wrong_counters_migrated(fake_redis):
    """Старі verbs:wrong:* мігрують у SRS-коробку 1 і видаляються при першому читанні."""
    gi, vi, _v = verbs.all_verbs()[0]
    uid = -7004
    await vdrill._r().hset(f"verbs:wrong:forms:{uid}", f"{gi}:{vi}", "2")
    state = await vdrill.srs_state(uid, "forms")  # тригерить _migrate_legacy
    assert state[(gi, vi)][0] == 1
    assert await vdrill._r().exists(f"verbs:wrong:forms:{uid}") == 0
