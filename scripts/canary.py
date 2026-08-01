"""Prod-canary: щоденний прохід happy-path бота на СИНТЕТИЧНОМУ користувачі.

Мета — ловити поломки ПЕРШИМИ, до того як їх побачить реальний ранковий учень.
Проходить сервісним шаром (НЕ через хендлери/Dispatcher — щоб не смітити
EventMiddleware-лічильниками) реальні PG+Redis та по одному дешевому пінгу
Anthropic/Azure. Після кожного прогону ПОВНІСТЮ прибирає за собою (gdpr.delete_data
+ явний доунок ключів дієслів). На будь-якому фейлі шле алерт у 🔧-канал і виходить з
кодом 1.

Запуск на homeserver (health :8080 без проброса портів, тож лише в контейнері):
    docker compose exec -T bot python - < scripts/canary.py
"""

from __future__ import annotations

import asyncio
import random
import sys
import traceback

# Синтетичний uid: НЕГАТИВНИЙ — реальний Telegram USER-id завжди додатний, тож колізія з
# живим користувачем неможлива, а admin-short-circuit (admin_id додатний) не спрацює.
# NB: відʼємні id — це namespace груп/каналів як CHAT-id, тож нудж-луп бота міг би теоретично
# слати на нього; захищено гейтом `uid <= 0` у scheduler._nudge_due.
CANARY_UID = -999_000_001
CANARY_UID2 = -999_000_002  # для перевірки шляху «оплата від новоствореного юзера»
CHARGE_A = f"canary-A-{CANARY_UID}"
CHARGE_B = f"canary-B-{CANARY_UID}"


class CheckError(AssertionError):
    """Провал канарки — з людським поясненням."""


async def _check_access() -> str:
    """grant_trial (шлях бага «marina») → гейт відкрито, не протерміновано."""
    from app.services import access, clock

    until = await access.grant_trial(CANARY_UID, "canary", referred_by=0, days=14)
    if not until:
        raise CheckError("grant_trial повернув порожній until")
    if not await access.is_allowed(CANARY_UID, admin_id=0):
        raise CheckError("is_allowed=False одразу після grant_trial")
    inf = await access.info(CANARY_UID)
    if inf.status != "approved":
        raise CheckError(f"status={inf.status!r}, очікували 'approved'")
    if access.is_expired(inf, clock.today_local()):
        raise CheckError("свіжий trial позначено як протермінований")
    return f"trial до {until}"


async def _check_payment() -> str:
    """apply_subscription: продовжує доступ, ідемпотентний за charge_id."""
    from app.services import billing

    stars, days = billing.plan_base("m")
    first = await billing.apply_subscription(CANARY_UID, days=days, stars=stars, charge_id=CHARGE_A)
    if not first:
        raise CheckError("apply_subscription повернув порожньо")
    if not await billing.has_payments(CANARY_UID):
        raise CheckError("has_payments=False після оплати")
    # ідемпотентність: той самий charge_id НЕ подовжує вдруге
    again = await billing.apply_subscription(CANARY_UID, days=days, stars=stars, charge_id=CHARGE_A)
    if again != first:
        raise CheckError(f"неідемпотентно: повтор charge_id змінив until {first}→{again}")
    # інший charge_id — має продовжити далі
    second = await billing.apply_subscription(CANARY_UID, days=days, stars=stars, charge_id=CHARGE_B)
    if second <= first:
        raise CheckError(f"новий платіж не продовжив доступ ({first}→{second})")
    # шлях «оплата від НОВОСТВОРЕНОГО юзера» (гілка u is None: flush перед FK-insert + or 0) —
    # окремий uid без попереднього рядка, інакше цю гілку канарка не покриває
    fresh = await billing.apply_subscription(CANARY_UID2, days=days, stars=stars, charge_id="canary-fresh")
    if not fresh:
        raise CheckError("оплата від нового юзера повернула порожньо (FK/flush-регрес?)")
    from app.services import access

    if not await access.is_allowed(CANARY_UID2, admin_id=0):
        raise CheckError("новий платник не отримав доступу")
    return f"оплата ок, доступ до {second}"


