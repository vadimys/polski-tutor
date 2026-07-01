from app.domain.models import Module
from app.services import mock, placement


def test_build_test_balanced_and_standalone():
    pairs = placement.build_test()
    sections = [s for s, _ in pairs]
    assert sections.count("gramatyka") == 8
    assert sections.count("czytanie") == 4
    # усі питання самодостатні (мають власний контекст)
    for section, idx in pairs:
        assert mock.section_items(section)[idx].context


def test_score_all_correct_only_measured():
    pairs = placement.build_test()
    chosen = [mock.section_items(s)[i].correct for s, i in pairs]
    r = placement.score(pairs, chosen)
    assert r.correct == r.total == len(pairs)
    assert r.overall_pct == 100
    assert set(r.per_module) <= {Module.GRAMATYKA.value, Module.CZYTANIE.value}
    assert Module.PISANIE.value not in r.per_module


def test_score_all_wrong():
    pairs = placement.build_test()
    chosen = []
    for s, i in pairs:
        it = mock.section_items(s)[i]
        chosen.append((it.correct + 1) % len(it.options))
    r = placement.score(pairs, chosen)
    assert r.overall_pct == 0
    assert r.level == "A1"
