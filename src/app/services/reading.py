"""«Читалочка» — секретний адмін-режим: фото тексту → інтерактивне читання для дитини.

Потік: адмін шле фото → OCR через Claude vision (`extract`) витягує польський текст,
ділить на короткі речення й будує словничок (кожне слово → український переклад).
Результат кешується в Redis під коротким id; хендлер дає читати весь текст / по реченнях
(тап на будь-яке слово → вимова + переклад) / словничок — усе зі сповільненням.

Чисті хелпери (`norm`/`word_tokens`/`translate`/`split_sentences`) тестуються без Redis/AI.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from redis.asyncio import Redis

from app.config import settings

_redis: Redis | None = None
_TTL = 30 * 24 * 3600  # читанка живе місяць — дитина може вертатись до тексту
_MAX_GLOSSARY = 120  # стеля словника (захист від величезних сторінок)

# JSON-схема витягу (structured output) — гарантовано валідний обʼєкт
EXTRACT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "text": {"type": "string"},
        "sentences": {"type": "array", "items": {"type": "string"}},
        "glossary": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"pl": {"type": "string"}, "uk": {"type": "string"}},
                "required": ["pl", "uk"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["title", "text", "sentences", "glossary"],
    "additionalProperties": False,
}

_SYSTEM = (
    "Ти — помічник для дитини, яка вчиться читати польською. На вході — ФОТО сторінки з "
    "польським текстом (книжка/зошит). Твоя задача — акуратно розпізнати текст і підготувати "
    "його до читання. Правила:\n"
    "1. Витягни РІВНО той польський текст, що на фото. Збережи ВСІ діакритики (ą ć ę ł ń ó ś ź ż). "
    "Не вигадуй і не додавай нічого, чого немає. Ігноруй сторонні написи (номери сторінок, "
    "підписи до картинок, службові позначки на кшталт «dź Dź»).\n"
    "2. `title` — короткий заголовок тексту (якщо є) або 2-3 слова про зміст.\n"
    "3. `text` — весь звʼязний текст; абзаци розділяй порожнім рядком.\n"
    "4. `sentences` — той самий текст, поділений на КОРОТКІ рядки для читання (речення; довгі "
    "речення можна ділити по комах/тире). Кожен рядок — те, що дитині зручно прочитати за раз.\n"
    "5. `glossary` — КОЖНЕ різне слово з тексту (у формі, як у тексті, малими літерами, без "
    "пунктуації) з простим українським перекладом У КОНТЕКСТІ. Включай і службові слова "
    "(i, w, z, na, do, ale). Максимум "
    + str(_MAX_GLOSSARY)
    + " слів. Переклад — 1-3 слова, зрозуміло дитині.\n"
    "Відповідай лише структурованим JSON."
)


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def norm(word: str) -> str:
    """Нормалізувати слово для звірки: малі літери, без пунктуації по краях."""
    return re.sub(r"^\W+|\W+$", "", word.strip().lower(), flags=re.UNICODE)


_WORD_RE = re.compile(r"[^\s]+")


def word_tokens(sentence: str) -> list[str]:
    """Розбити речення на токени (слова з пунктуацією, як у тексті) для кнопок-слів."""
    return _WORD_RE.findall(sentence.strip())


def split_sentences(text: str) -> list[str]:
    """Фолбек-поділ на речення (якщо AI не дав `sentences`)."""
    parts = re.split(r"(?<=[.!?…])\s+|\n+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def gloss_map(obj: dict) -> dict[str, str]:
    """Словник {нормалізоване_слово: переклад} для швидкого пошуку по тапу."""
    out: dict[str, str] = {}
    for it in obj.get("glossary", []):
        pl = norm(str(it.get("pl", "")))
        uk = str(it.get("uk", "")).strip()
        if pl and uk and pl not in out:
            out[pl] = uk
    return out


def translate(obj: dict, token: str) -> str | None:
    """Переклад слова (за нормалізованим ключем) або None, якщо нема у словнику."""
    return gloss_map(obj).get(norm(token))


def _rid(text: str) -> str:
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:12]  # noqa: S324


async def extract(image_b64: str, media_type: str = "image/jpeg") -> dict | None:
    """OCR + підготовка тексту через Claude vision. None → AI вимкнено/збій/порожньо."""
    from app.integrations import ai

    obj = await ai.ask_json_image(
        _SYSTEM,
        "Проаналізуй це зображення й підготуй текст до читання.",
        image_b64,
        EXTRACT_SCHEMA,
        media_type=media_type,
        strong=True,
        max_tokens=4000,
        label="reading_ocr",
    )
    if not isinstance(obj, dict) or not str(obj.get("text", "")).strip():
        return None
    # нормалізуємо/підчищаємо структуру
    text = str(obj["text"]).strip()
    sentences = [str(s).strip() for s in obj.get("sentences", []) if str(s).strip()]
    if not sentences:
        sentences = split_sentences(text)
    glossary = [
        {"pl": str(g.get("pl", "")).strip(), "uk": str(g.get("uk", "")).strip()}
        for g in obj.get("glossary", [])
        if str(g.get("pl", "")).strip() and str(g.get("uk", "")).strip()
    ][:_MAX_GLOSSARY]
    return {
        "title": str(obj.get("title", "")).strip() or "Текст",
        "text": text,
        "sentences": sentences,
        "glossary": glossary,
    }


async def stash(obj: dict) -> str:
    """Зберегти читанку в Redis, повернути короткий id для callback_data."""
    rid = _rid(obj["text"])
    await _r().set(f"polski:read:{rid}", json.dumps(obj, ensure_ascii=False), ex=_TTL)
    return rid


async def load(rid: str) -> dict | None:
    raw = await _r().get(f"polski:read:{rid}")
    if not raw:
        return None
    if isinstance(raw, bytes):
        raw = raw.decode()
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return None
