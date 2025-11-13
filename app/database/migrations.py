"""
Миграции и заполнение БД начальными данными.
"""

import json
from pathlib import Path
from typing import Dict, Any

from app.database.connection import db
from app.database.models import Content, Image, Translation, Setting
from app.database.repositories import ContentRepository, ImageRepository, SettingRepository, TranslationRepository
from app.utils.logger import get_logger

logger = get_logger()


def migrate_json_to_db(data_dir: Path) -> None:
    """
    Миграция данных из JSON файлов в базу данных.
    Выполняется только один раз при первом запуске.
    
    Args:
        data_dir: Путь к папке data с JSON файлами
    """
    # Проверяем, была ли уже выполнена миграция
    if SettingRepository.get('migration_completed') == 'true':
        logger.info("Миграция уже выполнена ранее, пропускаем")
        return
    
    logger.info("Начинаем миграцию данных из JSON в SQLite")
    
    try:
        # Миграция переводов
        _migrate_translations(data_dir / 'translations.json')
        
        # Миграция контента секций (из различных JSON файлов)
        _migrate_content_files(data_dir)
        
        # Миграция изображений (из backgrounds JSON и других)
        _migrate_images(data_dir)
        
        # Миграция настроек видимости секций
        _migrate_sections_visibility(data_dir / 'sections_visibility.json')
        
        # Помечаем миграцию как завершённую
        SettingRepository.set('migration_completed', 'true', 'bool', 'Флаг завершения миграции JSON -> SQLite')
        SettingRepository.set('migration_date', str(db.func.current_timestamp()), 'string', 'Дата миграции')
        
        logger.info("Миграция данных успешно завершена")
        
    except Exception as exc:
        logger.error(f"Ошибка при миграции данных: {exc}")
        db.session.rollback()
        raise


def _migrate_translations(translations_file: Path) -> None:
    """Миграция переводов из translations.json."""
    if not translations_file.exists():
        logger.warning(f"Файл переводов не найден: {translations_file}")
        return
    
    try:
        with translations_file.open('r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for key, entry in data.items():
            original = entry.get('meta', {}).get('original', '')
            translations = entry.get('translations', {})
            
            for locale, trans_data in translations.items():
                value = trans_data.get('value', '')
                source = trans_data.get('source', 'manual')
                
                if value:
                    TranslationRepository.set(
                        key=key,
                        locale=locale,
                        value=value,
                        original_value=original,
                        source=source
                    )
                    count += 1
        
        logger.info(f"Мигрировано {count} переводов")
        
    except Exception as exc:
        logger.error(f"Ошибка миграции переводов: {exc}")


def _migrate_content_files(data_dir: Path) -> None:
    """Миграция контента из различных JSON файлов."""
    content_files = {
        'hero_content.json': 'hero',
        'about_content.json': 'about',
        'products_content.json': 'products',
        'services_content.json': 'services',
        'personalization_content.json': 'personalization',
        'contacts_content.json': 'contacts',
        'blog_content.json': 'blog',
        'auracloud_slider.json': 'auracloud_slider',
    }
    
    total_count = 0
    
    for filename, section in content_files.items():
        file_path = data_dir / filename
        if not file_path.exists():
            logger.warning(f"Файл контента не найден: {filename}")
            continue
        
        try:
            with file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            
            count = _migrate_section_data(section, data)
            total_count += count
            logger.info(f"Мигрировано {count} записей из {filename}")
            
        except Exception as exc:
            logger.error(f"Ошибка миграции {filename}: {exc}")
    
    logger.info(f"Всего мигрировано {total_count} записей контента")


def _migrate_section_data(section: str, data: Any, prefix: str = '') -> int:
    """
    Рекурсивная миграция данных секции.
    
    Args:
        section: Название секции
        data: Данные для миграции
        prefix: Префикс для вложенных ключей
        
    Returns:
        Количество мигрированных записей
    """
    count = 0
    
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, (dict, list)):
                # Сохраняем сложные структуры как JSON
                ContentRepository.set(
                    section=section,
                    key=full_key,
                    value=json.dumps(value, ensure_ascii=False),
                    data_type='json'
                )
                count += 1
            elif isinstance(value, str):
                ContentRepository.set(
                    section=section,
                    key=full_key,
                    value=value,
                    data_type='text'
                )
                count += 1
            elif value is not None:
                # Преобразуем другие типы в строки
                ContentRepository.set(
                    section=section,
                    key=full_key,
                    value=str(value),
                    data_type='text'
                )
                count += 1
    
    elif isinstance(data, list):
        # Для списков сохраняем как JSON
        ContentRepository.set(
            section=section,
            key=prefix or 'data',
            value=json.dumps(data, ensure_ascii=False),
            data_type='json'
        )
        count += 1
    
    return count


