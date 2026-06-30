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
    "app.bot.keyboards",
    "app.handlers.start",
    "app.handlers.placement",
    "app.handlers.lesson",
    "app.scheduler",
    "app.main",
]


@pytest.mark.parametrize("mod", MODULES)
def test_import(mod):
    importlib.import_module(mod)
