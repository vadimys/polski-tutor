"""Модуль письма (Pisanie) — на ОФІЦІЙНИХ матеріалах Держкомісії.

Завдання — реальні екзаменаційні набори (zestawy) з офіційного пробного тесту й
збірника PISANIE B1 (certyfikatpolski.pl). Формат: 3 набори по 2 завдання (a — коротка
форма, b — довша), обираєш один, робиш обидва. Оцінювання — за ОФІЦІЙНОЮ шкалою:
wykonanie zadania 0-10 · środki językowe 0-10 · poprawność językowa 0-10 = /30 (поріг 15).
Вимоги жанрів (GENRE_REQ) — з офіційних «metryczek form wypowiedzi».
Жодних вигаданих завдань: усе з опублікованих матеріалів комісії.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from app.integrations import ai
from app.services.feedback import parse_official_pisanie, strip_official_line


@dataclass
class Task:
    genre: str  # ключ до GENRE_REQ
    prompt: str  # офіційне формулювання (польською) + короткий укр. глос
    words: int


@dataclass
class WritingSet:
    id: str
    a: Task  # коротка форма
    b: Task  # довша форма


SOURCE = "офіційний зразок Держкомісії (B1)"

# Реальні екзаменаційні набори з офіційних матеріалів (пробний тест + збірник PISANIE B1)
SETS: list[WritingSet] = [
    WritingSet(
        "t1",
        Task("ogłoszenie",
             "Organizuje Pan/Pani imprezę urodzinową w mieszkaniu dla wielu gości. Hałas może "
             "przeszkadzać sąsiadom. Proszę napisać ogłoszenie, które powiesi Pan/Pani w windzie. "
             "(оголошення сусідам про вечірку)", 30),
        Task("list prywatny",
             "Odpoczywa Pan/Pani na wakacjach w swoim rodzinnym kraju. Proszę napisać list do "
             "przyjaciela z Polski, w którym opowie Pan/Pani o swoim pobycie. (лист другові про відпочинок)",
             170),
    ),
    WritingSet(
        "t2",
        Task("zaproszenie",
             "Od niedawna pracuje Pan/Pani w polskiej firmie. Proszę napisać e-mail z zaproszeniem "
             "na spotkanie przy grillu w ogrodzie dla nowych kolegów z pracy. (e-mail-запрошення на гриль)",
             40),
        Task("recenzja",
             "«Ten serial ostatnio obejrzałam/obejrzałem». Proszę zaprezentować serial i wyrazić "
             "własną opinię na jego temat. (презентація серіалу + власна думка)", 160),
    ),
    WritingSet(
        "t3",
        Task("życzenia",
             "Pana/Pani przyjaciel za miesiąc bierze ślub, ale nie może Pan/Pani być na uroczystości. "
             "Proszę poinformować go i napisać życzenia dla młodej pary. (побажання молодятам)", 30),
        Task("charakterystyka",
             "«Mam dobrą szefową / dobrego szefa». Proszę napisać charakterystykę swojego pracodawcy. "
             "(характеристика керівника)", 170),
    ),
    WritingSet(
        "p1",
        Task("pozdrowienia",
             "Proszę napisać pozdrowienia z wakacji do swojego dyrektora/profesora/nauczyciela. "
             "(привітання з відпустки керівнику)", 25),
        Task("esej",
             "«Każdy ma jakieś zainteresowania» — proszę napisać o swoim hobby. (про своє хобі)", 175),
    ),
    WritingSet(
        "p2",
        Task("zaproszenie",
             "Proszę zaprosić swoich sąsiadów (starszych państwa) na imieniny/urodziny. "
             "(запросити літніх сусідів на іменини)", 30),
        Task("list prywatny",
             "Proszę napisać list do kolegi/koleżanki, w którym opisze Pan/Pani swoje mieszkanie. "
             "(лист із описом квартири)", 170),
    ),
    WritingSet(
        "p3",
        Task("ogłoszenie",
             "Zgubił/Zgubiła Pan/Pani swój zegarek. Proszę napisać ogłoszenie. (оголошення про загублений годинник)",
             30),
        Task("opowiadanie",
             "«Nie lubię poniedziałków» — proszę napisać opowiadanie. (оповідання)", 170),
    ),
    WritingSet(
        "p4",
        Task("zaproszenie",
             "Proszę napisać zaproszenie dla kolegi na swoje urodziny. (запрошення на уродини)", 30),
        Task("charakterystyka",
             "Proszę opisać i scharakteryzować swojego ulubionego nauczyciela. (характеристика улюбленого вчителя)",
             170),
    ),
    WritingSet(
        "p5",
        Task("ogłoszenie",
             "Szuka Pan/Pani sublokatora do dużego mieszkania w centrum. Proszę napisać ogłoszenie "
             "do rozwieszenia w okolicy. (оголошення про пошук співмешканця)", 30),
        Task("list prywatny",
             "Proszę napisać list do przyjaciół, w którym zachęci ich Pan/Pani do wspólnego spędzenia "
             "wakacji w miejscowości, która bardzo się Panu/Pani spodobała. (лист-заохочення разом відпочити)",
             170),
    ),
    WritingSet(
        "p6",
        Task("list prywatny",
             "W krótkim liście proszę podziękować starszej sąsiadce za opiekę nad mieszkaniem podczas "
             "Pana/Pani tygodniowej nieobecności. (лист-подяка сусідці)", 30),
        Task("opowiadanie",
             "Proszę opowiedzieć ciekawą historię ze swojego dzieciństwa. (цікава історія з дитинства)", 170),
    ),
]

# Обов'язкові елементи форм — з офіційних «metryczek form wypowiedzi» (PISANIE B1)
GENRE_REQ: dict[str, str] = {
    "życzenia": "місце й дата; звертання (вокатив з «!»); текст під нагоду; підпис",
    "pozdrowienia": "місце й дата; звертання; короткий текст; підпис",
    "zaproszenie": "хто кого запрошує; з якої нагоди; де і коли; (офіц. — повний підпис)",
    "zawiadomienie": "місце й дата; що/де/коли (від)будеться; хто повідомляє",
    "ogłoszenie": "хто оголошує; з якою метою (sprzedaje/wynajmuje/poszukuje); предмет; контакт",
    "list prywatny": "місце й дата (справа вгорі); звертання (вокатив з «!»); вступ (мета)+розвиток+"
                     "закінчення; ввічлива формула на кінець; підпис",
    "opis osoby": "вступ (хто, обставини); зовнішність; закінчення (враження автора)",
    "charakterystyka": "дані особи (імʼя/вік/професія); зовнішність; риси характеру (+/-); риси розуму; "
                       "зацікавлення; оцінка особи",
    "opowiadanie": "вступ+розвиток+закінчення; логічна хронологія; зазвичай минулий час",
    "sprawozdanie": "час/місце/обставини/мета; перебіг подій; оцінка",
    "recenzja": "вступ (про що думка); розвиток (опис/зміст); закінчення (оцінка з обґрунтуванням)",
    "esej": "вступ; власні погляди + аргументи; закінчення",
}


def pick_set() -> WritingSet:
    return random.choice(SETS)


def set_by_id(set_id: str) -> WritingSet | None:
    return next((s for s in SETS if s.id == set_id), None)


_SYSTEM = (
    "Ти — екзаменатор Державної комісії (Państwowa Komisja ds. Poświadczania Znajomości JPjO), "
    "що оцінює письмову роботу на іспиті B1 СТРОГО за ОФІЦІЙНИМИ критеріями (максимум 30 балів):\n"
    "• WYKONANIE ZADANIA (0-10): чи виконано ОБИДВА завдання (a і b), відповідність ЖАНРУ та його "
    "обов'язковим елементам, композиція, обсяг (допускається різниця ~20 слів від норми).\n"
    "• ŚRODKI JĘZYKOWE (0-10): багатство й різноманітність лексики та граматичних структур, доречність.\n"
    "• POPRAWNOŚĆ JĘZYKOWA (0-10): граматика, орфографія, пунктуація.\n"
    "Поріг складання модуля — 50% (15/30). Оцінюй суворо, як на реальному іспиті, але фідбек давай "
    "УКРАЇНСЬКОЮ, конкретно й підбадьорливо. Формат Telegram: лише <b>...</b> та емодзі, БЕЗ markdown.\n"
    "Структура відповіді:\n"
    "• <b>Оцінка</b> — по кожному критерію коротко чому саме стільки.\n"
    "• <b>Виконання жанру</b> — чи є обов'язкові елементи форми (перелічені нижче), чого бракує.\n"
    "• <b>Помилки</b> — 4-6 конкретних: «було → стало» + коротке пояснення.\n"
    "• <b>Порада</b> — 1-2 фрази, що підтягнути.\n"
    "• <b>Зразок</b> — як можна було краще (польською), стисло.\n"
    "ОСТАННІЙ рядок — СТРОГО: WYNIK: wykonanie=N środki=N poprawność=N (кожне ціле 0-10)."
)


def _prompt(ws: WritingSet, text_a: str, text_b: str) -> str:
    req_a = GENRE_REQ.get(ws.a.genre, "—")
    req_b = GENRE_REQ.get(ws.b.genre, "—")
    return (
        f"ЗАВДАННЯ a ({ws.a.genre}, ~{ws.a.words} слів): {ws.a.prompt}\n"
        f"Обов'язкові елементи форми «{ws.a.genre}»: {req_a}\n"
        f"Відповідь учня (a):\n«{text_a}»\n\n"
        f"ЗАВДАННЯ b ({ws.b.genre}, ~{ws.b.words} слів): {ws.b.prompt}\n"
        f"Обов'язкові елементи форми «{ws.b.genre}»: {req_b}\n"
        f"Відповідь учня (b):\n«{text_b}»\n\n"
        "Оціни ВЕСЬ набір за офіційною шкалою 30 балів і дай фідбек за вказаною структурою."
    )


async def feedback(ws: WritingSet, text_a: str, text_b: str) -> tuple[str, tuple[int, int, int] | None]:
    """(фідбек, (wykonanie, środki, poprawność)|None). '' якщо AI недоступний."""
    out = await ai.ask(_SYSTEM, _prompt(ws, text_a, text_b), strong=True, max_tokens=1900)
    if not out:
        return "", None
    return strip_official_line(out), parse_official_pisanie(out)
