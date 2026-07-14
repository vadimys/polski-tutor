# RUNBOOK — Polski B1 Coach (на випадок пожежі)

Швидкі дії, коли щось пішло не так. Усе виконується на homeserver: `ssh vadym@homeserver.local`, тоді `cd ~/polski-tutor`.

## Здоров'я і логи

```bash
docker compose ps                          # хто живий / healthy
docker compose exec -T bot python -c "import urllib.request;print(urllib.request.urlopen('http://localhost:8080/health',timeout=5).read().decode())"
docker compose logs --tail=100 bot         # останні логи бота
docker compose logs -f bot                 # хвіст у реальному часі
```

`/health` → `{"status":"ok","db":"ok","redis":"ok"}` = все добре. `degraded` → дивись, що `fail` (db/redis).

## Рестарт / редеплой

```bash
docker compose restart bot                 # просто перезапустити
git pull --ff-only && docker compose up -d --build bot   # викотити нову версію
```

## Відкат (нова версія зламала прод)

```bash
git log --oneline -5                       # знайти останній добрий коміт
git revert --no-edit <bad_sha>             # або: git reset --hard <good_sha>
git push origin main
git pull --ff-only && docker compose up -d --build bot
```

## Наплив / перевантаження

- **Шторм 429 від Anthropic / дорого:** опусти стелю одночасних викликів у `.env` → `AI_MAX_CONCURRENCY=3`, тоді `docker compose up -d --force-recreate bot`. Ліміт на юзера: `AI_DAILY_LIMIT`.
- **Спам алертів:** `ALERT_THROTTLE_SECS` (за замовч. 600).
- **Бюджет-поріг алерту:** `AI_DAILY_BUDGET_USD` (0 = вимкнути).
- **CPU/RAM/диск:** `docker stats` (миттєвий зріз). Диск: `df -h`, `docker system df`; чистка: `docker system prune -f`.

## Postgres

- **Бекапи** лежать у `~/polski-tutor/backups/` (щоденні/тижневі/місячні, ротація автоматична).
- **Зробити бекап негайно:** `docker compose exec -T postgres-backup /backup.sh`
- **Відновити з дампа** (⚠️ перезапише дані):
  ```bash
  docker compose stop bot
  gunzip -c backups/daily/polski-<дата>.sql.gz | docker compose exec -T postgres psql -U polski -d polski
  docker compose start bot
  ```
- **Ручний дамп:** `docker compose exec -T postgres pg_dump -U polski polski | gzip > manual-$(date +%F).sql.gz`

## Redis

- Стан учнів + FSM + лічильники. `maxmemory 256mb`, `noeviction` (при переповненні — помилки запису, не тихе витіснення).
- Перевірка: `docker compose exec -T redis redis-cli info memory | grep used_memory_human`
- Кількість ключів: `docker compose exec -T redis redis-cli dbsize`

## Моніторинг

- **healthchecks.io** — зовнішній вартовий: якщо бот/хост мовчить >8 хв, прилітає алерт. Ping-URL у `.env` (`HEALTHCHECK_URL`).
- **netdata** (opt-in): `docker compose --profile monitoring up -d netdata` → `http://homeserver.local:19999`.
- Бот сам шле адміну: помилки (з тротлінгом) і бюджет-алерт AI. Дашборд: `/admin` у боті.

## Типові інциденти

| Симптом | Перша дія |
|---|---|
| Бот не відповідає | `docker compose ps` → якщо не `Up`, `docker compose up -d bot`; глянь `logs --tail=100 bot` |
| `/health` = degraded (db) | `docker compose logs postgres`; `docker compose restart postgres` |
| `/health` = degraded (redis) | `docker compose logs redis`; `docker compose restart redis` |
| Наплив, лаги | опусти `AI_MAX_CONCURRENCY`, перевір `docker stats` |
| Диск заповнений | `docker system prune -f`; перевір `backups/` і логи |
| Зламав реліз | відкат (див. вище) |
