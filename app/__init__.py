"""
Инициализация Flask приложения OilFusion Landing.
Создание и конфигурирование основного приложения.
"""

from flask import Flask
from app.utils.logger import setup_logger
from app.config.settings import Config


def create_app(config_class=Config) -> Flask:
    """
    Фабрика приложений Flask.
    
    Args:
        config_class: Класс конфигурации приложения
        
    Returns:
        Flask: Настроенное приложение Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация логгера
    logger = setup_logger()
    logger.info("Инициализация Flask приложения OilFusion Landing")
    
    # Регистрация blueprints
    from app.routes import main_bp, admin_bp, backgrounds_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(backgrounds_bp)
    
    logger.info("Flask приложение успешно инициализировано")
    
    return app




