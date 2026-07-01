"""Стартовий placement-тест: банк питань (A1→B1) + скоринг по модулях.

Об'єктивні MCQ вимірюють ЛИШЕ Gramatykę і Czytanie (з лексикою). Продуктивні
модулі (Pisanie/Mówienie) і Słuchanie тут НЕ оцінюються — їхню готовність
даємо тільки коли учень реально зробить відповідну вправу (без вигаданих цифр).
Тест щоразу різний: build_test() бере випадкову збалансовану вибірку з банку.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from app.domain.models import Module


@dataclass
class Question:
    id: str
    module: Module
    level: str  # A1 / A2 / B1
    text: str
    options: list[str]
    correct: int  # індекс правильної опції
    explain: str  # пояснення українською


@dataclass
class PlacementResult:
    overall_pct: int
    level: str
    per_module: dict[str, int]  # готовність 0..100 за модулем
    correct: int
    total: int


QUESTIONS: list[Question] = [
    Question("g1", Module.GRAMATYKA, "A1", "Uzupełnij: To jest ___ książka.",
             ["mój", "moja", "moje", "moi"], 1,
             "«książka» — жіночий рід → moja. Як укр. «моя книжка»."),
    Question("g2", Module.GRAMATYKA, "A1", "Uzupełnij (biernik): Mam ___ .",
             ["kot", "kota", "kotem", "kocie"], 1,
             "Після «mam» — знахідний (biernik). Істота ч.р.: kot → kota."),
    Question("g3", Module.GRAMATYKA, "A2", "Uzupełnij (dopełniacz): Idę do ___ .",
             ["sklep", "sklepu", "sklepie", "sklepem"], 1,
             "Прийменник «do» вимагає родового (dopełniacz): sklep → sklepu."),
    Question("g4", Module.GRAMATYKA, "A2", "Wczoraj ___ całą książkę.",
             ["czytałem", "przeczytałem", "czytam", "przeczytam"], 1,
             "«całą книжку» = результат, доконаний вид (dokonany): przeczytałem."),
    Question("g5", Module.GRAMATYKA, "B1", "Gdybym miał czas, ___ do kina.",
             ["pójdę", "poszedłbym", "idę", "szedłem"], 1,
             "Умовний спосіб (tryb przypuszczający): poszedłbym («пішов би»)."),
    Question("g6", Module.GRAMATYKA, "A2", "Mieszkam ___ Polsce.",
             ["w", "na", "do", "z"], 0,
             "Країни — прийменник «w» + місцевий: w Polsce. (Але: na Ukrainie!)"),
    Question("g7", Module.GRAMATYKA, "A1", "On ___ studentem.",
             ["jest", "są", "jestem", "jesteś"], 0,
             "«być» у 3 особі однини: on jest. Після «być» — orzecznik у narzędniku."),
    Question("g8", Module.GRAMATYKA, "B1", "Ten film jest ___ niż tamten.",
             ["ciekawy", "ciekawszy", "najciekawszy", "ciekawie"], 1,
             "Вищий ступінь (stopień wyższy): ciekawy → ciekawszy + niż."),
    Question("g9", Module.GRAMATYKA, "A2", "Interesuję się ___ .",
             ["muzyka", "muzyką", "muzyki", "muzyce"], 1,
             "«interesować się» вимагає orzędника (narzędnik): muzyką."),
    Question("g10", Module.GRAMATYKA, "B1", "Musisz się uczyć, ___ zdać egzamin.",
             ["że", "żeby", "bo", "ale"], 1,
             "Мета («щоб») — сполучник żeby + інфінітив."),
    Question("g11", Module.GRAMATYKA, "B1", "Dzieci ___ w parku.",
             ["bawili się", "bawiły się", "bawią", "bawić"], 1,
             "Минулий час, не-чоловічо-особовий рід (dzieci): bawiły się."),
    Question("g12", Module.GRAMATYKA, "A2", "Lubię ___ z mlekiem.",
             ["kawa", "kawę", "kawą", "kawie"], 1,
             "Після «lubię» — знахідний: kawa → kawę."),
    Question("c1", Module.CZYTANIE, "A2",
             "Anna pracuje w szpitalu jako pielęgniarka. — Gdzie pracuje Anna?",
             ["w szkole", "w szpitalu", "w sklepie", "w biurze"], 1,
             "У тексті прямо: «w szpitalu» (у лікарні)."),
    Question("c2", Module.CZYTANIE, "A2",
             "Anna pracuje jako pielęgniarka. — Kim jest Anna z zawodu?",
             ["nauczycielką", "pielęgniarką", "lekarką", "sprzedawczynią"], 1,
             "«pielęgniarka» = медсестра."),
    Question("c3", Module.CZYTANIE, "B1",
             "Choć pogoda była fatalna, postanowiliśmy nie odwoływać wycieczki. "
             "— Czy odwołali wycieczkę?",
             ["Tak", "Nie", "Nie wiadomo", "Częściowo"], 1,
             "«nie odwoływać» = не скасовувати → Nie. «Choć» = хоча."),
    Question("c4", Module.CZYTANIE, "A1", "Co znaczy «dziękuję»?",
             ["вибач", "дякую", "будь ласка", "до побачення"], 1,
             "dziękuję = дякую."),
    Question("c5", Module.CZYTANIE, "B1", "«Urząd» to po ukraińsku...",
             ["лікарня", "установа / відомство", "магазин", "школа"], 1,
             "urząd = установа/відомство (важливо для резиденції: urząd wojewódzki)."),
    Question("c6", Module.CZYTANIE, "B1", "Fałszywy przyjaciel: polskie «sklep» znaczy...",
             ["склеп / гробниця", "магазин", "підвал", "шафа"], 1,
             "«Фальшивий друг»: sklep = МАГАЗИН, не «склеп»!"),
    # --- Розширення банку (для варіативності тесту) ---
    Question("g13", Module.GRAMATYKA, "A1", "To są moje ___ (książka).",
             ["książka", "książki", "książkę", "książek"], 1,
             "Множина називного: książka → książki («мої книжки»)."),
    Question("g14", Module.GRAMATYKA, "A2", "Nie mam ___ (czas).",
             ["czas", "czasu", "czasem", "czasie"], 1,
             "Заперечення «nie mam» → родовий: czas → czasu."),
    Question("g15", Module.GRAMATYKA, "B1", "Gdybym ___ czas, pomógłbym ci.",
             ["mam", "miał", "będę miał", "mieć"], 1,
             "Умовний: gdybym + минулий → gdybym miał («якби я мав»)."),
    Question("g16", Module.GRAMATYKA, "A2", "Jadę ___ Warszawy.",
             ["do", "na", "w", "z"], 0,
             "Напрямок до міста: «do» + родовий → do Warszawy."),
    Question("g17", Module.GRAMATYKA, "A2", "Spotkamy się ___ poniedziałek.",
             ["w", "na", "do", "o"], 0,
             "Дні тижня: «w» + biernik → w poniedziałek."),
    Question("g18", Module.GRAMATYKA, "B1", "To ___ film, jaki widziałem. (dobry)",
             ["dobry", "lepszy", "najlepszy", "dobrze"], 2,
             "Найвищий ступінь (нерегулярний): dobry → lepszy → najlepszy."),
    Question("g19", Module.GRAMATYKA, "A1", "___ się nazywasz?",
             ["Co", "Jak", "Gdzie", "Kiedy"], 1,
             "«Jak się nazywasz?» = Як тебе звати?"),
    Question("g20", Module.GRAMATYKA, "A2", "Uczę ___ polskiego.",
             ["się", "siebie", "sobie", "sam"], 0,
             "Зворотне дієслово: uczyć SIĘ («вчитися»)."),
    Question("g21", Module.GRAMATYKA, "B1", "Idę do lekarza, ___ jestem chory.",
             ["bo", "że", "żeby", "ani"], 0,
             "Причина: «bo» = тому що."),
    Question("g22", Module.GRAMATYKA, "A2", "Mój brat jest ___ ode mnie. (stary)",
             ["stary", "starszy", "najstarszy", "staro"], 1,
             "Вищий ступінь + «od»: starszy ode mnie («старший за мене»)."),
    Question("g23", Module.GRAMATYKA, "A1", "___ masz lat?",
             ["Ile", "Jak", "Co", "Gdzie"], 0,
             "«Ile masz lat?» = Скільки тобі років?"),
    Question("g24", Module.GRAMATYKA, "B1", "Studenci ___ egzamin wczoraj. (zdać)",
             ["zdali", "zdały", "zdać", "zdadzą"], 0,
             "Минулий, чоловічо-особовий (studenci): zdali."),
    Question("c7", Module.CZYTANIE, "A2",
             "Kasia lubi gotować. W weekend upiekła ciasto dla rodziny. "
             "— Co zrobiła Kasia w weekend?",
             ["ugotowała zupę", "upiekła ciasto", "kupiła ciasto", "nic"], 1,
             "«upiekła ciasto» = спекла торт/пиріг."),
    Question("c8", Module.CZYTANIE, "B1",
             "Mimo że był zmęczony, poszedł na trening. — Czy poszedł na trening?",
             ["Tak", "Nie", "Nie wiadomo", "Później"], 0,
             "«Mimo że» = попри те що → усе одно пішов → Tak."),
    Question("c9", Module.CZYTANIE, "A1", "Co znaczy «pociąg»?",
             ["потяг", "автобус", "літак", "корабель"], 0,
             "pociąg = потяг."),
    Question("c10", Module.CZYTANIE, "B1", "Fałszywy przyjaciel: «dywan» znaczy...",
             ["диван", "килим", "стіл", "шафа"], 1,
             "Пастка! dywan = КИЛИМ, а диван — kanapa/sofa."),
    Question("c11", Module.CZYTANIE, "A2",
             "Sklep: pon–pt 9–18, sob 9–14, niedziela nieczynne. — Czy pracuje w niedzielę?",
             ["Tak", "Nie", "Tylko rano", "Nie wiadomo"], 1,
             "«niedziela nieczynne» = у неділю зачинено → Nie."),
    Question("c12", Module.CZYTANIE, "B1", "«Zameldowanie» to po ukraińsku...",
             ["реєстрація місця проживання", "звільнення", "запрошення", "оплата"], 0,
             "zameldowanie = реєстрація місця проживання (важливо для pobytu)."),
]


def _level_from_pct(pct: int) -> str:
    if pct < 40:
        return "A1"
    if pct < 65:
        return "A2"
    if pct < 85:
        return "B1 (низький)"
    return "B1+"


def by_id(qid: str) -> Question | None:
    return next((q for q in QUESTIONS if q.id == qid), None)


def build_test(n_grammar: int = 12, n_reading: int = 6) -> list[Question]:
    """Випадковий збалансований тест (щоразу різні питання з банку)."""
    grammar = [q for q in QUESTIONS if q.module == Module.GRAMATYKA]
    reading = [q for q in QUESTIONS if q.module == Module.CZYTANIE]
    picked = random.sample(grammar, min(n_grammar, len(grammar)))
    picked += random.sample(reading, min(n_reading, len(reading)))
    random.shuffle(picked)
    return picked


def score(answers: dict[str, int]) -> PlacementResult:
    """Результат за {question_id: обраний_індекс}.

    per_module містить ЛИШЕ реально виміряні модулі (граматика/читання).
    Продуктивні (Pisanie/Mówienie) і Słuchanie тут НЕ оцінюються — їхня
    готовність зʼявляється, коли учень робить відповідні вправи (чесно).
    """
    by_module: dict[Module, list[bool]] = {}
    correct = 0
    for qid, chosen in answers.items():
        q = by_id(qid)
        if q is None:
            continue
        ok = chosen == q.correct
        correct += int(ok)
        by_module.setdefault(q.module, []).append(ok)

    total = sum(len(v) for v in by_module.values())
    overall = round(correct / total * 100) if total else 0
    per_module = {
        mod.value: round(sum(res) / len(res) * 100) for mod, res in by_module.items()
    }
    return PlacementResult(
        overall_pct=overall,
        level=_level_from_pct(overall),
        per_module=per_module,
        correct=correct,
        total=total,
    )
