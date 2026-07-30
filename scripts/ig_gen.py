"""Генератор IG-контенту у фірмовому стилі (каруселі 1080×1350, сторіс/рілс-кадри 1080×1920).

Стиль: білий фон · польський червоний #DC143C · чорний текст · хуки Arial Black ·
польські слова JetBrains Mono Bold на червоних плашках (як <code> у боті) · лого B1.
Вивід: marketing/out/ (gitignored). Використання: python3 scripts/ig_gen.py
"""

from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "marketing" / "out"
OUT.mkdir(parents=True, exist_ok=True)

RED = (220, 20, 60)
DARK = (24, 24, 28)
GREY = (110, 110, 118)
WHITE = (255, 255, 255)
CREAM = (255, 250, 246)

_BLACK_F = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
_BOLD_F = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_REG_F = "/System/Library/Fonts/Supplemental/Arial.ttf"
_MONO_F = str(pathlib.Path.home() / "Library/Fonts/JetBrainsMono-ExtraBold.ttf")

W_POST, H_POST = 1080, 1350
W_ST, H_ST = 1080, 1920
M = 84  # поля


def f(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def _wrap(d: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, maxw: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = f"{cur} {w}".strip()
            if d.textlength(t, font=font) <= maxw:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def _text_block(d, xy, text, font, fill, maxw, lh=1.18) -> int:
    """Малює текст з переносами; повертає y-нижче блока."""
    x, y = xy
    for line in _wrap(d, text, font, maxw):
        d.text((x, y), line, font=font, fill=fill)
        y += int(font.size * lh)
    return y


def _chip(d, xy, text, font, pad=(38, 22), bg=RED, fg=WHITE, radius=26) -> tuple[int, int]:
    """Плашка з польським словом (як <code> у боті). Повертає (x_right, y_bottom)."""
    x, y = xy
    tw = d.textlength(text, font=font)
    th = font.size
    box = (x, y, x + tw + 2 * pad[0], y + th + 2 * pad[1])
    d.rounded_rectangle(box, radius=radius, fill=bg)
    d.text((x + pad[0], y + pad[1] - 4), text, font=font, fill=fg)
    return int(box[2]), int(box[3])


def _header(img: Image.Image, d: ImageDraw.ImageDraw, w: int) -> None:
    """Шапка: лого + хендл."""
    logo = Image.open(ROOT / "images" / "logo_b1_square.png").convert("RGBA").resize((92, 92))
    img.paste(logo, (M, 56), logo)
    d.text((M + 112, 74), "polski.b1.coach", font=f(_BOLD_F, 34), fill=GREY)


def _footer_dots(d, w, h, total, idx) -> None:
    """Прогрес-дотси каруселі."""
    cx = w // 2 - (total * 34) // 2
    for i in range(total):
        color = RED if i == idx else (225, 220, 218)
        d.ellipse((cx + i * 34, h - 64, cx + i * 34 + 16, h - 48), fill=color)


def _swipe(d, w, h, text="гортай →") -> None:
    d.text((w - M - d.textlength(text, font=f(_BOLD_F, 34)), h - 118), text,
           font=f(_BOLD_F, 34), fill=RED)


def slide(idx: int, total: int, kicker: str, title: str, body_fn, out: str,
          size=(W_POST, H_POST), swipe=True) -> None:
    """Каркас слайда: шапка → кікер → великий заголовок → тіло (body_fn) → футер."""
    w, h = size
    img = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, w, 12), fill=RED)  # тонка фірмова смуга зверху
    _header(img, d, w)
    y = 220
    if kicker:
        d.text((M, y), kicker.upper(), font=f(_BOLD_F, 36), fill=RED)
        y += 72
    y = _text_block(d, (M, y), title, f(_BLACK_F, 84), DARK, w - 2 * M, lh=1.1) + 30
    body_fn(img, d, y, w)
    _footer_dots(d, w, h, total, idx)
    if swipe and idx < total - 1:
        _swipe(d, w, h)
    img.save(OUT / out)
    print("OK", out)


