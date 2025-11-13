"""
Репозитории для работы с моделями базы данных.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from werkzeug.datastructures import FileStorage

from app.database.connection import db
from app.database.models import Content, Image, Setting, Translation
from app.utils.logger import get_logger

logger = get_logger()


class ImageRepository:
    """Репозиторий для работы с изображениями."""
    
    @staticmethod
    def create(
        filename: str,
        original_filename: str,
        url: str,
        section: str,
        field: str,
        size_bytes: int = 0,
        mime_type: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> Image:
        """
        Создание новой записи изображения.
        
        Args:
            filename: Уникальное имя файла
            original_filename: Оригинальное имя файла
            url: URL изображения
            section: Секция (hero, about, products, etc.)
            field: Поле (background, logo, feature_icon, etc.)
            size_bytes: Размер файла в байтах
            mime_type: MIME-тип файла
            width: Ширина изображения
            height: Высота изображения
            
        Returns:
            Image: Созданная запись изображения
        """
        image = Image(
            filename=filename,
            original_filename=original_filename,
            url=url,
            section=section,
            field=field,
            size_bytes=size_bytes,
            mime_type=mime_type,
            width=width,
            height=height
        )
        db.session.add(image)
        db.session.commit()
        logger.info(f"Изображение сохранено в БД: {filename} ({section}.{field})")
        return image
    
    @staticmethod
    def get_by_section_field(section: str, field: str) -> Optional[Image]:
        """Получение изображения по секции и полю."""
        return Image.query.filter_by(section=section, field=field).first()
    
    @staticmethod
    def get_by_filename(filename: str) -> Optional[Image]:
        """Получение изображения по имени файла."""
        return Image.query.filter_by(filename=filename).first()
    
    @staticmethod
    def list_by_section(section: str) -> List[Image]:
        """Получение всех изображений секции."""
        return Image.query.filter_by(section=section).all()
    
    @staticmethod
    def update_url(section: str, field: str, url: str) -> Optional[Image]:
        """Обновление URL изображения."""
        image = ImageRepository.get_by_section_field(section, field)
        if image:
            image.url = url
            image.updated_at = datetime.utcnow()
            db.session.commit()
            logger.info(f"URL изображения обновлён: {section}.{field}")
        return image
    
    @staticmethod
    def delete(image_id: int) -> bool:
        """Удаление изображения из БД."""
        image = Image.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()
            logger.info(f"Изображение удалено из БД: {image.filename}")
            return True
        return False


class ContentRepository:
    """Репозиторий для работы с контентом."""
    
    @staticmethod
    def set(section: str, key: str, value: str, data_type: str = 'text') -> Content:
        """
        Установка значения контента.
        
        Args:
            section: Секция
            key: Ключ
            value: Значение
            data_type: Тип данных (text, json, html)
            
        Returns:
            Content: Запись контента
        """
        content = Content.query.filter_by(section=section, key=key).first()
        if content:
            content.value = value
            content.data_type = data_type
            content.updated_at = datetime.utcnow()
        else:
            content = Content(
                section=section,
                key=key,
                value=value,
                data_type=data_type
            )
            db.session.add(content)
        db.session.commit()
        return content
    
    @staticmethod
    def get(section: str, key: str, default: Optional[str] = None) -> Optional[str]:
        """Получение значения контента."""
        content = Content.query.filter_by(section=section, key=key).first()
        return content.value if content else default
    
    @staticmethod
    def get_section(section: str) -> Dict[str, str]:
        """Получение всех данных секции."""
        contents = Content.query.filter_by(section=section).all()
        result = {}
        for content in contents:
            if content.data_type == 'json':
                try:
                    result[content.key] = json.loads(content.value)
                except json.JSONDecodeError:
                    result[content.key] = content.value
            else:
                result[content.key] = content.value
        return result
    
    @staticmethod
    def delete(section: str, key: str) -> bool:
        """Удаление записи контента."""
        content = Content.query.filter_by(section=section, key=key).first()
        if content:
            db.session.delete(content)
            db.session.commit()
            return True
        return False


class TranslationRepository:
    """Репозиторий для работы с переводами."""
    
    @staticmethod
    def set(key: str, locale: str, value: str, original_value: Optional[str] = None, source: str = 'manual') -> Translation:
        """
        Установка перевода.
        
        Args:
            key: Ключ перевода
            locale: Локаль (ru, lv, en)
            value: Переведённое значение
            original_value: Оригинальное значение
            source: Источник (manual, auto)
            
        Returns:
            Translation: Запись перевода
        """
        translation = Translation.query.filter_by(key=key, locale=locale).first()
        if translation:
            translation.value = value
            if original_value:
                translation.original_value = original_value
            translation.source = source
            translation.updated_at = datetime.utcnow()
        else:
            translation = Translation(
                key=key,
                locale=locale,
                value=value,
                original_value=original_value,
                source=source
            )
            db.session.add(translation)
        db.session.commit()
        return translation
    
    @staticmethod
    def get(key: str, locale: str) -> Optional[str]:
        """Получение перевода."""
        translation = Translation.query.filter_by(key=key, locale=locale).first()
        return translation.value if translation else None
    
    @staticmethod
    def get_by_locale(locale: str) -> Dict[str, str]:
        """Получение всех переводов для локали."""
        translations = Translation.query.filter_by(locale=locale).all()
        return {t.key: t.value for t in translations}
    
    @staticmethod
    def list_all() -> List[Translation]:
        """Получение всех переводов."""
        return Translation.query.all()


class SettingRepository:
    """Репозиторий для работы с настройками."""
    
    @staticmethod
    def set(key: str, value: str, value_type: str = 'string', description: Optional[str] = None) -> Setting:
        """Установка настройки."""
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.value_type = value_type
            if description:
                setting.description = description
            setting.updated_at = datetime.utcnow()
        else:
            setting = Setting(
                key=key,
                value=value,
                value_type=value_type,
                description=description
            )
            db.session.add(setting)
        db.session.commit()
        return setting
    
    @staticmethod
    def get(key: str, default: Optional[str] = None) -> Optional[str]:
        """Получение значения настройки."""
        setting = Setting.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """Получение булевой настройки."""
        value = SettingRepository.get(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')
    
    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        """Получение целочисленной настройки."""
        value = SettingRepository.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

