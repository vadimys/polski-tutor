FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Best practice: не-root користувач (мінімізуємо поверхню)
RUN useradd --create-home --uid 10001 appuser
USER appuser

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "app.main"]
