"""Повний reset прогресу: оркестратор чистить УСІ підсистеми (нічого не забуто)."""

from app.services import goals, mistakes, progress, state, vocab


async def test_full_reset_calls_all_subsystems(monkeypatch):
    called: list[tuple[str, int]] = []

    async def rp(uid):
        called.append(("reset_progress", uid))

    async def g(uid):
        called.append(("goals", uid))

    async def m(uid):
        called.append(("mistakes", uid))

    async def p(uid):
        called.append(("progress", uid))

    async def v(uid):
        called.append(("vocab", uid))

    monkeypatch.setattr(state, "reset_progress", rp)
    monkeypatch.setattr(goals, "reset", g)
    monkeypatch.setattr(mistakes, "clear", m)
    monkeypatch.setattr(progress, "reset_marks", p)
    monkeypatch.setattr(vocab, "reset", v)

    await state.full_reset(42)

    names = [c[0] for c in called]
    assert names == ["reset_progress", "goals", "mistakes", "progress", "vocab"]
    assert all(c[1] == 42 for c in called)  # усе на того самого користувача