async def _check_placement() -> str:
    """build_test + score наскрізь. НЕ round-trip .correct (то тавтологія 100%), а:
    (1) інваріанти контенту — кожне питання має ≥2 варіанти й correct у межах;
    (2) score реально розрізняє: усі-правильні→100, усі-НЕправильні→низько."""
    from app.services import mock, placement

    random.seed(20260801)  # стабільний прогін
    pairs = placement.build_test()
    if not pairs:
        raise CheckError("build_test повернув порожньо")
    for sec, i in pairs:
        it = mock.section_items(sec)[i]
        if len(it.options) < 2:
            raise CheckError(f"питання {sec}[{i}] має <2 варіантів")
        if not (0 <= it.correct < len(it.options)):
            raise CheckError(f"correct={it.correct} поза межами options({len(it.options)}) у {sec}[{i}]")
    right = placement.score(pairs, [mock.section_items(sec)[i].correct for sec, i in pairs])
    if right.overall_pct != 100 or not right.level:
        raise CheckError(f"усі-правильні мали дати 100%/level, дали {right.overall_pct}%/{right.level!r}")
    if "gramatyka" not in right.per_module:
        raise CheckError(f"per_module без 'gramatyka': {list(right.per_module)}")
    # усі-неправильні: обрати варіант, що НЕ дорівнює correct → score має бути низьким
    wrong_pick = [(1 if mock.section_items(sec)[i].correct == 0 else 0) for sec, i in pairs]
    wrong = placement.score(pairs, wrong_pick)
    if wrong.overall_pct >= right.overall_pct:
        raise CheckError(f"score не розрізняє: неправильні={wrong.overall_pct}% ≥ правильні={right.overall_pct}%")
    return f"placement 100%→{right.level}, all-wrong→{wrong.overall_pct}%"


async def _check_exercise() -> str:
    """Крок воронки «вправа»: update_readiness пише Session + перераховує готовність."""
    from sqlalchemy import func, select

    from app.db.base import session_factory
    from app.db.models import Session as ExSession
    from app.services import state as user_state

    async def _sessions() -> int:
        async with session_factory()() as s:
            return (
                await s.execute(
                    select(func.count()).select_from(ExSession).where(ExSession.user_id == CANARY_UID)
                )
            ).scalar() or 0

    before = await _sessions()
    await user_state.update_readiness(CANARY_UID, "gramatyka", 80)
    after = await _sessions()
    if after <= before:  # строго зросла (не «≥1 зі старого сміття»); ловить teacher/viewas early-return
        raise CheckError(f"update_readiness не додав Session ({before}→{after})")
    st = await user_state.load(CANARY_UID)
    if "gramatyka" not in (st.readiness or {}):
        raise CheckError(f"readiness не перерахувалась: {st.readiness}")
    return f"вправа зафіксована (Session {before}→{after})"


async def _check_verbs_srs() -> str:
    """Один раунд тренажера дієслів: правильна відповідь підіймає SRS-коробку."""
    from app import verbs
    from app.services import verbs as vdrill

    catalog = verbs.all_verbs()
    if not catalog:
        raise CheckError("порожній каталог дієслів")
    gi, vi, _v = catalog[0]

    async def _box() -> int:
        return (await vdrill.srs_state(CANARY_UID, "forms")).get((gi, vi), (0, ""))[0]

    box0 = await _box()
    await vdrill.record_answer(CANARY_UID, gi, vi, ok=True, kind="forms")
    box1 = await _box()
    await vdrill.record_answer(CANARY_UID, gi, vi, ok=True, kind="forms")
    box2 = await _box()
    # прогресія має бути НАСКРІЗНОЮ (0→1→2), а не лише «є рух» — інакше баг on_correct
    # (напр. cap на 1 → SRS фактично вимкнено) лишився б зеленим
    if not (box0 < box1 < box2):
        raise CheckError(f"SRS-прогресія зламана: {box0}→{box1}→{box2} (очікували строго зростання)")
    return f"SRS-коробка {box0}→{box1}→{box2}"


