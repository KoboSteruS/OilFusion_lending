"""
Определение локали пользователя.
"""

from __future__ import annotations

import ipaddress
from functools import lru_cache
from typing import Optional

import requests
from flask import Request
from loguru import logger

from app.i18n.const import COUNTRY_LANGUAGE_MAP, DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


class LocaleDetector:
    """
    Определяет предпочтительный язык пользователя.
    """

    GEO_IP_ENDPOINT = "https://ipapi.co/{ip}/json/"

    def __init__(self, default_language: str = DEFAULT_LANGUAGE) -> None:
        self._default_language = default_language

    def detect(self, request: Request, session_locale: Optional[str] = None) -> str:
        """
        Определяет язык интерфейса исходя из запроса и данных сессии.
        """
        # query parameter имеет максимальный приоритет
        query_locale = self._validate_locale(request.args.get("lang"))
        if query_locale:
            return query_locale

        if session_locale:
            validated = self._validate_locale(session_locale)
            if validated:
                return validated

        header_locale = self._validate_locale(request.accept_languages.best_match(SUPPORTED_LANGUAGES))
        if header_locale:
            return header_locale

        geo_locale = self._detect_by_geo(request)
        if geo_locale:
            return geo_locale

        return self._default_language

    @staticmethod
    def _validate_locale(locale: Optional[str]) -> Optional[str]:
        if locale and locale.lower() in SUPPORTED_LANGUAGES:
            return locale.lower()
        return None

    def _detect_by_geo(self, request: Request) -> Optional[str]:
        ip_address = self._extract_ip(request)
        if not ip_address:
            return None
        if self._is_private_ip(ip_address):
            return None

        try:
            response = self._geo_request(ip_address)
            if not response:
                return None
            country_code = response.get("country_code")
            if not country_code:
                return None
            locale = COUNTRY_LANGUAGE_MAP.get(country_code.upper())
            return self._validate_locale(locale)
        except Exception as exc:  # noqa: BLE001
            logger.warning("GeoIP detection failed: {}", exc)
            return None

    @staticmethod
    def _extract_ip(request: Request) -> Optional[str]:
        header_order = (
            "CF-Connecting-IP",
            "X-Forwarded-For",
            "X-Real-IP",
        )
        for header in header_order:
            value = request.headers.get(header)
            if value:
                # X-Forwarded-For может содержать несколько IP
                ip_candidate = value.split(",")[0].strip()
                if ip_candidate:
                    return ip_candidate
        return request.remote_addr

    @staticmethod
    def _is_private_ip(ip: str) -> bool:
        try:
            ip_address = ipaddress.ip_address(ip)
            return ip_address.is_private or ip_address.is_loopback
        except ValueError:
            return True

    @classmethod
    @lru_cache(maxsize=1024)
    def _geo_request(cls, ip: str) -> Optional[dict]:
        url = cls.GEO_IP_ENDPOINT.format(ip=ip)
        response = requests.get(url, timeout=2)
        if response.status_code != 200:
            return None
        return response.json()

