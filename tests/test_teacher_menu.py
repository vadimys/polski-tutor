"""Меню викладача: живе й функціональне саме для викладача (не мікс учнівського)."""

from app.bot.keyboards import menu_kb, teacher_materials_kb, teacher_menu_kb


def _cbs(markup):
    return {b.callback_data for row in markup.inline_keyboard for b in row if b.callback_data}


def test_teacher_menu_is_teacher_focused():
    cbs = _cbs(teacher_menu_kb())
    # має бути: клас, матеріали, запрошення, оплати, підтримка
    assert {"teacher:class", "teacher:materials", "teacher:invite", "teacher:revenue"} <= cbs
    # НЕ має учнівського: тест рівня, урок дня, персональний план, місії, авто-навчання, SRS
    for leak in ("placement:start", "lesson:start", "plan:show", "coach:now", "review:start", "lb:me", "asgn:me"):
        assert leak not in cbs, f"учнівська кнопка протекла в меню викладача: {leak}"


def test_teacher_materials_has_preview_and_catalog():
    cbs = _cbs(teacher_materials_kb())
    assert "teacher:catalog" in cbs and "exam:open" in cbs
    # доступ до всіх типів вправ як превʼю
    assert {"listening:start", "drill:start", "writing:start", "speaking:start", "mock:open"} <= cbs


def test_student_menu_unchanged_has_learner_items():
    cbs = _cbs(menu_kb())
    assert {"coach:now", "placement:start", "lesson:start", "asgn:me", "lb:me"} <= cbs
