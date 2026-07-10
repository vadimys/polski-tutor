"""Глобальний обробник помилок: витягання user_id для кореляції в логах/алертах."""

from app.handlers.errors import _uid


class _User:
    def __init__(self, uid):
        self.id = uid


class _Msg:
    def __init__(self, uid):
        self.from_user = _User(uid)


class _Update:
    def __init__(self, message=None, callback_query=None):
        self.message = message
        self.callback_query = callback_query


class _Event:
    def __init__(self, update):
        self.update = update


def test_uid_from_message():
    assert _uid(_Event(_Update(message=_Msg(111)))) == 111


def test_uid_from_callback():
    assert _uid(_Event(_Update(callback_query=_Msg(222)))) == 222


def test_uid_none_when_absent():
    assert _uid(_Event(_Update())) is None
