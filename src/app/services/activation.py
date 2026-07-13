"""Активація нового учня — перші кроки до «aha» (skill onboarding).

Аха-момент: «бот знає мій рівень і дає реальну підготовку до B1». Ведемо до нього
через ОДИН наступний крок + видимий прогрес чеклиста (мотивація). Кроки виводимо
з наявних сигналів (placement/сесії/слова/серія) — без нового сховища.
"""

from __future__ import annotations

# (ключ, рядок чеклиста, короткий підпис кнопки, callback запуску) — за цінністю
STEPS: list[tuple[str, str, str, str]] = [
    ("placement", "Пройти стартовий тест — визначу твій рівень", "📝 Стартовий тест", "placement:start"),
    ("exercise", "Зробити першу вправу (реальний формат іспиту)", "⚡ Перша вправа", "coach:now"),
    ("word", "Додати перше слово в памʼять", "🔁 Повторення слів", "review:start"),
    ("habit", "Повернутися завтра — серія 2 дні поспіль", "⚡ Навчатись", "coach:now"),
]


async def checklist(user_id: int) -> list[dict]:
    """Стан кроків активації для учня (done — з наявних сигналів прогресу)."""
    from app.services import progress, vocab
    from app.services import state as user_state

    st = await user_state.load(user_id)
    total_sessions, _ = await progress.counts(user_id)
    words = await vocab.count(user_id)
    done = {
        "placement": st.placement_done,
        "exercise": total_sessions > 0,
        "word": words > 0,
        "habit": st.streak >= 2,
    }
    return [
        {"key": k, "label": lbl, "short": short, "cb": cb, "done": done[k]}
        for k, lbl, short, cb in STEPS
    ]


def next_step(steps: list[dict]) -> dict | None:
    """Перший невиконаний крок (фокус сесії — one goal per session)."""
    return next((s for s in steps if not s["done"]), None)


def all_done(steps: list[dict]) -> bool:
    return all(s["done"] for s in steps)


def render(steps: list[dict]) -> str:
    n = sum(1 for s in steps if s["done"])
    head = (
        f"🚀 <b>З чого почати</b> ({n}/{len(steps)})\n"
        "<i>Перші кроки до впевненого B1:</i>\n"
    )
    lines = [("✅ " if s["done"] else "◻️ ") + s["label"] for s in steps]
    return head + "\n".join(lines)
