"""Модуль мовлення (Mówienie) — на ОФІЦІЙНИХ матеріалах Держкомісії.

Реальні типи завдань іспиту: монолог (Zadanie 2) і комунікативна ситуація (Zadanie 3),
з офіційними прикладами тем/сценаріїв. (Опис фотографії — Zadanie 1 — потребує світлин,
додається окремо.) Оцінювання — за ОФІЦІЙНОЮ шкалою мовлення (частина, доступна з
транскрипту): wykonanie zadania (0-7 монолог / 0-6 ситуація), gramatyka 0-8, słownictwo
i styl 0-8. Фонетику/плавність із тексту чесно НЕ оцінюємо (потрібен аудіо-рівень).
Жодних вигаданих завдань: усе з опублікованих матеріалів комісії.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from app.integrations import ai
from app.services.feedback import parse_official_mowienie, strip_official_line


@dataclass
class SpeakTask:
    id: str
    kind: str  # 'monolog' (Zad2) | 'sytuacja' (Zad3) | 'opis' (Zad1)
    prompt: str
    max_wykonanie: int  # офіц.: опис 7, монолог 7, ситуація 6
    photo_url: str = ""  # для kind='opis'
    photo_source: str = ""


SOURCE = "офіційний зразок Держкомісії (B1)"

# Реальні завдання з офіц. збірника MÓWIENIE B1 і пробного тесту
TASKS: list[SpeakTask] = [
    # Zadanie 2 — MONOLOG (0-7)
    SpeakTask("m_film", "monolog",
              "Proszę opowiedzieć o filmie, który Pani/Pan najlepiej pamięta. "
              "(розкажи про фільм, який найкраще памʼятаєш)", 7),
    SpeakTask("m_miejsce", "monolog",
              "Proszę opowiedzieć o miejscowości, którą warto zobaczyć w Pani/Pana kraju. "
              "(про місцевість, яку варто побачити у твоїй країні)", 7),
    SpeakTask("m_jezyki", "monolog",
              "Czy zgadza się Pani/Pan z opinią, że nauka języków obcych daje nowe możliwości "
              "w życiu? Proszę uzasadnić odpowiedź. (чи мови дають нові можливості — обґрунтуй)", 7),
    SpeakTask("m_rodzina", "monolog",
              "Temat: Moja rodzina. Proszę opowiedzieć o swojej rodzinie (kim są, jak wyglądają, "
              "czym się zajmują, relacje). (про свою родину)", 7),
    SpeakTask("m_rzeczy", "monolog",
              "Rzeczy, bez których trudno byłoby mi żyć. Proszę opisać i uzasadnić. "
              "(речі, без яких важко жити — опиши й обґрунтуй)", 7),
    # Zadanie 3 — SYTUACJA KOMUNIKACYJNA (0-6) — рольова
    SpeakTask("s_lekcja", "sytuacja",
              "Znalazł(a) Pan/Pani ogłoszenie «Polski dla obcokrajowców». Chce Pan/Pani zdawać "
              "egzamin. Proszę zadzwonić i umówić się na lekcję. (подзвони й домовся про урок)", 6),
    SpeakTask("s_hotel", "sytuacja",
              "Chce Pan/Pani przyjechać z rodziną na tydzień do Krakowa. Proszę zadzwonić do hotelu, "
              "zarezerwować miejsca i zapytać o warunki pobytu. (заброньуй готель, спитай умови)", 6),
    SpeakTask("s_meble", "sytuacja",
              "Mieszka Pani/Pan z kolegą w jednym pokoju. Chce Pani/Pan inaczej ustawić meble, "
              "a kolega nie chce zmian. Proszę go przekonać. (переконай сусіда переставити меблі)", 6),
    SpeakTask("s_kino", "sytuacja",
              "Kolega proponuje wyjście do kina na komedię, ale Pani/Pan woli koncert muzyki poważnej. "
              "Proszę uzgodnić wspólny plan. (узгодь спільний план — кіно чи концерт)", 6),
    SpeakTask("s_narty", "sytuacja",
              "Kolega nie umie jeździć na nartach. Proszę przekonać go, że najlepsza metoda nauki "
              "to wyjazd z Panią/Panem w góry. (переконай поїхати вчитися на лижах)", 6),
]

_KIND_LABEL = {
    "opis": "Опис фотографії (Zadanie 1)",
    "monolog": "Монолог (Zadanie 2)",
    "sytuacja": "Комунікативна ситуація (Zadanie 3)",
}

_OPIS_PROMPT = (
    "Proszę opisać fotografię i przedstawioną na niej sytuację. "
    "(опиши: люди — хто, зовнішність, емоції, стосунки; місце — де, plany, кольори, пора; "
    "дії — що роблять)"
)

# Опис ілюстрації (Zadanie 1). Світлини — вільні ліцензії (Wikimedia Commons).
PHOTOS: list[SpeakTask] = [
    SpeakTask("p_picnic", "opis", _OPIS_PROMPT, 7,
              "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Family_Picnic_Near_Orchard_Point_Marina.jpg/1280px-Family_Picnic_Near_Orchard_Point_Marina.jpg",
              "Wikimedia Commons, CC BY 2.0"),
    SpeakTask("p_class", "opis", _OPIS_PROMPT, 7,
              "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/A_public_high_school_teacher_in_a_classroom_in_the_United_States_08.jpg/1280px-A_public_high_school_teacher_in_a_classroom_in_the_United_States_08.jpg",
              "Wikimedia Commons, CC BY 4.0"),
    SpeakTask("p_football", "opis", _OPIS_PROMPT, 7,
              "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Boy_are_playing_football_at_Jabal_Elba_%2CEgypt.jpg/1280px-Boy_are_playing_football_at_Jabal_Elba_%2CEgypt.jpg",
              "Wikimedia Commons, CC BY-SA 4.0"),
    SpeakTask("p_market", "opis", _OPIS_PROMPT, 7,
              "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Child_working_selling_vegetables_in_downtown_Maracaibo.jpg/1280px-Child_working_selling_vegetables_in_downtown_Maracaibo.jpg",
              "Wikimedia Commons, CC0"),
    SpeakTask("p_office", "opis", _OPIS_PROMPT, 7,
              "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Novell_people_working_late_2007.jpg/1280px-Novell_people_working_late_2007.jpg",
              "Wikimedia Commons, CC BY 2.0"),
    SpeakTask("p_restaurant", "opis", _OPIS_PROMPT, 7,
              "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Dinner_at_Hong_Kong_Thai_Restaurant_%282878442821%29.jpg/1280px-Dinner_at_Hong_Kong_Thai_Restaurant_%282878442821%29.jpg",
              "Wikimedia Commons, CC0"),
]


def pick_task() -> SpeakTask:
    return random.choice(TASKS)


def pick_photo() -> SpeakTask:
    return random.choice(PHOTOS)


def task_by_id(task_id: str) -> SpeakTask | None:
    return next((t for t in TASKS + PHOTOS if t.id == task_id), None)


def _system(task: SpeakTask) -> str:
    if task.kind == "opis":
        wykonanie = (
            "• WYKONANIE ZADANIA: 0-7 — опис має охопити ТРИ елементи: osoby (люди), "
            "miejsce/sytuacja (місце, plany, кольори, пора), czynności (що роблять); "
            "структура «від загального до деталей».\n"
            "ВАЖЛИВО: ти НЕ бачиш фото — оцінюй мову, повноту й структуру ОПИСУ з транскрипту, "
            "не суди відповідність реальному фото.\n"
        )
    else:
        wykonanie = (
            f"• WYKONANIE ZADANIA: 0-{task.max_wykonanie} — чи виконано комунікативне завдання, "
            "повнота, структура (вступ-розвиток-закінчення для монологу; досягнення мети розмови "
            "для ситуації), доречність.\n"
        )
    return (
        "Ти — екзаменатор Державної комісії (PKPZJPjO), що оцінює усну відповідь B1 за "
        "ОФІЦІЙНИМИ критеріями. Тобі дають ТРАНСКРИПТ (розпізнаний із голосу, можливі неточності).\n"
        f"Оціни за офіційною шкалою для цього завдання ({_KIND_LABEL[task.kind]}):\n"
        f"{wykonanie}"
        "• GRAMATYKA: 0-8.\n"
        "• SŁOWNICTWO I STYL: 0-8 (доречність офіц./неофіц. регістру).\n"
        "ВАЖЛИВО: фонетику й плавність із транскрипту НЕ оцінюй (чесно скажи, що це лише на аудіо).\n"
        "Фідбек УКРАЇНСЬКОЮ, конкретно й підбадьорливо. Формат Telegram: лише <b>...</b> й емодзі, "
        "БЕЗ markdown. Структура:\n"
        "• <b>Оцінка</b> — по кожному критерію коротко чому.\n"
        "• <b>Виконання завдання</b> — що вдалося, чого бракує для повного балу.\n"
        "• <b>Помилки</b> — 3-5: «було → стало» + пояснення.\n"
        "• <b>Корисні фрази</b> — 1-2 природні польські звороти для цього типу завдання.\n"
        f"ОСТАННІЙ рядок — СТРОГО: WYNIK: wykonanie=N gramatyka=N słownictwo=N "
        f"(wykonanie 0-{task.max_wykonanie}, решта 0-8)."
    )


def _prompt(task: SpeakTask, transcript: str) -> str:
    return (
        f"Завдання ({_KIND_LABEL[task.kind]}): {task.prompt}\n\n"
        f"Транскрипт відповіді учня:\n«{transcript}»\n\n"
        "Оціни за офіційними критеріями вище і дай фідбек за вказаною структурою."
    )


def readiness_pct(task: SpeakTask, wykonanie: int, gramatyka: int, slownictwo: int) -> int:
    """Відсоток за доступними з транскрипту критеріями (wykonanie + gramatyka + słownictwo)."""
    got = min(wykonanie, task.max_wykonanie) + min(gramatyka, 8) + min(slownictwo, 8)
    return round(got / (task.max_wykonanie + 16) * 100)


async def feedback(task: SpeakTask, transcript: str) -> tuple[str, tuple[int, int, int] | None]:
    out = await ai.ask(_system(task), _prompt(task, transcript), strong=True, max_tokens=1500)
    if not out:
        return "", None
    return strip_official_line(out), parse_official_mowienie(out)
