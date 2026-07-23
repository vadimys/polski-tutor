"""Навчальні інструкції до продуктивних завдань (мовлення + письмо).

Що робить: перед записом/письмом показує учневі — 🎯 що від нього хочуть,
🪜 як будувати відповідь, 💬 корисні фрази, 📊 за чим оцінюють; окремою кнопкою —
📝 орієнтовний зразок СТРУКТУРИ (на нейтральній ситуації, щоб учити формат, а не
списувати конкретне завдання).

Джерело вимог і критеріїв — офіційні матеріали Держкомісії (визначення Zadań 1/2/3,
шкали wykonanie/gramatyka/słownictwo, metryczki form wypowiedzi). Зразки позначені як
ілюстративні моделі, а не «офіційні відповіді».
"""

from __future__ import annotations

from dataclasses import dataclass

# --- МОВЛЕННЯ (Mówienie) ---------------------------------------------------


@dataclass(frozen=True)
class SpeakGuide:
    goal: str
    steps: list[str]
    phrases: list[str]
    criteria: str
    example: str


_SPEAKING: dict[str, SpeakGuide] = {
    "sytuacja": SpeakGuide(
        goal=(
            "Це <b>рольова гра</b>: ти — учасник ситуації. Треба не переказати умову, а "
            "<b>розіграти розмову</b> й досягти мети (домовитися / переконати / забронювати)."
        ),
        steps=[
            "Відреагуй на співрозмовника (привітання / визнання його позиції)",
            "Чітко скажи, чого хочеш саме ти",
            "Наведи аргумент (чому це важливо / зручно)",
            "Запропонуй компроміс або зніми заперечення",
            "Підсумуй домовленість і спитай згоди",
        ],
        phrases=[
            "Proponuję, żeby… (Пропоную, щоб…)",
            "Może zrobimy tak, że…? (Може, зробимо так, що…?)",
            "Rozumiem Cię, ale wolałbym/wolałabym… (Розумію, але я б волів…)",
            "Zgadzam się, tylko… (Погоджуюсь, тільки…)",
            "Umówmy się, że… Co o tym myślisz? (Домовмося, що… Як тобі?)",
        ],
        criteria="Wykonanie 0-6 (чи досягнуто мети й усі кроки) · Gramatyka 0-8 · Słownictwo i styl 0-8.",
        example=(
            "🎭 <i>Ситуація (інша, для прикладу структури): друг кличе на каву, ти волієш чай.</i>\n\n"
            "«Cześć! Wiem, że masz ochotę na kawę, ale ja wolałbym herbatę — kawa nie służy mi "
            "wieczorem. Może pójdziemy do kawiarni, gdzie mają i jedno, i drugie? Ty zamówisz kawę, "
            "a ja herbatę. Umówmy się tak — pasuje Ci? Dla mnie to idealne rozwiązanie.»\n\n"
            "👆 Зверни увагу: <b>реакція → своя позиція → аргумент → компроміс → згода</b>."
        ),
    ),
    "monolog": SpeakGuide(
        goal=(
            "Зв'язне <b>монологічне висловлювання</b> на тему з <b>власною думкою й "
            "обґрунтуванням</b> (а не 1-2 речення)."
        ),
        steps=[
            "Вступ — про що говоритимеш / теза",
            "Розвиток — 2-3 думки, кожну підкріпи прикладом чи причиною",
            "Закінчення — підсумок і власна позиція",
        ],
        phrases=[
            "Moim zdaniem… (На мою думку…)",
            "Po pierwsze… po drugie… (По-перше… по-друге…)",
            "Na przykład… (Наприклад…)",
            "Dlatego uważam, że… (Тому вважаю, що…)",
            "Podsumowując… (Підсумовуючи…)",
        ],
        criteria="Wykonanie 0-7 (повнота, структура вступ-розвиток-закінчення) · Gramatyka 0-8 · Słownictwo i styl 0-8.",
        example=(
            "🎭 <i>Тема (для прикладу структури): улюблена пора року.</i>\n\n"
            "«Moją ulubioną porą roku jest jesień. Po pierwsze, lubię jesienne kolory — żółte i "
            "czerwone liście wyglądają pięknie. Po drugie, nie jest już gorąco, więc mogę dużo "
            "spacerować. Na przykład w weekendy chodzę do parku z rodziną. Dlatego uważam, że "
            "jesień to najprzyjemniejsza pora roku. Podsumowując — to czas spokoju i piękna.»\n\n"
            "👆 <b>вступ → 2 думки з прикладами → висновок</b>."
        ),
    ),
    "opis": SpeakGuide(
        goal=(
            "Описати фото за <b>трьома елементами</b>: <b>особи</b>, <b>місце</b>, <b>дії</b> — "
            "і коротко припустити контекст."
        ),
        steps=[
            "Загальний план — що зображено, де це відбувається",
            "Особи — хто, зовнішність, емоції, стосунки між ними",
            "Дії — що люди роблять",
            "Деталі — кольори, пора дня/року, задній план",
            "Коротке припущення / враження",
        ],
        phrases=[
            "Na zdjęciu widzę… (На фото я бачу…)",
            "Na pierwszym planie… / W tle… (На передньому плані… / На задньому…)",
            "Wygląda na to, że… (Схоже, що…)",
            "Wydaje mi się, że… (Мені здається, що…)",
            "Prawdopodobnie… (Ймовірно…)",
        ],
        criteria="Wykonanie 0-7 (три елементи + структура) · Gramatyka 0-8 · Słownictwo i styl 0-8.",
        example=(
            "🎭 <i>Для прикладу структури (без конкретного фото):</i>\n\n"
            "«Na zdjęciu widzę rodzinę w parku. Na pierwszym planie są rodzice i dwoje dzieci — "
            "wszyscy się uśmiechają, wyglądają na zadowolonych. Siedzą na kocu i jedzą kanapki. "
            "W tle widać drzewa i słońce, więc to chyba letni weekend. Wydaje mi się, że dobrze się "
            "razem bawią.»\n\n"
            "👆 <b>загальний план → особи → дії → деталі → припущення</b>."
        ),
    ),
}


