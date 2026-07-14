"""Admin Mini App: похідний URL дашборда з базового webapp_url."""

from app.bot import webapp_admin
from app.config import settings


def test_admin_url_from_app_base(monkeypatch):
    monkeypatch.setattr(settings, "webapp_url", "https://x.com/app")
    assert webapp_admin.admin_url() == "https://x.com/admin"


def test_admin_url_from_bare_domain(monkeypatch):
    monkeypatch.setattr(settings, "webapp_url", "https://x.com")
    assert webapp_admin.admin_url() == "https://x.com/admin"
    monkeypatch.setattr(settings, "webapp_url", "https://x.com/")
    assert webapp_admin.admin_url() == "https://x.com/admin"
