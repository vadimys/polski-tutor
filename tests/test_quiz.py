import pytest

from app.bot import quiz


class _FakeMsg:
    def __init__(self):
        self.edited_text = None
        self.markup_cleared = False

    async def edit_text(self, text):
        self.edited_text = text

    async def edit_reply_markup(self, reply_markup=None):
        self.markup_cleared = reply_markup is None


class _FakeCb:
    def __init__(self, data):
        self.data = data
        self.message = _FakeMsg()
        self.answered_with = None

    async def answer(self, text=None, **kwargs):
        self.answered_with = text if text is not None else ""


@pytest.mark.asyncio
async def test_read_answer_valid_returns_choice():
    cb = _FakeCb("dr:ans:2:1")
    assert await quiz.read_answer(cb, current_pos=2) == 1


@pytest.mark.asyncio
async def test_read_answer_stale_returns_none_and_clears():
    cb = _FakeCb("dr:ans:0:1")  # qidx=0, а поточне питання 3 → стале
    assert await quiz.read_answer(cb, current_pos=3) is None
    assert cb.message.markup_cleared
    assert "вже пройдено" in cb.answered_with


@pytest.mark.asyncio
async def test_read_answer_malformed_returns_none():
    cb = _FakeCb("garbage")
    assert await quiz.read_answer(cb, current_pos=0) is None


@pytest.mark.asyncio
async def test_show_verdict_correct_and_wrong():
    cb_ok = _FakeCb("x:ans:0:1")
    assert await quiz.show_verdict(cb_ok, 1, 1, ["a", "b"], "Q?", "бо") is True
    assert "Dobrze" in cb_ok.message.edited_text
    cb_no = _FakeCb("x:ans:0:0")
    assert await quiz.show_verdict(cb_no, 0, 1, ["a", "b"], "Q?", "") is False
    assert "Poprawnie" in cb_no.message.edited_text


def test_parse_answer_valid():
    assert quiz.parse_answer("pl:ans:3:1") == (3, 1)
    assert quiz.parse_answer("dr:ans:0:2") == (0, 2)
    assert quiz.parse_answer("ls:ans:5:0") == (5, 0)


def test_parse_answer_rejects_bad():
    assert quiz.parse_answer("pl:ans:0") is None  # старий формат (3 частини)
    assert quiz.parse_answer("garbage") is None
    assert quiz.parse_answer("pl:ans:x:y") is None


def test_verdict_card_correct():
    out = quiz.verdict_card("Pytanie?", 1, 1, ["a", "b", "c"], "бо так")
    assert "Dobrze" in out and "бо так" in out and "Pytanie?" in out


def test_verdict_card_wrong_shows_answer():
    out = quiz.verdict_card("Pytanie?", 0, 2, ["a", "b", "c"], "")
    assert "Poprawnie" in out and "c" in out
