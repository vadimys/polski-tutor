"""Оцінювання якості фідбеку: детермінований контракт + парсинг вердикту + рендер.

Ці тести — регрес-гейт у CI (без API): ловлять дрейф формату/шкали/мови у фідбеку
письма, мовлення й оцінці відкритих завдань, перш ніж це побачить учень.
"""

from app.services import eval_feedback as ef


# ── письмо ──────────────────────────────────────────────────────────────────
def test_writing_contract_ok():
    fb = "<b>Оцінка</b> добре. <b>Помилки</b>: було→стало. <b>Порада</b>: читай. <b>Зразок</b>: ..."
    assert ef.contract_issues(fb, (6, 5, 4)) == []


def test_writing_contract_catches_violations():
    assert "порожній фідбек" in ef.contract_issues("", (5, 5, 5))
    assert any("не розпарсено" in i for i in ef.contract_issues("Помилки Порада Зразок текст", None))
    assert any("шкали" in i for i in ef.contract_issues("Помилки Порада Зразок", (11, 5, 5)))
    assert any("Зразок" in i for i in ef.contract_issues("Помилки і Порада є", (5, 5, 5)))
    assert any("українською" in i for i in ef.contract_issues("Pomylki Porada Zrazok po polsku", (5, 5, 5)))


# ── мовлення (інша шкала: wykonanie 0-7, gramatyka/słownictwo 0-8) ────────────
_SPEAK_BOUNDS = [(0, 7), (0, 8), (0, 8)]


def test_speaking_contract_ok():
    fb = "<b>Оцінка</b>. <b>Помилки</b>: było→стало. <b>Корисні фрази</b>: chętnie przyjadę."
    assert ef.speaking_contract(fb, (5, 6, 6), _SPEAK_BOUNDS) == []


def test_speaking_contract_catches_scale_and_sections():
    # 9 виходить за wykonanie 0-7 → дрейф шкали
    assert any("шкали" in i for i in ef.speaking_contract("Помилки Корисні фрази", (9, 6, 6), _SPEAK_BOUNDS))
    # немає обовʼязкової секції «Корисні фрази»
    assert any("Корисні фрази" in i for i in ef.speaking_contract("є лише Помилки", (5, 6, 6), _SPEAK_BOUNDS))
    assert any("не розпарсено" in i for i in ef.speaking_contract("Помилки Корисні фрази", None, _SPEAK_BOUNDS))


# ── відкриті завдання (список вердиктів ok/feedback) ──────────────────────────
def test_open_contract_ok():
    results = [{"ok": True, "feedback": "правильно"}, {"ok": False, "feedback": "не те слово"}]
    assert ef.open_contract(results, 2) == []


def test_open_contract_catches_violations():
    assert ef.open_contract(None, 2) == ["немає результатів (None)"]
    assert any("≠ 2" in i for i in ef.open_contract([{"ok": True, "feedback": "ок"}], 2))
    assert any("ok не bool" in i for i in ef.open_contract([{"ok": "yes", "feedback": "ок"}], 1))
    assert any("порожній" in i for i in ef.open_contract([{"ok": True, "feedback": ""}], 1))
    assert any("українською" in i for i in ef.open_contract([{"ok": True, "feedback": "dobrze"}], 1))


# ── рендер ────────────────────────────────────────────────────────────────────
def test_render_calibration_flags_mismatch():
    rows = [
        {"level": "слабка", "scores": (7, 6, 6), "expect_pass": False, "got_pass": True, "contract": [], "verdict": None},
    ]
    t = ef.render_calibration(rows)
    assert "⚠️" in t and "Розбіжностей: 1" in t


def test_render_calibration_uses_detail_and_title():
    rows = [
        {"level": "сильна", "detail": "72%", "expect_pass": True, "got_pass": True, "contract": [], "verdict": None},
    ]
    t = ef.render_calibration(rows, title="Фідбек мовлення")
    assert "Фідбек мовлення" in t and "72%" in t and "✅ Калібрування ок." in t
