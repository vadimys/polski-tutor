#!/usr/bin/env bash
set -euo pipefail
# Пуш-нагадування через ntfy.
# NTFY_TOPIC підтягується з ~/.polski.env (або заміни тут на свій топік).
NTFY_TOPIC="${NTFY_TOPIC:-polski-CHANGE-ME}"
MSG="${1:-Урок польської готовий}"
curl -fsS \
  -H "Title: PolskiTutor" \
  -H "Tags: books" \
  -d "$MSG" \
  "https://ntfy.sh/${NTFY_TOPIC}" >/dev/null
