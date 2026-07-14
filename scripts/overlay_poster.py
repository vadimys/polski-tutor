#!/usr/bin/env python3
"""Скласти постер: тепле фото + лого B1 + Telegram-бейдж + QR-картка + людяний текст.

Текст переписано за stop-slop (жива мова, «ти», без тире й тріад). Кирилиця —
Pillow+Arial (моделі її ламають). QR-картку кропимо з офіційного t.me-шеру бота.
Вхід: poster_clean.jpg + logo_b1_circle.png + t_me-polski_b1_Coach_bot.jpg → poster_final.jpg.
"""

from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
_NAVY = (23, 33, 48)
_TG = (41, 169, 234)  # telegram blue
_PANEL = (250, 247, 240, 216)

# людяний текст (stop-slop: жива мова, «ти», конкретика, без тире/тріад)
KICKER = "Polski B1 · бот у Telegram"
HEAD = "Готуєшся\nдо іспиту B1?"
SUB = ("Безкоштовний помічник у Telegram.\n"
       "Щодня по 15 хвилин, пояснення\nукраїнською. Спробуй сьогодні.")
QR_CAP = "Наведи камеру й почни  ↓"


def _plane(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    """Telegram-бейдж: синє коло + білий паперовий літачок."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=_TG)
    pts = [(-0.62, -0.02), (0.64, -0.46), (0.18, 0.52), (-0.02, 0.10)]
    d.polygon([(cx + x * r, cy + y * r) for x, y in pts], fill=(255, 255, 255))
    d.polygon([(cx + 0.18 * r, cy + 0.52 * r), (cx + 0.30 * r, cy + 0.06 * r),
               (cx - 0.02 * r, cy + 0.10 * r)], fill=(210, 233, 246))


def _panel(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], pad: int) -> None:
    d.rounded_rectangle([box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad],
                        radius=pad, fill=_PANEL)


def build() -> None:
    img = Image.open(ROOT / "poster_clean.jpg").convert("RGBA")
    W, H = img.size
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    m = int(W * 0.05)
    pad = int(W * 0.028)
    f_head = ImageFont.truetype(_BOLD, int(W * 0.078))
    f_sub = ImageFont.truetype(_REG, int(W * 0.033))
    f_kick = ImageFont.truetype(_BOLD, int(W * 0.028))
    f_cap = ImageFont.truetype(_BOLD, int(W * 0.030))

    # лого B1 (верх-ліво)
    logo = Image.open(ROOT / "logo_b1_circle.png").convert("RGBA")
    ls = int(W * 0.135)
    logo = logo.resize((ls, ls))
    img.alpha_composite(logo, (m, m))

    # кикер + Telegram-бейдж (праворуч від лого)
    kx = m + ls + int(W * 0.02)
    _plane(d, kx + int(W * 0.028), m + ls // 2 - int(W * 0.01), int(W * 0.028))
    d.text((kx + int(W * 0.075), m + ls // 2 - int(W * 0.02)), KICKER, font=f_kick, fill=_NAVY)

    # заголовок (панель, ліва частина)
    hy = int(H * 0.20)
    hb = d.multiline_textbbox((m + pad, hy + pad), HEAD, font=f_head, spacing=pad // 2)
    _panel(d, (m, hy, hb[2], hb[3]), pad)
    d.multiline_text((m + pad, hy + pad), HEAD, font=f_head, fill=_NAVY, spacing=pad // 2)
    d.rounded_rectangle([m + pad, hb[3] + pad + 6, m + pad + int(W * 0.20), hb[3] + pad + 6 + int(H * 0.006)],
                        radius=6, fill=(225, 6, 44))  # червоний акцент (як у лого)

    # підзаголовок (ліва колонка)
    sy = int(H * 0.44)
    sb = d.multiline_textbbox((m + pad, sy + pad), SUB, font=f_sub, spacing=pad // 3)
    _panel(d, (m, sy, sb[2], sb[3]), pad)
    d.multiline_text((m + pad, sy + pad), SUB, font=f_sub, fill=_NAVY, spacing=pad // 3)

    # QR-картка (кроп із офіційного t.me-шеру) — низ-ліво
    qr = Image.open(ROOT / "t_me-polski_b1_Coach_bot.jpg").convert("RGBA")
    qw, qh = qr.size
    qr = qr.crop((int(qw * 0.11), int(qh * 0.22), int(qw * 0.89), int(qh * 0.66)))
    tw = int(W * 0.40)
    qr = qr.resize((tw, int(qr.size[1] * tw / qr.size[0])))
    qx, qy = m, H - qr.size[1] - m
    img.alpha_composite(qr, (qx, qy))
    # підпис над QR
    cb = d.textbbox((0, 0), QR_CAP, font=f_cap)
    d.text((qx, qy - int(H * 0.045)), QR_CAP, font=f_cap, fill=_NAVY)

    out = ROOT / "poster_final.jpg"
    Image.alpha_composite(img, ov).convert("RGB").save(out, quality=92)
    print(f"OK → {out} ({out.stat().st_size} байт, {W}x{H})")


if __name__ == "__main__":
    build()
