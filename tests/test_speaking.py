from app.services import speaking


def test_tasks_valid():
    ids = [t.id for t in speaking.TASKS]
    assert len(ids) == len(set(ids))
    assert len(speaking.TASKS) >= 6
    for t in speaking.TASKS:
        assert t.prompt
        assert t.kind in ("monolog", "sytuacja")
        assert t.max_wykonanie in (6, 7)


def test_task_by_id():
    assert speaking.task_by_id("m_film") is not None
    assert speaking.task_by_id("nope") is None


def test_official_max_matches_kind():
    for t in speaking.TASKS:
        assert t.max_wykonanie == (7 if t.kind == "monolog" else 6)


def test_photo_tasks_valid():
    assert len(speaking.PHOTOS) >= 4
    for t in speaking.PHOTOS:
        assert t.kind == "opis"
        assert t.max_wykonanie == 7
        assert t.photo_url.startswith("https://upload.wikimedia.org/")
        assert t.photo_source  # атрибуція ліцензії
    # task_by_id знаходить і фото-завдання
    assert speaking.task_by_id(speaking.PHOTOS[0].id) is not None
def test_readiness_pct():
    t = speaking.task_by_id("m_film")  # monolog, max 7
    assert speaking.readiness_pct(t, 7, 8, 8) == 100
    assert speaking.readiness_pct(t, 0, 0, 0) == 0
    # клемпінг перевищень
    assert speaking.readiness_pct(t, 99, 99, 99) == 100
