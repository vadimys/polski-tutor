# PolskiTutor — встановлення (покроково)

Агент-тьютор польської в окремому Obsidian-vault. Реактивно — викликаєш сам у Claude Code;
проактивно — cron на сервері щоранку генерує урок і шле пуш на телефон.

---

## Передумови
- Obsidian + плагін `obsidian-claude-code` (у тебе вже є).
- Claude Code CLI (`claude`) — на робочій машині й на Dell-сервері. Перевір: `claude --version`.
- Акаунт GitHub (приватний репозиторій під vault).
- Dell-сервер на Ubuntu, який працює цілодобово.
- Застосунок **ntfy** на телефоні (App Store / Google Play).

---

## Крок 1. Поклади vault на робочу машину
1. Розпакуй `PolskiTutor/` у зручне місце (напр. `~/Obsidian/PolskiTutor`).
2. В Obsidian: *Open folder as vault* → вкажи цю теку.
3. Перевір, що бачиш `CLAUDE.md`, теки `agent/`, `state/`, `lessons/`.

✅ Чек-поінт: vault відкривається, файли на місці.

---

## Крок 2. Перший запуск тьютора (реактивно)
1. Запусти Claude Code в цьому vault (через плагін obsidian-claude-code).
2. Напиши: `запусти агента з agent/tutor.md`.
3. Він має прочитати стан, привітатися й запропонувати режим. Пройди коротку сесію.
4. Перевір, що після сесії оновилися `state/vocab.md` і `log/sessions.md`.

✅ Чек-поінт: тьютор веде сесію й сам пише оновлення у стан.

---

## Крок 3. Git + приватний GitHub-репозиторій
У теці vault:
```bash
cd ~/Obsidian/PolskiTutor
git init
git add -A
git commit -m "init PolskiTutor"
```
Створи приватний репо на GitHub (напр. `polski-tutor`), тоді:
```bash
git remote add origin git@github.com:ТВІЙ_АКАУНТ/polski-tutor.git
git branch -M main
git push -u origin main
```

✅ Чек-поінт: репозиторій приватний, файли на GitHub, `.polski.env` НЕ потрапив (його й немає у vault).

---

## Крок 4. Налаштуй Dell-сервер
```bash
# 1) Клонуй vault на сервер у домашню теку
cd ~
git clone git@github.com:ТВІЙ_АКАУНТ/polski-tutor.git PolskiTutor

# 2) Перевір, що claude доступний саме цьому користувачу
which claude && claude --version
```

### Авторизація Claude Code на сервері (один раз) — обери ОДНЕ:
**Варіант А — підписка (без API-ключа, $0 зверху):**
```bash
claude login      # пройди вхід; токен збережеться, headless потім його реюзає
```
**Варіант Б — API-ключ (pay-as-you-go, ~$1–2/міс на Haiku):**
```bash
cp ~/PolskiTutor/.polski.env.example ~/.polski.env
nano ~/.polski.env     # розкоментуй рядок ANTHROPIC_API_KEY і встав ключ
```

### Топік ntfy:
```bash
# якщо ще не створив .polski.env:
cp ~/PolskiTutor/.polski.env.example ~/.polski.env
nano ~/.polski.env     # заміни NTFY_TOPIC на свій випадковий рядок
```

✅ Чек-поінт: `~/PolskiTutor` на сервері, claude авторизований, `~/.polski.env` заповнений.

---

## Крок 5. Тест daily.sh вручну
```bash
chmod +x ~/PolskiTutor/scripts/*.sh
~/PolskiTutor/scripts/daily.sh
```
Має: згенеруватися `lessons/<сьогодні>.md`, оновитися `state/`, з'явитися коміт у GitHub
і прийти пуш на телефон.

❗ Якщо `claude: command not found` у скрипті — додай повний шлях. Знайди його:
`which claude`, тоді встав цей шлях у `export PATH=...` у `scripts/daily.sh`.

✅ Чек-поінт: урок створено, запушено в git, пуш на телефон прийшов.

---

## Крок 6. Cron (щодня о 8:00)
```bash
crontab -e
```
Додай рядок:
```
0 8 * * * /home/ТВІЙ_ЮЗЕР/PolskiTutor/scripts/daily.sh >> /home/ТВІЙ_ЮЗЕР/PolskiTutor/log/cron.log 2>&1
```
Час міняй під себе (`8` → потрібна година). Лог помилок піде в `log/cron.log`.

✅ Чек-поінт: `crontab -l` показує рядок.

---

## Крок 7. ntfy на телефоні
1. Встанови застосунок ntfy.
2. *Subscribe to topic* → впиши той самий топік, що в `~/.polski.env` (`NTFY_TOPIC`).
3. Зроби тест: `~/PolskiTutor/scripts/push.sh "тест"` — має прийти сповіщення.

✅ Чек-поінт: тестовий пуш прийшов на телефон.

---

## Крок 8. Синк vault на телефон (щоб бачити уроки в Obsidian мобільно)
Два варіанти:
- **Obsidian Git** (плагін на мобільному Obsidian) — тягне той самий GitHub-репо. Узгоджується з git-підходом.
- **Obsidian Sync** (платний офіційний) — найпростіше, але окрема підписка.

Якщо хочеш бачити уроки ще й на робочій машині — там роби `git pull` перед сесією
(або теж постав плагін Obsidian Git з автопулом).

✅ Чек-поінт: ранкова нотатка уроку з'являється в Obsidian на телефоні.

---

## Як користуватися щодня
- **Зранку:** прийшов пуш → відкрив нотатку `lessons/<дата>.md`, пройшов урок очима.
- **Коли є час:** запусти `tutor` у Claude Code на робочій машині — жива розмова/повторення,
  агент сам підтягує due-слова й оновлює прогрес.
- Усе синкається через git, стан накопичується у `state/`.

## Підкрутити під себе
- Модель: у `agent/*.md` поле `model:` — `claude-haiku-4-5` (дешево) → `claude-sonnet-4-6` (багатша розмова).
- Рівень/теми: правь `state/progress.md` (черга тем, рівень).
- Час уроку: рядок cron.
- Інтервали SRS: блок «SRS» у `agent/tutor.md`.
