from app.services import vocab


def test_quiz_items_structure():
    due = [("kot", "кіт"), ("pies", "пес")]
    pool = [("kot", "кіт"), ("pies", "пес"), ("dom", "дім"), ("woda", "вода"), ("czas", "час")]
    items = vocab.quiz_items(due, pool)
    assert len(items) == 2
    for it, (pl, uk) in zip(items, due, strict=True):
        assert it["key"] == pl
        assert it["opts"][it["correct"]] == uk  # правильний індекс вказує на правильний переклад
        assert 2 <= len(it["opts"]) <= 4
        assert uk in it["opts"]


def test_quiz_items_skips_when_no_distractors():
    # лише 1 слово в пулі → немає дистракторів → 1 варіант → пропускаємо
    assert vocab.quiz_items([("kot", "кіт")], [("kot", "кіт")]) == []


def test_quiz_items_dedupes_distractors():
    due = [("kot", "кіт")]
    pool = [("kot", "кіт"), ("a", "дім"), ("b", "дім"), ("c", "вода")]  # «дім» двічі
    it = vocab.quiz_items(due, pool)[0]
    assert len(it["opts"]) == len(set(it["opts"]))  # без дублів
