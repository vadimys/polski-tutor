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
HEAD = ["Склади іспит B1 легко", "з Телеграм-ботом"]
BENEFITS = [
    "Усі 5 частин іспиту, щодня по 15 хвилин",
    "Пояснення українською, від самого нуля",
    "Перевірка письма й розмови з AI-тренером",
]
CTA1 = "Скануй QR-код або знайди бот у Telegram:"
HANDLE = "@polski_b1_coach_bot"
CTA2 = "  і почни вчитися безкоштовно"


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


def _check(d, x, y, s) -> None:
    d.line([(x, y + s * 0.55), (x + s * 0.38, y + s * 0.9), (x + s, y)], fill=_AMBER, width=6, joint="curve")


BOT_URL = "https://t.me/polski_b1_coach_bot"
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
    f_kick = ImageFont.truetype(_BOLD, 27)
    f_head = _fit(max(HEAD, key=len), 92, 60, maxw)
    lh = int(f_head.size * 1.12)
    f_ben = ImageFont.truetype(_REG, 33)
    f_cta = ImageFont.truetype(_BOLD, 34)
    f_handle = ImageFont.truetype(_BOLD, 37)

    # лого (верх-ліво) + Telegram-лого (верх-право)
    logo = Image.open(ROOT / "logo_b1_circle.png").convert("RGBA").resize((104, 104))
    img.paste(logo, (LM, 58), logo)
    _tg(img, W - LM - 46, 110, 46)

    # кикер (letter-spaced) + великий заголовок-хук
    d.text((LM, 196), " ".join(KICKER), font=f_kick, fill=_AMBER)
    y = 244
    for line in HEAD:
        d.text((LM, y), line, font=f_head, fill=_WHITE)
        y += lh
    d.rounded_rectangle([LM, y + 6, LM + 150, y + 14], radius=4, fill=_RED)

    # вигоди (з галочками)
    y += 66
    for b in BENEFITS:
        _check(d, LM + 4, y + 6, 26)
        d.text((LM + 52, y), b, font=f_ben, fill=(238, 242, 250))
        y += 58

    # CTA у два рядки: два способи почати + безкоштовно; хендл підсвічено білим
    y += 26
    d.text((LM, y), CTA1, font=f_cta, fill=_AMBER)
    y += 48
    d.text((LM, y), HANDLE, font=f_handle, fill=_WHITE)
    d.text((LM + f_handle.getlength(HANDLE), y + 2), CTA2, font=f_cta, fill=_AMBER)

    # власний QR на кремовій картці (світле тло + темні модулі = гарантований скан)
    qs = 440
    qr = _make_qr(qs)
    pad = 40
    cw2 = qs + pad * 2
    cx0 = (W - cw2) // 2
    cy0 = y + 70
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
