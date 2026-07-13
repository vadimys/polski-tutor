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
