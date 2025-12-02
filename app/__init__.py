"""
Инициализация Flask приложения OilFusion Landing.
Создание и конфигурирование основного приложения.
"""

from flask import Flask, g, request, session

from app.config.settings import Config
from app.database import init_db
from app.i18n import DEFAULT_LANGUAGE, LANGUAGE_LABELS, LocaleDetector, SUPPORTED_LANGUAGES
from app.i18n.manager import translation_manager
from app.utils.logger import setup_logger


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

    # Инициализация базы данных
    init_db(app)
    logger.info("База данных SQLite инициализирована")

    # Регистрация blueprints
    from app.routes import admin_bp, backgrounds_bp, main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(backgrounds_bp)

    # Инициализация определения локали
    locale_detector = LocaleDetector()

    @app.before_request
    def _set_locale() -> None:
        locale = locale_detector.detect(request, session.get("locale"))
        g.locale = locale
        session["locale"] = locale
        g.translation_manager = translation_manager

    @app.context_processor
    def _inject_i18n():
        return {
            "current_locale": getattr(g, "locale", DEFAULT_LANGUAGE),
            "available_locales": SUPPORTED_LANGUAGES,
            "locale_labels": LANGUAGE_LABELS,
        }
    
    # Регистрируем хелперы для работы с контентом
    from app.helpers import inject_content_helper
    app.context_processor(inject_content_helper)

    logger.info("Flask приложение успешно инициализировано")

    return app


# Создаём объект приложения на уровне модуля, чтобы gunicorn app:app работал на платформах
# где нельзя изменить команду запуска.
app = create_app()