async def _check_ai_ping() -> str:
    """Пінг Anthropic: cheap-tier (Haiku), strong-tier (Sonnet — письмо/уроки) і
    structured output (ask_json) — щоб зловити зникнення моделі/квоти/json-режиму."""
    from app.integrations import ai

    if not ai.enabled():
        raise CheckError("ai.enabled()=False — відсутній/битий ANTHROPIC_API_KEY")
    cheap = await ai.ask("Reply with exactly: OK", "ping", strong=False, max_tokens=5, label="canary")
    if not cheap.strip():
        raise CheckError("порожня відповідь cheap-tier (Haiku): ключ/квота/мережа?")
    strong = await ai.ask("Reply with exactly: OK", "ping", strong=True, max_tokens=5, label="canary")
    if not strong.strip():
        raise CheckError("порожня відповідь strong-tier (Sonnet): модель/квота — письмо/уроки ляжуть")
    # additionalProperties:false — вимога API structured-output (як у реальних схемах застосунку)
    schema = {
        "type": "object", "additionalProperties": False,
        "properties": {"ok": {"type": "boolean"}}, "required": ["ok"],
    }
    js = await ai.ask_json("Return {\"ok\": true}", "ping", schema, strong=False, max_tokens=30, label="canary")
    if not isinstance(js, dict) or "ok" not in js:
        raise CheckError(f"structured output (ask_json) зламано: {js!r}")
    return "AI ok (Haiku+Sonnet+json)"


async def _check_tts_azure() -> str:
    """Azure Neural TTS напряму (НЕ через tts.synthesize — той маскує збій піпером)."""
    from app.integrations import cloud_tts

    if not cloud_tts.available():
        raise CheckError("cloud_tts.available()=False — відсутній AZURE_TTS_KEY/REGION")
    data = await cloud_tts.synthesize("dzień dobry", slow=True)  # реальне польське слово, прод-шлях
    if not data:
        raise CheckError("Azure TTS повернув None (квота/ключ/мережа?)")
    if len(data) < 1000:  # порожній/деградований payload під 200-OK
        raise CheckError(f"підозріло малий TTS-payload: {len(data)} байт")
    if not data.startswith(b"OggS"):  # валідний Ogg-контейнер, а не HTML-помилка/сміття
        raise CheckError(f"TTS-payload не Ogg (перші байти {data[:4]!r})")
    return f"Azure TTS ok ({len(data)} байт Ogg)"


async def _check_health() -> str:
    """Внутрішній health застосунку (db+redis)."""
    from app import health

    ok, parts = await health.check()
    if not ok:
        raise CheckError(f"health не ok: {parts}")
    return f"health {parts}"


CHECKS = [
    ("access", _check_access),
    ("payment", _check_payment),
    ("placement", _check_placement),
    ("exercise", _check_exercise),
    ("verbs_srs", _check_verbs_srs),
    ("ai_ping", _check_ai_ping),
    ("tts_azure", _check_tts_azure),
    ("health", _check_health),
]


