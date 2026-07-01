"""Щоденне тренування — коротка вибірка з ОФІЦІЙНОГО банку (services/mock).

Раніше тут був мій власний банк питань; за правилом «тільки офіційне»
([[polski-official-only-rule]]) тренування тепер бере реальні питання з офіційного
пробного тесту (services/mock), лише коротшими сесіями (5 питань).
"""

from __future__ import annotations

import random

from app.domain.models import Module
from app.services import mock

# Модулі, які тренує дрил (об'єктивні MCQ з офіц. тесту)
DRILLABLE = (Module.GRAMATYKA, Module.CZYTANIE)


def session_indices(section: str, n: int = 5) -> list[int]:
    """Випадкові індекси n офіційних САМОДОСТАТНІХ питань секції.

    Самодостатнє = має власний контекст (it.context). Питання TAK/NIE, що
    спираються на спільний текст (показаний раніше), у випадкову вибірку не беремо —
    інакше вони були б без тексту й нерозв'язні.
    """
    items = mock.section_items(section)
    standalone = [i for i, it in enumerate(items) if it.context]
    random.shuffle(standalone)
    return standalone[: min(n, len(standalone))]