# ───────────────────────── ПІЛОТ: карусель-квіз «szukam pracy» ─────────────────────────
def build_carousel_szukac() -> None:
    T = 4

    def s1(img, d, y, w):  # питання-квіз
        y += 26
        d.text((M, y), "Як правильно?", font=f(_BOLD_F, 44), fill=GREY)
        y += 96
        _chip(d, (M, y), "A)  Szukam pracę", f(_MONO_F, 52), bg=(245, 240, 238), fg=DARK)
        y += 140
        _chip(d, (M, y), "B)  Szukam pracy", f(_MONO_F, 52), bg=(245, 240, 238), fg=DARK)
        y += 190
        d.text((M, y), "Відповідь — на наступному слайді  →", font=f(_REG_F, 40), fill=GREY)

    slide(0, T, "міні-квіз · граматика", "Це слово\nзавалює іспит", s1, "car1_s1.png")

    def s2(img, d, y, w):
        y += 10
        _chip(d, (M, y), "✓  Szukam pracy", f(_MONO_F, 56))
        y += 170
        y = _text_block(d, (M, y), "szukać завжди йде з Dopełniacz\n(кого? чого?)",
                        f(_BOLD_F, 48), DARK, w - 2 * M) + 40
        y = _text_block(d, (M, y),
                        "Каже «szukam pracę» — і поляк одразу чує іноземця. "
                        "А на іспиті це мінус бали в граматиці й письмі.",
                        f(_REG_F, 42), GREY, w - 2 * M)

    slide(1, T, "відповідь", "PracY.\nНе pracę!", s2, "car1_s2.png")

    def s3(img, d, y, w):
        pairs = [
            ("słuchać muzyki", "слухати музику"),
            ("uczyć się polskiego", "вчити польську"),
            ("bać się egzaminu", "боятися іспиту"),
            ("potrzebować pomocy", "потребувати допомоги"),
        ]
        for pl, uk in pairs:
            _chip(d, (M, y), pl, f(_MONO_F, 44), pad=(34, 18))
            y += 104
            d.text((M + 6, y), uk, font=f(_REG_F, 36), fill=GREY)
            y += 76

    slide(2, T, "запамʼятай", "Ці 4 теж\nз Dopełniacz", s3, "car1_s3.png")

    def s4(img, d, y, w):
        y += 6
        y = _text_block(d, (M, y),
                        "У нашому Telegram-боті є тренажер rekcji: він питає такі пастки, "
                        "запамʼятовує твої помилки і повторює їх, доки не закріпиш.",
                        f(_REG_F, 44), DARK, w - 2 * M, lh=1.3) + 44
        y = _text_block(d, (M, y), "Тренуєшся на РЕАЛЬНИХ минулих іспитах. 15 хв на день.",
                        f(_BOLD_F, 44), DARK, w - 2 * M, lh=1.25) + 60
        _chip(d, (M, y), "→ лінк у шапці профілю", f(_BOLD_F, 46))

    slide(3, T, "тренуйся", "Скласти B1\nз першого разу", s4, "car1_s4.png", swipe=False)




# ───────────────────────── РІЛС: кадри 1080×1920 (безпечні зони: верх 250, низ 420) ─────
def _reel_frame(out: str, kicker: str, lines: list[tuple[str, str]], footer: str = "") -> None:
    """Кадр рілса: по центру вертикалі. lines: [(тип, текст)] тип: hook/big/chip/dim/gap."""
    img = Image.new("RGB", (W_ST, H_ST), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W_ST, 14), fill=RED)
    logo = Image.open(ROOT / "images" / "logo_b1_square.png").convert("RGBA").resize((84, 84))
    img.paste(logo, (M, 300), logo)
    d.text((M + 104, 318), "polski.b1.coach", font=f(_BOLD_F, 32), fill=GREY)
    y = 560
    if kicker:
        d.text((M, y), kicker.upper(), font=f(_BOLD_F, 40), fill=RED)
        y += 92
    for kind, text in lines:
        if kind == "hook":
            y = _text_block(d, (M, y), text, f(_BLACK_F, 104), DARK, W_ST - 2 * M, lh=1.08) + 36
        elif kind == "big":
            y = _text_block(d, (M, y), text, f(_BOLD_F, 56), DARK, W_ST - 2 * M, lh=1.22) + 30
        elif kind == "chip":
            _, y2 = _chip(d, (M, y), text, f(_MONO_F, 60), pad=(44, 28))
            y = y2 + 44
        elif kind == "chip_dim":
            _, y2 = _chip(d, (M, y), text, f(_MONO_F, 56), pad=(40, 24),
                          bg=(245, 240, 238), fg=DARK)
            y = y2 + 36
        elif kind == "dim":
            y = _text_block(d, (M, y), text, f(_REG_F, 44), GREY, W_ST - 2 * M, lh=1.25) + 28
        elif kind == "gap":
            y += int(text)
    if footer:
        d.text((M, H_ST - 500), footer, font=f(_BOLD_F, 40), fill=RED)
    img.save(OUT / out)
    print("OK", out)


