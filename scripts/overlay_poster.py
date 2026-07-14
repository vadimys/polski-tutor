#!/usr/bin/env python3
"""Рекламний пост (ad-creative): тематичний фон + хук → вигоди → CTA + QR.

Фон — згенерований силует Кракова на заході (bg_theme.jpg, без тексту).
Поверх — темний скрим для читабельності, лого B1, заголовок-хук, 3 конкретні
вигоди, заклик вчитися й біла картка з вирізаним QR + Telegram-бейджем.
Копірайт за copywriting/marketing-psychology (мрія жити в Польщі + вигоди + CTA).
Кирилиця — Pillow+Arial. FB-портрет 1080x1350. → poster_final.jpg.
"""

from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
_WHITE = (255, 255, 255)
_AMBER = (247, 197, 122)
_RED = (233, 63, 78)
_GREEN = (46, 107, 62)
_TG = (41, 169, 234)
_INK = (24, 30, 44)

W, H = 1080, 1350
LM = 90
KICKER = "ДЕРЖАВНИЙ ІСПИТ З ПОЛЬСЬКОЇ · РІВЕНЬ B1"
HEAD = ["Склади іспит B1", "і залишся в Польщі"]
BENEFITS = [
    "Усі 5 частин іспиту — щодня по 15 хвилин",
    "Пояснення українською, від самого нуля",
    "Перевірка письма й розмови з AI-тренером",
]
CTA = "Скануй QR і почни вчитися — безкоштовно"
HANDLE = "@polski_b1_coach_bot"


def _cover(im: Image.Image) -> Image.Image:
    iw, ih = im.size
    s = max(W / iw, H / ih)
    im = im.resize((int(iw * s), int(ih * s)))
    x = (im.size[0] - W) // 2
    y = (im.size[1] - H) // 2
    return im.crop((x, y, x + W, y + H))


def _scrim(img: Image.Image) -> None:
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = ov.load()
    for y in range(H):
        t = y / H
        a = int(205 - 165 * t) if t < 0.62 else int(105 - 90 * (t - 0.62) / 0.38)
        for x in range(W):
            px[x, y] = (12, 20, 38, max(a, 0))
    img.alpha_composite(ov)


def _plane(d, cx, cy, r) -> None:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=_TG)
    pts = [(-0.62, -0.02), (0.64, -0.46), (0.18, 0.52), (-0.02, 0.10)]
    d.polygon([(cx + x * r, cy + y * r) for x, y in pts], fill=_WHITE)
    d.polygon([(cx + 0.18 * r, cy + 0.52 * r), (cx + 0.30 * r, cy + 0.06 * r),
               (cx - 0.02 * r, cy + 0.10 * r)], fill=(210, 233, 246))


def _check(d, x, y, s) -> None:
    d.line([(x, y + s * 0.55), (x + s * 0.38, y + s * 0.9), (x + s, y)], fill=_AMBER, width=6, joint="curve")


def _extract_qr() -> Image.Image:
    card = Image.open(ROOT / "t_me-polski_b1_Coach_bot.jpg").convert("RGB")
    cw, ch = card.size
    return card.crop((int(cw * 0.15), int(ch * 0.345), int(cw * 0.85), int(ch * 0.63)))


def build() -> None:
    img = _cover(Image.open(ROOT / "bg_theme.jpg").convert("RGB")).convert("RGBA")
    _scrim(img)
    d = ImageDraw.Draw(img)
    f_kick = ImageFont.truetype(_BOLD, 27)
    f_head = ImageFont.truetype(_BOLD, 66)
    f_ben = ImageFont.truetype(_REG, 33)
    f_cta = ImageFont.truetype(_BOLD, 34)
    f_handle = ImageFont.truetype(_BOLD, 37)

    # лого (верх-ліво) + Telegram-бейдж (верх-право)
    logo = Image.open(ROOT / "logo_b1_circle.png").convert("RGBA").resize((104, 104))
    img.paste(logo, (LM, 58), logo)
    _plane(d, W - LM - 42, 110, 42)

    # кикер (letter-spaced) + заголовок-хук
    d.text((LM, 210), " ".join(KICKER), font=f_kick, fill=_AMBER)
    y = 258
    for line in HEAD:
        d.text((LM, y), line, font=f_head, fill=_WHITE)
        y += 78
    d.rounded_rectangle([LM, y + 6, LM + 150, y + 14], radius=4, fill=_RED)

    # вигоди (з галочками)
    y += 66
    for b in BENEFITS:
        _check(d, LM + 4, y + 6, 26)
        d.text((LM + 52, y), b, font=f_ben, fill=(238, 242, 250))
        y += 58

    # CTA
    y += 24
    d.text((LM, y), CTA, font=f_cta, fill=_AMBER)

    # біла картка з QR (центр, низ)
    cw2 = 520
    cx0 = (W - cw2) // 2
    cy0 = 792
    qr = _extract_qr()
    qs = 400
    qr = qr.resize((qs, int(qr.size[1] * qs / qr.size[0])))
    card_h = 44 + qr.size[1] + 92
    d.rounded_rectangle([cx0, cy0, cx0 + cw2, cy0 + card_h], radius=40, fill=_WHITE)
    img.paste(qr, ((W - qs) // 2, cy0 + 44))

    # Telegram-бейдж + хендл усередині картки
    hb = d.textbbox((0, 0), HANDLE, font=f_handle)
    hw = hb[2] - hb[0]
    br, gap = 24, 16
    total = br * 2 + gap + hw
    gx = (W - total) // 2
    by = cy0 + card_h - 48
    _plane(d, gx + br, by, br)
    d.text((gx + br * 2 + gap, by - (hb[3] - hb[1]) // 2 - hb[1]), HANDLE, font=f_handle, fill=_GREEN)

    out = ROOT / "poster_final.jpg"
    img.convert("RGB").save(out, quality=92)
    print(f"OK → {out} ({out.stat().st_size} байт, {W}x{H})")


if __name__ == "__main__":
    build()
