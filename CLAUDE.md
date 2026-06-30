# Polski B1 Coach — підготовка до іспиту B1 з польської

**Telegram-бот** для щоденної підготовки користувача до державного іспиту B1
(*egzamin certyfikatowy*), ціль — **5 грудня 2026**. Україномовний учень, старт A1.
Іспит: 5 модулів, треба **≥50% у КОЖНОМУ** окремо.

> Раніше це був Obsidian-vault із Claude Code-агентом (`agent/*.md`, `state/*.md`, `scripts/`).
> Тепер ядро — Python/aiogram-бот у `src/app/`. Vault-файли лишені як **довідка з методики**
> (промпти, пріоритетна граматика, SRS-логіка) — джерело для системних промптів бота.

## Архітектура (src/app/)
- `config.py` — env-налаштування (BOT_TOKEN, ANTHROPIC_API_KEY, моделі, TIMEZONE, LESSON_HOUR, EXAM_DATE).
- `main.py` — точка входу: aiogram polling + `RedisStorage` + запуск `scheduler.daily_nudge_loop`.
- `domain/models.py` — `Module` (5 модулів), `UserState`, `VocabItem`.
- `services/` — `srs.py` (Leitner, чисті функції), `state.py` (стан учня JSON у Redis),
  `placement.py` (банк питань + скоринг), `clock.py` (час/днів до іспиту).
- `integrations/ai.py` — Anthropic, тіровано (`strong`=Sonnet для письма/уроків, cheap=Haiku).
- `handlers/` — `start.py` (/start), `placement.py` (тест, FSM), `lesson.py` (урок).
- `bot/keyboards.py` — інлайн-клавіатури.

## Конвенції
- **Пояснення — українською, ПРОСТО, з прикладами.** Цільова мова — польська. Завжди підсвічуй
  «фальшивих друзів». Адаптивно домішувати польську в пояснення в міру прогресу.
- aiogram інжектить `FSMContext` лише в параметр з імʼям `state` — тому стан-сервіс
  імпортуй як `from app.services import state as user_state` у хендлерах із FSM.
- Форматування повідомлень — HTML (`<b>`), без markdown.
- Деплой: homeserver, `docker compose up -d --build` (поряд із ботом Zelika, окремий токен/compose).
  `.env` — на сервері, у git не потрапляє.

## Стан розробки
MVP: /start + placement-тест + мікро-урок + щоденне нагадування. Далі (беклог):
SRS-движок у щоденному флоу, фідбек письма (Sonnet), дрили читання/граматики,
мовлення (голос→Whisper→фідбек), дашборд 5 модулів, повні моки до грудня.
Деталі плану — у памʼяті проєкту (memory: polski-b1-project).
