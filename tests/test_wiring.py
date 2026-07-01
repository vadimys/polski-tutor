"""Перевірка цілісності збірки: усі роутери на місці, main валідний.

Ловить «обрізані» файли (порожній prefix компілюється й імпортується, але
без потрібних атрибутів) — чого простий import-тест не помічає.
"""

from aiogram import Router


def test_all_handlers_have_router():
    from app.handlers import (
        admin,
        drills,
        lesson,
        listening,
        menu,
        mock,
        onboarding,
        placement,
        plan,
        privacy,
        quizpoll,
        review,
        speaking,
        start,
        writing,
    )

    mods = (
        start, onboarding, admin, privacy, quizpoll, placement, lesson, writing, drills,
        review, speaking, listening, mock, plan, menu,
    )
    for module in mods:
        assert isinstance(module.router, Router), module.__name__


def test_main_entrypoint_intact():
    from app.main import COMMANDS, main

    assert callable(main)
    assert len(COMMANDS) >= 7  # усі команди на місці
    cmds = {c.command for c in COMMANDS}
    assert {"prywatnosc", "moidane", "zapomnij"} <= cmds  # GDPR-команди на місці


def test_privacy_notice_present():
    from app.handlers.privacy import PRIVACY_NOTICE, PRIVACY_SHORT

    assert "Anthropic" in PRIVACY_NOTICE  # розкриття US-процесора (Ch. V GDPR)
    assert "/zapomnij" in PRIVACY_NOTICE and "/moidane" in PRIVACY_NOTICE
    assert "/prywatnosc" in PRIVACY_SHORT


def test_scheduler_intact():
    from app.scheduler import daily_nudge_loop

    assert callable(daily_nudge_loop)


def test_wave2_functions_present():
    """Хвиля 2: retry/refund/purge/sentry на місці (регресія на обрізані файли)."""
    from app.integrations import ai
    from app.main import _init_sentry
    from app.services import gdpr, limits

    assert ai._MAX_ATTEMPTS >= 2
    assert callable(limits.refund_ai)
    assert callable(gdpr.purge_stale)
    assert callable(_init_sentry)
