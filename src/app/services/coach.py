"""Розумний підбір наступної дії («⚡ Навчатись зараз») — прибирає тертя вибору.

Чиста функція: за станом (тест пройдено?, готовність+обсяг по модулях, слів на
повторення) вирішує НАЙКОРИСНІШУ дію зараз і пояснює чому. Пріоритет — до головної
цілі (усі модулі ≥50%): спершу діагностика → непокриті модулі → повторення (щоб не
забути) → найслабший модуль.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.models import MODULE_LABELS, Module

# модуль → (callback запуску вправи, коротка назва дії)
_MODULE_ACTION: dict[str, tuple[str, str]] = {
    "pisanie": ("writing:start", "✍️ Письмо"),
    "mowienie": ("speaking:start", "🗣 Мовлення"),
    "sluchanie": ("listening:start", "🎧 Аудіювання"),
    "czytanie": ("drill:start", "🎯 Тренування (читання/граматика)"),
    "gramatyka": ("drill:start", "🎯 Тренування (граматика/читання)"),
}
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
    cb, lbl = _MODULE_ACTION[wk.value]
    return Action(cb, lbl, f"{MODULE_LABELS[wk]} — зараз найслабший, тягнемо його вгору")
