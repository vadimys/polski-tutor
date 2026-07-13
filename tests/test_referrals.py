"""Учнівські реферали: парсинг лінка + побудова (чисті функції)."""

from app.services import referrals


def test_parse_friend_payload():
    assert referrals.parse("r12345") == 12345
    assert referrals.parse("t999") is None  # teacher — не наш префікс
    assert referrals.parse("g7") is None  # group — не наш
    assert referrals.parse("rabc") is None
    assert referrals.parse("") is None


def test_link_format():
    assert referrals.link("polski_bot", 42) == "https://t.me/polski_bot?start=r42"