def _migrate_images(data_dir: Path) -> None:
    """Миграция информации об изображениях."""
    backgrounds_file = data_dir / 'section_backgrounds.json'
    
    if not backgrounds_file.exists():
        logger.warning("Файл backgrounds не найден")
        return
    
    try:
        with backgrounds_file.open('r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        sections = data.get('sections', {})
        
        for section_name, section_data in sections.items():
            if isinstance(section_data, dict):
                for field_name, image_url in section_data.items():
                    if image_url and isinstance(image_url, str):
                        # Извлекаем имя файла из URL
                        filename = Path(image_url).name
                        
                        # Проверяем, не существует ли уже эта запись
                        existing = ImageRepository.get_by_section_field(section_name, field_name)
                        if not existing:
                            ImageRepository.create(
                                filename=filename,
                                original_filename=filename,
                                url=image_url,
                                section=section_name,
                                field=field_name
                            )
                            count += 1
        
        logger.info(f"Мигрировано {count} записей изображений")
        
    except Exception as exc:
        logger.error(f"Ошибка миграции изображений: {exc}")


def _migrate_sections_visibility(visibility_file: Path) -> None:
    """Миграция настроек видимости секций."""
    if not visibility_file.exists():
        logger.warning("Файл sections_visibility не найден")
        return
    
    try:
        with visibility_file.open('r', encoding='utf-8') as f:
            data = json.load(f)
        
        sections = data.get('sections', {})
        count = 0
        
        for section_name, is_visible in sections.items():
            SettingRepository.set(
                key=f'section_visible_{section_name}',
                value=str(is_visible).lower(),
                value_type='bool',
                description=f'Видимость секции {section_name}'
            )
            count += 1
        
        logger.info(f"Мигрировано {count} настроек видимости секций")
        
    except Exception as exc:
        logger.error(f"Ошибка миграции настроек видимости: {exc}")


def create_default_data() -> None:
    """
    Создание дефолтных данных при первом запуске, если JSON файлов нет.
    """
    # Проверяем, есть ли уже данные в БД
    if Content.query.first() or Translation.query.first():
        logger.info("В БД уже есть данные, создание дефолтных данных не требуется")
        return
    
    logger.info("Создание дефолтных данных для новой установки")
    
    try:
        # Создаём базовый контент для Hero секции
        ContentRepository.set('hero', 'slogan', 'Balance in every drop', 'text')
        ContentRepository.set('hero', 'subtitle', 'Персонализированные масла на основе технологий AuraCloud® 3D и ДНК-тестирования', 'text')
        ContentRepository.set('hero', 'cta_primary', 'Подобрать масло', 'text')
        ContentRepository.set('hero', 'cta_secondary', 'Записаться', 'text')
        ContentRepository.set('hero', 'scroll_text', 'Прокрутите вниз', 'text')
        
        # Создаём базовые переводы
        _create_default_translations()
        
        # Создаём базовые настройки
        SettingRepository.set('default_language', 'ru', 'string', 'Язык по умолчанию')
        SettingRepository.set('auto_translation_enabled', 'false', 'bool', 'Автоматический перевод')
        
        # Настройки видимости секций (все включены)
        for section in ['hero', 'about', 'products', 'services', 'personalization', 'reviews', 'blog', 'contacts']:
            SettingRepository.set(f'section_visible_{section}', 'true', 'bool', f'Видимость секции {section}')
        
        logger.info("Дефолтные данные успешно созданы")
        
    except Exception as exc:
        logger.error(f"Ошибка создания дефолтных данных: {exc}")
        db.session.rollback()
        raise


def _create_default_translations() -> None:
    """Создание базовых переводов."""
    default_translations = {
        'hero.slogan': {
            'lv': 'Līdzsvars katrā pilienā',
            'en': 'Balance in every drop'
        },
        'hero.subtitle': {
            'lv': 'Personalizētas eļļas, pamatojoties uz AuraCloud® 3D un DNS testēšanas tehnoloģijām',
            'en': 'Personalized oils based on AuraCloud® 3D and DNA testing technologies'
        },
        'hero.cta_primary': {
            'lv': 'Izvēlēties eļļu',
            'en': 'Select Oil'
        },
        'hero.cta_secondary': {
            'lv': 'Pierakstīties',
            'en': 'Book Appointment'
        },
    }
    
    for key, translations in default_translations.items():
        original = ContentRepository.get('hero', key.split('.')[1], '')
        for locale, value in translations.items():
            TranslationRepository.set(key, locale, value, original, 'manual')

