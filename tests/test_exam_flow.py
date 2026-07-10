"""Повний мок /egzamin: побудова послідовності всіх типів + оцінка закритих кроків."""

from app import content
from app.handlers import exam


def test_build_seq_includes_all_types_for_2020():
    from app.services import listening

    seq = exam._build_seq("2020")
    assert {s["t"] for s in seq} == {"listen", "mcq", "match", "fill", "open"}
    # кількість кроків = аудіо-питання + MCQ + усі під-пункти тасків
    n_listen = sum(
        len(seg.questions)
        for lid in content.exam_listening_ids("2020")
        for seg in listening.by_id(lid).segments
    )
    n_mcq = len(content.by_id("2020").items)
    n_match = sum(len(t.prompts) for t in content.exam_match_tasks("2020"))
    n_fill = sum(len(t.prompts) for t in content.exam_fill_tasks("2020"))
    n_open = sum(len(t.prompts) for t in content.exam_open_tasks("2020"))
    assert len(seq) == n_listen + n_mcq + n_match + n_fill + n_open


def test_2019_seq_mcq_only():
    seq = exam._build_seq("2019")
    assert {s["t"] for s in seq} == {"mcq"}


def test_all_exams_buildable_for_picker():
    # пікер /egzamin показує всі тести — кожен має будувати непорожній мок
    for e in content.all_exams():
        assert exam._build_seq(e.id), f"порожній seq для {e.id}"


def test_seq_sections_stable_order():
    # аудіювання першим (модуль 1 реального іспиту), тоді читання, граматика
    assert exam._seq_sections(exam._build_seq("2020")) == ["sluchanie", "czytanie", "gramatyka"]


def test_grade_closed_listen():
    from app.services import listening

    seq = exam._build_seq("2020")
    step = next(s for s in seq if s["t"] == "listen")
    q = listening.by_id(step["ex"]).segments[step["si"]].questions[step["qi"]]
    assert exam._grade_closed("2020", step, q.correct)
    assert not exam._grade_closed("2020", step, (q.correct + 1) % len(q.options))


def test_grade_closed_mcq():
    seq = exam._build_seq("2020")
    step = next(s for s in seq if s["t"] == "mcq")
    it = content.exam_items("2020", step["sec"])[step["i"]]
    assert exam._grade_closed("2020", step, it.correct)
    assert not exam._grade_closed("2020", step, (it.correct + 1) % len(it.options))


def test_grade_closed_match():
    seq = exam._build_seq("2020")
    step = next(s for s in seq if s["t"] == "match")
    mt = content.exam_match_tasks("2020")[step["ti"]]
    assert exam._grade_closed("2020", step, mt.key[step["gi"]])
    wrong = (mt.key[step["gi"]] + 1) % len(mt.options)
    assert not exam._grade_closed("2020", step, wrong)


def test_grade_closed_fill():
    seq = exam._build_seq("2020")
    step = next(s for s in seq if s["t"] == "fill")
    ft = content.exam_fill_tasks("2020")[step["ti"]]
    assert exam._grade_closed("2020", step, ft.accepted[step["gi"]][0])
    assert not exam._grade_closed("2020", step, "zzz-нонсенс")
    assert not exam._grade_closed("2020", step, "")  # пропуск


def test_grade_closed_open_is_not_closed():
    # open не оцінюється синхронно (лише через AI-батч) → _grade_closed завжди False
    step = {"t": "open", "sec": "gramatyka", "ti": 0, "gi": 0}
    assert exam._grade_closed("2020", step, "будь-що") is False