def speaking_instruction(kind: str) -> str:
    g = _SPEAKING.get(kind)
    if g is None:
        return ""
    steps = "\n".join(f"{i}. {s}" for i, s in enumerate(g.steps, 1))
    phrases = "\n".join(f"• {p}" for p in g.phrases)
    return (
        f"🎯 <b>Що зробити:</b> {g.goal}\n\n"
        f"🪜 <b>Як будувати відповідь:</b>\n{steps}\n\n"
        f"💬 <b>Корисні фрази:</b>\n{phrases}\n\n"
        f"📊 <b>За чим оцінюю:</b> {g.criteria}"
    )


def speaking_example(kind: str) -> str:
    g = _SPEAKING.get(kind)
    return g.example if g is not None else "Зразок для цього завдання недоступний."


# --- Керована практика (крок-за-кроком) для продуктивних завдань ---

# Кроки для мовлення за типом завдання (інструкція + банк фраз на кожен крок)
_GUIDED_SPEAK: dict[str, list[tuple[str, list[str]]]] = {
    "sytuacja": [
        ("Крок 1/5 — Відреагуй на співрозмовника: привітайся і визнай його ідею.",
         ["Cześć! / Dzień dobry!", "Rozumiem, że chcesz…", "Wiem, że masz ochotę na…"]),
        ("Крок 2/5 — Скажи, чого хочеш ТИ (своя позиція).",
         ["Ale ja wolałbym / wolałabym…", "Wolę raczej…", "Mnie bardziej pasuje…"]),
        ("Крок 3/5 — Наведи аргумент: чому це для тебе важливо/зручно.",
         ["…bo… (…бо…)", "Dlatego że…", "Zależy mi na tym, ponieważ…"]),
        ("Крок 4/5 — Запропонуй компроміс.",
         ["Może zrobimy tak, że…?", "Proponuję kompromis:…", "A gdybyśmy…?"]),
        ("Крок 5/5 — Підсумуй домовленість і спитай згоди.",
         ["Umówmy się, że…", "Czyli robimy tak:…", "Co o tym myślisz? / Pasuje Ci?"]),
    ],
    "monolog": [
        ("Крок 1/4 — Вступ: назви тему й свою тезу (про що говоритимеш).",
         ["Chciałbym opowiedzieć o…", "Moim zdaniem…", "Ten temat jest ważny, bo…"]),
        ("Крок 2/4 — Перша думка + приклад.",
         ["Po pierwsze,…", "Na przykład…", "Widać to, gdy…"]),
        ("Крок 3/4 — Друга думка + приклад.",
         ["Po drugie,…", "Poza tym,…", "Innym przykładem jest…"]),
        ("Крок 4/4 — Висновок: підсумок і власна позиція.",
         ["Podsumowując,…", "Dlatego uważam, że…", "Właśnie dlatego…"]),
    ],
    "opis": [
        ("Крок 1/5 — Загальний план: що зображено й де.",
         ["Na zdjęciu widzę…", "Zdjęcie przedstawia…", "To jest…"]),
        ("Крок 2/5 — Особи: хто, зовнішність, емоції.",
         ["Na pierwszym planie…", "Widać osoby, które…", "Wyglądają na…"]),
        ("Крок 3/5 — Дії: що люди роблять.",
         ["Oni właśnie…", "W tym momencie…", "Wydaje się, że…"]),
        ("Крок 4/5 — Деталі: кольори, пора, задній план.",
         ["W tle…", "Dominują kolory…", "Prawdopodobnie jest to…"]),
        ("Крок 5/5 — Припущення / враження.",
         ["Myślę, że…", "Być może…", "Całość sprawia wrażenie…"]),
    ],
}

