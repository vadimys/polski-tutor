"""Модуль мовлення (Mówienie): теми монологів + AI-фідбек із транскрипту."""

from __future__ import annotations

import random
from dataclasses import dataclass

from app.integrations import ai
from app.services.feedback import parse_score, strip_score_line


@dataclass
class SpeakingTask:
    id: str
    prompt: str


# Теми монологів B1 (близькі до іспиту та життя учня)
TASKS: list[SpeakingTask] = [
    SpeakingTask("dzien", "Opowiedz o swoim typowym dniu: co robisz rano, po południu, wieczorem."),
    SpeakingTask("miasto", "Opisz miasto, w którym mieszkasz: co tam jest, co lubisz, czego brakuje."),
    SpeakingTask("polski", "Dlaczego uczysz się polskiego? Jakie masz plany na przyszłość w Polsce?"),
    SpeakingTask("praca", "Opowiedz o swojej pracy lub wymarzonej pracy: czym się zajmujesz."),
    SpeakingTask("weekend", "Jak spędzasz weekend? Opowiedz o swoim ostatnim wolnym dniu."),
    SpeakingTask("zdrowie", "Co robisz, żeby być zdrowym? Sport, jedzenie, sen — opowiedz."),
    SpeakingTask("podroze", "Opowiedz o miejscu, które chciał(a)byś odwiedzić, i dlaczego."),
]


def pick_task() -> SpeakingTask:
    return random.choice(TASKS)


def task_by_id(task_id: str) -> SpeakingTask | None:
    return next((t for t in TASKS if t.id == task_id), None)


_SYSTEM = (
    "Ти — доброзичливий екзаменатор іспиту B1 з польської (модуль Mówienie) ТА репетитор "
    "для україномовного учня. Тобі дають ТРАНСКРИПТ усного монологу учня (розпізнаний "
    "автоматично, тому можливі дрібні неточності розпізнавання). "
    "Оцінюєш за критеріями B1: (1) розкриття теми; (2) звʼязність і плавність (наскільки "
    "видно з тексту); (3) граматична правильність; (4) словниковий запас. "
    "ВАЖЛИВО: вимову з транскрипту оцінити НЕ можна — чесно про це не суди. "
    "Фідбек УКРАЇНСЬКОЮ, конкретно й підбадьорливо. Формат Telegram: лише <b>...</b> та емодзі, "
    "БЕЗ markdown. Структура:\n"
    "• <b>Що добре</b> — 1–2 пункти.\n"
    "• <b>Помилки</b> — 3–5: «було → стало» + коротке пояснення.\n"
    "• <b>Кращі фрази</b> — 1–2 природніші польські формулювання на цю тему.\n"
    "ОСТАННІЙ рядок — строго: WYNIK: NN  (0–100, орієнтовний % за B1 Mówienie)."
)


def _prompt(task: SpeakingTask, transcript: str) -> str:
    return (
        f"Тема монологу: {task.prompt}\n\n"
        f"Транскрипт відповіді учня:\n«{transcript}»\n\n"
        "Оціни за критеріями B1 Mówienie і дай фідбек за вказаною структурою."
    )


async def feedback(task: SpeakingTask, transcript: str) -> tuple[str, int | None]:
    out = await ai.ask(_SYSTEM, _prompt(task, transcript), strong=True, max_tokens=1400)
    if not out:
        return "", None
    return strip_score_line(out), parse_score(out)
