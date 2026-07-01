"""Внутрішній HTTP /health — для docker healthcheck та моніторингу.

Порт 8080 усередині контейнера (не публікується назовні). Перевіряє живий
конект до Postgres і Redis; 200 якщо все ок, 503 якщо щось лежить.
"""

from __future__ import annotations

import logging

from aiohttp import web
from redis.asyncio import Redis
from sqlalchemy import text

from app.config import settings
from app.db.base import engine

logger = logging.getLogger(__name__)

_runner: web.AppRunner | None = None  # утримуємо посилання, щоб сервер не збирався GC


async def _health(_request: web.Request) -> web.Response:
    detail: dict[str, str] = {}
    ok = True
    try:
        async with engine().connect() as conn:
            await conn.execute(text("SELECT 1"))
        detail["db"] = "ok"
    except Exception:  # noqa: BLE001 — health не має падати сам
        ok = False
        detail["db"] = "fail"
    try:
        r = Redis.from_url(settings.redis_url)
        await r.ping()
        await r.aclose()
        detail["redis"] = "ok"
    except Exception:  # noqa: BLE001
        ok = False
        detail["redis"] = "fail"
    return web.json_response(
        {"status": "ok" if ok else "degraded", **detail},
        status=200 if ok else 503,
    )


async def start_health_server(port: int = 8080) -> None:
    """Піднімає /health на event loop бота (fire-and-forget)."""
    global _runner
    app = web.Application()
    app.router.add_get("/health", _health)
    _runner = web.AppRunner(app)
    await _runner.setup()
    site = web.TCPSite(_runner, "0.0.0.0", port)
    await site.start()
    logger.info("Health-сервер на :%d/health", port)
