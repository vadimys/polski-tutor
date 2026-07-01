"""Імпорт усіх модулів — ловить помилки імпорту й дає базове покриття."""

import importlib

import pytest

MODULES = [
    "app.config",
    "app.domain.models",
    "app.services.srs",
    "app.services.state",
    "app.services.placement",
    "app.services.clock",
    "app.integrations.ai",
    "app.integrations.speech",
    "app.integrations.tts",
    "app.db.base",
    "app.db.models",
    "app.services.access",
    "app.services.exam_dates",
    "app.services.plan",
    "app.services.progress",
    "app.services.limits",
    "app.services.badges",
    "app.services.gdpr",
    "app.bot.keyboards",
    "app.bot.ui",
    "app.bot.quiz",
    "app.bot.access_mw",
    "app.services.writing",
    "app.services.drills",
    "app.services.vocab",
    "app.services.feedback",
    "app.services.speaking",
    "app.services.listening",
    "app.services.mock",
    "app.handlers.start",
    "app.handlers.onboarding",
    "app.handlers.admin",
    "app.handlers.errors",
    "app.handlers.placement",
    "app.handlers.lesson",
    "app.handlers.writing",
    "app.handlers.drills",
    "app.handlers.review",
    "app.handlers.speaking",
    "app.handlers.listening",
    "app.handlers.mock",
    "app.handlers.plan",
    "app.handlers.privacy",
    "app.handlers.menu",
    "app.health",
    "app.scheduler",
    "app.main",
]


@pytest.mark.parametrize("mod", MODULES)
def test_import(mod):
    importlib.import_module(mod)
