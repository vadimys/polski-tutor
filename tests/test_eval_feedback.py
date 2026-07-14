"""Оцінювання якості фідбеку: детермінований контракт + парсинг вердикту + рендер."""

from app.services import eval_feedback as ef


def test_contract_ok():
    fb = "<b>Оцінка</b> добре. <b>Помилки</b>: було→стало. <b>Порада</b>: читай. <b>Зразок</b>: ..."
    assert ef.contract_issues(fb, (6, 5, 4)) == []


def test_contract_catches_violations():
    assert "порожній фідбек" in ef.contract_issues("", (5, 5, 5))
    assert any("WYNIK" in i for i in ef.contract_issues("Помилки Порада Зразок текст", None))
    assert any("0-10" in i for i in ef.contract_issues("Помилки Порада Зразок", (11, 5, 5)))
    assert any("Зразок" in i for i in ef.contract_issues("Помилки і Порада є", (5, 5, 5)))
    assert any("українською" in i for i in ef.contract_issues("Pomylki Porada Zrazok tylko po polsku", (5, 5, 5)))


def test_render_calibration_flags_mismatch():
    rows = [
        {"level": "слабка", "scores": (7, 6, 6), "expect_pass": False, "got_pass": True, "contract": [], "verdict": None},
    ]
    t = ef.render_calibration(rows)
    assert "⚠️" in t and "Розбіжностей: 1" in t
