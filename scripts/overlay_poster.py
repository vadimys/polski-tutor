#!/usr/bin/env python3
"""Постер = ЦІЛІСНА офіційна QR-картка бота + простий нейтральний текст.

Ніяких колажів: беремо готову брендовану картку (t_me-...jpg — зелений фон,
лого B1, QR з літачком, @хендл) і додаємо лише короткий нейтральний текст у
порожні зони зверху й знизу. Кирилиця — Pillow+Arial. → poster_final.jpg.
"""

from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
_GREEN = (36, 82, 52)  # темно-зелений у тон QR

HEAD = "Польська до іспиту B1"
SUB = "Безкоштовний бот у Telegram · пояснення українською"


def _center(d, y, text, font, fill):
    b = d.textbbox((0, 0), text, font=font)
    d.text(((d._image.size[0] - (b[2] - b[0])) / 2, y), text, font=font, fill=fill)


def build() -> None:
    img = Image.open(ROOT / "t_me-polski_b1_Coach_bot.jpg").convert("RGB")
    W, H = img.size
    d = ImageDraw.Draw(img)
    f_head = ImageFont.truetype(_BOLD, int(W * 0.072))
    f_sub = ImageFont.truetype(_REG, int(W * 0.037))

    _center(d, int(H * 0.115), HEAD, f_head, _GREEN)
    _center(d, int(H * 0.80), SUB, f_sub, _GREEN)

    out = ROOT / "poster_final.jpg"
    img.save(out, quality=92)
    print(f"OK → {out} ({out.stat().st_size} байт, {W}x{H})")


if __name__ == "__main__":
    build()
