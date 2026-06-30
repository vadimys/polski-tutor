FROM python:3.12-slim

# ffmpeg — аудіо (.oga/.ogg); libgomp1 — для ctranslate2 (whisper); curl — завантаження моделей
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

# Передзавантажуємо модель Whisper у образ (щоб у рантаймі не лізти в мережу)
RUN python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8', download_root='/opt/models')" \
    && chmod -R a+rX /opt/models

# Модель уже в образі → у рантаймі не лізти в мережу (й не писати в read-only кеш)
ENV HF_HUB_OFFLINE=1

# Голос piper для Słuchanie (TTS). Завантаження НЕ фатальне: якщо не вдалось —
# модуль аудіювання деградує до тексту (tts.available()==False), образ збереться.
RUN mkdir -p /opt/voices && cd /opt/voices \
    && BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/gosia/medium" \
    && (curl -fsSL -O "$BASE/pl_PL-gosia-medium.onnx" \
        && curl -fsSL -O "$BASE/pl_PL-gosia-medium.onnx.json" \
        || echo "WARN: piper voice download failed — Słuchanie буде у текстовому режимі") \
    && chmod -R a+rX /opt/voices

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Best practice: не-root користувач
RUN useradd --create-home --uid 10001 appuser
USER appuser

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "app.main"]
