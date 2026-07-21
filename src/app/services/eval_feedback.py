"""Оцінювання ЯКОСТІ нашого AI-фідбеку (skill advanced-evaluation).

Накриває ВСІ три шляхи AI-оцінювання: письмо (pisanie), мовлення (mówienie) і
відкриті граматичні завдання (трансформація/opencheck). Дві шари (skill: спершу
детерміновані пре-чеки, тоді LLM-judge):

1. КОНТРАКТ (детерміновано, дешево, тестується, крутиться і в проді у лог):
   `contract_issues` (письмо), `speaking_contract`, `open_contract` — бали розпарсені
   й у межах шкали, є обовʼязкові секції, фідбек українською.
2. LLM-as-judge (`judge`, `speaking_judge`, `open_judge`) — direct scoring за офіційною
   рубрикою, evidence-before-score, «ігноруй довжину / не завищуй за впевнений тон»
   (мітигація length/authority bias). Judge на ІНШІЙ моделі (cheap/Haiku), ніж
   генератор (strong/Sonnet) → мітигуємо self-enhancement bias.

Калібрувальні фікстури — синтетичні ВХІДНІ проби (не офіційні ключі): свідомо слабка
робота має провалюватись, сильна — складатись; хибна відповідь має відхилятись.
"""

from __future__ import annotations

import re

from app.integrations import ai

_CYRILLIC = re.compile(r"[а-яіїєґ]", re.IGNORECASE)

# обовʼязкові секції фідбеку — контракт формату (з *_SYSTEM відповідних модулів)
_WRITING_REQUIRED = ("Помилки", "Порада", "Зразок")
_SPEAK_REQUIRED = ("Помилки", "Корисні фрази")


# ─────────────────────────── детерміновані контракти ───────────────────────────
def _missing_sections(feedback: str, required: tuple[str, ...]) -> list[str]:
    return [f"немає секції «{s}»" for s in required if s.lower() not in feedback.lower()]


def _score_bounds_issue(
    scores: tuple[int, ...] | None, bounds: list[tuple[int, int]]
) -> str | None:
    if scores is None:
        return "бали не розпарсено"
    if len(scores) != len(bounds):
        return f"к-сть балів ≠ {len(bounds)}: {scores}"
    if any(not (lo <= x <= hi) for x, (lo, hi) in zip(scores, bounds, strict=True)):
        return f"бал поза межами шкали: {scores}"
    return None


def _feedback_contract(
    feedback: str,
    scores: tuple[int, ...] | None,
    *,
    required: tuple[str, ...],
    bounds: list[tuple[int, int]],
) -> list[str]:
    """Спільний контроль фідбеку з балами (письмо/мовлення)."""
    if not (feedback or "").strip():
        return ["порожній фідбек"]
    issues: list[str] = []
    bad = _score_bounds_issue(scores, bounds)
    if bad:
        issues.append(bad)
    issues += _missing_sections(feedback, required)
    if not _CYRILLIC.search(feedback):
        issues.append("фідбек не українською")
    return issues


def contract_issues(feedback: str, scores: tuple[int, int, int] | None) -> list[str]:
    """Контракт фідбеку письма (офіц. шкала 0-10 × 3). Порожній список = все ок."""
    return _feedback_contract(
        feedback, scores, required=_WRITING_REQUIRED, bounds=[(0, 10)] * 3
    )


def speaking_contract(
    feedback: str, scores: tuple[int, int, int] | None, bounds: list[tuple[int, int]]
) -> list[str]:
    """Контракт фідбеку мовлення. bounds — межі шкали (wykonanie/gramatyka/słownictwo)."""
    return _feedback_contract(feedback, scores, required=_SPEAK_REQUIRED, bounds=bounds)


def open_contract(results: list[dict] | None, n: int) -> list[str]:
    """Контракт оцінки відкритих завдань: к-сть збіглась, кожен вердикт валідний."""
    if results is None:
        return ["немає результатів (None)"]
    issues: list[str] = []
    if len(results) != n:
        issues.append(f"к-сть results ≠ {n}: {len(results)}")
    for i, r in enumerate(results, 1):
        if not isinstance(r.get("ok"), bool):
            issues.append(f"#{i}: ok не bool")
        fb = str(r.get("feedback", "")).strip()
        if not fb:
            issues.append(f"#{i}: порожній фідбек")
        elif not _CYRILLIC.search(fb):
            issues.append(f"#{i}: фідбек не українською")
    return issues


