"""Реєстр офіційного контенту: агрегат/за-тестом, latest, валідність ключів."""

from app import content


def test_registry_nonempty_and_latest_is_complete():
    assert len(content.EXAMS) >= 2
    lt = content.latest()
    assert content.by_id(lt.id) is lt
    assert len({it.section for it in lt.items}) >= 2  # дефолт /egzamin — повний тест


def test_all_items_aggregates_across_exams():
    r = content.all_items("czytanie")
    g = content.all_items("gramatyka")
    # 2019 + 2020 + 2024-02/04 (повні) + 2024-06 (читання) → пул росте
    assert len(r) >= 94 and len(g) >= 128
    assert len(content.all_items_flat()) == len(r) + len(g)


def test_exam_items_and_sections():
    eid = content.latest().id
    secs = content.exam_sections(eid)
    assert "czytanie" in secs and "gramatyka" in secs
    assert content.exam_items(eid, "czytanie")  # непорожньо


def test_keys_valid_everywhere():
    for it in content.all_items_flat():
        assert it.section in ("sluchanie", "czytanie", "gramatyka")
        assert 0 <= it.correct < len(it.options)
        assert len(it.options) >= 2 and it.question and it.explain


def test_deterministic_order():
    # стабільний порядок → індекси лишаються валідними між викликами
    assert content.all_items("gramatyka") == content.all_items("gramatyka")


def test_match_tasks_wellformed():
    tasks = content.all_match_tasks()
    assert tasks, "має бути хоча б одне завдання-зіставлення"
    for t in tasks:
        # довжини узгоджені
        assert len(t.prompts) == len(t.key) == len(t.explain)
        # кожен ключ вказує в межах пулу опцій
        for k in t.key:
            assert 0 <= k < len(t.options)
        # немає повторів у ключі (кожен фрагмент — рівно один пропуск)
        assert len(set(t.key)) == len(t.key)
        # усі опції реально використані (без «зайвих» у цих завданнях 2020)
        assert set(t.key) == set(range(len(t.options)))
        assert t.section in ("czytanie", "gramatyka")
        assert t.title and t.intro


def test_match_section_filter():
    czyt = content.all_match_tasks("czytanie")
    assert len(czyt) == len(content.all_match_tasks())  # усі поточні — читання
    assert content.all_match_tasks("gramatyka") == []
    assert content.exam_match_tasks("2020")  # 2020 має зіставлення


def test_match_kb_callbacks_parse():
    """Літерні кнопки match_kb сумісні з quiz.read_answer (формат ma:ans:<q>:<opt>)."""
    from app.bot.keyboards import match_kb
    from app.bot.quiz import parse_answer

    kb = match_kb(7, qidx=2)
    letter_cbs = [
        btn.callback_data
        for row in kb.inline_keyboard
        for btn in row
        if btn.callback_data and btn.callback_data.startswith("ma:ans:")
    ]
    assert len(letter_cbs) == 7  # 7 фрагментів → 7 літер
    parsed = [parse_answer(c) for c in letter_cbs]
    assert parsed == [(2, i) for i in range(7)]  # (qidx, opt)
