from app.domain.models import Module
from app.services import progress


def _full(v: int) -> dict[str, int]:
    return {m.value: v for m in Module}


def test_verdict_ready_all_high():
    status, weak = progress.readiness_verdict(_full(80))
    assert status == "ready" and weak == []


def test_verdict_gaps_when_one_below_threshold():
    r = _full(80)
    r[Module.PISANIE.value] = 40
    status, weak = progress.readiness_verdict(r)
    assert status == "gaps" and Module.PISANIE in weak


def test_verdict_incomplete_when_modules_missing():
    status, missing = progress.readiness_verdict({Module.CZYTANIE.value: 90})
    assert status == "incomplete" and Module.PISANIE in missing


def test_verdict_boundary_70_is_ready():
    assert progress.readiness_verdict(_full(70))[0] == "ready"  # ≥70 = готовий
    assert progress.readiness_verdict(_full(69))[0] == "gaps"
