"""Груповий лідерборд: рейтинг учнів за стріком і готовністю (мотивація когорти).

Best-practice: винагороджуємо РЕГУЛЯРНІСТЬ (стрік) насамперед, тоді готовність.
Дані беремо зі збереженого стану (streak/readiness) — без важкого перерахунку.
"""

from __future__ import annotations

from sqlalchemy import select

from app.db.base import session_factory
from app.db.models import User
from app.services import quest

_MEDALS = ("🥇", "🥈", "🥉")


async def board(ids: list[int]) -> list[dict]:
    """Рейтинг учнів (за стріком ↓, тоді готовність ↓). [{id,name,streak,overall,rank}]."""
    if not ids:
        return []
    async with session_factory()() as s:
        users = list((await s.execute(select(User).where(User.id.in_(ids)))).scalars().all())
    rows = [
        {
            "id": u.id,
            "name": f"@{u.username}" if u.username else f"учень{u.id % 10000}",
            "streak": u.streak,
            "overall": quest.overall_pct(u.readiness or {}),
        }
        for u in users
    ]
    rows.sort(key=lambda r: (r["streak"], r["overall"]), reverse=True)
    for i, r in enumerate(rows):
        r["rank"] = i + 1
    return rows


def render(rows: list[dict], title: str, highlight_id: int | None = None) -> str:
    if not rows:
        return f"🏆 <b>{title}</b>\nПоки немає учнів для рейтингу."
    lines = [f"🏆 <b>{title}</b>", "<i>Рейтинг за серією 🔥 (регулярність), тоді готовністю 🏁.</i>\n"]
    for r in rows:
        mark = _MEDALS[r["rank"] - 1] if r["rank"] <= 3 else f"{r['rank']}."
        me = " ← ти" if highlight_id and r["id"] == highlight_id else ""
        lines.append(f"{mark} {r['name']} · 🔥{r['streak']} · 🏁{r['overall']}%{me}")
    return "\n".join(lines)
