#!/usr/bin/env python3
"""Локальний генератор постера через Gemini image API (Nano Banana).

Ключ — з файлу .gemini.key (gitignored) або env GEMINI_API_KEY. Ніколи не друкуємо ключ.
Пробує новий interactions-API (gemini-3.1-flash-image, aspect_ratio 4:5), фолбек —
класичний generateContent (gemini-2.5-flash-image). Зберігає результат у файл.

Використання:
    python3 scripts/gen_poster.py [out.png] [prompt_file]
"""

from __future__ import annotations

import base64
import json
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _key() -> str:
    import os

    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if k:
        return k
    f = ROOT / ".gemini.key"
    if f.exists():
        return f.read_text().strip()
    sys.exit("Нема ключа: створи .gemini.key або встанови GEMINI_API_KEY")


def _post(url: str, headers: dict, body: dict) -> tuple[int, bytes]:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:  # noqa: S310 — фіксований google URL
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def _extract_b64(data: dict) -> str | None:
    # interactions-API
    oi = data.get("output_image") or (data.get("interaction") or {}).get("output_image")
    if isinstance(oi, dict) and oi.get("data"):
        return oi["data"]
    for out in data.get("output", []) if isinstance(data.get("output"), list) else []:
        if isinstance(out, dict) and out.get("type") == "image" and out.get("data"):
            return out["data"]
    # generateContent-API
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inl = part.get("inlineData") or part.get("inline_data")
            if isinstance(inl, dict) and inl.get("data"):
                return inl["data"]
    return None


def generate(prompt: str, out: pathlib.Path) -> None:
    key = _key()
    attempts = [
        (
            "interactions/gemini-3.1-flash-image",
            "https://generativelanguage.googleapis.com/v1beta/interactions",
            {"x-goog-api-key": key},
            {
                "model": "gemini-3.1-flash-image",
                "input": [{"type": "text", "text": prompt}],
                "response_format": {"type": "image", "mime_type": "image/jpeg", "aspect_ratio": "4:5", "image_size": "2K"},
            },
        ),
        (
            "generateContent/gemini-2.5-flash-image",
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={key}",
            {},
            {"contents": [{"parts": [{"text": prompt}]}]},
        ),
    ]
    for name, url, headers, body in attempts:
        status, raw = _post(url, headers, body)
        if status != 200:
            print(f"[{name}] HTTP {status}: {raw[:300].decode(errors='replace')}")
            continue
        try:
            b64 = _extract_b64(json.loads(raw))
        except json.JSONDecodeError:
            print(f"[{name}] невалідний JSON у відповіді")
            continue
        if not b64:
            print(f"[{name}] у відповіді нема зображення (перші 300б): {raw[:300].decode(errors='replace')}")
            continue
        out.write_bytes(base64.b64decode(b64))
        print(f"OK [{name}] → {out} ({out.stat().st_size} байт)")
        return
    sys.exit("Не вдалося згенерувати жодним методом (див. помилки вище).")


_DEFAULT_PROMPT = (
    "Warm, hopeful vertical marketing poster, 4:5 aspect ratio. A friendly Ukrainian woman "
    "in her early 30s, authentic real-person look (not corporate stock), gentle confident smile, "
    "holding a smartphone showing a chat app, sitting by a bright window in a cozy modern apartment. "
    "Soft warm morning light, shallow depth of field, authentic editorial photography — NOT generic "
    "AI art, no purple gradients, no clutter. Subtle Ukrainian blue-and-yellow accent in the palette "
    "(scarf/mug/soft shapes), tasteful, not a flag. Clean composition with generous empty space at "
    "top and bottom for text. Crisp modern sans-serif Ukrainian text spelled EXACTLY: "
    "top headline «Склади іспит B1 — і залишся в Польщі впевнено»; "
    "subtitle «Особистий тренер польської в Telegram · 15 хв на день»; "
    "bottom rounded button «Почни безкоштовно → @polski_b1_Coach_bot». "
    "Trustworthy, warm, aspirational mood. Sharp legible text, professional social poster."
)

if __name__ == "__main__":
    out_path = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "poster.png")
    prompt = (
        pathlib.Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else _DEFAULT_PROMPT
    )
    generate(prompt, out_path)
