"""Async SQLAlchemy: engine + фабрика сесій (lazy, без конекту при імпорті)."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    pass


_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker | None = None


def engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        # Пул під наплив: 10 постійних + 20 overflow (=30 конектів стелі). pre_ping —
        # відсіює «мертві» конекти; recycle — не тримаємо конект вічно (таймаути БД).
        _engine = create_async_engine(
            settings.database_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800,
        )
    return _engine


def session_factory() -> async_sessionmaker:
    global _sessionmaker
    if _sessionmaker is None:
        _sessionmaker = async_sessionmaker(engine(), expire_on_commit=False)
    return _sessionmaker
