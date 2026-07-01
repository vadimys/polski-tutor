"""Доменні моделі: модулі іспиту, стан учня, лексика."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class Module(StrEnum):
    """П'ять модулів іспиту B1 (треба ≥50% у КОЖНОМУ окремо)."""

    SLUCHANIE = "sluchanie"
    CZYTANIE = "czytanie"
    GRAMATYKA = "gramatyka"
    PISANIE = "pisanie"
    MOWIENIE = "mowienie"


MODULE_LABELS: dict[Module, str] = {
    Module.SLUCHANIE: "🎧 Słuchanie (аудіювання)",
    Module.CZYTANIE: "📖 Czytanie (читання)",
    Module.GRAMATYKA: "🔤 Gramatyka (граматика)",
    Module.PISANIE: "✍️ Pisanie (письмо)",
    Module.MOWIENIE: "🗣 Mówienie (мовлення)",
}


@dataclass
class VocabItem:
    """Слово в інтервальному повторенні (Leitner)."""

    pl: str
    uk: str
    box: int = 1
    due: str = ""  # YYYY-MM-DD


@dataclass
class UserState:
    """Персональний стан учня (зберігається в Redis як JSON)."""

    user_id: int
    level: str = "A1"
    streak: int = 0
    last_lesson: str = ""  # YYYY-MM-DD
    placement_done: bool = False
    lesson_hour: int = 8
    # готовність 0..100 за кожним модулем (ключі — Module.value)
    readiness: dict[str, int] = field(default_factory=dict)

    def weakest_module(self) -> Module:
        """Модуль-фокус уроку. Спершу — ще НЕ виміряні (найбільша невідомість),
        у порядку пріоритету (Pisanie — страх користувача + обов'язкові 50%);
        коли всі мають дані — найнижчий відсоток."""
        priority = (
            Module.PISANIE,
            Module.MOWIENIE,
            Module.SLUCHANIE,
            Module.GRAMATYKA,
            Module.CZYTANIE,
        )
        for m in priority:
            if m.value not in self.readiness:
                return m
        return Module(min(self.readiness, key=lambda k: self.readiness[k]))
