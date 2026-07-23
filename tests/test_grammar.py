"""Розділ «Граматика»: цілісність контенту + навігація + прогрес (чисті функції)."""

from app import grammar
from app.services import grammar as gp


def test_registry_nonempty_and_ids_unique():
    assert len(grammar.all_modules()) >= 12  # повний базовий курс
    ids = grammar.all_lesson_ids()
    assert len(ids) == len(set(ids)), "id уроків мають бути унікальні"
    assert len(ids) >= 55


def test_every_lesson_has_cards_and_valid_quiz():
    for m in grammar.all_modules():
        assert m.id and m.icon and m.title
        for ls in m.lessons:
            assert ls.cards, f"урок {ls.id} без карток"
            for c in ls.cards:
                assert c.title and c.body
            for q in ls.quiz:  # ключ у межах опцій
                assert 0 <= q.correct < len(q.options), f"хибний ключ у quiz уроку {ls.id}"
                assert len(q.options) >= 2


def test_lookup_and_module_of():
    ls = grammar.lesson_by_id("alf_intro")
    assert ls is not None and ls.title
    assert grammar.module_of("alf_intro").id == "alfabet"
    assert grammar.module_by_id("alfabet") is not None
    assert grammar.lesson_by_id("nema") is None


def test_next_lesson_walks_path_and_ends():
    ids = grammar.all_lesson_ids()
    # кожен, крім останнього, має наступний; останній → None
    for cur, nxt in zip(ids, ids[1:], strict=False):
        assert grammar.next_lesson(cur).id == nxt
    assert grammar.next_lesson(ids[-1]) is None


def test_progress_pure_functions():
    ids = grammar.all_lesson_ids()
    assert gp.overall_pct(set()) == 0
    assert gp.overall_pct(set(ids)) == 100
    m = grammar.all_modules()[0]
    got, total = gp.module_progress({m.lessons[0].id}, m)
    assert got == 1 and total == len(m.lessons)