def build_reel1_frames() -> None:
    _reel_frame("reel1_f1.png", "", [
        ("hook", "Це слово\nзавалює\nіспит B1"),
        ("gap", "40"),
        ("dim", "перевір себе за 10 секунд"),
    ])
    _reel_frame("reel1_f2.png", "як сказати «шукаю роботу»?", [
        ("gap", "20"),
        ("chip_dim", "A)  Szukam pracę"),
        ("gap", "20"),
        ("chip_dim", "B)  Szukam pracy"),
    ])
    _reel_frame("reel1_f3.png", "правильно", [
        ("chip", "Szukam pracy"),
        ("big", "szukać завжди тягне Dopełniacz (кого? чого?)"),
        ("dim", "«szukam pracę» — і поляк одразу чує іноземця"),
    ])
    _reel_frame("reel1_f4.png", "так само", [
        ("chip", "słuchać muzyki"),
        ("dim", "слухати музику — теж Dopełniacz"),
    ])
    _reel_frame("reel1_f5.png", "і ще", [
        ("chip", "bać się egzaminu"),
        ("dim", "боятися іспиту — і знову Dopełniacz"),
    ])
    _reel_frame("reel1_f6.png", "тренуйся", [
        ("hook", "Такі пастки\nпитає наш\nтренажер"),
        ("gap", "30"),
        ("big", "у Telegram, на реальних минулих іспитах"),
        ("gap", "10"),
        ("chip", "→ лінк у шапці"),
    ])




def build_story_quiz1() -> None:
    """Сторіс-квіз: питання зверху, порожня зона по центру-низу під нативний стікер IG."""
    img = Image.new("RGB", (W_ST, H_ST), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W_ST, 14), fill=RED)
    logo = Image.open(ROOT / "images" / "logo_b1_square.png").convert("RGBA").resize((84, 84))
    img.paste(logo, (M, 220), logo)
    d.text((M + 104, 238), "polski.b1.coach", font=f(_BOLD_F, 32), fill=GREY)
    y = 420
    d.text((M, y), "ЩОДЕННИЙ КВІЗ", font=f(_BOLD_F, 40), fill=RED)
    y += 100
    y = _text_block(d, (M, y), "Жінка каже:\n«я вчора була вдома»", f(_BLACK_F, 88), DARK,
                    W_ST - 2 * M, lh=1.1) + 50
    _chip(d, (M, y), "A)  byłem w domu", f(_MONO_F, 54), pad=(40, 24),
          bg=(245, 240, 238), fg=DARK)
    y += 130
    _chip(d, (M, y), "B)  byłam w domu", f(_MONO_F, 54), pad=(40, 24),
          bg=(245, 240, 238), fg=DARK)
    y += 170
    _text_block(d, (M, y), "голосуй стікером нижче ↓\nвідповідь — у наступній сторіс",
                f(_REG_F, 38), GREY, W_ST - 2 * M, lh=1.4)
    img.save(OUT / "story_quiz1.png")
    print("OK story_quiz1.png")


if __name__ == "__main__":
    build_carousel_szukac()
    build_reel1_frames()
    build_story_quiz1()
