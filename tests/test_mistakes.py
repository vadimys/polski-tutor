"""Колода помилок: стабільний дедуп-хеш питання (Redis-CRUD — перевіряється наживо)."""

from app.services import mistakes


def test_qhash_stable_and_dedups():
    a = mistakes._qhash("Що означає слово X?")
    b = mistakes._qhash("  Що означає слово X?  ")  # пробіли обрізаються → той самий
    assert a == b and len(a) == 12


def test_qhash_differs():
    assert mistakes._qhash("питання A") != mistakes._qhash("питання B")
