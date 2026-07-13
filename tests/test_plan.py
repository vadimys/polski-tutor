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


def test_render_uses_daily_goal_not_hardcoded_60():
    p30 = plan.build("2026-12-05", True, {"czytanie": 100}, TODAY, daily_min=30)
    text = plan.render(p30)
    assert "~30 хв" in text and "твоя з /cel" in text
    # 60 → інша розкладка (більші числа), 30 → менші
    p60 = plan.build("2026-12-05", True, {"czytanie": 100}, TODAY, daily_min=60)
    assert "~60 хв" in plan.render(p60)


def test_milestones_future_and_active():
    # 20 тижнів до іспиту → усі віхи майбутні («за N тиж»)
    ms = plan.milestones(20, {})
    assert all("🔜" in m for m in ms)
    # 2 тижні лишилось, готовність низька → поріг «≥50%» позначено ⚠️
    ms2 = plan.milestones(2, {"sluchanie": 30, "czytanie": 30, "gramatyka": 30,
                              "pisanie": 30, "mowienie": 30})
    assert any("⚠️" in m and "≥50%" in m for m in ms2)
    # усі ≥50% → поріг досягнуто ✅
    ms3 = plan.milestones(2, {m: 60 for m in
                              ("sluchanie", "czytanie", "gramatyka", "pisanie", "mowienie")})
    assert any("✅" in x and "≥50%" in x for x in ms3)


def test_render_includes_milestones_when_dated():
    p = plan.build("2026-12-05", True, {"czytanie": 100}, TODAY)
    assert "Віхи до іспиту" in plan.render(p)
