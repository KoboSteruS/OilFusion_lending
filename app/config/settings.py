"""
Конфигурационный файл приложения.
Содержит все настройки для различных окружений.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """
    Базовый класс конфигурации приложения.
    Загружает настройки из переменных окружения с fallback на значения по умолчанию.
    """
    
    # Базовые настройки
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Flask настройки
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING: bool = os.getenv('TESTING', 'False').lower() == 'true'
    
    # Настройки сервера
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '5000'))
    
    # Настройки шаблонов
    TEMPLATES_AUTO_RELOAD: bool = True
    
    # Настройки загрузки файлов
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB максимум
    UPLOAD_FOLDER: str = 'app/static/img'
    ALLOWED_EXTENSIONS: set = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    
    # Настройки безопасности
    SESSION_COOKIE_SECURE: bool = not DEBUG
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Lax'
    PERMANENT_SESSION_LIFETIME: int = 3600  # 1 час
    
    # Настройки логирования
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: Optional[str] = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Информация о компании
    COMPANY_NAME: str = "OilFusion"
    COMPANY_SLOGAN: str = "Balance in every drop"
    COMPANY_EMAIL: str = os.getenv('COMPANY_EMAIL', 'info@oilfusion.com')
    COMPANY_PHONE: str = os.getenv('COMPANY_PHONE', '+7 (XXX) XXX-XX-XX')
    COMPANY_ADDRESS: str = os.getenv('COMPANY_ADDRESS', 'г. Москва, ул. Примерная, д. 1')
    
    # Настройки Google Maps
    GOOGLE_MAPS_API_KEY: str = os.getenv('GOOGLE_MAPS_API_KEY', '')
    COMPANY_LATITUDE: str = os.getenv('COMPANY_LATITUDE', '55.751244')
    COMPANY_LONGITUDE: str = os.getenv('COMPANY_LONGITUDE', '37.618423')

    # Настройки интернационализации
    SUPPORTED_LANGUAGES = ('ru', 'lv', 'en')
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'ru')
    AUTO_TRANSLATION_ENABLED: bool = os.getenv('AUTO_TRANSLATION_ENABLED', 'false').lower() == 'true'
    
    @classmethod
    def init_app(cls, app):
        """
        Инициализация специфичных для приложения настроек.
        
        Args:
            app: Экземпляр Flask приложения
        """
        pass


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
    """Конфигурация для production"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    DEBUG = True


# Словарь конфигураций
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}





