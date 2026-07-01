from datetime import date

from app.domain.models import Module
from app.services import plan

TODAY = date(2026, 7, 1)


def test_weak_order_untested_first():
    # виміряні czytanie/gramatyka високі; продуктивні невиміряні → попереду
    order = plan.weak_order({"czytanie": 100, "gramatyka": 80})
    assert order[0] in (Module.PISANIE, Module.MOWIENIE, Module.SLUCHANIE)
    assert order[-1] == Module.CZYTANIE  # найсильніший — останній


def test_plan_with_date_has_phases_and_taper():
    p = plan.build("2026-12-05", True, {"czytanie": 100, "gramatyka": 75}, TODAY)
    assert p.has_date and p.days_left > 0 and p.weeks_left >= 1
    titles = " ".join(ph.title for ph in p.phases)
    assert "Тейпер" in titles  # довгий період → є тейпер
    assert any("Відпрацювання" in ph.title for ph in p.phases)


def test_plan_without_date_is_free():
    p = plan.build("", False, {"czytanie": 100}, TODAY)
    assert not p.has_date
    assert any("Реєстрація" in ph.title for ph in p.phases)


def test_render_mentions_priority_and_rule():
    p = plan.build("2026-12-05", True, {"czytanie": 100}, TODAY)
    text = plan.render(p)
    assert "≥50%" in text
    assert "план" in text.lower()


def test_short_sprint_no_crash():
    # іспит за 10 днів → короткий спринт, без падіння
    p = plan.build("2026-07-11", True, {}, TODAY)
    assert p.phases  # хоч одна фаза
