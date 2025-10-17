"""
Модуль маршрутизации приложения.
"""

from app.routes.main import main_bp
from app.routes.admin import admin_bp
from app.routes.backgrounds import backgrounds_bp

__all__ = ['main_bp', 'admin_bp', 'backgrounds_bp']




