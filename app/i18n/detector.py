"""
Определение локали пользователя.
"""

from __future__ import annotations

from typing import Optional

from flask import Request

from app.i18n.const import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


class LocaleDetector:
    """
    Определяет предпочтительный язык пользователя.
    GeoIP и Accept-Language отключены для ускорения загрузки.
    """

    def __init__(self, default_language: str = DEFAULT_LANGUAGE) -> None:
        self._default_language = default_language

    def detect(self, request: Request, session_locale: Optional[str] = None) -> str:
        """
        Определяет язык интерфейса исходя из запроса и данных сессии.
        По умолчанию возвращает русский язык.
        """
        # query parameter имеет максимальный приоритет
        query_locale = self._validate_locale(request.args.get("lang"))
        if query_locale:
            return query_locale

        # Проверяем сохранённый язык в сессии
        if session_locale:
            validated = self._validate_locale(session_locale)
            if validated:
                return validated

        # Возвращаем русский по умолчанию (гео-детекция и Accept-Language отключены для скорости)
        return self._default_language

    @staticmethod
    def _validate_locale(locale: Optional[str]) -> Optional[str]:
        if locale and locale.lower() in SUPPORTED_LANGUAGES:
            return locale.lower()
        return None

