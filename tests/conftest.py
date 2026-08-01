"""Тестова конфігурація: BOT_TOKEN до імпорту app.*, src у sys.path + DB-фікстура."""

import os
import sys
from pathlib import Path

os.environ.setdefault("BOT_TOKEN", "test:token")

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pytest_asyncio  # noqa: E402
from sqlalchemy import event  # noqa: E402
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402


@pytest_asyncio.fixture
async def db():
    """Свіжа in-memory SQLite БД на тест + перевизначення session_factory усього застосунку.
    FK CASCADE увімкнено (PRAGMA), тож каскади/констрейнти поводяться як у PG."""
    from app.db import (
        base,
        models,  # noqa: F401 — реєструє таблиці в Base.metadata
    )

    engine = create_async_engine(
        "sqlite+aiosqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )

    @event.listens_for(engine.sync_engine, "connect")
    def _fk_on(dbapi_conn, _rec):  # noqa: ANN001, ANN202
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        cur.close()

    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    prev_engine, prev_maker = base._engine, base._sessionmaker
    base._engine, base._sessionmaker = engine, maker
    try:
        yield maker
    finally:
        base._engine, base._sessionmaker = prev_engine, prev_maker
        await engine.dispose()


@pytest_asyncio.fixture
async def fake_redis(monkeypatch):
    """In-memory Redis для тестів Redis-шляхів у CI (де немає redis-сервісу).

    Патчить `Redis.from_url` → fakeredis з єдиним FakeServer (усі сервіси-синглтони
    бачать спільні дані), і скидає закешовані клієнти сервісів, які тест чіпає, щоб
    не було витоку стану між тестами. Повертає FakeServer (за потреби прямого доступу)."""
    import fakeredis.aioredis as far

    server = far.FakeServer()

    def _from_url(_url, **kw):
        return far.FakeRedis(server=server, decode_responses=kw.get("decode_responses", False))

    monkeypatch.setattr("redis.asyncio.Redis.from_url", staticmethod(_from_url))

    # скинути ліниві module-global синглтони, щоб перестворились проти fake
    import app.services.league as _league
    import app.services.sim_quota as _quota
    import app.services.verbs as _verbs

    for mod in (_verbs, _league, _quota):
        monkeypatch.setattr(mod, "_redis", None, raising=False)
    yield server
    for mod in (_verbs, _league, _quota):
        monkeypatch.setattr(mod, "_redis", None, raising=False)
