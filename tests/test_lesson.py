from app.domain.models import Module
from app.handlers import lesson


def test_parse_lesson_valid_with_code_fence():
    raw = (
        '```json\n{"topic":"T","grammar":"G",'
        '"vocab":[{"pl":"kot","ua":"кіт","example":"To kot."}],"task":"zrób to"}\n```'
    )
    out = lesson._parse_lesson(raw, Module.PISANIE)
    assert out is not None
    assert out["topic"] == "T" and out["vocab_n"] == 1
    assert "kot" in out["vocab"] and out["task"] == "zrób to"
    assert out["module"] == "pisanie"


def test_parse_lesson_invalid_returns_none():
    assert lesson._parse_lesson("not json at all", Module.PISANIE) is None
    assert lesson._parse_lesson('{"topic":"x"}', Module.PISANIE) is None  # бракує полів


def test_fallback_lesson_has_all_fields():
    fb = lesson._fallback_lesson(Module.GRAMATYKA)
    assert {"topic", "grammar", "vocab", "task", "vocab_n", "module", "label"} <= fb.keys()


def test_exercise_cb_covers_every_module():
    for m in Module:
        assert m.value in lesson._EXERCISE_CB  # кнопка «Виконати» знає, куди вести кожен модуль


def _datas(markup):
    return [b.callback_data for row in markup.inline_keyboard for b in row]


def test_menu_kb_review_button_uses_registered_callback():
    """Регрес: кнопка повторення слів шле review:start (обробляється), не мертвий review:show."""
    fb = lesson._fallback_lesson(Module.PISANIE)
    datas = _datas(lesson._menu_kb(fb, due_n=5))
    assert "review:start" in datas
    assert "review:show" not in datas  # review:show — стан-залежний rv-флоу, не вхід


def test_parse_lesson_extracts_vocab_say():
    raw = (
        '{"topic":"T","grammar":"G","task":"zrób","vocab":['
        '{"pl":"kot","ua":"кіт","example":"To kot."},'
        '{"pl":"pies","ua":"пес","example":"To pies."}]}'
    )
    out = lesson._parse_lesson(raw, Module.PISANIE)
    # [мітка, текст-для-озвучення] = слово + приклад
    assert out["vocab_say"] == [["kot", "kot. To kot."], ["pies", "pies. To pies."]]


def test_vocab_say_word_only_when_no_example():
    out = lesson._vocab_say([{"pl": "dom", "ua": "дім"}])
    assert out == [["dom", "dom"]]


def test_vocab_sanitizes_messy_ai_output():
    """Регрес: AI пхає теги+переклад+примітку в example → чистимо (баг «страшне вікно» + 37с аудіо)."""
    raw = (
        '{"topic":"T","grammar":"G","task":"z","vocab":[{"pl":"wniosek","ua":"<b>заява</b>",'
        '"example":"<b>Składam wniosek.</b> — Я подаю заяву. ⚠️ Не плутай з wkład!"}]}'
    )
    out = lesson._parse_lesson(raw, Module.PISANIE)
    # без ЕКРАНОВАНИХ тегів (&lt;), без спойлера, переклад відкритий, без укр. у прикладі
    assert "&lt;" not in out["vocab"] and "tg-spoiler" not in out["vocab"]
    assert "заява" in out["vocab"] and "Я подаю" not in out["vocab"]
    # аудіо — тільки чиста польська
    assert out["vocab_say"][0][1] == "wniosek. Składam wniosek."


def test_fallback_lesson_has_vocab_say():
    assert lesson._fallback_lesson(Module.GRAMATYKA)["vocab_say"]  # непорожній


def test_section_kb_vocab_has_speak_buttons():
    """Розділ «Слова» містить кнопки say:<id> для кожного слова + навігацію."""
    say_items = [("kot", "abc123"), ("pies", "def456")]
    datas = _datas(lesson._section_kb("vocab", "pisanie", say_items))
    assert "say:abc123" in datas and "say:def456" in datas
    assert "les:menu" in datas  # навігація «Назад» на місці
