"""Словниковий стор із SRS (Redis hash на користувача).

Поле = польське слово, значення = JSON {uk, box, due}. Інтервали рахує srs.py.
Стартовий банк STARTER сіється при першому запуску (побут + теми резиденції).
"""

from __future__ import annotations

import json
from datetime import date

from redis.asyncio import Redis

from app.config import settings
from app.domain.models import VocabItem
from app.services import srs

_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(user_id: int) -> str:
    return f"polski:vocab:{user_id}"


# Стартова лексика B1: побут + адмін/резиденція (громадянство, urząd, karta pobytu)
STARTER: list[tuple[str, str]] = [
    ("czas", "час"), ("praca", "робота"), ("dom", "дім"), ("woda", "вода"),
    ("jedzenie", "їжа"), ("pieniądze", "гроші"), ("zdrowie", "здоров'я"),
    ("rodzina", "сім'я"), ("dziecko", "дитина"), ("miasto", "місто"),
    ("ulica", "вулиця"), ("samochód", "автомобіль"), ("pociąg", "потяг"),
    ("tydzień", "тиждень"), ("miesiąc", "місяць"), ("rok", "рік"),
    ("godzina", "година"), ("jutro", "завтра"), ("wczoraj", "вчора"),
    ("mówić", "говорити"), ("rozumieć", "розуміти"), ("pomagać", "допомагати"),
    ("potrzebować", "потребувати"), ("musieć", "мусити"),
    # адмін / резиденція
    ("urząd", "установа / відомство"), ("wniosek", "заява / клопотання"),
    ("pobyt", "перебування"), ("obywatelstwo", "громадянство"),
    ("zezwolenie", "дозвіл"), ("meldunek", "реєстрація (прописка)"),
    ("dowód osobisty", "посвідчення особи"), ("paszport", "паспорт"),
    ("podpis", "підпис"), ("termin", "термін / дата"), ("opłata", "оплата"),
    ("zaświadczenie", "довідка"), ("cudzoziemiec", "іноземець"),
    ("karta pobytu", "карта перебування"), ("umowa", "договір"),
]


def _dump(uk: str, box: int, due: str) -> str:
    return json.dumps({"uk": uk, "box": box, "due": due}, ensure_ascii=False)


async def seed_if_empty(user_id: int, today: date) -> int:
    """Засіяти стартовий банк, якщо словник порожній. Повертає к-ть доданих."""
    r = _r()
    k = _key(user_id)
    if await r.hlen(k):
        return 0
    mapping = {pl: _dump(uk, 1, today.isoformat()) for pl, uk in STARTER}
    await r.hset(k, mapping=mapping)
    return len(mapping)


async def add(user_id: int, pl: str, uk: str, today: date) -> bool:
    """Додати нове слово (box=1), якщо ще немає. True, якщо додано."""
    r = _r()
    k = _key(user_id)
    if await r.hexists(k, pl):
        return False
    await r.hset(k, pl, _dump(uk, 1, today.isoformat()))
    return True


async def get(user_id: int, pl: str) -> VocabItem | None:
    raw = await _r().hget(_key(user_id), pl)
    if not raw:
        return None
    d = json.loads(raw)
    return VocabItem(pl=pl, uk=d["uk"], box=d.get("box", 1), due=d.get("due", ""))


async def due(user_id: int, today: date) -> list[VocabItem]:
    """Слова, що «доспіли» до повторення."""
    data = await _r().hgetall(_key(user_id))
    out: list[VocabItem] = []
    for pl, raw in data.items():
        d = json.loads(raw)
        if srs.is_due(d.get("due", ""), today):
            out.append(VocabItem(pl=pl, uk=d["uk"], box=d.get("box", 1), due=d.get("due", "")))
    return out


async def review(user_id: int, pl: str, correct: bool, today: date) -> None:
    """Оновити коробку/дату слова після відповіді (Leitner)."""
    it = await get(user_id, pl)
    if it is None:
        return
    box = srs.on_correct(it.box) if correct else srs.on_wrong(it.box)
    await _r().hset(_key(user_id), pl, _dump(it.uk, box, srs.next_due(box, today)))


async def counts(user_id: int, today: date) -> tuple[int, int]:
    """(усього слів, скільки доспіло сьогодні)."""
    data = await _r().hgetall(_key(user_id))
    due_n = sum(1 for raw in data.values() if srs.is_due(json.loads(raw).get("due", ""), today))
    return len(data), due_n
