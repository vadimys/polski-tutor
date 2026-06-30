#!/usr/bin/env bash
set -euo pipefail

# cron має куций PATH — додаємо типові розташування claude/git/curl
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"

# === НАЛАШТУЙ за потреби ===
VAULT="${VAULT:-$HOME/PolskiTutor}"
# ===========================

# Авторизація + топік ntfy. API-ключ (за потреби) і NTFY_TOPIC — у ~/.polski.env
[ -f "$HOME/.polski.env" ] && source "$HOME/.polski.env"

cd "$VAULT"

# 1) Підтягнути останній стан
git pull -q --rebase || true

# 2) Згенерувати урок (headless, дешева модель Haiku)
claude -p "$(cat agent/daily.md)" \
  --model claude-haiku-4-5 \
  --permission-mode acceptEdits \
  --allowedTools "Read,Write,Edit"

# 3) Зберегти урок назад у GitHub
git add -A
git commit -qm "lesson $(date +%F)" || true
git push -q || true

# 4) Пуш на телефон
"$VAULT/scripts/push.sh" "Урок польської на $(date +%d.%m) готовий 📚"
