#!/usr/bin/env python3
"""Накласти коректний український текст на textless-постер (Pillow + Arial Cyrillic).

Напівпрозорі кремові панелі під заголовком/підзаголовком + суцільна CTA-пігулка →
гарантована читабельність поверх фото. Вхід: poster_clean.jpg → вихід: poster_final.jpg.
"""

from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
_NAVY = (18, 42, 66)
_WHITE = (255, 255, 255)
_PANEL = (250, 247, 240, 205)  # кремова напівпрозора підкладка

HEAD = "Склади іспит B1 —\nі залишся в Польщі\nвпевнено"
SUB = "Особистий тренер польської\nв Telegram · 15 хв на день\n· пояснення українською"
CTA = "Почни безкоштовно  →  @polski_b1_Coach_bot"


def _wrap_panel(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font, pad: int) -> tuple[int, int]:
    x, y = xy
    bbox = draw.multiline_textbbox((x + pad, y + pad), text, font=font, spacing=pad // 2)
    return bbox[2] + pad, bbox[3] + pad


def build(src: pathlib.Path, out: pathlib.Path) -> None:
    img = Image.open(src).convert("RGB")
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    m = int(W * 0.055)  # поле
    f_head = ImageFont.truetype(_BOLD, int(W * 0.072))
    f_sub = ImageFont.truetype(_REG, int(W * 0.037))
    f_cta = ImageFont.truetype(_BOLD, int(W * 0.036))
    pad = int(W * 0.03)

    # заголовок (верх, кремова панель)
    hb = d.multiline_textbbox((m + pad, int(H * 0.045) + pad), HEAD, font=f_head, spacing=pad // 2)
    d.rounded_rectangle(
        [m - pad // 2, int(H * 0.045) - pad // 2, hb[2] + pad, hb[3] + pad],
        radius=pad, fill=_PANEL,
    )
    d.multiline_text((m + pad, int(H * 0.045) + pad), HEAD, font=f_head, fill=_NAVY, spacing=pad // 2)
    # жовтий акцент-риска під заголовком
    d.rounded_rectangle([m, hb[3] + pad + 8, m + int(W * 0.22), hb[3] + pad + 8 + int(H * 0.006)],
                        radius=6, fill=(244, 180, 0))

    # підзаголовок (ліва колонка, нижче)
    sy = int(H * 0.60)
    sb = d.multiline_textbbox((m + pad, sy + pad), SUB, font=f_sub, spacing=pad // 3)
    d.rounded_rectangle([m - pad // 2, sy - pad // 2, sb[2] + pad, sb[3] + pad], radius=pad, fill=_PANEL)
    d.multiline_text((m + pad, sy + pad), SUB, font=f_sub, fill=_NAVY, spacing=pad // 3)

    # CTA-пігулка (низ)
    cb = d.textbbox((0, 0), CTA, font=f_cta)
    cw, ch = cb[2] - cb[0], cb[3] - cb[1]
    px, py = int(W * 0.05), int(W * 0.028)
    cx, cyy = m, int(H * 0.88)
    d.rounded_rectangle([cx, cyy, cx + cw + px * 2, cyy + ch + py * 2], radius=(ch + py * 2) // 2, fill=_NAVY)
    d.text((cx + px, cyy + py - cb[1]), CTA, font=f_cta, fill=_WHITE)

    Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB").save(out, quality=92)
    print(f"OK → {out} ({out.stat().st_size} байт, {W}x{H})")


if __name__ == "__main__":
    build(ROOT / "poster_clean.jpg", ROOT / "poster_final.jpg")
