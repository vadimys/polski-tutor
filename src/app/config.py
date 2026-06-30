"""Конфіг застосунку (env → типізовані налаштування)."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Telegram
    bot_token: str

    # AI (тіровано: сильна модель для письма/фідбеку, дешева для дрилів)
    anthropic_api_key: str | None = None
    strong_model: str = "claude-sonnet-4-6"
    cheap_model: str = "claude-haiku-4-5-20251001"

    # Інфра
    redis_url: str = "redis://redis:6379/0"

    # Навчання / графік
    timezone: str = "Europe/Warsaw"
    lesson_hour: int = 8
    exam_date: str = "2026-12-05"


settings = Settings()  # type: ignore[call-arg]
