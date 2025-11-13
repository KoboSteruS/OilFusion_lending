"""
Константы подсистемы интернационализации.
"""

from __future__ import annotations

from typing import Dict, Tuple

SUPPORTED_LANGUAGES: Tuple[str, ...] = ("ru", "lv", "en")
DEFAULT_LANGUAGE: str = "ru"

LANGUAGE_LABELS: Dict[str, str] = {
    "ru": "RU",
    "lv": "LV",
    "en": "EN",
}

# Соответствие ISO-кодов стран предпочтительным языкам интерфейса.
COUNTRY_LANGUAGE_MAP: Dict[str, str] = {
    "RU": "ru",
    "LV": "lv",
    "LT": "lv",  # часть пользователей Латвии может определяться как LT
    "EE": "lv",  # ближний регион, применяем латышский как договорённость
    "US": "en",
    "GB": "en",
    "AU": "en",
    "CA": "en",
    "IE": "en",
    "NZ": "en",
}

