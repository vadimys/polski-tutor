"""Розумний підбір наступної дії («⚡ Навчатись зараз») — прибирає тертя вибору.

Чиста функція: за станом (тест пройдено?, готовність+обсяг по модулях, слів на
повторення) вирішує НАЙКОРИСНІШУ дію зараз і пояснює чому. Пріоритет — до головної
цілі (усі модулі ≥50%): спершу діагностика → непокриті модулі → повторення (щоб не
забути) → найслабший модуль.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.models import MODULE_LABELS, Module

# модуль → формати вправ (усі — реальні типи іспиту B1). Ротуємо між ними, щоб учень
# тренував УСІ формати модуля, а не лише MCQ-дрил (перший = базовий/діагностичний).
_FORMATS: dict[str, list[tuple[str, str]]] = {
    "pisanie": [("writing:start", "✍️ Письмо")],
    "mowienie": [("speaking:start", "🗣 Мовлення"), ("speaking:photo", "🖼 Опис фото")],
    "sluchanie": [("listening:start", "🎧 Аудіювання"), ("amatch:open", "🔗 Аудіо-зіставлення")],
    "czytanie": [
        ("drill:start", "🎯 Тренування (читання)"),
        ("match:open", "🧩 Зіставлення (Czytanie III/IV)"),
        ("mock:czytanie", "📋 МОК читання"),
    ],
    "gramatyka": [
        ("drill:start", "🎯 Тренування (граматика)"),
        ("fill:open", "✏️ Впиши форму (Gramatyka IV)"),
        ("open:open", "🔄 Трансформації (Gramatyka V/VI)"),
        ("mock:gramatyka", "📋 МОК граматики"),
    ],
}


def _format_for(module: str, attempts: dict[str, int]) -> tuple[str, str]:
    """Формат вправи модуля з ротацією за к-стю спроб (детерміновано, без випадковості):
    що більше вже практикував модуль — то інший формат іспиту пропонуємо."""
    fmts = _FORMATS.get(module) or [("coach:now", module)]
    return fmts[attempts.get(module, 0) % len(fmts)]


# базовий (діагностичний) формат модуля — для непокритих і первинного вимірювання
_MODULE_ACTION: dict[str, tuple[str, str]] = {m: f[0] for m, f in _FORMATS.items()}
# продуктивні — раніше (їх найдовше «розганяти»)
_PRIORITY = ["pisanie", "mowienie", "sluchanie", "gramatyka", "czytanie"]

_REVIEW_THRESHOLD = 3  # від скількох слів на повторення — робимо повторення першим


@dataclass
class Action:
    cb: str  # callback_data, що запускає дію
    label: str  # що саме робимо
    reason: str  # чому саме це зараз


def _weakest(readiness: dict[str, int]) -> Module:
    return min(Module, key=lambda m: (readiness.get(m.value, 0), _PRIORITY.index(m.value)))


def choose(
    placement_done: bool, readiness: dict[str, int], attempts: dict[str, int], due_reviews: int
) -> Action:
    """Найкорисніша дія зараз (для кнопки «⚡ Навчатись зараз»)."""
    if not placement_done:
        return Action("placement:start", "📝 Стартовий тест",
                      "спершу визначимо твій рівень — і я підбиратиму найкорисніше")

    unmeasured = [m for m in _PRIORITY if attempts.get(m, 0) == 0]
    if unmeasured:
        cb, lbl = _MODULE_ACTION[unmeasured[0]]
        return Action(cb, lbl, f"{MODULE_LABELS[Module(unmeasured[0])]} ще не пробували — "
                              "перевірмо, щоб бачити повну картину")

    if due_reviews >= _REVIEW_THRESHOLD:
        return Action("review:start", "🔁 Повторення слів",
                      f"{due_reviews} слів чекають — закріпимо, поки не забулись")

    wk = _weakest(readiness)
    cb, lbl = _format_for(wk.value, attempts)  # ротація форматів — тренуємо всі типи іспиту
    return Action(cb, lbl, f"{MODULE_LABELS[wk]} — зараз найслабший; тренуємо формат «{lbl}»")
