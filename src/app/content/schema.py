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
class MatchTask:
    """Зіставлення (dopasowanie) — офіц. тип Czytanie Zad III/IV.

    Вставити фрагменти в текст (Zad III) або зіставити заголовки з абзацами (Zad IV).
    Опорні фрагменти (`options`, порядок A–H) показуємо ОДИН раз; далі кожен пропуск
    (`prompts[i]`) → вибір фрагмента-літери. `key[i]` = індекс правильного в `options`.
    Приклад (PRZYKŁAD) із arkusz у пул НЕ включаємо — лишаються реальні пропуски.
    """

    section: str  # 'czytanie'
    title: str  # людяна назва (для пікера)
    intro: str  # інструкція + опорний текст (з маркерами пропусків), показ раз
    options: list[str]  # пул фрагментів (порядок A, B, C…)
    prompts: list[str]  # по одному на пропуск/заголовок (локальний контекст)
    key: list[int]  # key[i] = індекс у options для prompts[i]
    explain: list[str]  # пояснення на кожен пропуск (та ж довжина, що prompts)


@dataclass
class FreeFillTask:
    """Вписати форму (free-fill) — офіц. тип Gramatyka Zad IV.

    Учень ВПИСУЄ форму слова (не вибір!). `prompts[i]` = локальний контекст із
    інфінітивом у дужках; `accepted[i]` = список прийнятних відповідей (варіанти,
    напр. ["będziemy mieli", "będziemy mieć"]). Порівняння — нормалізоване
    (регістр/пробіли/пунктуація), діакритика зберігається.
    """

    section: str  # 'gramatyka'
    title: str
    intro: str  # інструкція + приклад/уривок, показ раз
    prompts: list[str]  # по одному на пропуск (локальний контекст + інфінітив)
    accepted: list[list[str]]  # прийнятні відповіді на кожен пропуск
    explain: list[str]  # пояснення на кожен пропуск


# усі структуровані (не плоскі MCQ) завдання
Task = MatchTask | FreeFillTask


@dataclass
class Exam:
    id: str  # стабільний ключ, напр. "2019", "2024-06"
    label: str  # людяна назва для UI
    kind: str  # 'sample' (пробний) | 'real' (минулий іспит)
    year: int
    items: list[MCQItem] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)  # структуровані (не-MCQ) завдання

    def section(self, section: str) -> list[MCQItem]:
        return [it for it in self.items if it.section == section]

    def match_tasks(self, section: str | None = None) -> list[MatchTask]:
        return [
            t for t in self.tasks
            if isinstance(t, MatchTask) and (section is None or t.section == section)
        ]

    def fill_tasks(self, section: str | None = None) -> list[FreeFillTask]:
        return [
            t for t in self.tasks
            if isinstance(t, FreeFillTask) and (section is None or t.section == section)
        ]
