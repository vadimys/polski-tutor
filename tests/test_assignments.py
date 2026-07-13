"""Завдання: парсинг дедлайну + рендери (чисті функції)."""

from datetime import date

from app.services import assignments as a

TODAY = date(2026, 7, 13)


def test_parse_deadline_formats():
    assert a.parse_deadline("2026-11-20", TODAY) == "2026-11-20"
    assert a.parse_deadline("20.11.2026", TODAY) == "2026-11-20"
    assert a.parse_deadline("20.11", TODAY) == "2026-11-20"  # рік поточний
    # ДД.ММ у минулому цього року → наступний рік
    assert a.parse_deadline("01.01", TODAY) == "2027-01-01"


def test_parse_deadline_rejects_past_and_junk():
    assert a.parse_deadline("2020-01-01", TODAY) is None  # у минулому
    assert a.parse_deadline("завтра", TODAY) is None
    assert a.parse_deadline("", TODAY) is None
    assert a.parse_deadline("99.99", TODAY) is None


def test_deadline_label():
    assert "сьогодні" in a.deadline_label("2026-07-13", TODAY)
    assert "завтра" in a.deadline_label("2026-07-14", TODAY)
    assert "протерміновано на 2" in a.deadline_label("2026-07-11", TODAY)
    assert "ще 5 дн" in a.deadline_label("2026-07-18", TODAY)


def test_render_student():
    rows = [
        {"id": 1, "title": "Пройти аудіювання", "deadline": "2026-07-14", "done": False},
        {"id": 2, "title": "Есе 200 слів", "deadline": "2026-07-20", "done": True},
    ]
    t = a.render_student(rows, TODAY)
    assert "◻️ <b>Пройти аудіювання</b>" in t and "завтра" in t
    assert "✅ <b>Есе 200 слів</b>" in t
    assert "немає активних" in a.render_student([], TODAY)


def test_render_teacher():
    rows = [{"id": 1, "title": "Есе", "deadline": "2026-07-20", "done": 3, "total": 5}]
    t = a.render_teacher(rows, "Ранкова B1", TODAY)
    assert "Ранкова B1" in t and "виконали 3/5" in t
    assert "Створи перше" in a.render_teacher([], "Клас", TODAY)


def test_module_short():
    assert a.module_short("sluchanie").startswith("🎧")
    assert "Pisanie" in a.module_short("pisanie")
    assert a.module_short("") == ""
    assert a.module_short("bogus") == "bogus"


def test_render_student_auto_hint():
    rows = [{"id": 1, "title": "Аудіо", "deadline": "2026-07-20", "module": "sluchanie", "done": False}]
    t = a.render_student(rows, TODAY)
    assert "🤖 зарахується само" in t and "Słuchanie" in t
    # виконане — без підказки авто
    rows[0]["done"] = True
    assert "🤖" not in a.render_student(rows, TODAY)


def test_render_teacher_shows_module():
    rows = [{"id": 1, "title": "Аудіо", "deadline": "2026-07-20", "module": "sluchanie", "done": 1, "total": 3}]
    assert "🤖" in a.render_teacher(rows, "Клас", TODAY)
