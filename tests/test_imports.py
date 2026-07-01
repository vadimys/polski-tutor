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
    "app.bot.keyboards",
    "app.bot.ui",
    "app.services.writing",
    "app.services.drills",
    "app.services.vocab",
    "app.services.feedback",
    "app.services.speaking",
    "app.services.listening",
    "app.services.mock",
    "app.handlers.start",
    "app.handlers.placement",
    "app.handlers.lesson",
    "app.handlers.writing",
    "app.handlers.drills",
    "app.handlers.review",
    "app.handlers.speaking",
    "app.handlers.listening",
    "app.handlers.mock",
    "app.handlers.menu",
    "app.scheduler",
    "app.main",
]


@pytest.mark.parametrize("mod", MODULES)
def test_import(mod):
    importlib.import_module(mod)
