"""
Хелперы для работы с мультиязычным контентом.
"""

from flask import g
from typing import Any, Dict, Optional

from app.database import ContentRepository
from app.i18n import DEFAULT_LANGUAGE


def get_content(section: str, key: str, default: str = '') -> str:
    """
    Получить контент на текущем языке пользователя.
    
    Args:
        section: Секция (hero, about, products, etc.)
        key: Ключ контента
        default: Значение по умолчанию
        
    Returns:
        Контент на текущем языке или fallback на русский
    """
    locale = getattr(g, 'locale', DEFAULT_LANGUAGE)
    return ContentRepository.get(section, key, locale, default)


def get_section_content(section: str) -> Dict[str, Any]:
    """
    Получить весь контент секции на текущем языке.
    
    Args:
        section: Секция (hero, about, products, etc.)
        
    Returns:
        Словарь с контентом секции на текущем языке
    """
    locale = getattr(g, 'locale', DEFAULT_LANGUAGE)
    return ContentRepository.get_section(section, locale)


def inject_content_helper():
    """
    Контекст-процессор для внедрения хелперов в шаблоны.
    """
    return {
        'get_content': get_content,
        'get_section_content': get_section_content,
    }




