"""Mini App: валідація підпису Telegram initData (критично для безпеки даних)."""

import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

from app.bot import webapp
from app.config import settings


def _signed(uid: int, token: str | None = None, auth_date: int | None = None) -> str:
    token = token or settings.bot_token  # підписуємо тим самим токеном, що валідує сервер
    fields = {
        "auth_date": str(auth_date or int(time.time())),
        "query_id": "AAAA",
        "user": json.dumps({"id": uid, "first_name": "T"}),
    }
    data_check = "\n".join(f"{k}={fields[k]}" for k in sorted(fields))
    secret = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    fields["hash"] = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()
    return urlencode(fields)


def test_valid_init_data_returns_uid():
    assert webapp.validate_init_data(_signed(42)) == 42


def test_tampered_payload_rejected():
    bad = _signed(42).replace("first_name", "hacked")
    assert webapp.validate_init_data(bad) is None


def test_wrong_token_rejected():
    assert webapp.validate_init_data(_signed(42, token="wrong:token:xyz")) is None  # noqa: S106


def test_expired_rejected():
    assert webapp.validate_init_data(_signed(42, auth_date=1)) is None


def test_empty_or_garbage_rejected():
    assert webapp.validate_init_data("") is None
    assert webapp.validate_init_data("garbage&no=hash") is None
