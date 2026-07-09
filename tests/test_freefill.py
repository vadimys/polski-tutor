"""Free-fill: нормалізація/звірка + валідність даних завдань."""

from app import content
from app.services import freefill


def test_normalize():
    assert freefill.normalize("  Daje.  ") == "daje"
    assert freefill.normalize("Będziemy   Mieli") == "będziemy mieli"
    assert freefill.normalize("mówi,") == "mówi"


def test_is_correct_basic_and_variants():
    assert freefill.is_correct("daje", ["daje"])
    assert freefill.is_correct(" DAJE ", ["daje"])  # регістр/пробіли
    assert not freefill.is_correct("dają", ["daje"])  # інша форма
    # варіанти
    acc = ["będziemy mieli", "będziemy mieć"]
    assert freefill.is_correct("będziemy mieć", acc)
    assert freefill.is_correct("Będziemy Mieli", acc)
    assert not freefill.is_correct("mamy", acc)


def test_diacritics_matter():
    # діакритику зберігаємо — pracowali (з ł було б інше слово); тут перевіряємо ó/o
    assert freefill.is_correct("mówi", ["mówi"])
    assert not freefill.is_correct("mowi", ["mówi"])


def test_empty_answer_wrong():
    assert not freefill.is_correct("", ["daje"])
    assert not freefill.is_correct("   ", ["daje"])


def test_fill_tasks_wellformed():
    tasks = content.all_fill_tasks()
    assert tasks, "має бути хоча б одне free-fill завдання"
    for t in tasks:
        assert len(t.prompts) == len(t.accepted) == len(t.explain)
        for acc in t.accepted:
            assert acc and all(isinstance(x, str) and x.strip() for x in acc)
        assert t.section in ("czytanie", "gramatyka")
        assert t.title and t.intro


def test_fill_section_filter():
    assert content.all_fill_tasks("gramatyka")  # 2020 Zad IV
    assert content.all_fill_tasks("czytanie") == []
    assert content.exam_fill_tasks("2020")
