"""ORM-моделі. Таблиця users: стан навчання + поля контролю доступу (схема готова)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, BigInteger, Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # telegram user id
    username: Mapped[str] = mapped_column(String(64), default="")

    # стан навчання
    level: Mapped[str] = mapped_column(String(16), default="A1")
    streak: Mapped[int] = mapped_column(Integer, default=0)
    last_lesson: Mapped[str] = mapped_column(String(16), default="")
    placement_done: Mapped[bool] = mapped_column(Boolean, default=False)
    lesson_hour: Mapped[int] = mapped_column(Integer, default=8)
    readiness: Mapped[dict] = mapped_column(JSON, default=dict)

    # контроль доступу (для грандіозного плану; наразі дефолти)
    exam_date: Mapped[str] = mapped_column(String(16), default="")
    exam_date_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    access_status: Mapped[str] = mapped_column(String(16), default="pending")  # pending/approved/denied
    access_until: Mapped[str] = mapped_column(String(16), default="")
    requested_at: Mapped[str] = mapped_column(String(32), default="")
    decided_at: Mapped[str] = mapped_column(String(32), default="")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Session(Base):
    """Лог кожної вправи (для трендів/статистики/прогнозу)."""

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    module: Mapped[str] = mapped_column(String(16))
    score: Mapped[int] = mapped_column(Integer)  # результат саме цієї вправи, 0..100
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
