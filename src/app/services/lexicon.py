"""Вільний словник за темами (для мікро-навчання будь-де).

Це ДОПОМІЖНА лексика (не екзаменаційне завдання): теми — за офіційним тематичним
каталогом B1, слова генеруються дешевою моделлю й кешуються (генерація раз на тему,
далі — з кешу). Порядок — від найлегших до найважчих. Готовність НЕ рухає.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from redis.asyncio import Redis

from app.config import settings
from app.integrations import ai

_redis: Redis | None = None
_TTL = 90 * 24 * 3600
_N = 20  # слів на тему

# Теми — за офіційним тематичним каталогом egzamin certyfikatowy B1
TOPICS: list[tuple[str, str]] = [
    ("czlowiek", "🧍 Людина: зовнішність, характер, емоції"),
    ("dom", "🏠 Дім і побут"),
    ("rodzina", "👨‍👩‍👧 Родина і стосунки"),
    ("praca", "💼 Робота і кар'єра"),
    ("urzad", "🏛 Урядові справи, документи"),
    ("zdrowie", "🩺 Здоров'я і тіло"),
    ("zakupy", "🛒 Покупки й послуги"),
    ("jedzenie", "🍽 Їжа і напої"),
    ("podroze", "✈️ Подорожі й транспорт"),
    ("edukacja", "🎓 Освіта й навчання"),
    ("czas_wolny", "🎭 Дозвілля, культура, спорт"),
    ("spoleczenstwo", "🌍 Суспільство, природа, технології"),
]
_LABELS = dict(TOPICS)


@dataclass
class Word:
    pl: str
    ua: str
    example: str
    level: int  # 1 легке .. 3 складне


def label(topic_key: str) -> str:
    return _LABELS.get(topic_key, topic_key)


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _prompt(topic_label: str) -> str:
    return (
        "Ти — укладач словника для підготовки до польського іспиту B1.\n"
        f"Згенеруй {_N} корисних польських слів за темою «{topic_label}» для рівня B1.\n"
        'Поверни СТРОГО JSON-масив об\'єктів {"pl","ua","example","level"}:\n'
        "• pl — польське слово (базова форма);\n"
        "• ua — стислий український переклад; якщо це «фальшивий друг» — познач «(!фальш. друг)»;\n"
        "• example — коротке речення польською з цим словом;\n"
        "• level — 1 (уживане/легке), 2 (середнє), 3 (складніше).\n"
        "Слова — від найуживаніших до складніших, без повторів. Тільки валідний JSON."
    )


def _parse(raw: str) -> list[Word]:
    s = raw.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\s*", "", s).rstrip("`").strip()
    i, j = s.find("["), s.rfind("]")
    if i < 0 or j < 0:
        return []
    try:
        arr = json.loads(s[i : j + 1])
    except (ValueError, TypeError):
        return []
    words: list[Word] = []
    for o in arr:
        if isinstance(o, dict) and o.get("pl") and o.get("ua"):
            try:
                lvl = int(o.get("level", 1))
            except (ValueError, TypeError):
                lvl = 1
            words.append(Word(str(o["pl"]).strip(), str(o["ua"]).strip(),
                              str(o.get("example", "")).strip(), max(1, min(3, lvl))))
    words.sort(key=lambda w: w.level)  # від найлегших до найважчих
    return words


async def words_for(topic_key: str) -> list[Word]:
    """Слова теми (з кешу; за відсутності — згенерувати дешевою моделлю й закешувати)."""
    key = f"polski:lex:{topic_key}"
    cached = await _r().get(key)
    if cached:
        return [Word(**w) for w in json.loads(cached)]
    if not ai.enabled():
        return []
    raw = await ai.ask("Ти вкладаєш польсько-українські навчальні словники.",
                       _prompt(label(topic_key)), strong=False, max_tokens=1800)
    words = _parse(raw)
    if words:
        await _r().set(key, json.dumps([w.__dict__ for w in words], ensure_ascii=False), ex=_TTL)
    return words
