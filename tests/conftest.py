"""Тестова конфігурація: BOT_TOKEN до імпорту app.*, src у sys.path."""

import os
import sys
from pathlib import Path

os.environ.setdefault("BOT_TOKEN", "test:token")

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
