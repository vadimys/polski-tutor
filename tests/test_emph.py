"""emph: зберігає авторські <i>/<b>, екранує решту (контент розрахований на HTML)."""

from app.bot.ui import emph


def test_emph_preserves_i_b_escapes_rest():
    assert emph("зайве — <b>z</b>") == "зайве — <b>z</b>"
    assert emph("→ <i>przed</i>") == "→ <i>przed</i>"
    assert emph("a <b>x</b> & <i>y</i>") == "a <b>x</b> &amp; <i>y</i>"
    # небезпечні теги лишаються екранованими
    assert emph("<script>alert(1)</script>") == "&lt;script&gt;alert(1)&lt;/script&gt;"
    assert emph("") == ""


def test_emph_no_raw_angle_left_for_plain():
    # звичайний текст без тегів не отримує жодних < >
    assert "<" not in emph("Kilka miesięcy ___ wakacjami")
