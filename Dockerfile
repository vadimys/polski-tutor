FROM python:3.12-slim

# ffmpeg — аудіо (.oga/.ogg); libgomp1 — для ctranslate2 (whisper); curl — завантаження моделей
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) Важкі залежності — ОКРЕМИЙ шар (кешується між змінами коду; список синхронний з pyproject)
RUN pip install --no-cache-dir \
    "aiogram>=3.13,<4" "redis>=5" "anthropic>=0.40" "pydantic-settings>=2.5" \
    "tzdata>=2024.1" "faster-whisper>=1.0" "piper-tts>=1.2"

# 2) Whisper-модель у образ (офлайн у рантаймі). Кешується окремо від коду.
RUN python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8', download_root='/opt/models')" \
    && chmod -R a+rX /opt/models
ENV HF_HUB_OFFLINE=1

# 3) Голос piper для Słuchanie. Завантаження НЕ фатальне → деградація до тексту.
RUN mkdir -p /opt/voices && cd /opt/voices \
    && BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/gosia/medium" \
    && (curl -fsSL -O "$BASE/pl_PL-gosia-medium.onnx" \
        && curl -fsSL -O "$BASE/pl_PL-gosia-medium.onnx.json" \
        || echo "WARN: piper voice download failed — Słuchanie у текстовому режимі") \
    && chmod -R a+rX /opt/voices

# 4) Застосунок — лише цей шар рерраниться при зміні коду (deps/моделі кешовані)
COPY pyproject.toml README.md alembic.ini ./
COPY migrations ./migrations
COPY src ./src
RUN pip install --no-cache-dir --no-deps .

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Best practice: не-root користувач
RUN useradd --create-home --uid 10001 appuser
USER appuser

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "app.main"]