# ─────────────────────────────── LLM-as-judge ───────────────────────────────
# 4 стандартні критерії (1-5) — спільні для всіх трьох judge, щоб _avg_verdict працював
_JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "rubric_adherence": {"type": "integer"},
        "error_accuracy": {"type": "integer"},
        "score_consistency": {"type": "integer"},
        "usefulness": {"type": "integer"},
        "evidence": {"type": "string"},
        "issues": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "rubric_adherence", "error_accuracy", "score_consistency", "usefulness", "evidence", "issues",
    ],
    "additionalProperties": False,
}

_JUDGE_RUBRIC = (
    "Спершу наведи докази (evidence), потім бали. Ігноруй довжину відповіді. Не завищуй "
    "за впевнений тон. Для кожного критерію (шкала 1-5):\n"
    "• rubric_adherence — чи спирається оцінка на офіційні критерії;\n"
    "• error_accuracy — чи вказані помилки справді помилки й виправлення коректні;\n"
    "• score_consistency — чи вердикт/бали узгоджені з переліченими помилками;\n"
    "• usefulness — чи конкретна й дієва оцінка для учня.\n"
    "Дай по кожному критерію бал 1-5, докази (evidence) й перелік проблем (issues)."
)

_WRITING_JUDGE_SYSTEM = (
    "Ти — старший методист польської, який ПЕРЕВІРЯЄ ЯКІСТЬ фідбеку іншого репетитора "
    "на письмову роботу учня рівня B1 (офіційна шкала: wykonanie 0-10, środki 0-10, "
    "poprawność 0-10). Оцінюєш НЕ роботу учня, а сам ФІДБЕК.\n" + _JUDGE_RUBRIC
)

_SPEAK_JUDGE_SYSTEM = (
    "Ти — старший методист польської, який ПЕРЕВІРЯЄ ЯКІСТЬ фідбеку на УСНУ відповідь "
    "учня B1 (за транскриптом; шкала wykonanie / gramatyka 0-8 / słownictwo 0-8). "
    "Оцінюєш НЕ відповідь учня, а сам ФІДБЕК. Врахуй: фонетику й плавність із тексту "
    "оцінювати НЕ можна — добрий фідбек це чесно зазначає, а не вигадує.\n" + _JUDGE_RUBRIC
)

_OPEN_JUDGE_SYSTEM = (
    "Ти — старший методист польської, який ПЕРЕВІРЯЄ ЯКІСТЬ автоматичної оцінки "
    "граматичної трансформації B1. Дано оригінал, обовʼязкове слово, офіційний зразок, "
    "відповідь студента і ВЕРДИКТ (зараховано/ні + фідбек). Оцінюєш НЕ студента, а якість "
    "самого ВЕРДИКТУ: чи правильно він зарахував/відхилив і чи корисний фідбек.\n" + _JUDGE_RUBRIC
)


async def _judge(system: str, prompt: str) -> dict | None:
    """LLM-as-judge на cheap-моделі (не strong-генератор) → self-enhancement bias↓."""
    out = await ai.ask_json(system, prompt, _JUDGE_SCHEMA, max_tokens=700, cache=True, label="eval")
    return out if isinstance(out, dict) else None


async def judge(
    task: str, answer: str, feedback: str, scores: tuple[int, int, int] | None
) -> dict | None:
    """Judge якості фідбеку письма. None якщо AI вимкнено/збій."""
    prompt = (
        f"ЗАВДАННЯ учневі:\n{task}\n\n"
        f"ВІДПОВІДЬ учня:\n«{answer}»\n\n"
        f"ФІДБЕК репетитора (оцінюєш ЙОГО):\n{feedback}\n\n"
        f"Виставлені бали (wykonanie, środki, poprawność): {scores}\n\n"
        "Оціни якість фідбеку за 4 критеріями. Спершу докази (evidence), тоді бали."
    )
    return await _judge(_WRITING_JUDGE_SYSTEM, prompt)


async def speaking_judge(
    task: str, transcript: str, feedback: str, scores: tuple[int, int, int] | None
) -> dict | None:
    """Judge якості фідбеку мовлення."""
    prompt = (
        f"ЗАВДАННЯ учневі:\n{task}\n\n"
        f"ТРАНСКРИПТ відповіді учня:\n«{transcript}»\n\n"
        f"ФІДБЕК репетитора (оцінюєш ЙОГО):\n{feedback}\n\n"
        f"Виставлені бали (wykonanie, gramatyka, słownictwo): {scores}\n\n"
        "Оціни якість фідбеку за 4 критеріями. Спершу докази (evidence), тоді бали."
    )
    return await _judge(_SPEAK_JUDGE_SYSTEM, prompt)


