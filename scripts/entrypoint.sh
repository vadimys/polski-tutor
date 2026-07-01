#!/usr/bin/env bash
set -euo pipefail

# Застосувати міграції БД перед стартом (лише для основного процесу бота)
if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
    echo "[entrypoint] alembic upgrade head…"
    alembic upgrade head
fi

exec "$@"
