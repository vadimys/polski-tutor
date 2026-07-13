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
    ai_daily_limit: int = 30  # ліміт AI-вправ на користувача/добу (контроль витрат; адмін — без ліміту)

    # Адмін (єдиний адмін-акаунт — для запитів на доступ)
    admin_id: int = 0

    # Інфра
    redis_url: str = "redis://redis:6379/0"
    database_url: str = "postgresql+asyncpg://polski:polski@postgres:5432/polski"

    # Observability (опційно): якщо задано SENTRY_DSN — трекінг помилок без нагляду
    sentry_dsn: str | None = None

    # Whisper (локальне розпізнавання голосу для модуля Mówienie)
    whisper_model: str = "small"
    whisper_dir: str = "/opt/models"

    # Piper TTS (локальне озвучення для модуля Słuchanie)
    piper_model: str = "/opt/voices/pl_PL-gosia-medium.onnx"

    # Навчання / графік
    timezone: str = "Europe/Warsaw"
    lesson_hour: int = 8
    exam_date: str = "2026-12-05"

    # Trial: учень за посиланням викладача — довший; органічний (сам знайшов) — коротший
    trial_days: int = 30
    organic_trial_days: int = 14

    # Підписка через Telegram Stars (XTR). 300⭐ ≈ ~25 zł/міс — нижче ринку self-study
    # (Duolingo 63 zł, Babbel 59 zł, Busuu 39 zł); нижче середнього. Змінюється в .env.
    sub_stars: int = 300  # місячна підписка у Stars
    sub_days: int = 30  # на скільки днів продовжує місячна
    sub_year_stars: int = 2000  # річна (~44% дешевше за 12×міс — стандартний річний дисконт)
    sub_year_days: int = 365
    referral_discount_pct: int = 20  # знижка для учнів, приведених викладачем
    winback_extend_days: int = 3  # разова реактивація (churn save-offer «не встиг спробувати»)

    # Mini App (WebApp-панель): публічний HTTPS-URL через cloudflared-тунель.
    # Порожній → кнопку «Панель» не показуємо (бот повністю працює й без тунеля).
    webapp_url: str = ""


settings = Settings()  # type: ignore[call-arg]
