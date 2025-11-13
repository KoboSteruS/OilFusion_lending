"""
Модуль инициализации подсистемы интернационализации.
"""

from app.i18n.const import SUPPORTED_LANGUAGES, LANGUAGE_LABELS, DEFAULT_LANGUAGE
from app.i18n.manager import TranslationManager
from app.i18n.detector import LocaleDetector
from app.i18n.translator import GoogleTranslationProvider

__all__ = [
    "SUPPORTED_LANGUAGES",
    "LANGUAGE_LABELS",
    "DEFAULT_LANGUAGE",
    "TranslationManager",
    "LocaleDetector",
    "GoogleTranslationProvider",
]

