"""Стартовий placement-тест: банк питань (A1→B1) + скоринг по модулях.

Об'єктивні MCQ-питання вимірюють Gramatykę і Czytanie (включно з лексикою).
Продуктивні модулі (Pisanie/Mówienie) і Słuchanie аудіо тут не тестуються —
їхня готовність виставляється консервативно від загального рівня й уточнюється
в перших уроках. Так чесніше, ніж вдавати точність там, де її немає.
"""

from __future__ import annotations

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
]


def _level_from_pct(pct: int) -> str:
    if pct < 40:
        return "A1"
    if pct < 65:
        return "A2"
    if pct < 85:
        return "B1 (низький)"
    return "B1+"


def score(answers: dict[str, int]) -> PlacementResult:
    """Порахувати результат за словником {question_id: обраний_індекс}."""
    by_module: dict[Module, list[bool]] = {}
    correct = 0
    for q in QUESTIONS:
        if q.id not in answers:
            continue
        ok = answers[q.id] == q.correct
        correct += int(ok)
        by_module.setdefault(q.module, []).append(ok)

    total = sum(len(v) for v in by_module.values())
    overall = round(correct / total * 100) if total else 0

    per_module: dict[str, int] = {}
    # виміряні модулі — реальний %
    for mod, results in by_module.items():
        per_module[mod.value] = round(sum(results) / len(results) * 100)
    # невиміряні — консервативна оцінка від загального рівня
    if Module.SLUCHANIE.value not in per_module:
        per_module[Module.SLUCHANIE.value] = round(overall * 0.8)
    if Module.PISANIE.value not in per_module:
        per_module[Module.PISANIE.value] = round(overall * 0.5)
    if Module.MOWIENIE.value not in per_module:
        per_module[Module.MOWIENIE.value] = round(overall * 0.5)

    return PlacementResult(
        overall_pct=overall,
        level=_level_from_pct(overall),
        per_module=per_module,
        correct=correct,
        total=total,
    )
