"""Квест-мапа «Похід до B1 · 5 грудня» — наратив-подорож із станціями-модулями.

Позиція = готовність по 5 модулях; ціль кожної станції — 70% (READY_THRESHOLD).
Фінальний «бос» — повний мок, відкривається, коли всі модулі ≥50%. Чиста функція
рендеру (легко тестувати), стан не тримаємо — рахуємо з readiness/дат/рівня.
"""

from __future__ import annotations

from app.bot.ui import bar
from app.domain.models import MODULE_LABELS, Module
from app.services.progress import READY_THRESHOLD

PASS = 50  # поріг складання модуля на іспиті


def overall_pct(readiness: dict[str, int]) -> int:
    """Скільки % шляху до «готовий» пройдено (середня готовність / поріг готовності)."""
    avg = sum(readiness.get(m.value, 0) for m in Module) / len(Module)
    return min(100, round(avg / READY_THRESHOLD * 100))


def _path(pct: int) -> str:
    """Горизонтальна стежка з маркером позиції: 🏁▰▰🚶▱▱🏆."""
    slots = 10
    pos = min(slots - 1, pct * slots // 100)
    cells = ["▰" if i < pos else "▱" for i in range(slots)]
    cells[pos] = "🚶"
    return "🏁" + "".join(cells) + "🏆"


def render(readiness: dict[str, int], days_left: int | None, level: int, streak: int) -> str:
    pct = overall_pct(readiness)
    head = ["🗺 <b>Похід до B1</b>"]
    if days_left is not None:
        head.append(f"До іспиту: <b>{days_left}</b> днів · пройдено <b>{pct}%</b> шляху")
    else:
        head.append(f"Пройдено <b>{pct}%</b> шляху до готовності")
    head.append(_path(pct))

    # станції — модулі, від найсильнішого до найслабшого; найслабший = «ти тут»
    mods = sorted(Module, key=lambda m: readiness.get(m.value, 0), reverse=True)
    weakest = min(Module, key=lambda m: readiness.get(m.value, 0))
    lines = ["", "<b>Станції:</b>"]
    for m in mods:
        v = readiness.get(m.value, 0)
        icon = "✅" if v >= READY_THRESHOLD else ("🚶" if m is weakest else ("🔓" if v > 0 else "🔒"))
        here = " ← <b>ти тут</b>" if m is weakest and v < READY_THRESHOLD else ""
        lines.append(f"{icon} {MODULE_LABELS[m]} {bar(v)}{here}")

    all_pass = all(readiness.get(m.value, 0) >= PASS for m in Module)
    boss = (
        "🏆 <b>Бос: повний мок</b> — усі модулі ≥50%, час на генеральну репетицію! (/mok)"
        if all_pass
        else "🔒 <b>Бос: повний мок</b> — відкриється, коли ВСІ модулі досягнуть 50%"
    )
    tail = [f"\n{boss}", f"\n⭐ Рівень <b>{level}</b> · 🔥 <b>{streak}</b> дн поспіль"]
    if pct >= 100:
        tail.append("\n🎉 <b>Ти пройшов увесь шлях — схоже, готовий до B1!</b>")
    return "\n".join(head + lines + tail)
