"""Чесна оцінка готовності: формула score + вердикт (incomplete/gaps/almost/ready)."""

from app.domain.models import MODULE_LABELS, Module
from app.services import progress
from app.services.progress import ModuleStat


def test_two_lucky_days_is_not_ready():
    """Ключова вимога: 2 вдалі вправи за 2 дні ≠ готовий (низька впевненість)."""
    assert progress.readiness_score(85, attempts=2, days=2, days_since=0) < 30


def test_sustained_practice_reaches_mastery():
    """Багато вправ за кілька днів із добрим балом → впевнено (≥70)."""
    assert progress.readiness_score(85, attempts=10, days=5, days_since=0) >= 70


def test_single_high_score_capped_low():
    assert progress.readiness_score(100, attempts=1, days=1, days_since=0) < 20


def test_freshness_decays_with_idle():
    full = progress.readiness_score(85, 10, 5, days_since=0)
    graced = progress.readiness_score(85, 10, 5, days_since=7)  # ще без спаду
    faded = progress.readiness_score(85, 10, 5, days_since=35)  # довгий простій
    assert graced == full
    assert faded < full // 2 + 5  # помітно впало


def _stats(pcts: dict[str, int], attempts: int = 10) -> dict[str, ModuleStat]:
    return {
        m.value: ModuleStat(pcts.get(m.value, 0), attempts if m.value in pcts else 0,
                            3, 0, pcts.get(m.value, 0) >= 70)
        for m in Module
    }


def _all(v: int) -> dict[str, int]:
    return {m.value: v for m in Module}


def test_verdict_incomplete_when_module_unmeasured():
    stats = _stats({Module.CZYTANIE.value: 80})  # решта — 0 спроб
    status, mods = progress.verdict(stats, is_mock_ok=True)
    assert status == "incomplete" and Module.PISANIE in mods


def test_verdict_gaps_when_below_mastery():
    stats = _stats({**_all(80), Module.PISANIE.value: 40})
    status, mods = progress.verdict(stats, is_mock_ok=True)
    assert status == "gaps" and Module.PISANIE in mods


def test_verdict_almost_when_no_mock():
    status, _ = progress.verdict(_stats(_all(80)), is_mock_ok=False)
    assert status == "almost"


def test_verdict_ready_only_with_mock():
    status, _ = progress.verdict(_stats(_all(80)), is_mock_ok=True)
    assert status == "ready"


def test_scene_almost_points_to_mock():
    from app.handlers.menu import _readiness_scene

    text, markup = _readiness_scene(inf=None, status="almost", mods=[])
    assert text is not None and "/mok" in text


def test_scene_gaps_lists_modules():
    from app.handlers.menu import _readiness_scene

    text, markup = _readiness_scene(inf=None, status="gaps", mods=[Module.PISANIE])
    assert text is not None and MODULE_LABELS[Module.PISANIE] in text