async def open_judge(item: dict, verdict: dict | None) -> dict | None:
    """Judge якості вердикту відкритого завдання (зараховано/ні + фідбек)."""
    v = verdict or {}
    prompt = (
        f"Оригінал: {item.get('original')}\n"
        f"Обовʼязкове слово: {item.get('word')}\n"
        f"Офіційний зразок: {' / '.join(item.get('models', []))}\n"
        f"Відповідь студента: {item.get('answer') or '(порожньо)'}\n\n"
        f"ВЕРДИКТ (оцінюєш ЙОГО): {'зараховано' if v.get('ok') else 'НЕ зараховано'}\n"
        f"Фідбек вердикту: {v.get('feedback', '')}\n\n"
        "Оціни якість вердикту за 4 критеріями. Спершу докази (evidence), тоді бали."
    )
    return await _judge(_OPEN_JUDGE_SYSTEM, prompt)


# ───────────────────────────────── рендер ─────────────────────────────────
def _yn(b: bool) -> str:
    return "✓" if b else "✗"


def _avg_verdict(v: dict) -> float:
    keys = ("rubric_adherence", "error_accuracy", "score_consistency", "usefulness")
    vals = [v[k] for k in keys if isinstance(v.get(k), (int, float))]
    return round(sum(vals) / len(vals), 1) if vals else 0.0


def render_calibration(rows: list[dict], *, title: str = "Калібрування фідбеку") -> str:
    """Звіт калібрування: чи збігається очікуваний вердикт із фактичним + контракт + judge."""
    if not rows:
        return "🧪 Немає результатів калібрування."
    lines = [f"🧪 <b>{title}</b>\n"]
    for r in rows:
        detail = r.get("detail") or (f"{sum(r['scores'])}/30" if r.get("scores") else "—")
        mark = "✅" if r["got_pass"] == r["expect_pass"] else "⚠️"
        lines.append(
            f"{mark} <b>{r['level']}</b>: {detail} "
            f"(очікув. {_yn(r['expect_pass'])} · факт {_yn(r['got_pass'])})"
        )
        if r.get("contract"):
            lines.append("   ⛔ контракт: " + "; ".join(r["contract"]))
        v = r.get("verdict")
        if v:
            avg = _avg_verdict(v)
            issues = "; ".join(v["issues"][:2]) if v.get("issues") else ""
            lines.append(f"   ⚖️ judge: {avg}/5 сер." + (f" · {issues}" if issues else ""))
    mism = sum(1 for r in rows if r["got_pass"] != r["expect_pass"])
    lines.append(
        f"\n{'✅ Калібрування ок.' if not mism else f'⚠️ Розбіжностей: {mism} — перевір суворість.'}"
    )
    return "\n".join(lines)


# ─────────────────────────── калібрувальні фікстури ───────────────────────────
# Синтетичні ВХІДНІ проби (не офіційні ключі) — дозволено правилом official-only.
_WRITING_FIXTURES: list[dict] = [
    {
        "level": "свідомо слабка",
        "answer_a": "Ja pisać list. Pogoda dobre. Ja lubić. Do widzenia.",
        "answer_b": "To jest ok. Ja nie wiem co pisać tu. Koniec.",
        "expect_pass": False,
    },
    {
        "level": "сильна",
        "answer_a": (
            "Cześć Aniu! Dziękuję za zaproszenie na urodziny. Bardzo chętnie przyjadę "
            "w sobotę. Zastanawiam się, co Ci kupić w prezencie — może książkę, którą "
            "od dawna chciałaś przeczytać? Daj znać, o której mam być. Do zobaczenia!"
        ),
        "answer_b": (
            "Szanowni Państwo, chciałabym zarezerwować stolik na cztery osoby w piątek "
            "wieczorem o godzinie dziewiętnastej. Proszę o potwierdzenie rezerwacji "
            "mailem. Z poważaniem, Maria Kowalska."
        ),
        "expect_pass": True,
    },
]

