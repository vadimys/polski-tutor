# Polski B1 Coach 🇵🇱

Telegram-бот — персональна щоденна підготовка до державного іспиту **B1** з польської
(*egzamin certyfikatowy z języka polskiego jako obcego*).

**Ціль:** скласти іспит **5 грудня 2026**. Тренуємо всі 5 модулів, бо на іспиті треба
**≥50% у кожному окремо**: 🎧 Słuchanie · 📖 Czytanie · 🔤 Gramatyka · ✍️ Pisanie · 🗣 Mówienie.

## Що вміє (MVP)
- `/start` — привітання, рівень, лічильник днів до іспиту.
- `/test` — стартовий placement-тест (~18 питань A1→B1) → оцінка рівня + готовність за модулями.
- `/lekcja` — мікро-урок під найслабший модуль (генерує Claude, пояснення українською).
- Щоденне нагадування о `LESSON_HOUR` (за замовч. 8:00 Europe/Warsaw) + лічильник стріку.

## Архітектура
- Python 3.12, **aiogram** (long polling) + **Redis** (FSM-сторедж і стан учня).
- AI — **Anthropic API**, тіровано: `cheap_model` (Haiku) для дрилів, `strong_model` (Sonnet)
  для уроків/фідбеку письма.
- Стан учня — JSON у Redis (`app/services/state.py`); SRS Leitner — `app/services/srs.py`.
- Хоститься на homeserver через `docker compose` (поряд із ботом Zelika; окремий токен).

Педагогічний «мозок» (промпти, методика, пріоритетна граматика) — у `agent/*.md`, `state/*.md`
(спадок vault-прототипу, тепер довідка для системних промптів бота).

## Локально / тести
```bash
pip install -e ".[dev]"
BOT_TOKEN=test:token PYTHONPATH=src pytest -q
```

## Деплой (homeserver)
```bash
git pull --ff-only
docker compose up -d --build
```
`.env` створюється на сервері з `.env.example` (у git не потрапляє). CI (GitHub Actions)
ганяє ruff + mypy + pytest на кожен push.
