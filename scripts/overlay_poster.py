#!/usr/bin/env python3
"""Окремий креативний пост: власний дизайн + лого B1 + вирізаний QR + мін. текст.

QR вирізаємо з офіційної картки (t_me-...jpg), лого беремо локально (logo_b1_circle.png).
Власний преміум-фон (темно-синій градієнт), біла картка з QR, Telegram-бейдж біля
хендла. Кирилиця — Pillow+Arial. FB-портрет 1080x1350. → poster_final.jpg.
"""

from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
_NAVY_TOP = (26, 42, 68)
_NAVY_BOT = (14, 24, 42)
_WHITE = (255, 255, 255)
_RED = (225, 6, 44)
_GREEN = (46, 107, 62)
_MUTE = (176, 190, 214)
_TG = (41, 169, 234)

W, H = 1080, 1350
HEAD = "Польська до іспиту B1"
SUB = "Безкоштовний бот у Telegram · пояснення українською"
HANDLE = "@polski_b1_coach_bot"


def _grad() -> Image.Image:
    base = Image.new("RGB", (W, H))
    px = base.load()
    for y in range(H):
        t = y / H
        px_row = tuple(int(_NAVY_TOP[i] + (_NAVY_BOT[i] - _NAVY_TOP[i]) * t) for i in range(3))
        for x in range(W):
            px[x, y] = px_row
    return base


def _plane(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=_TG)
    pts = [(-0.62, -0.02), (0.64, -0.46), (0.18, 0.52), (-0.02, 0.10)]
    d.polygon([(cx + x * r, cy + y * r) for x, y in pts], fill=_WHITE)
    d.polygon([(cx + 0.18 * r, cy + 0.52 * r), (cx + 0.30 * r, cy + 0.06 * r),
               (cx - 0.02 * r, cy + 0.10 * r)], fill=(210, 233, 246))


def _center(d, y, text, font, fill) -> int:
    b = d.textbbox((0, 0), text, font=font)
    d.text(((W - (b[2] - b[0])) / 2, y), text, font=font, fill=fill)
    return b[3] - b[1]


def _extract_qr() -> Image.Image:
    card = Image.open(ROOT / "t_me-polski_b1_Coach_bot.jpg").convert("RGB")
    cw, ch = card.size
    return card.crop((int(cw * 0.15), int(ch * 0.345), int(cw * 0.85), int(ch * 0.63)))


def build() -> None:
    img = _grad()
    d = ImageDraw.Draw(img)
    f_head = ImageFont.truetype(_BOLD, 58)
    f_sub = ImageFont.truetype(_REG, 30)
    f_handle = ImageFont.truetype(_BOLD, 40)

    # лого B1 (верх-центр)
    logo = Image.open(ROOT / "logo_b1_circle.png").convert("RGBA")
    ls = 200
    logo = logo.resize((ls, ls))
    img.paste(logo, ((W - ls) // 2, 90), logo)

    # заголовок + червоний акцент
    _center(d, 340, HEAD, f_head, _WHITE)
    d.rounded_rectangle([(W - 150) // 2, 430, (W + 150) // 2, 438], radius=4, fill=_RED)

    # біла картка з QR
    cx0, cy0, cx1, cy1 = 230, 500, 850, 1180
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=44, fill=_WHITE)
    qr = _extract_qr()
    qs = 500
    qr = qr.resize((qs, int(qr.size[1] * qs / qr.size[0])))
    qx = (W - qs) // 2
    img.paste(qr, (qx, cy0 + 44))

    # Telegram-бейдж + хендл (центрований блок унизу картки)
    hb = d.textbbox((0, 0), HANDLE, font=f_handle)
    hw = hb[2] - hb[0]
    br = 26
    gap = 18
    total = br * 2 + gap + hw
    gx = (W - total) // 2
    _plane(d, gx + br, cy1 - 66, br)
    d.text((gx + br * 2 + gap, cy1 - 66 - (hb[3] - hb[1]) // 2 - hb[1]), HANDLE, font=f_handle, fill=_GREEN)

    # нижній нейтральний підпис
    _center(d, 1250, SUB, f_sub, _MUTE)

    out = ROOT / "poster_final.jpg"
    img.save(out, quality=92)
    print(f"OK → {out} ({out.stat().st_size} байт, {W}x{H})")


if __name__ == "__main__":
    build()
