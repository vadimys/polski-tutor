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
HEAD = "Готуйся до іспиту B1"
SUB = (
    "Помічник для підготовки до державного іспиту B1: "
    "щодня потроху всі 5 частин, українською, "
    "з перевіркою письма й розмови."
)
INVITE = "Цікаво? Заходь і спробуй."
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


def _tg(img: Image.Image, cx: int, cy: int, r: int) -> None:
    """Офіційний логотип Telegram (прозорий webp) з центром у (cx, cy), діаметр 2r."""
    logo = Image.open(ROOT / "Telegram_logo.svg.webp").convert("RGBA").resize((r * 2, r * 2))
    img.paste(logo, (cx - r, cy - r), logo)


def _fit(text: str, hi: int, lo: int, maxw: int) -> ImageFont.FreeTypeFont:
    """Найбільший Arial Bold, за якого text вміщується в maxw."""
    for size in range(hi, lo - 1, -2):
        f = ImageFont.truetype(_BOLD, size)
        if f.getlength(text) <= maxw:
            return f
    return ImageFont.truetype(_BOLD, lo)


def _wrap(text: str, font: ImageFont.FreeTypeFont, maxw: int) -> list[str]:
    """Розбити текст на рядки, що вміщуються в maxw."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if font.getlength(t) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


import os

# Дефолт — веб-лінк t.me (працює і з застосунком, і без; після відновлення домену).
# Через env QR_URL можна перемкнути на app-лінк tg://resolve?domain=... (якщо t.me знову ляже).
BOT_URL = os.environ.get("QR_URL", "https://t.me/polski_b1_coach_bot")
_CREAM = (245, 240, 230)


def _make_qr(size: int) -> Image.Image:
    """Власний чистий QR на BOT_URL: темні модулі на кремовому + лого B1 у центрі.

    Генеруємо самі (не кроп зі стилізованої картки) → гарантовано сканується.
    Висока корекція помилок (H) дозволяє центральне лого без втрати читабельності.
    """
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H

    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=16, border=2)
    q.add_data(BOT_URL)
    q.make(fit=True)
    qr = q.make_image(fill_color=(26, 36, 52), back_color=_CREAM).convert("RGBA").resize((size, size))
    lg = int(size * 0.22)
    logo = Image.open(ROOT / "logo_b1_circle.png").convert("RGBA").resize((lg, lg))
    c = (size - lg) // 2
    r = lg // 2 + int(size * 0.025)
    ImageDraw.Draw(qr).ellipse([size // 2 - r, size // 2 - r, size // 2 + r, size // 2 + r], fill=_CREAM)
    qr.paste(logo, (c, c), logo)
    return qr


def build(bg: str = "bg_theme.jpg", out_name: str = "poster_final.jpg") -> None:
    img = _cover(Image.open(ROOT / bg).convert("RGB")).convert("RGBA")
    _scrim(img)
    d = ImageDraw.Draw(img)
    maxw = W - 2 * LM
    f_head = _fit(HEAD, 82, 44, maxw)  # автопідгін під один рядок
    lh = int(f_head.size * 1.12)
    f_sub = ImageFont.truetype(_REG, 34)
    f_cta = ImageFont.truetype(_BOLD, 33)
    f_handle = ImageFont.truetype(_BOLD, 38)

    # лого (верх-ліво) + Telegram-лого (верх-право)
    logo = Image.open(ROOT / "logo_b1_circle.png").convert("RGBA").resize((104, 104))
    img.paste(logo, (LM, 58), logo)
    _tg(img, W - LM - 46, 110, 46)

    # заголовок в один рядок
    y = 206
    d.text((LM, y), HEAD, font=f_head, fill=_WHITE)
    y += lh
    d.rounded_rectangle([LM, y + 6, LM + 150, y + 14], radius=4, fill=_RED)

    # людський абзац від першої особи (не реклама)
    y += 52
    for line in _wrap(SUB, f_sub, maxw):
        d.text((LM, y), line, font=f_sub, fill=(238, 242, 250))
        y += 46

    # запрошення + хендл
    y += 16
    d.text((LM, y), INVITE, font=f_cta, fill=_AMBER)
    y += 54
    d.text((LM, y), HANDLE, font=f_handle, fill=_WHITE)

    # QR на кремовій картці (завершує постер; тепле «Усім удачі!» — у тексті поста)
    qs = 440
    qr = _make_qr(qs)
    pad = 40
    cw2 = qs + pad * 2
    cx0 = (W - cw2) // 2
    cy0 = y + 60
    card_h = qs + pad * 2
    d.rounded_rectangle([cx0, cy0, cx0 + cw2, cy0 + card_h], radius=44, fill=_CREAM)
    img.alpha_composite(qr, ((W - qs) // 2, cy0 + pad))

    out = ROOT / out_name
    img.convert("RGB").save(out, quality=92)
    print(f"OK → {out} ({out.stat().st_size} байт, {W}x{H})")


if __name__ == "__main__":
    import sys

    bg = sys.argv[1] if len(sys.argv) > 1 else "bg_theme.jpg"
    out_name = sys.argv[2] if len(sys.argv) > 2 else "poster_final.jpg"
    build(bg, out_name)
