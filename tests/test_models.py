from app.domain.models import MODULE_LABELS, Module, UserState


def test_weakest_module():
    st = UserState(
        user_id=1,
        readiness={
            "gramatyka": 70,
            "pisanie": 30,
            "czytanie": 80,
            "sluchanie": 60,
            "mowienie": 50,
        },
    )
    assert st.weakest_module() == Module.PISANIE


def test_weakest_default_when_empty():
    assert UserState(user_id=1).weakest_module() == Module.PISANIE


def test_weakest_prefers_untested_module():
    # виміряні лише граматика+читання → фокус на ще НЕ виміряному (Pisanie перший)
    st = UserState(user_id=1, readiness={"gramatyka": 75, "czytanie": 100})
    assert st.weakest_module() == Module.PISANIE


def test_all_modules_have_labels():
    for mod in Module:
        assert mod in MODULE_LABELS
