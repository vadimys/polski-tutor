"""Debounce-middleware: гасить подвійний тап тієї ж кнопки, пропускає інші/пізніші."""

import time

import pytest

from app.bot.debounce_mw import DebounceMiddleware


class _Cb:
    def __init__(self, data: str, uid: int = 1) -> None:
        self.data = data
        self.from_user = type("U", (), {"id": uid})()
        self.answered = 0

    async def answer(self, *a, **k) -> None:
        self.answered += 1


@pytest.mark.asyncio
async def test_double_tap_swallowed():
    mw = DebounceMiddleware()
    calls = []

    async def handler(ev, data):
        calls.append(ev.data)
        return "ok"

    r1 = await mw(handler, _Cb("x"), {})
    cb2 = _Cb("x")
    r2 = await mw(handler, cb2, {})  # миттєвий дубль
    assert calls == ["x"] and r1 == "ok" and r2 is None and cb2.answered == 1


@pytest.mark.asyncio
async def test_different_buttons_pass():
    mw = DebounceMiddleware()
    calls = []

    async def handler(ev, data):
        calls.append(ev.data)

    await mw(handler, _Cb("a"), {})
    await mw(handler, _Cb("b"), {})
    await mw(handler, _Cb("a", uid=2), {})  # інший користувач
    assert calls == ["a", "b", "a"]


@pytest.mark.asyncio
async def test_passes_after_window():
    mw = DebounceMiddleware()
    mw._seen[(1, "x")] = time.monotonic() - 1.0  # тап був давно
    calls = []

    async def handler(ev, data):
        calls.append(1)

    await mw(handler, _Cb("x"), {})
    assert len(calls) == 1
