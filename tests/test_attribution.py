"""Атрибуція джерел: парсинг мітки + лінки + рендер (чисті функції)."""

from app.services import admin_stats, attribution


def test_parse_source_accepts_campaign_tags():
    assert attribution.parse_source("fb_wielun") == "fb_wielun"
    assert attribution.parse_source("flyer") == "flyer"
    assert attribution.parse_source("FB_Wielun") == "fb_wielun"  # нормалізує регістр
    assert attribution.parse_source("  ig  ") == "ig"


def test_parse_source_rejects_referrals_and_junk():
    assert attribution.parse_source("r12345") is None  # реферал учня
    assert attribution.parse_source("t999") is None  # викладач
    assert attribution.parse_source("g7") is None  # група
    assert attribution.parse_source("") is None
    assert attribution.parse_source("a") is None  # закоротка
    assert attribution.parse_source("fb-wielun") is None  # дефіс недопустимий
    assert attribution.parse_source("x" * 33) is None  # задовга


def test_link_helpers():
    assert attribution.link("polski_b1_Coach_bot", "fb_wielun") == (
        "https://t.me/polski_b1_Coach_bot?start=fb_wielun"
    )
    assert attribution.tg_link("polski_b1_Coach_bot", "fb_wielun") == (
        "tg://resolve?domain=polski_b1_Coach_bot&start=fb_wielun"
    )


def test_render_sources_empty_and_sorted():
    assert "Ще немає позначених" in admin_stats.render_sources([])
    t = admin_stats.render_sources([("fb_wielun", 12), ("flyer", 3)])
    assert "всього позначених <b>15</b>" in t
    assert "<code>fb_wielun</code> — <b>12</b>" in t
    assert t.index("fb_wielun") < t.index("flyer")  # спадно за кількістю
