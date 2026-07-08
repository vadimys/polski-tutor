from app.domain.models import MODULE_LABELS, Module
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


class _St:
    def __init__(self, readiness):
        self.readiness = readiness


class _Inf:
    def __init__(self, confirmed=False, exam_date=None):
        self.confirmed = confirmed
        self.exam_date = exam_date


def test_scene_gaps_is_not_silent():
    """Регрес: коли всі модулі виміряні, але деякі <70% — сцена ПОКАЗУЄТЬСЯ (не None)."""
    from app.handlers.menu import _readiness_scene

    r = _full(80)
    r[Module.PISANIE.value] = 40
    text, markup = _readiness_scene(_St(r), _Inf())
    assert text is not None and markup is not None
    assert MODULE_LABELS[Module.PISANIE] in text


def test_scene_incomplete_has_menu_button():
    from app.handlers.menu import _readiness_scene

    text, markup = _readiness_scene(_St({Module.CZYTANIE.value: 90}), _Inf())
    assert text is not None and markup is not None


def test_scene_ready_with_date_has_menu_button():
    from app.handlers.menu import _readiness_scene

    text, markup = _readiness_scene(_St(_full(80)), _Inf(confirmed=True, exam_date="2026-12-05"))
    assert text is not None and markup is not None  # раніше було None → глухий кут