# Кроки для письма — універсальний офіційний лист (найпоширеніший і найстрашніший жанр)
_WRITING_STEPS: list[tuple[str, list[str]]] = [
    ("Крок 1/4 — Шапка: місце й дата (справа вгорі) + звертання.",
     ["Warszawa, 1.07.2026", "Szanowni Państwo,", "Szanowny Panie / Szanowna Pani,"]),
    ("Крок 2/4 — Вступ: мета звернення.",
     ["Zwracam się z uprzejmą prośbą o…", "Piszę w sprawie…", "Chciałbym / Chciałabym zapytać o…"]),
    ("Крок 3/4 — Розвиток: суть, деталі, аргументи (2–3 речення).",
     ["Sytuacja wygląda następująco:…", "W związku z tym…", "Załączam…"]),
    ("Крок 4/4 — Закінчення: ввічлива формула + підпис.",
     ["Z góry dziękuję za odpowiedź.", "Z poważaniem,", "Imię i nazwisko"]),
]


def _render_step(instr: str, phrases: list[str], write_hint: str) -> str:
    ph = "\n".join(f"• {p}" for p in phrases)
    return f"🪜 <b>{instr}</b>\n\n💬 Корисні фрази:\n{ph}\n\n{write_hint}"


def guided_speak_n(kind: str) -> int:
    return len(_GUIDED_SPEAK.get(kind, []))


def guided_speak_step(kind: str, i: int) -> str:
    instr, phrases = _GUIDED_SPEAK[kind][i]
    return _render_step(instr, phrases, "✍️ Напиши свою репліку польською (одним повідомленням).")


WRITING_STEPS_N = len(_WRITING_STEPS)


def writing_step(i: int) -> str:
    instr, phrases = _WRITING_STEPS[i]
    return _render_step(instr, phrases, "✍️ Напиши цю частину польською (одним повідомленням).")