_SPEAK_FIXTURES: list[dict] = [
    {
        "level": "свідомо слабка",
        "transcript": "Ja lubić film. Film dobre. Ja oglądać wczoraj. Nie wiem co mówić. To ładne. Koniec.",
        "expect_pass": False,
    },
    {
        "level": "сильна",
        "transcript": (
            "Film, który najlepiej pamiętam, to «Zielona mila». Obejrzałem go kilka lat "
            "temu i zrobił na mnie ogromne wrażenie. Akcja rozgrywa się w więzieniu, a "
            "główny bohater jest strażnikiem, który poznaje niezwykłego więźnia. Najbardziej "
            "podobało mi się to, że film porusza ważne tematy: sprawiedliwość i współczucie. "
            "Aktorzy grali znakomicie, a muzyka pasowała do nastroju. Po seansie długo "
            "myślałem o zakończeniu, bo było bardzo wzruszające. Poleciłbym ten film każdemu, "
            "kto lubi poważne, refleksyjne historie."
        ),
        "expect_pass": True,
    },
]

_OPEN_FIXTURES: list[dict] = [
    {
        "level": "правильна трансформація",
        "item": {
            "original": "Jan jest starszy od Anny.",
            "word": "młodsza",
            "models": ["Anna jest młodsza od Jana."],
            "answer": "Anna jest młodsza od Jana.",
        },
        "expect_ok": True,
    },
    {
        "level": "хибна (не те слово + інший сенс)",
        "item": {
            "original": "Trzeba posprzątać mieszkanie.",
            "word": "musimy",
            "models": ["Musimy posprzątać mieszkanie."],
            "answer": "Posprzątałem wczoraj.",
        },
        "expect_ok": False,
    },
]


async def run_calibration() -> list[dict]:
    """Калібрування фідбеку ПИСЬМА: фікстури → фідбек + контракт + judge."""
    from app.services import writing

    ws = writing.pick_set()
    task = f"a ({ws.a.genre}): {ws.a.prompt}\nb ({ws.b.genre}): {ws.b.prompt}"
    rows: list[dict] = []
    for fx in _WRITING_FIXTURES:
        fb, scores = await writing.feedback(ws, fx["answer_a"], fx["answer_b"])
        verdict = await judge(task, f"a: {fx['answer_a']}\nb: {fx['answer_b']}", fb, scores)
        rows.append(
            {
                "level": fx["level"],
                "scores": scores,
                "expect_pass": fx["expect_pass"],
                "got_pass": (sum(scores) >= 15) if scores else False,
                "contract": contract_issues(fb, scores),
                "verdict": verdict,
            }
        )
    return rows


async def run_speaking_calibration() -> list[dict]:
    """Калібрування фідбеку МОВЛЕННЯ: фікстури → фідбек + контракт + judge."""
    from app.services import speaking

    task = next((t for t in speaking.TASKS if t.kind == "monolog"), speaking.TASKS[0])
    bounds = [(0, task.max_wykonanie), (0, 8), (0, 8)]
    rows: list[dict] = []
    for fx in _SPEAK_FIXTURES:
        fb, scores = await speaking.feedback(task, fx["transcript"])
        pct = speaking.readiness_pct(task, *scores) if scores else 0
        verdict = await speaking_judge(task.prompt, fx["transcript"], fb, scores)
        rows.append(
            {
                "level": fx["level"],
                "detail": f"{pct}%",
                "expect_pass": fx["expect_pass"],
                "got_pass": pct >= 50,
                "contract": speaking_contract(fb, scores, bounds),
                "verdict": verdict,
            }
        )
    return rows


async def run_open_calibration() -> list[dict]:
    """Калібрування оцінки ВІДКРИТИХ завдань: фікстури → grade + контракт + judge."""
    from app.services import opencheck

    items = [{"n": i + 1, **fx["item"]} for i, fx in enumerate(_OPEN_FIXTURES)]
    graded = await opencheck.grade(items)
    contract = open_contract(graded, len(items))
    rows: list[dict] = []
    for i, fx in enumerate(_OPEN_FIXTURES):
        g = graded[i] if graded and i < len(graded) else None
        got_ok = bool(g["ok"]) if g else False
        verdict = await open_judge(items[i], g) if g else None
        # контракт — по всьому набору; кріпимо до першого рядка, щоб не дублювати
        rows.append(
            {
                "level": fx["level"],
                "detail": "зараховано" if got_ok else "не зараховано",
                "expect_pass": fx["expect_ok"],
                "got_pass": got_ok,
                "contract": contract if i == 0 else [],
                "verdict": verdict,
            }
        )
    return rows
