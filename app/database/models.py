"""
Модели базы данных OilFusion.
"""

from datetime import datetime
from typing import Optional

from app.database.connection import db


class Image(db.Model):
    """
    Модель для хранения изображений.
    """
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True, index=True)
    original_filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    section = db.Column(db.String(100), nullable=False, index=True)  # hero, about, products, etc.
    field = db.Column(db.String(100), nullable=False)  # background, logo, feature_icon, etc.
    size_bytes = db.Column(db.Integer, default=0)
    mime_type = db.Column(db.String(100))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f'<Image {self.filename} ({self.section}.{self.field})>'


class Content(db.Model):
    """
    Модель для хранения мультиязычного контента секций.
    """
    __tablename__ = 'content'
    
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False, index=True)  # hero, about, products, etc.
    key = db.Column(db.String(255), nullable=False, index=True)  # slogan, title, description, etc.
    
    # Мультиязычные поля
    value_ru = db.Column(db.Text, nullable=True)  # Русский (основной)
    value_lv = db.Column(db.Text, nullable=True)  # Латышский
    value_en = db.Column(db.Text, nullable=True)  # Английский
    
    data_type = db.Column(db.String(50), default='text')  # text, json, html
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('section', 'key', name='uq_section_key'),
    )
    
    def get_value(self, locale: str = 'ru') -> Optional[str]:
        """
        Получить значение для указанного языка с фоллбэком на русский.
        
        Args:
            locale: Код языка (ru, lv, en)
            
        Returns:
            Значение для языка или None
        """
        value = getattr(self, f'value_{locale}', None)
        # Если нет перевода, возвращаем русский как фоллбэк
        if not value and locale != 'ru':
            value = self.value_ru
        return value
    
    def set_value(self, value: str, locale: str = 'ru') -> None:
        """
        Установить значение для указанного языка.
        
        Args:
            value: Значение для сохранения
            locale: Код языка (ru, lv, en)
        """
        setattr(self, f'value_{locale}', value)
    
    def __repr__(self) -> str:
        return f'<Content {self.section}.{self.key}>'


class Translation(db.Model):
    """
    Модель для хранения переводов.
    """
    __tablename__ = 'translations'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False, index=True)
    locale = db.Column(db.String(10), nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    original_value = db.Column(db.Text)
    source = db.Column(db.String(20), default='manual')  # manual, auto
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('key', 'locale', name='uq_key_locale'),
    )
    
    def __repr__(self) -> str:
        return f'<Translation {self.key} ({self.locale})>'


class Setting(db.Model):
    """
    Модель для хранения настроек приложения.
    """
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False, unique=True, index=True)
    value = db.Column(db.Text, nullable=False)
    value_type = db.Column(db.String(50), default='string')  # string, int, bool, json
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f'<Setting {self.key}={self.value}>'

