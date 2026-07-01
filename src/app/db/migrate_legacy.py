"""Одноразова міграція стану учнів зі старого сховища (Redis-JSON) у Postgres.

Ідемпотентна й безпечна: копіює лише тих користувачів, яких ще немає в БД.
Запускається на старті; будь-яка помилка — не фатальна (лог + пропуск).
"""

from __future__ import annotations

import json
import logging

from app.config import settings
from app.db.base import session_factory
from app.db.models import User

logger = logging.getLogger(__name__)


async def migrate_from_redis() -> int:
    from redis.asyncio import Redis

    r = Redis.from_url(settings.redis_url, decode_responses=True)
    migrated = 0
    try:
        ids = await r.smembers("polski:users")
        for sid in ids:
            uid = int(sid)
            async with session_factory()() as s:
                if await s.get(User, uid) is not None:
                    continue  # вже в Postgres
                raw = await r.get(f"polski:user:{uid}")
                if not raw:
                    continue
                d = json.loads(raw)
                s.add(
                    User(
                        id=uid,
                        level=d.get("level", "A1"),
                        streak=d.get("streak", 0),
                        last_lesson=d.get("last_lesson", ""),
                        placement_done=d.get("placement_done", False),
                        lesson_hour=d.get("lesson_hour", settings.lesson_hour),
                        readiness=d.get("readiness", {}),
                    )
                )
                await s.commit()
                migrated += 1
    except Exception:  # noqa: BLE001
        logger.exception("legacy migration skipped")
    finally:
        await r.aclose()
    return migrated
