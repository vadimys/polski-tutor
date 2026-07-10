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
    # 2019 + 2020 + 2022×4 + 2023×4 + 2024×3 (повні) → пул росте
    assert len(r) >= 263 and len(g) >= 443
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


def test_mock_seq_includes_listening_first():
    """Повний мок /egzamin включає Słuchanie і ставить його першим (як реальний іспит)."""
    from app.handlers.exam import _build_seq

    seq = _build_seq(content.latest().id)
    assert any(s["t"] == "listen" for s in seq), "мок має містити аудіо-кроки"
    assert seq[0]["sec"] == "sluchanie", "аудіювання — перший модуль"
    # кожен listen-крок валідно резолвиться у питання
    from app.services import listening

    for s in seq:
        if s["t"] == "listen":
            ex = listening.by_id(s["ex"])
            assert ex and 0 <= s["qi"] < len(ex.segments[s["si"]].questions)


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
