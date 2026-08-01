"""«Розмова з екзаменатором» — діалоговий симулятор усної частини B1 (Mówienie, Zad3).

Turn-based: голос учня → STT → ця служба дає наступну репліку екзаменатора (Haiku, дешево)
→ TTS. Наприкінці — ОДНА строга оцінка за офіц. рубрикою Держкомісії (Sonnet). Два режими:
- exam (Іспит): екзаменатор НЕ перебиває/не виправляє, тримає роль і час, бал у кінці.
- practice (Тренування): делікатно підказує польське слово, якщо учень застряг.

Заземлення — реальні комунікативні ситуації з офіц. збірника MÓWIENIE B1 (Zadanie 3):
екзаменатор грає роль співрозмовника, реагує непередбачувано і РАЗ вводить перешкоду,
щоб учень досягав мети через переговори (як на справжньому іспиті).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from app.integrations import ai

logger = logging.getLogger(__name__)

MAX_TURNS = 6  # стеля реплік учня в одній розмові (бюджет + автентична довжина іспиту)
_END = "[KONIEC]"  # маркер, яким екзаменатор сигналить кінець розмови


@dataclass(frozen=True)
class Scenario:
    id: str
    title: str  # короткий укр. заголовок для меню
    setup_pl: str  # ситуація для учня (з офіц. матеріалів)
    setup_uk: str  # укр. пояснення
    examiner_role: str  # кого грає екзаменатор (PL)
    goal_uk: str  # комунікативна мета учня (укр.)
    register: str  # 'oficjalny' | 'nieoficjalny'
    obstacle_pl: str  # перешкода, яку екзаменатор РАЗ вводить (PL)
    opening_pl: str  # перша репліка екзаменатора, що починає діалог
    examples_uk: list[str] = field(default_factory=list)  # підказки-фрази (для режиму тренування UI)


# 5 реальних Zadanie 3 з офіц. збірника MÓWIENIE B1 (ролі/перешкоди — за офіц. прикладами діалогів)
SCENARIOS: list[Scenario] = [
    Scenario(
        id="hotel", title="Бронювання готелю",
        setup_pl="Chce Pan/Pani przyjechać z rodziną na tydzień do Krakowa. Proszę zadzwonić do "
                 "hotelu, zarezerwować miejsca i zapytać o warunki pobytu.",
        setup_uk="Дзвониш у готель у Кракові: заброньуй номери для родини на тиждень і спитай умови.",
        examiner_role="recepcjonista hotelu «Krakus»",
        goal_uk="забронювати номери на тиждень і дізнатися умови (ціна, сніданок, доїзд)",
        register="oficjalny",
        obstacle_pl="W podanym terminie wolne pokoje są tylko na dwóch różnych piętrach — zapytaj, "
                    "czy to problem, i zaproponuj alternatywę.",
        opening_pl="Hotel Krakus, recepcja, dzień dobry. W czym mogę pomóc?",
        examples_uk=["Chciałbym zarezerwować…", "Czy jest w cenie śniadanie?", "Ile kosztuje doba?"],
    ),
    Scenario(
        id="kurs", title="Запис на курс польської",
        setup_pl="Znalazł(a) Pan/Pani ogłoszenie «Polski dla obcokrajowców». Chce Pan/Pani zdawać "
                 "egzamin. Proszę zadzwonić i umówić się na lekcję.",
        setup_uk="Дзвониш у мовну школу: домовся про уроки польської для підготовки до іспиту.",
        examiner_role="pracownik szkoły językowej",
        goal_uk="домовитися про уроки (рівень, розклад, ціна) для підготовки до іспиту B1",
        register="oficjalny",
        obstacle_pl="Grupy na poziomie B1 są już pełne — zaproponuj tylko droższe lekcje "
                    "indywidualne i zobacz, jak uczeń zareaguje.",
        opening_pl="Szkoła językowa «Lingua», słucham. Dzień dobry!",
        examples_uk=["Dzwonię w sprawie kursu…", "Kiedy są zajęcia?", "Ile kosztuje jedna lekcja?"],
    ),
    Scenario(
        id="meble", title="Переставити меблі",
        setup_pl="Mieszka Pani/Pan z kolegą w jednym pokoju. Chce Pani/Pan inaczej ustawić meble, "
                 "a kolega nie chce zmian. Proszę go przekonać.",
        setup_uk="Живеш із колегою в кімнаті. Хочеш переставити меблі — переконай його (він проти).",
        examiner_role="kolega z pokoju, Marek, któremu jest wygodnie tak, jak jest",
        goal_uk="переконати сусіда погодитися переставити меблі (навести аргументи)",
        register="nieoficjalny",
        obstacle_pl="Bądź niechętny: «mnie pasuje tak, jak jest», podaj kontrargument (np. «ale wtedy "
                    "łóżko będzie przy oknie i będzie zimno») — ustąp dopiero, gdy uczeń przekona.",
        opening_pl="Słuchaj, co ty znowu kombinujesz z tymi meblami? Mnie jest dobrze tak, jak jest.",
        examples_uk=["Słuchaj, mam pomysł…", "Będzie więcej miejsca…", "Co ty na to?"],
    ),
    Scenario(
        id="kino", title="Кіно чи концерт",
        setup_pl="Kolega proponuje wyjście do kina na komedię, ale Pani/Pan woli koncert muzyki "
                 "poważnej. Proszę uzgodnić wspólny plan.",
        setup_uk="Колега кличе в кіно на комедію, а ти хочеш на концерт. Узгодьте спільний план.",
        examiner_role="kolega, który bardzo chce iść na komedię do kina",
        goal_uk="узгодити спільний план на вечір, врахувавши обидва бажання",
        register="nieoficjalny",
        obstacle_pl="Broń swojej opcji: «na koncercie muzyki poważnej się nudzę», szukaj kompromisu "
                    "dopiero, gdy uczeń zaproponuje rozsądny.",
        opening_pl="Hej! Idziemy dziś do kina na tę nową komedię? Wszyscy mówią, że super śmieszna!",
        examples_uk=["A może zamiast tego…", "Zróbmy tak, że…", "Wiem, ale ja wolę…"],
    ),
    Scenario(
        id="narty", title="Поїздка на лижі",
        setup_pl="Kolega nie umie jeździć na nartach. Proszę przekonać go, że najlepsza metoda nauki "
                 "to wyjazd z Panią/Panem w góry.",
        setup_uk="Колега не вміє кататися на лижах. Переконай його поїхати з тобою вчитися в гори.",
        examiner_role="kolega Tomek, który boi się jeździć na nartach",
        goal_uk="переконати колегу поїхати вчитися кататися на лижах у гори",
        register="nieoficjalny",
        obstacle_pl="Wyrażaj obawy: «boję się, że się przewrócę i połamię», «to chyba drogie» — "
                    "daj się przekonać dopiero po konkretnych argumentach.",
        opening_pl="Narty? Ja? Nie, nie… ja się boję, że sobie coś złamię. I to pewnie kosztuje majątek.",
        examples_uk=["Nie martw się, bo…", "Na początku jest łatwo…", "Obiecuję, że…"],
    ),
]

_BY_ID = {s.id: s for s in SCENARIOS}


def scenario_by_id(sid: str) -> Scenario | None:
    return _BY_ID.get(sid)


# ───────────────────────────── діалог (Haiku) ─────────────────────────────
def _persona(sc: Scenario, mode: str) -> str:
    base = (
        f"Jesteś życzliwym egzaminatorem państwowej komisji egzaminacyjnej (PKPZJPjO). "
        f"W tej rozmowie ODGRYWASZ ROLĘ: {sc.examiner_role}. "
        f"Sytuacja: {sc.setup_pl} "
        f"Rejestr wypowiedzi: {sc.register} — konsekwentnie się go trzymaj. "
        f"Prowadź naturalną rozmowę po POLSKU na poziomie B1. Mów KRÓTKO — 1–3 zdania, jak żywy "
        f"rozmówca, nie jak lektor. "
        f"Wprowadź (jeden raz, w odpowiednim momencie) komplikację, żeby uczeń musiał negocjować: "
        f"{sc.obstacle_pl} "
        f"Jesteś ROZMÓWCĄ, nie nauczycielem: NIE oceniaj, NIE poprawiaj błędów językowych, "
        f"NIE podpowiadaj gotowych odpowiedzi. "
        f"Gdy cel rozmowy zostanie osiągnięty LUB po około {MAX_TURNS} wymianach — grzecznie "
        f"zakończ rozmowę i na końcu dopisz znacznik {_END}."
    )
    if mode == "practice":
        base += (
            " TRYB ĆWICZENIA: jeśli uczeń wyraźnie utknął albo użył słowa po ukraińsku/rosyjsku, "
            "delikatnie zaproponuj właściwe polskie słowo w nawiasie kwadratowym […] i płynnie "
            "kontynuuj w swojej roli."
        )
    return base


def _history_text(history: list[tuple[str, str]]) -> str:
    if not history:
        return "(rozmowa się jeszcze nie zaczęła)"
    label = {"uczen": "Uczeń", "egzaminator": "Egzaminator"}
    return "\n".join(f"{label.get(who, who)}: {txt}" for who, txt in history)


def _parse_reply(raw: str) -> tuple[str, bool]:
    """Витягти текст репліки + чи це кінець (маркер [KONIEC])."""
    done = _END in raw
    text = raw.replace(_END, "").strip()
    return text, done


def is_capped(history: list[tuple[str, str]]) -> bool:
    """Чи вичерпано ліміт реплік учня (жорстка стеля бюджету/автентичності)."""
    return sum(1 for who, _ in history if who == "uczen") >= MAX_TURNS


async def next_reply(sc: Scenario, mode: str, history: list[tuple[str, str]]) -> tuple[str, bool]:
    """Наступна репліка екзаменатора (Haiku). Повертає (text, done).

    done=True, якщо екзаменатор завершив або досягнуто стелі реплік. '' → збій AI."""
    user = (
        f"Dotychczasowa rozmowa:\n{_history_text(history)}\n\n"
        f"Napisz swoją następną, krótką kwestię jako {sc.examiner_role}:"
    )
    raw = await ai.ask(_persona(sc, mode), user, strong=False, max_tokens=160, label="examiner")
    if not raw.strip():
        return "", True  # збій — коректно завершуємо розмову (хендлер покаже оцінку по наявному)
    text, done = _parse_reply(raw)
    if is_capped(history):  # після цієї відповіді учень уже вичерпав ліміт → закриваємо
        done = True
    return text, done


# ───────────────────────── оцінка (Sonnet, офіц. рубрика) ─────────────────────────
_GRADE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["wykonanie", "gramatyka", "slownictwo", "cel_osiagniety", "rejestr_ok", "feedback"],
    "properties": {
        "wykonanie": {"type": "integer"},  # realizacja zadania komunikacyjnego 0-6
        "gramatyka": {"type": "integer"},  # 0-8
        "slownictwo": {"type": "integer"},  # słownictwo i styl 0-8
        "cel_osiagniety": {"type": "boolean"},
        "rejestr_ok": {"type": "boolean"},
        "feedback": {"type": "string"},  # українською, коротко, з прикладами
    },
}

_GRADE_SYS = (
    "Jesteś surowym, ale sprawiedliwym egzaminatorem państwowej komisji (PKPZJPjO), część ustna "
    "B1 (Mówienie), Zadanie 3 — sytuacja komunikacyjna. Oceń WYŁĄCZNIE wypowiedzi ucznia w "
    "rozmowie według oficjalnej skali: wykonanie zadania (realizacja celu komunikacyjnego) 0–6; "
    "gramatyka 0–8; słownictwo i styl (w tym stosowność rejestru oficjalny/nieoficjalny) 0–8. "
    "NIE oceniaj wymowy ani płynności (to wymaga nagrania audio). Fonetyki nie dotykaj. "
    "Zwróć też: czy uczeń OSIĄGNĄŁ cel komunikacyjny, czy rejestr był poprawny, oraz krótki "
    "feedback PO UKRAIŃSKU (2–4 zdania, konkretnie: co dobrze, co poprawić, z przykładem). "
    "Odpowiedz tylko strukturą JSON."
)


@dataclass
class Verdict:
    wykonanie: int
    gramatyka: int
    slownictwo: int
    cel_osiagniety: bool
    rejestr_ok: bool
    feedback: str

    @property
    def total(self) -> int:
        return self.wykonanie + self.gramatyka + self.slownictwo  # з 22 доступних із тексту

    @property
    def max_total(self) -> int:
        return 6 + 8 + 8

    @property
    def pct(self) -> int:
        return round(self.total / self.max_total * 100)


async def grade(sc: Scenario, history: list[tuple[str, str]]) -> Verdict | None:
    """Одна строга оцінка всієї розмови (Sonnet). None → AI вимкнено/збій."""
    dialogue = _history_text(history)
    user = (
        f"Scenariusz (rola egzaminatora: {sc.examiner_role}; rejestr: {sc.register}; "
        f"cel ucznia: {sc.goal_uk}).\n\nPełna rozmowa:\n{dialogue}\n\n"
        f"Oceń wypowiedzi ucznia."
    )
    data = await ai.ask_json(_GRADE_SYS, user, _GRADE_SCHEMA, strong=True, max_tokens=700,
                             label="examiner_grade")
    if not isinstance(data, dict):
        return None
    try:
        return Verdict(
            wykonanie=max(0, min(6, int(data["wykonanie"]))),
            gramatyka=max(0, min(8, int(data["gramatyka"]))),
            slownictwo=max(0, min(8, int(data["slownictwo"]))),
            cel_osiagniety=bool(data["cel_osiagniety"]),
            rejestr_ok=bool(data["rejestr_ok"]),
            feedback=str(data["feedback"]),
        )
    except (KeyError, ValueError, TypeError):
        logger.exception("grade parse failed: %r", data)
        return None
