"""Розумний підбір «Навчатись зараз» — пріоритети дій."""

from app.domain.models import Module
from app.services import coach

_ALL = [m.value for m in Module]


def _att(measured: bool) -> dict[str, int]:
    return {m: (10 if measured else 0) for m in _ALL}


def test_placement_first_if_not_done():
    a = coach.choose(False, {}, _att(False), 0)
    assert a.cb == "placement:start"


def test_unmeasured_module_prioritized():
    att = _att(True)
    att[Module.MOWIENIE.value] = 0  # не пробували мовлення
    a = coach.choose(True, {m: 60 for m in _ALL}, att, 0)
    assert a.cb == "speaking:start"


def test_reviews_when_due_and_all_measured():
    a = coach.choose(True, {m: 60 for m in _ALL}, _att(True), due_reviews=5)
    assert a.cb == "review:start"


def test_weakest_module_when_no_reviews():
    readiness = {m: 70 for m in _ALL}
    readiness[Module.PISANIE.value] = 20  # найслабше — письмо
    a = coach.choose(True, readiness, _att(True), due_reviews=0)
    assert a.cb == "writing:start"


def test_action_has_reason():
    a = coach.choose(True, {m: 50 for m in _ALL}, _att(True), 0)
    assert a.reason and a.label