async def _cleanup() -> None:
    """Прибрати ВСІ сліди синтетичних користувачів (PG+Redis). Ідемпотентно.

    Заразом стереже РЕГРЕС самого gdpr: перевіряє, що gdpr прибрав ключі дієслів ДО
    belt-and-suspenders-доунка (інакше fallback замаскував би поломку _delete_redis)."""
    from redis.asyncio import Redis

    from app.config import settings
    from app.services import gdpr

    await gdpr.delete_data(CANARY_UID)
    await gdpr.delete_data(CANARY_UID2)

    r = Redis.from_url(settings.redis_url, decode_responses=True)
    try:
        gdpr_left_verbs = await r.exists(f"verbs:srs:forms:{CANARY_UID}")  # canary писав forms
        # belt-and-suspenders доунок ключів дієслів + aicost-мітка 'canary' (keyed by LABEL,
        # не uid → gdpr її не бачить; без цього — вічний фантомний рядок у /aicost)
        await r.delete(
            f"verbs:srs:forms:{CANARY_UID}", f"verbs:srs:rekcja:{CANARY_UID}",
            f"verbs:wrong:forms:{CANARY_UID}", f"verbs:wrong:rekcja:{CANARY_UID}",
        )
        for h in ("aicost:calls", "aicost:in", "aicost:out", "aicost:cread", "aicost:micro"):
            await r.hdel(h, "canary")
        if gdpr_left_verbs:
            raise CheckError("gdpr._delete_redis НЕ прибрав verbs:srs:forms (регрес фіксу)")
    finally:
        await r.aclose()


async def _verify_clean() -> None:
    """Прибирання спрацювало ПОВНІСТЮ: нема рядка, Session/Payment, жодного Redis-ключа з uid."""
    from redis.asyncio import Redis
    from sqlalchemy import func, select

    from app.config import settings
    from app.db.base import session_factory
    from app.db.models import Payment
    from app.db.models import Session as ExSession
    from app.services import access

    for uid in (CANARY_UID, CANARY_UID2):
        inf = await access.info(uid)
        if inf.status != "new":
            raise CheckError(f"cleanup неповний: uid={uid} status={inf.status!r} (очікували 'new')")
        async with session_factory()() as s:
            sess = (
                await s.execute(select(func.count()).select_from(ExSession).where(ExSession.user_id == uid))
            ).scalar() or 0
            pay = (
                await s.execute(select(func.count()).select_from(Payment).where(Payment.user_id == uid))
            ).scalar() or 0
        if sess or pay:
            raise CheckError(f"cleanup лишив рядки uid={uid}: Session={sess} Payment={pay}")

    r = Redis.from_url(settings.redis_url, decode_responses=True)
    try:  # ловить БУДЬ-ЯКИЙ новий клас ключів, що gdpr ще не чистить
        for uid in (CANARY_UID, CANARY_UID2):
            leftover = [k async for k in r.scan_iter(f"*{uid}*")]
            if leftover:
                raise CheckError(f"Redis-залишки для uid={uid}: {leftover[:8]}")
    finally:
        await r.aclose()


async def run() -> int:
    results: list[tuple[str, bool, str]] = []
    try:
        for name, fn in CHECKS:
            try:
                detail = await fn()
                results.append((name, True, detail))
            except Exception as exc:  # noqa: BLE001 — канарка не має падати цілком через 1 чек
                results.append((name, False, f"{type(exc).__name__}: {exc}"))
    finally:
        try:
            await _cleanup()
            await _verify_clean()
            results.append(("cleanup", True, "прибрано"))
        except Exception as exc:  # noqa: BLE001
            results.append(("cleanup", False, f"{type(exc).__name__}: {exc}"))

    failed = [(n, d) for n, ok, d in results if not ok]
    print("═══ CANARY ═══")
    for name, ok, detail in results:
        print(f"  {'✅' if ok else '❌'} {name}: {detail}")

    if failed:
        lines = "\n".join(f"• <b>{n}</b>: {d}" for n, d in failed)
        with _suppress():
            from app.services import alerts

            await alerts.send(f"🐤 <b>CANARY FAILED</b> ({len(failed)})\n{lines}")
        print(f"\nРЕЗУЛЬТАТ: FAIL ({len(failed)}/{len(results)})")
        return 1
    print(f"\nРЕЗУЛЬТАТ: OK ({len(results)} чеків)")
    return 0


class _suppress:
    """Дрібний контекст: алерт не має ронити канарку (мережа/токен)."""

    def __enter__(self) -> None:
        return None

    def __exit__(self, *exc: object) -> bool:
        if exc and exc[0] is not None:
            traceback.print_exc()
        return True


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
