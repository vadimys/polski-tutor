"""Розсилка: сегменти-мітки (чисте)."""

from app.services import broadcast


def test_segments_and_label():
    assert set(broadcast.SEGMENTS) == {"all", "students", "teachers", "paying", "trial", "inactive"}
    assert broadcast.label("paying") == "платні"
    assert broadcast.label("inactive") == "неактивні 7+ дн"
    assert broadcast.label("хз") == "хз"
