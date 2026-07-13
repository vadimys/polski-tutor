"""Адмін-консоль: чистий рендер огляду й картки користувача."""

from app.services import admin_stats


def test_role_emoji():
    assert admin_stats.role_emoji("teacher") == "👩‍🏫"
    assert admin_stats.role_emoji("student") == "🎓"


def test_render_overview():
    d = {
        "today": "2026-07-13", "total": 42, "active7": 10, "active30": 25, "new7": 5,
        "students": 38, "organic": 30, "referred": 8, "teachers": 4,
        "approved": 35, "pending": 2, "payers": 6, "revenue": 1800, "conv_pct": 16,
        "avg_readiness": 54, "passed": 3, "failed": 1, "pass_rate": 75,
    }
    t = admin_stats.render_overview(d)
    assert "Усього: <b>42</b>" in t and "Викладачі: <b>4</b>" in t
    assert "1800</b>⭐" in t and "конверсія 16%" in t
    assert "склали <b>3</b>" in t and "pass-rate 75%" in t
    assert "Сер. готовність учнів: <b>54%</b>" in t


def test_render_user_card():
    d = {
        "id": 5, "name": "@ola", "role": "student", "status": "approved", "until": "2026-08-01",
        "exam_date": "2026-12-05", "referred_by": 99, "level": "A2", "streak": 7,
        "placement_done": True,
        "readiness": {"sluchanie": 60, "czytanie": 70, "gramatyka": 55, "pisanie": 40, "mowienie": 50},
        "n_sessions": 23, "last": [("gramatyka", 80, "2026-07-12 10:00")],
        "pay_n": 1, "pay_stars": 300, "created_at": "2026-06-01 09:00",
    }
    t = admin_stats.render_user(d)
    assert "@ola" in t and "🎓 учень" in t
    assert "id99" in t  # реферер
    assert "🎧60%" in t and "✍️40%" in t  # готовність по модулях
    assert "Оплат: 1 (300⭐)" in t
    assert "placement ✅" in t


def test_render_segments():
    d = {
        "organic_total": 30, "organic_paying": 3, "organic_conv": 10,
        "referred_total": 8, "referred_paying": 4, "referred_conv": 50,
    }
    t = admin_stats.render_segments(d)
    assert "Самостійні:</b> 30" in t and "конверсія <b>10%</b>" in t
    assert "Від викладача:</b> 8" in t and "конверсія <b>50%</b>" in t


def test_render_group():
    d = {
        "id": 9, "name": "@teacher", "students": [
            {"id": 1, "name": "@a", "overall": 60, "status": "approved", "streak": 5, "paying": True},
            {"id": 2, "name": "@b", "overall": 20, "status": "pending", "streak": 0, "paying": False},
        ],
    }
    t = admin_stats.render_group(d)
    assert "@teacher" in t and "учнів: <b>2</b>" in t
    assert "@a" in t and "💎" in t and "🏁60%" in t
    assert "⏳ @b" in t  # pending → годинник


def test_render_group_empty():
    assert "немає учнів" in admin_stats.render_group({"id": 1, "name": "@t", "students": []})


def test_render_user_no_referrer_no_exam():
    d = {
        "id": 1, "name": "id1", "role": "teacher", "status": "approved", "until": "",
        "exam_date": "", "referred_by": 0, "level": "", "streak": 0, "placement_done": False,
        "readiness": {}, "n_sessions": 0, "last": [], "pay_n": 0, "pay_stars": 0,
        "created_at": "2026-06-01 09:00",
    }
    t = admin_stats.render_user(d)
    assert "👩‍🏫 викладач" in t and "Реферер: —" in t
    assert "📅 Іспит" not in t  # без дати — рядок відсутній
    assert "🎧0%" in t  # порожня готовність → нулі
