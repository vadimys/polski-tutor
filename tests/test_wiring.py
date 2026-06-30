"""Перевірка цілісності збірки: усі роутери на місці, main валідний.

Ловить «обрізані» файли (порожній prefix компілюється й імпортується, але
без потрібних атрибутів) — чого простий import-тест не помічає.
"""

from aiogram import Router


def test_all_handlers_have_router():
    from app.handlers import (
        drills,
        lesson,
        menu,
        placement,
        review,
        speaking,
        start,
        writing,
    )

    for module in (start, placement, lesson, writing, drills, review, speaking, menu):
        assert isinstance(module.router, Router), module.__name__


def test_main_entrypoint_intact():
    from app.main import COMMANDS, main

    assert callable(main)
    assert len(COMMANDS) >= 7  # усі команди на місці


def test_scheduler_intact():
    from app.scheduler import daily_nudge_loop

    assert callable(daily_nudge_loop)
