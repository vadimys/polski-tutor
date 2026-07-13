"""Індивідуальний план підготовки: зворотний графік від дати іспиту або вільний.

Детермінований (без вигадок): спирається на реальну дату іспиту, готовність по
модулях (з тесту/вправ) і правило іспиту ≥50% у кожному модулі. Акцент — на
найслабші модулі. Генерується на вимогу (завжди актуальний), не зберігається.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from app.domain.models import MODULE_LABELS, Module

# Тай-брейк за складністю/важливістю (продуктивні модулі — раніше)
_PRIORITY = [Module.PISANIE, Module.MOWIENIE, Module.SLUCHANIE, Module.GRAMATYKA, Module.CZYTANIE]

DAILY_MIN = 60
WEEKLY_MIN = DAILY_MIN * 7


@dataclass
class Phase:
    title: str
    span: str  # напр. «тижні 1–4»
    focus: str


@dataclass
class StudyPlan:
    has_date: bool
    days_left: int | None
    weeks_left: int | None
    weak: list[Module]  # найслабші спершу
    daily_min: int = 60  # денна ціль учня (з /cel) — план ділить час пропорційно
    phases: list[Phase] = field(default_factory=list)
    readiness: dict[str, int] = field(default_factory=dict)  # для віх-чекпойнтів


def weak_order(readiness: dict[str, int]) -> list[Module]:
    """Модулі від найслабшого; невиміряні (0) — попереду; тай-брейк за пріоритетом."""
    return sorted(Module, key=lambda m: (readiness.get(m.value, 0), _PRIORITY.index(m)))


def _phases_with_date(weeks: int, top2: list[str]) -> list[Phase]:
    acc = ", ".join(top2)
    taper = 1 if weeks >= 3 else 0
    core = weeks - taper
    foundation = max(1, round(core * 0.3)) if weeks >= 8 else (1 if weeks >= 4 else 0)
    mocks = max(1, round(core * 0.25)) if weeks >= 4 else 0
    intensive = max(1, core - foundation - mocks)

    phases: list[Phase] = []
    w = 1

    def span(n: int) -> str:
        nonlocal w
        s = f"тиждень {w}" if n == 1 else f"тижні {w}–{w + n - 1}"
        w += n
        return s

    if foundation:
        phases.append(Phase("🧱 Фундамент", span(foundation),
                            "базова граматика (відмінки, часи, аспект) + висока лексика, "
                            "щоденна звичка, читання/аудіо A2→B1"))
    phases.append(Phase("🎯 Відпрацювання модулів", span(intensive),
                        f"усі 5 модулів у форматі іспиту, БІЛЬШЕ на найслабші: {acc}. "
                        "Письмо (/pisanie) і мовлення (/mowienie) регулярно"))
    if mocks:
        phases.append(Phase("📋 Повні моки", span(mocks),
                            "офіційні моки (/mok) у режимі іспиту, аналіз помилок, "
                            f"добиваємо {acc} до впевнених ≥60%"))
    if taper:
        phases.append(Phase("🌱 Тейпер", span(taper),
                            "легке повторення, 1 контрольний мок, без перевантаження, "
                            "логістика дня іспиту"))
    return phases


def _phases_free(top2: list[str]) -> list[Phase]:
    acc = ", ".join(top2)
    return [
        Phase("🔁 Тижневий цикл", "щотижня",
              f"по колу всі 5 модулів + акцент на найслабші: {acc}; SRS-слова щодня"),
        Phase("📅 Реєстрація", "протягом 6 місяців",
              "зареєструйся на офіційну сесію і познач дату («📅 Вказати дату іспиту») — "
              "складу точний графік до іспиту й подовжу доступ, якщо треба"),
    ]


# віхи відносно дати: (тижнів до іспиту, підпис, поріг готовності всіх модулів або None=дія)
_MILESTONES: list[tuple[int, str, int | None]] = [
    (8, "🎯 Перший повний мок (/egzamin)", None),
    (4, "📗 Усі модулі ≥40%", 40),
    (2, "🚩 Усі модулі ≥50% (поріг іспиту!)", 50),
    (1, "🌱 Тапер + логістика дня іспиту", None),
]


def _min_ready(readiness: dict[str, int]) -> int:
    return min((readiness.get(m.value, 0) for m in Module), default=0)


def milestones(weeks_left: int, readiness: dict[str, int]) -> list[str]:
    """Чекпойнти відносно дати: майбутні → коли; активні → досягнуто/відстаєш."""
    mn = _min_ready(readiness)
    out: list[str] = []
    for wk, label, thr in _MILESTONES:
        if weeks_left > wk:
            out.append(f"🔜 {label} — за {weeks_left - wk} тиж")
        elif thr is None:
            out.append(f"▶️ {label} — час робити")
        else:
            out.append(f"{'✅' if mn >= thr else '⚠️'} {label}")
    return out


def build(
    exam_date: str, confirmed: bool, readiness: dict[str, int], today: date, daily_min: int = 60
) -> StudyPlan:
    weak = weak_order(readiness)
    top2 = [MODULE_LABELS[m] for m in weak[:2]]
    if confirmed and exam_date:
        try:
            exam = date.fromisoformat(exam_date)
        except ValueError:
            exam = today
        days = max(0, (exam - today).days)
        weeks = max(1, round(days / 7))
        return StudyPlan(
            True, days, weeks, weak, daily_min, _phases_with_date(weeks, top2), readiness
        )
    return StudyPlan(False, None, None, weak, daily_min, _phases_free(top2), readiness)


def render(plan: StudyPlan) -> str:
    lines = ["📅 <b>Твій індивідуальний план підготовки</b>\n"]
    if plan.has_date:
        lines.append(f"До іспиту: <b>{plan.days_left}</b> днів (~{plan.weeks_left} тижнів).\n")
    else:
        lines.append("Дата ще не підтверджена — <b>вільний адаптивний</b> план.\n")

    lines.append("<b>Фази:</b>")
    for p in plan.phases:
        lines.append(f"{p.title} <i>({p.span})</i>\n  {p.focus}")

    if plan.has_date and plan.weeks_left is not None:
        lines.append("\n<b>🏁 Віхи до іспиту:</b>")
        lines += [f"  {m}" for m in milestones(plan.weeks_left, plan.readiness)]

    weak2 = ", ".join(MODULE_LABELS[m] for m in plan.weak[:2])
    lines.append(f"\n🔎 <b>Пріоритет зараз:</b> {weak2}")
    g = plan.daily_min
    rep, gr, dr, ws = (max(1, round(g * x / 60)) for x in (10, 15, 20, 15))
    lines.append(
        f"\n🕐 <b>Щоденна ціль ~{g} хв</b> (твоя з /cel): {rep} повторення (SRS) · "
        f"{gr} граматика/лексика · {dr} дрил у форматі іспиту · {ws} письмо/мовлення."
    )
    lines.append("\nПравило іспиту: <b>≥50% у КОЖНОМУ</b> модулі — тому тягнемо найслабші.")
    return "\n".join(lines)
