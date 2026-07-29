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


def test_pick_drill_prioritizes_wrongs_and_no_repeats():
    coords = [(0, i) for i in range(10)]
    rng = random.Random(42)
    out = vdrill.pick_drill(coords, wrongs=[(0, 3), (0, 7)], k=5, rng=rng)
    pairs = [(g, v) for g, v, _ in out]
    assert len(pairs) == len(set(pairs)) == 5  # без повторів
    assert (0, 3) in pairs or (0, 7) in pairs  # «болючі» пріоритезовано
    assert all(0 <= p <= 5 for _, _, p in out)  # особа в межах


def test_pick_drill_without_wrongs():
    coords = [(0, i) for i in range(3)]
    out = vdrill.pick_drill(coords, wrongs=[], k=5, rng=random.Random(1))
    assert len(out) == 3  # не більше, ніж є дієслів


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
