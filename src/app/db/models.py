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
    # прогресія (durable): {xp, goal, freeze, streak, last} — щоб не втратити при flushdb Redis
    gamify: Mapped[dict] = mapped_column(JSON, default=dict)

    # ролі та реферали (B2B2C: учні платять, викладачі — безкоштовний канал залучення)
    role: Mapped[str] = mapped_column(String(16), default="student")  # student/teacher/admin
    referred_by: Mapped[int] = mapped_column(BigInteger, default=0)  # id викладача-реферера (0=немає)
    group_id: Mapped[int] = mapped_column(BigInteger, default=0)  # група викладача (0=без групи)

    # контроль доступу (для грандіозного плану; наразі дефолти)
    exam_date: Mapped[str] = mapped_column(String(16), default="")
    exam_date_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    exam_result: Mapped[str] = mapped_column(String(16), default="")  # ''/pending/passed/failed
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


class Group(Base):
    """Група (клас) викладача. Учень входить за join-лінком ?start=g<id>."""

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(BigInteger, index=True)
    name: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Payment(Base):
    """Лог оплат Telegram Stars (підписка учня) — для обліку й атрибуції викладачу."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    stars: Mapped[int] = mapped_column(Integer)  # сума у Stars (XTR)
    days: Mapped[int] = mapped_column(Integer)  # на скільки днів продовжено
    charge_id: Mapped[str] = mapped_column(String(128), default="")  # telegram_payment_charge_id
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
