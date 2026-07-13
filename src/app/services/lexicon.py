"""Вільний тематичний словник — «світового зразка» навчання лексики за темами.

Ієрархія: 12 тем (офіційний тематичний каталог B1) → ~5 підтем кожна → ~24 слова.
Слова AI-генеруються дешевою моделлю НА ПІДТЕМУ й кешуються (генерація раз, далі кеш).
Це ДОПОМІЖНА лексика (не екзаменаційне завдання) — готовність НЕ рухає.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from redis.asyncio import Redis

from app.config import settings
from app.integrations import ai

_redis: Redis | None = None
_TTL = 120 * 24 * 3600
_N = 24  # слів на підтему
_PREFIX = "polski:lex2"  # нова схема (тема:підтема); стара polski:lex — застаріла

# Теми — за офіційним тематичним каталогом egzamin certyfikatowy B1
TOPICS: list[tuple[str, str]] = [
    ("czlowiek", "🧍 Людина"),
    ("dom", "🏠 Дім і побут"),
    ("rodzina", "👨‍👩‍👧 Родина"),
    ("praca", "💼 Робота"),
    ("urzad", "🏛 Урядові справи"),
    ("zdrowie", "🩺 Здоров'я"),
    ("zakupy", "🛒 Покупки"),
    ("jedzenie", "🍽 Їжа і напої"),
    ("podroze", "✈️ Подорожі"),
    ("edukacja", "🎓 Освіта"),
    ("czas_wolny", "🎭 Дозвілля"),
    ("spoleczenstwo", "🌍 Суспільство і природа"),
]
_TOPIC_LABELS = dict(TOPICS)

# Підтеми кожної теми (slug, український підпис). ~5 на тему → структурований масштаб.
SUBTOPICS: dict[str, list[tuple[str, str]]] = {
    "czlowiek": [
        ("wyglad", "🧑 Зовнішність"),
        ("charakter", "🧠 Характер"),
        ("emocje", "😊 Емоції й почуття"),
        ("cialo", "🦵 Частини тіла"),
        ("etapy", "👶 Вік і етапи життя"),
    ],
    "dom": [
        ("mieszkanie", "🏢 Житло і кімнати"),
        ("meble", "🛋 Меблі"),
        ("sprzety", "🔌 Побутова техніка"),
        ("prace", "🧹 Домашні справи"),
        ("okolica", "🏘 Район і сусідство"),
    ],
    "rodzina": [
        ("czlonkowie", "👪 Члени родини"),
        ("relacje", "❤️ Стосунки"),
        ("swieta", "🎉 Свята й традиції"),
        ("dzieci", "🍼 Діти і виховання"),
        ("etapy", "💍 Етапи (шлюб, ювілеї)"),
    ],
    "praca": [
        ("zawody", "👷 Професії"),
        ("biuro", "🏢 На роботі / офіс"),
        ("szukanie", "📄 Пошук роботи, CV"),
        ("warunki", "💰 Умови й зарплата"),
        ("kariera", "📈 Кар'єра і розвиток"),
    ],
    "urzad": [
        ("dokumenty", "🪪 Документи"),
        ("formalnosci", "✍️ Заяви й формальності"),
        ("bank", "🏦 Банк і гроші"),
        ("poczta", "📮 Пошта"),
        ("uslugi", "🏛 Держпослуги"),
    ],
    "zdrowie": [
        ("lekarz", "🩺 У лікаря"),
        ("choroby", "🤒 Хвороби й симптоми"),
        ("apteka", "💊 Аптека і ліки"),
        ("cialo", "🫀 Тіло і органи"),
        ("styl", "🥗 Здоровий спосіб життя"),
    ],
    "zakupy": [
        ("sklepy", "🏬 Магазини"),
        ("ubrania", "👕 Одяг і взуття"),
        ("produkty", "🧺 Продукти й товари"),
        ("platnosci", "💳 Оплата і ціни"),
        ("uslugi", "🔧 Послуги"),
    ],
    "jedzenie": [
        ("owoce", "🥕 Овочі й фрукти"),
        ("dania", "🍲 Страви"),
        ("napoje", "🥤 Напої"),
        ("kuchnia", "🍳 Кухня і готування"),
        ("restauracja", "🍽 У ресторані"),
    ],
    "podroze": [
        ("transport", "🚆 Транспорт"),
        ("lotnisko", "🛫 Аеропорт і вокзал"),
        ("hotel", "🏨 Готель і житло"),
        ("zwiedzanie", "🗺 Туризм і огляд"),
        ("kierunki", "🧭 Напрямки й орієнтація"),
    ],
    "edukacja": [
        ("szkola", "🏫 Школа"),
        ("przedmioty", "📚 Предмети"),
        ("egzaminy", "📝 Іспити й оцінки"),
        ("studia", "🎓 Навчання і виш"),
        ("jezyki", "🗣 Вивчення мов"),
    ],
    "czas_wolny": [
        ("sport", "⚽ Спорт"),
        ("kultura", "🎬 Кіно, театр, музика"),
        ("hobby", "🎨 Хобі"),
        ("media", "📺 ТВ та інтернет"),
        ("spotkania", "🍹 Зустрічі й відпочинок"),
    ],
    "spoleczenstwo": [
        ("przyroda", "🌳 Природа й погода"),
        ("technologia", "💻 Технології"),
        ("ekologia", "♻️ Екологія"),
        ("media", "📰 ЗМІ та інформація"),
        ("panstwo", "🏛 Держава й суспільство"),
    ],
}


@dataclass
class Word:
    pl: str
    ua: str
    example: str
    level: int  # 1 легке .. 3 складне


def topic_label(topic_key: str) -> str:
    return _TOPIC_LABELS.get(topic_key, topic_key)


def subtopics(topic_key: str) -> list[tuple[str, str]]:
    return SUBTOPICS.get(topic_key, [])


def sub_label(topic_key: str, sub_key: str) -> str:
    for key, lbl in SUBTOPICS.get(topic_key, []):
        if key == sub_key:
            return lbl
    return sub_key


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(topic_key: str, sub_key: str) -> str:
    return f"{_PREFIX}:{topic_key}:{sub_key}"


def _prompt(topic_lbl: str, sub_lbl: str) -> str:
    return (
        "Ти — укладач польсько-українського навчального словника для іспиту B1.\n"
        f"Тема: «{topic_lbl}», підтема: «{sub_lbl}».\n"
        f"Згенеруй {_N} НАЙКОРИСНІШИХ польських слів САМЕ цієї підтеми (рівень A2–B1).\n"
        'Поверни СТРОГО JSON-масив об\'єктів {"pl","ua","example","level"}:\n'
        "• pl — польське слово в базовій формі (іменники з родом, якщо доречно — без дужок);\n"
        "• ua — стислий і ТОЧНИЙ український переклад (без приміток у дужках);\n"
        "• example — коротке природне речення польською з цим словом;\n"
        "• level — 1 (найуживаніше), 2 (середнє), 3 (складніше).\n"
        "Слова строго в межах підтеми, без повторів, від найуживаніших до складніших. "
        "Тільки валідний JSON, без пояснень."
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
    seen: set[str] = set()
    for o in arr:
        if not (isinstance(o, dict) and o.get("pl") and o.get("ua")):
            continue
        pl = str(o["pl"]).strip()
        if pl.lower() in seen:
            continue
        seen.add(pl.lower())
        try:
            lvl = int(o.get("level", 1))
        except (ValueError, TypeError):
            lvl = 1
        words.append(
            Word(pl, str(o["ua"]).strip(), str(o.get("example", "")).strip(), max(1, min(3, lvl)))
        )
    words.sort(key=lambda w: w.level)  # від найлегших до найважчих
    return words


async def words_for(topic_key: str, sub_key: str) -> list[Word]:
    """Слова підтеми (з кешу; за відсутності — згенерувати дешевою моделлю й закешувати)."""
    key = _key(topic_key, sub_key)
    cached = await _r().get(key)
    if cached:
        return [Word(**w) for w in json.loads(cached)]
    if not ai.enabled():
        return []
    raw = await ai.ask(
        "Ти вкладаєш польсько-українські навчальні словники.",
        _prompt(topic_label(topic_key), sub_label(topic_key, sub_key)),
        strong=False,
        max_tokens=2200,
    )
    words = _parse(raw)
    if words:
        await _r().set(key, json.dumps([w.__dict__ for w in words], ensure_ascii=False), ex=_TTL)
    return words


async def cached_words(topic_key: str, sub_key: str) -> list[Word] | None:
    """Слова підтеми ТІЛЬКИ з кешу (без генерації) — для прогресу в меню. None, якщо ще нема."""
    raw = await _r().get(_key(topic_key, sub_key))
    return [Word(**w) for w in json.loads(raw)] if raw else None


def _apply_edit(arr: list[dict], pl: str, ua: str, example: str | None) -> bool:
    """Чисте редагування списку слів (для тесту). True, якщо слово знайдено й змінено."""
    for o in arr:
        if o.get("pl") == pl:
            if ua:
                o["ua"] = ua
            if example is not None:
                o["example"] = example
            return True
    return False


def _apply_remove(arr: list[dict], pl: str) -> list[dict]:
    return [o for o in arr if o.get("pl") != pl]


async def edit_word(topic_key: str, sub_key: str, pl: str, ua: str, example: str | None = None) -> bool:
    """Виправити переклад/приклад слова у кеші підтеми (адмін). Зберігається для всіх."""
    key = _key(topic_key, sub_key)
    raw = await _r().get(key)
    if not raw:
        return False
    arr = json.loads(raw)
    if not _apply_edit(arr, pl, ua, example):
        return False
    await _r().set(key, json.dumps(arr, ensure_ascii=False), ex=_TTL)
    return True


async def remove_word(topic_key: str, sub_key: str, pl: str) -> bool:
    """Прибрати слово з кешу підтеми (адмін). Зберігається для всіх."""
    key = _key(topic_key, sub_key)
    raw = await _r().get(key)
    if not raw:
        return False
    await _r().set(key, json.dumps(_apply_remove(json.loads(raw), pl), ensure_ascii=False), ex=_TTL)
    return True


async def search(query: str, limit: int = 20) -> list[tuple[Word, str, str]]:
    """Пошук слова серед УЖЕ згенерованих (кешованих) підтем — по pl або ua (підрядок).
    Повертає [(Word, topic_key, sub_key)]. Регістронезалежно."""
    q = query.strip().lower()
    if len(q) < 2:
        return []
    out: list[tuple[Word, str, str]] = []
    r = _r()
    async for key in r.scan_iter(f"{_PREFIX}:*"):
        parts = key.split(":")
        if len(parts) != 4:
            continue
        _, _, topic_key, sub_key = parts
        raw = await r.get(key)
        if not raw:
            continue
        for w in json.loads(raw):
            if q in str(w.get("pl", "")).lower() or q in str(w.get("ua", "")).lower():
                out.append((Word(**w), topic_key, sub_key))
                if len(out) >= limit:
                    return out
    return out
