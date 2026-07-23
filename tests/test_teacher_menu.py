"""Меню викладача: живе й функціональне саме для викладача (не мікс учнівського)."""

from app.bot.keyboards import (
    class_menu_kb,
    exam_menu_kb,
    menu_kb,
    practice_menu_kb,
    teacher_materials_kb,
    teacher_menu_kb,
)


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


def test_student_menu_top_level_is_grouped():
    """Головне меню — чисте: щоденне + відкривачі підменю (не «стіна» з 20 кнопок)."""
    cbs = _cbs(menu_kb())
    assert {"coach:now", "lesson:start", "grammar:home", "lex:open", "review:start"} <= cbs
    assert {"menu:practice", "menu:exam", "menu:class"} <= cbs  # підрозділи


def test_all_learner_actions_reachable_via_menu_or_submenus():
    """Ніщо не загублено при групуванні: union меню + підменю покриває всі дії."""
    reachable = (
        _cbs(menu_kb()) | _cbs(practice_menu_kb()) | _cbs(exam_menu_kb()) | _cbs(class_menu_kb())
    )
    expected = {
        "coach:now", "lesson:start", "grammar:home", "lex:open", "review:start",
        "writing:start", "speaking:start", "speaking:photo", "listening:start",
        "drill:start", "match:open", "amatch:open", "fill:open", "open:open",
        "mock:open", "exam:open", "mistakes:open", "placement:start", "plan:show",
        "lb:me", "asgn:me", "ref:invite", "support:open",
    }
    missing = expected - reachable
    assert not missing, f"дії зникли з меню після групування: {missing}"
