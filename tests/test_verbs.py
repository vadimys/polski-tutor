"""Розділ «Дієслова»: цілісність даних + пошук + адаптивний підбір тренажера."""

import random

from app import verbs
from app.services import verbs as vdrill


def test_registry_and_ids_unique():
    assert len(verbs.all_groups()) == 9
    infs = [v.inf for _, _, v in verbs.all_verbs()]
    assert len(infs) == len(set(infs)), "інфінітиви мають бути унікальні"
    assert len(infs) >= 90


def test_every_verb_is_complete():
    for _, _, v in verbs.all_verbs():
        assert v.inf and v.uk
        assert len(v.present) == 6, f"{v.inf}: має бути 6 форм теперішнього"
        assert all(v.present), f"{v.inf}: порожня форма"
        assert v.past, f"{v.inf}: немає минулого часу"
        assert v.examples, f"{v.inf}: немає прикладу"
        if v.pair:  # якщо є видова пара — мають бути її ключові форми
            assert v.pair_hint, f"{v.inf}: пара без pair_hint"


def test_present_forms_match_person_endings():
    """Санітарний чек парадигм: my → -my, wy → -cie (універсально для польської)."""
    for _, _, v in verbs.all_verbs():
        base = v.present
        my = base[3].split()[0]  # відкинути "się"
        wy = base[4].split()[0]
        assert my.endswith("my"), f"{v.inf}: форма my «{base[3]}» не на -my"
        assert wy.endswith("cie"), f"{v.inf}: форма wy «{base[4]}» не на -cie"


def test_lookup_and_search():
    gi, vi, v = next((g, i, x) for g, i, x in verbs.all_verbs() if x.inf == "robić")
    assert verbs.verb_at(gi, vi) is v
    assert verbs.verb_at(99, 0) is None
    hits = verbs.search("robi")
    assert any(x.inf == "robić" for _, _, x in hits)
    assert any(x.inf == "szukać" for _, _, x in verbs.search("шукати"))
    assert verbs.search("") == []


def test_pick_srs_due_first_then_new_then_ahead():
    from datetime import date

    today = date(2026, 7, 29)
    coords = [(0, i) for i in range(10)]
    state = {
        (0, 3): (2, "2026-07-28"),  # доспіло (вчора)
        (0, 7): (1, "2026-07-29"),  # доспіло (сьогодні)
        (0, 1): (4, "2026-08-20"),  # ще не доспіло
    }
    out = vdrill.pick_srs(coords, state, today, k=5, rng=random.Random(42))
    pairs = [(g, v) for g, v, _ in out]
    assert len(pairs) == len(set(pairs)) == 5  # без повторів
    assert set(pairs[:2]) == {(0, 3), (0, 7)}  # доспілі — першими
    assert (0, 1) not in pairs  # майбутнє не береться, поки є нові
    assert all(0 <= p <= 5 for _, _, p in out)  # особа в межах


def test_pick_srs_reviews_ahead_when_nothing_else():
    from datetime import date

    today = date(2026, 7, 29)
    coords = [(0, 0), (0, 1)]
    state = {(0, 0): (3, "2026-08-05"), (0, 1): (2, "2026-08-01")}
    out = vdrill.pick_srs(coords, state, today, k=5, rng=random.Random(1))
    pairs = [(g, v) for g, v, _ in out]
    assert pairs == [(0, 1), (0, 0)]  # усе не доспіло → найближчі за датою першими


def test_due_count_pure():
    from datetime import date

    today = date(2026, 7, 29)
    state = {(0, 0): (1, "2026-07-29"), (0, 1): (2, "2026-09-01"), (0, 2): (1, "")}
    assert vdrill.due_count(state, today) == 2  # сьогодні + порожнє due


def test_rekcja_pool_and_options():
    pool = vdrill.rekcja_pool()
    assert len(pool) >= 8  # достатньо моделей для дистракторів
    assert "Dopełniacz" in pool and "na + Biernik" in pool
    opts = vdrill.rekcja_options("Dopełniacz", pool, rng=random.Random(7))
    assert len(opts) == 4 and len(set(opts)) == 4
    assert "Dopełniacz" in opts


def test_rekcja_q_values_come_from_pool_and_marked_verbs_have_text():
    pool = set(vdrill.rekcja_pool())
    for _, _, v in verbs.all_verbs():
        if v.rekcja_q:
            assert v.rekcja_q in pool
            assert v.rekcja, f"{v.inf}: rekcja_q без пояснювального rekcja"


def test_past_paradigm_for_all_verbs():
    """Парадигма минулого має виводитися для КОЖНОГО дієслова й бути консистентною."""
    for _, _, v in verbs.all_verbs():
        p = verbs.past_paradigm(v.past)
        assert p is not None, f"{v.inf}: past не парситься: {v.past!r}"
        assert len(p) == 6 and all(p)
        strip = [f.removesuffix(" się") for f in p]
        assert strip[0].endswith("em"), f"{v.inf}: ja(ч) «{p[0]}»"
        assert strip[1].endswith("am"), f"{v.inf}: ja(ж) «{p[1]}»"
        assert strip[3].endswith("a"), f"{v.inf}: ona «{p[3]}»"
        assert strip[5].endswith("y"), f"{v.inf}: one «{p[5]}»"
        assert len(set(p)) == 6, f"{v.inf}: форми минулого не унікальні: {p}"


def test_past_paradigm_critical_forms():
    """Відомі підступні форми — точні значення (ó→o, суплетивний iść)."""
    cases = {
        "móc": ["mogłem", "mogłam", "mógł", "mogła", "mogli", "mogły"],
        "iść": ["szedłem", "szłam", "szedł", "szła", "szli", "szły"],
        "jeść": ["jadłem", "jadłam", "jadł", "jadła", "jedli", "jadły"],
        "być": ["byłem", "byłam", "był", "była", "byli", "były"],
        "mieć": ["miałem", "miałam", "miał", "miała", "mieli", "miały"],
    }
    by_inf = {v.inf: v for _, _, v in verbs.all_verbs()}
    for inf, want in cases.items():
        assert verbs.past_paradigm(by_inf[inf].past) == want


def test_with_tenses_mixes_and_respects_availability():
    queue = [(0, 0, 2), (0, 1, 4)] * 15
    out = vdrill.with_tenses(queue, rng=random.Random(5))
    assert len(out) == len(queue)
    tenses = {t for _, _, _, t in out}
    assert tenses == {0, 1, 2}  # при 30 питаннях присутні всі три часи
    assert all(len(q) == 4 for q in out)


def test_future_paradigm_regular_and_reflexive():
    assert verbs.future_paradigm("robić") == [
        "będę robić", "będziesz robić", "będzie robić",
        "będziemy robić", "będziecie robić", "będą robić",
    ]
    assert verbs.future_paradigm("myć się")[0] == "będę się myć"
    assert verbs.future_paradigm("uczyć się")[5] == "będą się uczyć"
    for _, _, v in verbs.all_verbs():  # 6 унікальних форм для кожного
        p = verbs.future_paradigm(v.inf)
        assert len(set(p)) == 6
