from app.domain.models import Module
from app.services import drills, mock


def test_drillable_modules():
    assert Module.GRAMATYKA in drills.DRILLABLE
    assert Module.CZYTANIE in drills.DRILLABLE


def test_session_indices_valid():
    for section in ("gramatyka", "czytanie"):
        idxs = drills.session_indices(section, 5)
        assert len(idxs) == 5
        assert len(idxs) == len(set(idxs))  # без повторів
        total = len(mock.section_items(section))
        assert all(0 <= i < total for i in idxs)


def test_session_indices_capped_to_available():
    idxs = drills.session_indices("czytanie", 1000)
    assert len(idxs) == len(mock.section_items("czytanie"))
