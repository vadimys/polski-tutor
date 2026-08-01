"""Движок «Розмова з екзаменатором»: сценарії, персона, парсинг реплік, оцінка, квота."""

from __future__ import annotations

import pytest

from app.services import examiner, sim_quota


# ─────────────────────────── дані сценаріїв ───────────────────────────
def test_scenarios_wellformed():
    assert len(examiner.SCENARIOS) >= 5
    for sc in examiner.SCENARIOS:
        assert sc.register in ("oficjalny", "nieoficjalny")
        assert sc.setup_pl and sc.setup_uk and sc.examiner_role and sc.goal_uk
        assert sc.obstacle_pl and sc.opening_pl  # перешкода + стартова репліка обовʼязкові


def test_scenario_by_id():
    assert examiner.scenario_by_id("hotel").register == "oficjalny"
    assert examiner.scenario_by_id("meble").register == "nieoficjalny"
    assert examiner.scenario_by_id("nope") is None


# ─────────────────────────── персона ───────────────────────────
def test_persona_carries_role_and_register():
    sc = examiner.scenario_by_id("hotel")
    p = examiner._persona(sc, "exam")
    assert sc.examiner_role in p and "oficjalny" in p and "NIE poprawiaj" in p
    assert "TRYB ĆWICZENIA" not in p  # режим Іспит — без підказок


def test_persona_practice_adds_hint_policy():
    sc = examiner.scenario_by_id("meble")
    assert "TRYB ĆWICZENIA" in examiner._persona(sc, "practice")


# ─────────────────────────── парсинг/стеля ───────────────────────────
def test_parse_reply_marker():
    assert examiner._parse_reply("Dobrze, dziękuję. [KONIEC]") == ("Dobrze, dziękuję.", True)
    assert examiner._parse_reply("A ile osób?") == ("A ile osób?", False)


def test_is_capped_counts_learner_turns():
    hist = [("egzaminator", "a"), ("uczen", "b")] * (examiner.MAX_TURNS - 1)
    assert not examiner.is_capped(hist)
    hist += [("uczen", "x")]  # рівно MAX_TURNS реплік учня
    assert examiner.is_capped(hist)


def test_history_text_labels():
    t = examiner._history_text([("egzaminator", "Dzień dobry"), ("uczen", "Dzień dobry")])
    assert "Egzaminator: Dzień dobry" in t and "Uczeń: Dzień dobry" in t
    assert examiner._history_text([]) == "(rozmowa się jeszcze nie zaczęła)"


# ─────────────────────────── діалог (mock ai) ───────────────────────────
async def test_next_reply_parses_and_ends(monkeypatch):
    sc = examiner.scenario_by_id("hotel")

    async def _ask(system, user, **k):
        return "Niestety pokoje są na różnych piętrach. [KONIEC]"

    monkeypatch.setattr(examiner.ai, "ask", _ask)
    text, done = await examiner.next_reply(sc, "exam", [("egzaminator", "Dzień dobry")])
    assert text == "Niestety pokoje są na różnych piętrach." and done is True


async def test_next_reply_forces_done_on_cap(monkeypatch):
    sc = examiner.scenario_by_id("hotel")

    async def _ask(system, user, **k):
        return "Proszę bardzo."  # без маркера

    monkeypatch.setattr(examiner.ai, "ask", _ask)
    capped = [("uczen", "x")] * examiner.MAX_TURNS
    _text, done = await examiner.next_reply(sc, "exam", capped)
    assert done is True  # стеля реплік → закриваємо навіть без [KONIEC]


async def test_next_reply_empty_ai_ends(monkeypatch):
    sc = examiner.scenario_by_id("hotel")
    monkeypatch.setattr(examiner.ai, "ask", lambda *a, **k: _co(""))
    text, done = await examiner.next_reply(sc, "exam", [])
    assert text == "" and done is True


async def _co(v):
    return v


# ─────────────────────────── оцінка (mock ai) ───────────────────────────
async def test_grade_builds_verdict(monkeypatch):
    sc = examiner.scenario_by_id("hotel")

    async def _ask_json(system, user, schema, **k):
        return {"wykonanie": 5, "gramatyka": 6, "slownictwo": 7, "cel_osiagniety": True,
                "rejestr_ok": True, "feedback": "Добре впорався."}

    monkeypatch.setattr(examiner.ai, "ask_json", _ask_json)
    v = await examiner.grade(sc, [("uczen", "Chciałbym zarezerwować pokój.")])
    assert v.total == 18 and v.max_total == 22 and v.pct == 82 and v.cel_osiagniety


async def test_grade_clamps_out_of_range(monkeypatch):
    sc = examiner.scenario_by_id("hotel")

    async def _ask_json(system, user, schema, **k):
        return {"wykonanie": 99, "gramatyka": -3, "slownictwo": 8, "cel_osiagniety": False,
                "rejestr_ok": False, "feedback": "x"}

    monkeypatch.setattr(examiner.ai, "ask_json", _ask_json)
    v = await examiner.grade(sc, [("uczen", "a")])
    assert v.wykonanie == 6 and v.gramatyka == 0  # клемп у межі рубрики


async def test_grade_none_on_ai_fail(monkeypatch):
    sc = examiner.scenario_by_id("hotel")

    async def _ask_json(system, user, schema, **k):
        return None

    monkeypatch.setattr(examiner.ai, "ask_json", _ask_json)
    assert await examiner.grade(sc, [("uczen", "a")]) is None


# ─────────────────────────── квота ───────────────────────────
@pytest.fixture
def _sub(monkeypatch):
    paid = {"v": True}

    async def _has(uid):
        return paid["v"]

    import app.services.billing as billing

    monkeypatch.setattr(billing, "has_payments", _has)
    return paid


async def test_quota_subscriber_three_per_week(fake_redis, _sub, monkeypatch):
    monkeypatch.setattr(sim_quota, "_redis", None, raising=False)
    assert await sim_quota.remaining(-9001) == 3
    for _ in range(3):
        await sim_quota.consume(-9001)
    assert await sim_quota.remaining(-9001) == 0


async def test_quota_trial_one_per_week(fake_redis, _sub, monkeypatch):
    monkeypatch.setattr(sim_quota, "_redis", None, raising=False)
    _sub["v"] = False  # trial
    assert await sim_quota.remaining(-9002) == 1
    await sim_quota.consume(-9002)
    assert await sim_quota.remaining(-9002) == 0
