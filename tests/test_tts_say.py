"""Реєстр озвучення: короткий стабільний id для callback_data."""

from app.services import tts_say


def test_sid_stable_and_short():
    a = tts_say.sid_for("dzień dobry")
    b = tts_say.sid_for("  dzień dobry  ")  # обрізаємо пробіли → той самий id
    assert a == b
    assert len(a) == 14
    assert len(f"say:{a}") <= 64  # влазить у ліміт callback_data Telegram


def test_sid_differs_for_different_text():
    assert tts_say.sid_for("kot") != tts_say.sid_for("pies")


def test_slow_and_normal_get_distinct_cache_tags():
    # нормальний і сповільнений темп мусять кешуватися окремо (різний file_id)
    assert tts_say._tag(slow=False) != tts_say._tag(slow=True)
