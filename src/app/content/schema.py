"""Схема офіційного контенту B1 — реєстр екзаменаційних тестів Держкомісії.

Кожен Exam = один офіційний тест (пробний або реальний минулий іспит). Секції MCQ
(czytanie/gramatyka) — дослівно з PDF. Аудіювання/письмо/мовлення поки поза цим
реєстром (у своїх сервісах). Порядок EXAMS: найстаріший → найновіший (latest = last).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MCQItem:
    section: str  # 'czytanie' | 'gramatyka'
    context: str
    question: str
    options: list[str]
    correct: int
    explain: str


@dataclass
class Exam:
    id: str  # стабільний ключ, напр. "2019", "2024-06"
    label: str  # людяна назва для UI
    kind: str  # 'sample' (пробний) | 'real' (минулий іспит)
    year: int
    items: list[MCQItem] = field(default_factory=list)

    def section(self, section: str) -> list[MCQItem]:
        return [it for it in self.items if it.section == section]
