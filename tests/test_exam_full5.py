"""Фіналка /egzamin: зведення всіх 5 модулів + CTA добити продуктивні модулі."""

from app.handlers import exam
from app.services.progress import ModuleStat


def _stat(pct, attempts=5):
    return ModuleStat(pct=pct, attempts=attempts, days=3, days_since=0, mastered=pct >= 50)


def _cbs(markup):
    return [b.callback_data for row in markup.inline_keyboard for b in row]


async def test_full5_offers_missing_productive(monkeypatch):
    # 3 авто-модулі виміряні, письмо/мовлення — ще ні → CTA на обидва
    async def fake_compute(uid):
        return {
            "sluchanie": _stat(60), "czytanie": _stat(70), "gramatyka": _stat(55),
            "pisanie": _stat(0, attempts=0), "mowienie": _stat(0, attempts=0),
        }

    monkeypatch.setattr(exam.progress, "compute", fake_compute)
    text, markup = await exam._full_exam_block(1)
    cbs = _cbs(markup)
    assert "writing:start" in cbs and "speaking:start" in cbs
    assert "ще не міряно" in text


async def test_full5_all_pass(monkeypatch):
    async def fake_compute(uid):
        return {m: _stat(80) for m in ("sluchanie", "czytanie", "gramatyka", "pisanie", "mowienie")}

    monkeypatch.setattr(exam.progress, "compute", fake_compute)
    text, markup = await exam._full_exam_block(1)
    cbs = _cbs(markup)
    assert "складаєш іспит" in text
    assert "writing:start" not in cbs and "speaking:start" not in cbs  # нічого добивати


async def test_full5_below_threshold_no_cta_when_measured(monkeypatch):
    # усі 5 виміряні, але є <50% → без CTA продуктивних, є заклик підтягнути
    async def fake_compute(uid):
        return {
            "sluchanie": _stat(40), "czytanie": _stat(70), "gramatyka": _stat(55),
            "pisanie": _stat(60), "mowienie": _stat(45),
        }

    monkeypatch.setattr(exam.progress, "compute", fake_compute)
    text, markup = await exam._full_exam_block(1)
    cbs = _cbs(markup)
    assert "Підтягни" in text
    assert "writing:start" not in cbs and "speaking:start" not in cbs
    assert "❌" in text  # позначено провальні модулі