def guided_available(kind: str) -> bool:
    return kind in _GUIDED_SPEAK


# --- ПИСЬМО (Pisanie) ------------------------------------------------------

# емодзі-бейджі жанрів (для дружньої картки завдання)
_GENRE_EMOJI = {
    "ogłoszenie": "📢",
    "list prywatny": "💌",
    "zaproszenie": "🎟",
    "recenzja": "⭐",
    "życzenia": "🎉",
    "charakterystyka": "🧑",
    "pozdrowienia": "✉️",
    "esej": "📝",
    "opowiadanie": "📖",
    "opis osoby": "🧑",
    "zawiadomienie": "📣",
    "sprawozdanie": "📄",
}


def genre_badge(genre: str) -> str:
    """Емодзі + назва жанру (для заголовків блоків завдань)."""
    return f"{_GENRE_EMOJI.get(genre, '📝')} {genre}"


def word_range(words: int) -> tuple[int, int]:
    """Розумний діапазон обсягу навколо норми.

    Пласке «±20» несправедливе для КОРОТКИХ форм: для ~30 слів воно дало б 10-50,
    а 10 слів — це вже не завдання. Тому допуск пропорційний (≈⅓ норми), але не більший
    за 20 слів (стеля для довгих форм) і не менший за 8 (мінімальний люфт для коротких).
    Напр.: 25→17-33 · 30→20-40 · 40→27-53 · 170→150-190 · 175→155-195.
    """
    tol = min(20, max(8, round(words / 3)))
    return max(1, words - tol), words + tol


def _range_hint(words: int) -> str:
    lo, hi = word_range(words)
    return f"~{words} слів (≈{lo}–{hi})"


def writing_instruction(
    a_genre: str, a_req: str, a_words: int, b_genre: str, b_req: str, b_words: int
) -> str:
    return (
        "🎯 <b>Що зробити:</b> виконай <b>обидва</b> завдання, кожне у своєму жанрі з усіма "
        "обов'язковими елементами форми. Тримайся приблизного обсягу (нижче за орієнтир "
        "втрачаєш бали за неповноту; трохи більше — не страшно).\n\n"
        f"🪜 <b>Завдання a — {genre_badge(a_genre)}</b> · {_range_hint(a_words)}. "
        f"Обов'язкові елементи:\n{a_req}\n\n"
        f"🪜 <b>Завдання b — {genre_badge(b_genre)}</b> · {_range_hint(b_words)}. "
        f"Обов'язкові елементи:\n{b_req}\n\n"
        "💬 <b>Регістр:</b> офіційно — <i>Szanowni Państwo… Z poważaniem</i>; "
        "приватно — <i>Cześć / Drogi X… Pozdrawiam / Ściskam</i>.\n\n"
        "📊 <b>За чим оцінюю (0-30, поріг 15):</b> Wykonanie 0-10 (жанр+елементи+обсяг) · "
        "Środki językowe 0-10 (багатство мови) · Poprawność 0-10 (граматика/орфографія)."
    )


def writing_example() -> str:
    return (
        "🎭 <i>Приклад структури короткої форми — ogłoszenie (оголошення):</i>\n\n"
        "«<b>OGŁOSZENIE</b>\n"
        "Uprzejmie informuję, że w sobotę 14 czerwca w godzinach 18:00–22:00 organizuję w moim "
        "mieszkaniu (nr 12) przyjęcie urodzinowe. Przepraszam za ewentualny hałas i proszę "
        "sąsiadów o wyrozumiałość. W razie problemów proszę o kontakt.\n"
        "Z góry dziękuję, Anna Kowalska (m. 12)»\n\n"
        "👆 Є всі елементи: <b>хто оголошує · з якою метою · що/де/коли · контакт/підпис</b>.\n"
        "Для довгої форми (list/opowiadanie тощо) тримай: <b>вступ → розвиток → закінчення</b> "
        "і всі обов'язкові елементи жанру, перелічені вище."
    )
