"""SayCleanup-middleware: прибирає вимову при навігації, не чіпає при самому 🔊."""

import pytest

from app.bot import say_cleanup_mw
from app.bot.say_cleanup_mw import SayCleanupMiddleware


class _Msg:
    chat = type("C", (), {"id": 55})()


class _Cb:
    def __init__(self, data):
        self.data = data
        self.message = _Msg()


@pytest.fixture
def spy(monkeypatch):
    calls = []

    async def fake_forget(bot, chat_id):
        calls.append(chat_id)

    monkeypatch.setattr(say_cleanup_mw.tts_say, "forget_voice", fake_forget)
    return calls


async def _run(cb, data):
    async def handler(ev, d):
        return "ok"

    return await SayCleanupMiddleware()(handler, cb, data)


@pytest.mark.asyncio
async def test_navigation_clears_voice(spy):
    r = await _run(_Cb("lesson:start"), {"bot": object()})
    assert r == "ok" and spy == [55]


@pytest.mark.asyncio
async def test_say_callback_not_cleared(spy):
    await _run(_Cb("say:abc123"), {"bot": object()})
    assert spy == []  # сам 🔊 не чіпаємо (say-хендлер сам керує)


@pytest.mark.asyncio
async def test_no_bot_noop(spy):
    await _run(_Cb("menu:home"), {})  # нема bot у data
    assert spy == []
