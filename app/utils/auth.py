"""
Модуль аутентификации для админки через JWT токены в URL.
Обеспечивает защиту административной части приложения.
"""

import jwt
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import abort, current_app
from typing import Optional, Dict, Any
from app.utils.logger import get_logger

logger = get_logger()


def generate_admin_token(secret_key: str, expires_hours: int = 8760) -> str:
    """
    Генерирует JWT токен для доступа к админке.
    По умолчанию токен действителен 1 год (8760 часов).
    
    Args:
        secret_key: Секретный ключ для подписи токена
        expires_hours: Срок действия токена в часах (по умолчанию 1 год)
        
    Returns:
        Строка с JWT токеном
    """
    payload = {
        'admin': True,
        'exp': datetime.utcnow() + timedelta(hours=expires_hours),
        'iat': datetime.utcnow(),
        'jti': secrets.token_urlsafe(16)  # Уникальный идентификатор токена
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    logger.info(f"Сгенерирован новый админский токен (срок действия: {expires_hours} часов)")
    
    return token


def verify_admin_token(token: str, secret_key: str) -> bool:
    """
    Проверяет валидность JWT токена для доступа к админке.
    
    Args:
        token: JWT токен для проверки
        secret_key: Секретный ключ для проверки подписи
        
    Returns:
        True если токен валиден, False иначе
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Проверяем, что это админский токен
        if not payload.get('admin'):
            logger.warning("Попытка доступа с не-админским токеном")
            return False
        
        logger.info(f"Успешная проверка токена (jti: {payload.get('jti', 'unknown')})")
        return True
        
    except jwt.ExpiredSignatureError:
        logger.warning("Попытка доступа с истекшим токеном")
        return False
    except jwt.InvalidTokenError as e:
        logger.warning(f"Попытка доступа с невалидным токеном: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Ошибка при проверке токена: {str(e)}")
        return False


def decode_admin_token(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
    """
    Декодирует JWT токен и возвращает его payload.
    
    Args:
        token: JWT токен для декодирования
        secret_key: Секретный ключ для проверки подписи
        
    Returns:
        Словарь с данными токена или None если токен невалиден
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except Exception as e:
        logger.error(f"Ошибка при декодировании токена: {str(e)}")
        return None


def require_admin_token(f):
    """
    Декоратор для защиты маршрутов админки.
    Проверяет наличие и валидность токена в URL.
    
    Usage:
        @admin_bp.route('/<token>/admin/some-route')
        @require_admin_token
        def protected_route(token):
            # Защищенная логика
            pass
    """
    @wraps(f)
    def decorated_function(token, *args, **kwargs):
        # Получаем секретный ключ из конфигурации
        secret_key = current_app.config.get('SECRET_KEY')
        
        if not secret_key:
            logger.error("SECRET_KEY не найден в конфигурации!")
            abort(500, description="Ошибка конфигурации сервера")
        
        # Проверяем токен
        if not verify_admin_token(token, secret_key):
            logger.warning(f"Отклонен доступ с невалидным токеном: {token[:20]}...")
            abort(403, description="Доступ запрещен. Невалидный токен.")
        
        # Токен валиден - выполняем функцию
        return f(token, *args, **kwargs)
    
    return decorated_function


def generate_secure_token() -> str:
    """
    Генерирует безопасный случайный токен (не JWT).
    Используется для дополнительной защиты.
    
    Returns:
        Строка с безопасным токеном
    """
    return secrets.token_urlsafe(32)


def get_token_info(token: str, secret_key: str) -> Dict[str, Any]:
    """
    Получает информацию о токене (срок действия, дата создания и т.д.).
    
    Args:
        token: JWT токен
        secret_key: Секретный ключ
        
    Returns:
        Словарь с информацией о токене
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        exp_timestamp = payload.get('exp')
        iat_timestamp = payload.get('iat')
        
        return {
            'valid': True,
            'admin': payload.get('admin', False),
            'expires_at': datetime.fromtimestamp(exp_timestamp).isoformat() if exp_timestamp else None,
            'issued_at': datetime.fromtimestamp(iat_timestamp).isoformat() if iat_timestamp else None,
            'jti': payload.get('jti', 'unknown')
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

