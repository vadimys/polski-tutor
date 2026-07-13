"""Support-inbox: мітки категорій + рендер тікета (чисте)."""

from app.services import support


def test_cat_label():
    assert support.cat_label("problem") == "🛠 Проблема"
    assert support.cat_label("idea") == "💡 Ідея"
    assert support.cat_label("хз") == "хз"  # невідоме — як є


def test_render_ticket_new_and_closed():
    t = {"uid": 42, "name": "@ola", "cat": "idea", "text": "додайте темну тему", "status": "new",
         "at": "2026-07-13 10:00"}
    r = support.render_ticket(7, t)
    assert "Тікет #7" in r and "💡 Ідея" in r and "🟢 нове" in r
    assert "@ola" in r and "id <code>42</code>" in r and "темну тему" in r
    t["status"] = "closed"
    assert "☑️ закрито" in support.render_ticket(7, t)


def test_support_keyboard_callbacks():
    from app.bot.keyboards import support_category_kb

    cbs = [b.callback_data for row in support_category_kb().inline_keyboard for b in row]
    assert cbs == ["support:cat:problem", "support:cat:idea"]
