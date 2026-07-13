"""Оцінювання ЯКОСТІ нашого AI-фідбеку письма (skill advanced-evaluation).

Дві шари (skill: детерміновані пре-чеки → LLM-judge):
1. `contract_issues` — ДЕТЕРМІНОВАНІ перевірки контракту фідбеку (бали розпарсені й у
   0-10, є обовʼязкові секції, українською). Дешево, тестується, крутиться і в проді (лог).
2. LLM-as-judge (`judge`) — direct scoring за ОФІЦІЙНОЮ рубрикою B1, evidence-before-score.
   Judge на ІНШІЙ моделі (cheap/Haiku), ніж генератор (strong/Sonnet) → мітигуємо
   self-enhancement bias. Калібрувальні фікстури — синтетичні ВХІДНІ проби (не офіційні
   ключі): свідомо слабка робота має провалюватись, сильна — складатись.
"""

from __future__ import annotations

import json
import re

from app.integrations import ai

# обовʼязкові секції фідбеку (з writing._SYSTEM) — контракт формату
_REQUIRED = ("Помилки", "Порада", "Зразок")
_CYRILLIC = re.compile(r"[а-яіїєґ]", re.IGNORECASE)


def contract_issues(feedback: str, scores: tuple[int, int, int] | None) -> list[str]:
    """Детермінований контроль контракту. Порожній список = все ок."""
    issues: list[str] = []
    if not (feedback or "").strip():
        issues.append("порожній фідбек")
        return issues
    if scores is None:
        issues.append("не розпарсено рядок WYNIK (бали)")
    else:
        if any(not (0 <= x <= 10) for x in scores):
            issues.append(f"бал поза 0-10: {scores}")
    for sec in _REQUIRED:
        if sec.lower() not in feedback.lower():
            issues.append(f"немає секції «{sec}»")
    if not _CYRILLIC.search(feedback):
        issues.append("фідбек не українською")
    return issues


_JUDGE_SYSTEM = (
    "Ти — старший методист польської, який ПЕРЕВІРЯЄ ЯКІСТЬ фідбеку іншого репетитора "
    "на письмову роботу учня рівня B1 (офіційна шкала: wykonanie 0-10, środki 0-10, "
    "poprawność 0-10). Оцінюєш НЕ роботу учня, а сам ФІДБЕК. Спершу наведи докази, потім бал.\n"
    "Ігноруй довжину відповіді. Не завищуй за впевнений тон. Для кожного критерію (шкала 1-5):\n"
    "• rubric_adherence — чи спирається фідбек на 3 офіційні критерії;\n"
    "• error_accuracy — чи вказані помилки справді помилки й виправлення коректні;\n"
    "• score_consistency — чи виставлені бали узгоджені з переліченими помилками;\n"
    "• usefulness — чи конкретний і дієвий фідбек для учня.\n"
    "Відповідь — СТРОГО JSON: {\"rubric_adherence\":N,\"error_accuracy\":N,"
    "\"score_consistency\":N,\"usefulness\":N,\"evidence\":\"...\",\"issues\":[\"...\"]}"
)


def _judge_prompt(task: str, answer: str, feedback: str, scores: tuple[int, int, int] | None) -> str:
    return (
        f"ЗАВДАННЯ учневі:\n{task}\n\n"
        f"ВІДПОВІДЬ учня:\n«{answer}»\n\n"
        f"ФІДБЕК репетитора (оцінюєш ЙОГО):\n{feedback}\n\n"
        f"Виставлені бали (wykonanie, środki, poprawność): {scores}\n\n"
        "Оціни якість фідбеку за 4 критеріями. Спершу докази (evidence), тоді бали."
    )


def parse_verdict(raw: str) -> dict | None:
    """Витягти JSON-вердикт із відповіді judge (толерантно до обгортки)."""
    m = re.search(r"\{.*\}", raw or "", re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except (ValueError, TypeError):
        return None


async def judge(task: str, answer: str, feedback: str, scores: tuple[int, int, int] | None) -> dict | None:
    """LLM-as-judge на ІНШІЙ моделі (cheap), ніж генератор (strong). None якщо AI вимкнено."""
    out = await ai.ask(_JUDGE_SYSTEM, _judge_prompt(task, answer, feedback, scores), max_tokens=700)
    return parse_verdict(out) if out else None


def render_calibration(rows: list[dict]) -> str:
    """Звіт калібрування: чи слабкі роботи провалюються, сильні складаються, контракт цілий."""
    if not rows:
        return "🧪 Немає результатів калібрування."
    lines = ["🧪 <b>Калібрування фідбеку письма</b>\n"]
    for r in rows:
        total = sum(r["scores"]) if r.get("scores") else 0
        mark = "✅" if r["got_pass"] == r["expect_pass"] else "⚠️"
        lines.append(
            f"{mark} <b>{r['level']}</b>: {total}/30 "
            f"(очікували {'скл.' if r['expect_pass'] else 'незд.'}, "
            f"вийшло {'скл.' if r['got_pass'] else 'незд.'})"
        )
        if r.get("contract"):
            lines.append("   ⛔ контракт: " + "; ".join(r["contract"]))
        v = r.get("verdict")
        if v:
            avg = _avg_verdict(v)
            lines.append(f"   ⚖️ judge: {avg}/5 сер." + (f" · {'; '.join(v['issues'][:2])}" if v.get("issues") else ""))
    mism = sum(1 for r in rows if r["got_pass"] != r["expect_pass"])
    lines.append(f"\n{'✅ Калібрування ок.' if not mism else f'⚠️ Розбіжностей: {mism} — перевір суворість.'}")
    return "\n".join(lines)


def _avg_verdict(v: dict) -> float:
    keys = ("rubric_adherence", "error_accuracy", "score_consistency", "usefulness")
    vals = [v[k] for k in keys if isinstance(v.get(k), (int, float))]
    return round(sum(vals) / len(vals), 1) if vals else 0.0


# Синтетичні калібрувальні проби (ВХІДНІ дані, не офіційні ключі): свідомо слабка
# робота має провалюватись (<15/30), сильна — складатись. Ловлять «занадто мʼякий»
# або «занадто суворий» оцінювач + злам контракту фідбеку.
FIXTURES: list[dict] = [
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


async def run_calibration() -> list[dict]:
    """Прогнати фікстури через наш фідбек + контракт + judge → рядки для звіту."""
    from app.services import writing

    ws = writing.pick_set()
    task = f"a ({ws.a.genre}): {ws.a.prompt}\nb ({ws.b.genre}): {ws.b.prompt}"
    rows: list[dict] = []
    for fx in FIXTURES:
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
