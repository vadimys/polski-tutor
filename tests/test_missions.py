"""Місії: детермінований щоденний вибір (без Redis — claim перевіряється наживо)."""

from app.services import missions


def test_daily_mission_deterministic():
    m1 = missions.daily_mission(123, "2026-07-08")
    m2 = missions.daily_mission(123, "2026-07-08")
    assert m1 == m2
    assert m1["id"] and m1["xp"] > 0 and m1["kinds"]


def test_daily_mission_from_pool():
    ids = {m["id"] for m in missions._DAILY}
    for day in range(1, 20):
        m = missions.daily_mission(777, f"2026-07-{day:02d}")
        assert m["id"] in ids


def test_different_users_can_differ():
    got = {missions.daily_mission(u, "2026-07-08")["id"] for u in range(30)}
    assert len(got) >= 2  # ротація дає різні місії різним користувачам
