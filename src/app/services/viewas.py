"""View-as: адмін тимчасово «дивиться очима» ролі (student/teacher/referred) для тесту.

Оверрайд рендеру/поведінки (Redis-прапор). ⚠️ Прогрес у адміна один — це тест UX/флоу,
не ізольовані дані. Для окремих історій навчання — вторинні тест-акаунти.
"""

from __future__ import annotations

from redis.asyncio import Redis

from app.config import settings

_MODES = ("student", "teacher", "referred")
_redis: Redis | None = None


def _r() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(user_id: int) -> str:
    return f"admin:viewas:{user_id}"


async def set_mode(user_id: int, mode: str) -> None:
    if mode in _MODES:
        await _r().set(_key(user_id), mode)


async def get(user_id: int) -> str:
    return str(await _r().get(_key(user_id)) or "")


async def clear(user_id: int) -> None:
    await _r().delete(_key(user_id))


def role_for(mode: str, real_role: str) -> str:
    """Ефективна роль для рендеру: teacher→teacher; student/referred→student; інакше реальна."""
    if mode == "teacher":
        return "teacher"
    if mode in ("student", "referred"):
        return "student"
    return real_role
