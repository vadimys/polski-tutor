# Лендінг Polski B1 Coach (SEO, Cloudflare Pages)

Статичний одноекранник → воронка в @polski_b1_Coach_bot (мітки `?start=web_*`).
UA-first, бренд бота (польський червоний + B1 + Arial Black + монофонт-екзам-фрази).

## Деплой (коли буде домен)
1. Заміни `REPLACE-DOMAIN` у `index.html` (canonical/og/url) і `robots.txt` на реальний домен.
2. Додай `og.jpg` (1200×630) у цю папку — генерувати постер-тулінгом (scripts/gen_poster.py).
3. Cloudflare Pages → Connect to Git → цей репо → root `site/` → Build command: (none) → Deploy.
4. Прив'яжи домен у Pages → DNS автоматично. Увімкни Cloudflare Web Analytics (cookieless — без кукі-банера).
5. Google Search Console → верифікуй домен → додай sitemap.

## Статус
Копірайт/дизайн доведено (превʼю-Artifact апрувиться Вадимом). Домен + деплой — відкладено (рішення «поки без домену»).
Наступні cornerstone-статті (SEO-беклог): формат 5 модулів · B1 для карти побиту/громадянства ·
пробний іспит онлайн · Розмова з екзаменатором · rekcja дієслів.
