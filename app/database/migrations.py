"""
Миграции и заполнение БД начальными данными.
Поддержка мультиязычного контента (ru, lv, en).
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Set

from app.database.connection import db
from app.database.models import Content, Image, Setting, Translation
from app.database.repositories import (
    ContentRepository,
    ImageRepository,
    SettingRepository,
    TranslationRepository,
)
from app.utils.logger import get_logger

logger = get_logger()

# Версия миграции - увеличивать при изменении структуры данных
MIGRATION_VERSION = "2.0.0"

# Поддерживаемые языки
SUPPORTED_LOCALES: Set[str] = {"ru", "lv", "en"}


def _is_multilang_dict(value: Any) -> bool:
    """
    Проверяет, является ли значение мультиязычным словарём.
    Мультиязычный словарь содержит только ключи из SUPPORTED_LOCALES.
    
    Args:
        value: Значение для проверки
        
    Returns:
        True если это мультиязычный словарь
    """
    if not isinstance(value, dict):
        return False
    
    keys = set(value.keys())
    # Мультиязычный если все ключи - это локали и есть хотя бы 'ru'
    return keys.issubset(SUPPORTED_LOCALES) and "ru" in keys


def migrate_json_to_db(data_dir: Path) -> None:
    """
    Миграция данных из JSON файлов в базу данных.
    Выполняется при первом запуске или при изменении версии миграции.
    
    Args:
        data_dir: Путь к папке data с JSON файлами
    """
    current_version = SettingRepository.get("migration_version")
    
    if current_version == MIGRATION_VERSION:
        logger.info(f"Миграция версии {MIGRATION_VERSION} уже выполнена, пропускаем")
        return
    
    if current_version:
        logger.info(f"Обнаружена новая версия миграции: {current_version} -> {MIGRATION_VERSION}")
        # Очищаем старые данные контента для ремиграции
        _clear_content_data()
    
    logger.info(f"Начинаем миграцию данных версии {MIGRATION_VERSION}")
    
    try:
        # Миграция переводов
        _migrate_translations(data_dir / "translations.json")
        
        # Миграция контента секций (из различных JSON файлов)
        _migrate_content_files(data_dir)
        
        # Миграция изображений (из backgrounds JSON и других)
        _migrate_images(data_dir)
        
        # Миграция настроек видимости секций
        _migrate_sections_visibility(data_dir / "sections_visibility.json")
        
        # Помечаем миграцию как завершённую
        SettingRepository.set(
            "migration_version", MIGRATION_VERSION, "string", "Версия выполненной миграции"
        )
        SettingRepository.set(
            "migration_completed", "true", "bool", "Флаг завершения миграции"
        )
        
        logger.info(f"Миграция версии {MIGRATION_VERSION} успешно завершена")
        
    except Exception as exc:
        logger.error(f"Ошибка при миграции данных: {exc}")
        db.session.rollback()
        raise


def _clear_content_data() -> None:
    """Очистка данных контента для ремиграции."""
    try:
        Content.query.delete()
        db.session.commit()
        logger.info("Старые данные контента очищены для ремиграции")
    except Exception as exc:
        logger.error(f"Ошибка очистки данных: {exc}")
        db.session.rollback()


def _migrate_translations(translations_file: Path) -> None:
    """Миграция переводов из translations.json."""
    if not translations_file.exists():
        logger.warning(f"Файл переводов не найден: {translations_file}")
        return
    
    try:
        with translations_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
        count = 0
        for key, entry in data.items():
            original = entry.get("meta", {}).get("original", "")
            translations = entry.get("translations", {})
            
            for locale, trans_data in translations.items():
                value = trans_data.get("value", "")
                source = trans_data.get("source", "manual")
                
                if value:
                    TranslationRepository.set(
                        key=key,
                        locale=locale,
                        value=value,
                        original_value=original,
                        source=source,
                    )
                    count += 1
        
        logger.info(f"Мигрировано {count} переводов")
        
    except Exception as exc:
        logger.error(f"Ошибка миграции переводов: {exc}")


def _migrate_content_files(data_dir: Path) -> None:
    """Миграция контента из различных JSON файлов."""
    content_files = {
        "hero_content.json": "hero",
        "about_content.json": "about",
        "products_content.json": "products",
        "services_content.json": "services",
        "personalization_content.json": "personalization",
        "contacts_content.json": "contacts",
        "blog_content.json": "blog",
        "auracloud_slider.json": "auracloud_slider",
    }
    
    total_count = 0
    
    for filename, section in content_files.items():
        file_path = data_dir / filename
        if not file_path.exists():
            logger.warning(f"Файл контента не найден: {filename}")
            continue
        
        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            
            count = _migrate_section_data(section, data)
            total_count += count
            logger.info(f"Мигрировано {count} записей из {filename}")
            
        except Exception as exc:
            logger.error(f"Ошибка миграции {filename}: {exc}")
    
    logger.info(f"Всего мигрировано {total_count} записей контента")


def _migrate_section_data(section: str, data: Any, prefix: str = "") -> int:
    """
    Рекурсивная миграция данных секции с поддержкой мультиязычности.
    
    Поддерживаемые форматы:
    1. Мультиязычный: {"title": {"ru": "...", "lv": "...", "en": "..."}}
    2. Простой: {"title": "..."}
    3. Вложенные структуры и массивы
    
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
            # Пропускаем служебные поля
            if key in ("updated_at", "created_at"):
                continue
                
            full_key = f"{prefix}.{key}" if prefix else key
            
            # Проверяем мультиязычную структуру
            if _is_multilang_dict(value):
                # Мультиязычное значение - записываем в соответствующие поля
                ContentRepository.set(
                    section=section,
                    key=full_key,
                    value_ru=value.get("ru"),
                    value_lv=value.get("lv"),
                    value_en=value.get("en"),
                    data_type="text",
                )
                count += 1
            elif isinstance(value, list):
                # Массив - проверяем содержимое на мультиязычность
                processed_list = _process_multilang_list(value)
                ContentRepository.set(
                    section=section,
                    key=full_key,
                    value_ru=json.dumps(processed_list.get("ru", value), ensure_ascii=False),
                    value_lv=json.dumps(processed_list.get("lv"), ensure_ascii=False) if processed_list.get("lv") else None,
                    value_en=json.dumps(processed_list.get("en"), ensure_ascii=False) if processed_list.get("en") else None,
                    data_type="json",
                )
                count += 1
            elif isinstance(value, dict):
                # Вложенный объект - проверяем содержит ли мультиязычные поля
                if _contains_multilang_fields(value):
                    # Разделяем по языкам
                    processed = _extract_multilang_object(value)
                    ContentRepository.set(
                        section=section,
                        key=full_key,
                        value_ru=json.dumps(processed.get("ru", value), ensure_ascii=False),
                        value_lv=json.dumps(processed.get("lv"), ensure_ascii=False) if processed.get("lv") else None,
                        value_en=json.dumps(processed.get("en"), ensure_ascii=False) if processed.get("en") else None,
                        data_type="json",
                    )
                else:
                    # Обычный объект без мультиязычности
                    ContentRepository.set(
                        section=section,
                        key=full_key,
                        value_ru=json.dumps(value, ensure_ascii=False),
                        data_type="json",
                    )
                count += 1
            elif isinstance(value, str):
                ContentRepository.set(
                    section=section,
                    key=full_key,
                    value_ru=value,
                    data_type="text",
                )
                count += 1
            elif value is not None:
                # Числа, булевы и прочие примитивы
                ContentRepository.set(
                    section=section,
                    key=full_key,
                    value_ru=str(value),
                    data_type="text",
                )
                count += 1
    
    elif isinstance(data, list):
        processed_list = _process_multilang_list(data)
        ContentRepository.set(
            section=section,
            key=prefix or "data",
            value_ru=json.dumps(processed_list.get("ru", data), ensure_ascii=False),
            value_lv=json.dumps(processed_list.get("lv"), ensure_ascii=False) if processed_list.get("lv") else None,
            value_en=json.dumps(processed_list.get("en"), ensure_ascii=False) if processed_list.get("en") else None,
            data_type="json",
        )
        count += 1
    
    return count


def _contains_multilang_fields(obj: Dict) -> bool:
    """Проверяет, содержит ли объект мультиязычные поля."""
    for value in obj.values():
        if _is_multilang_dict(value):
            return True
        if isinstance(value, dict) and _contains_multilang_fields(value):
            return True
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and _contains_multilang_fields(item):
                    return True
    return False


def _extract_multilang_object(obj: Dict) -> Dict[str, Dict]:
    """
    Извлекает мультиязычные версии объекта.
    
    Returns:
        {"ru": {...}, "lv": {...}, "en": {...}}
    """
    result = {"ru": {}, "lv": {}, "en": {}}
    
    for key, value in obj.items():
        if _is_multilang_dict(value):
            for locale in SUPPORTED_LOCALES:
                if value.get(locale):
                    result[locale][key] = value[locale]
                elif value.get("ru"):
                    result[locale][key] = value["ru"]  # Fallback на русский
        elif isinstance(value, dict) and _contains_multilang_fields(value):
            nested = _extract_multilang_object(value)
            for locale in SUPPORTED_LOCALES:
                result[locale][key] = nested.get(locale, nested.get("ru", value))
        elif isinstance(value, list):
            processed = _process_multilang_list(value)
            for locale in SUPPORTED_LOCALES:
                result[locale][key] = processed.get(locale, processed.get("ru", value))
        else:
            # Одинаковое значение для всех языков
            for locale in SUPPORTED_LOCALES:
                result[locale][key] = value
    
    return result


def _process_multilang_list(items: list) -> Dict[str, list]:
    """
    Обрабатывает список с мультиязычными элементами.
    
    Returns:
        {"ru": [...], "lv": [...], "en": [...]}
    """
    if not items:
        return {"ru": items}
    
    # Проверяем, есть ли мультиязычные элементы
    has_multilang = False
    for item in items:
        if isinstance(item, dict) and _contains_multilang_fields(item):
            has_multilang = True
            break
    
    if not has_multilang:
        return {"ru": items}
    
    result = {"ru": [], "lv": [], "en": []}
    
    for item in items:
        if isinstance(item, dict) and _contains_multilang_fields(item):
            processed = _extract_multilang_object(item)
            for locale in SUPPORTED_LOCALES:
                result[locale].append(processed[locale])
        else:
            for locale in SUPPORTED_LOCALES:
                result[locale].append(item)
    
    return result


def _migrate_images(data_dir: Path) -> None:
    """Миграция информации об изображениях."""
    backgrounds_file = data_dir / "section_backgrounds.json"
    
    if not backgrounds_file.exists():
        logger.warning("Файл backgrounds не найден")
        return
    
    try:
        with backgrounds_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
        count = 0
        sections = data.get("sections", {})
        
        for section_name, section_data in sections.items():
            if isinstance(section_data, dict):
                for field_name, image_url in section_data.items():
                    if image_url and isinstance(image_url, str):
                        filename = Path(image_url).name
                        
                        existing = ImageRepository.get_by_section_field(section_name, field_name)
                        if not existing:
                            ImageRepository.create(
                                filename=filename,
                                original_filename=filename,
                                url=image_url,
                                section=section_name,
                                field=field_name,
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
        with visibility_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
        sections = data.get("sections", {})
        count = 0
        
        for section_name, is_visible in sections.items():
            SettingRepository.set(
                key=f"section_visible_{section_name}",
                value=str(is_visible).lower(),
                value_type="bool",
                description=f"Видимость секции {section_name}",
            )
            count += 1
        
        logger.info(f"Мигрировано {count} настроек видимости секций")
        
    except Exception as exc:
        logger.error(f"Ошибка миграции настроек видимости: {exc}")


def create_default_data() -> None:
    """
    Создание дефолтных данных при первом запуске, если JSON файлов нет.
    """
    if Content.query.first() or Translation.query.first():
        logger.info("В БД уже есть данные, создание дефолтных данных не требуется")
        return
    
    logger.info("Создание дефолтных данных для новой установки")
    
    try:
        # Hero секция
        ContentRepository.set(
            "hero", "slogan",
            value_ru="Balance in every drop",
            value_lv="Līdzsvars katrā pilienā",
            value_en="Balance in every drop",
            data_type="text",
        )
        ContentRepository.set(
            "hero", "subtitle",
            value_ru="Персонализированные масла на основе технологий AuraCloud® 3D и ДНК-тестирования",
            value_lv="Personalizētas eļļas, pamatojoties uz AuraCloud® 3D un DNS testēšanas tehnoloģijām",
            value_en="Personalized oils based on AuraCloud® 3D and DNA testing technologies",
            data_type="text",
        )
        ContentRepository.set(
            "hero", "cta_primary",
            value_ru="Подобрать масло",
            value_lv="Izvēlēties eļļu",
            value_en="Select Oil",
            data_type="text",
        )
        ContentRepository.set(
            "hero", "cta_secondary",
            value_ru="Записаться",
            value_lv="Pierakstīties",
            value_en="Book Appointment",
            data_type="text",
        )
        
        # Contacts секция
        ContentRepository.set(
            "contacts", "title",
            value_ru="Контакты",
            value_lv="Kontakti",
            value_en="Contacts",
            data_type="text",
        )
        ContentRepository.set(
            "contacts", "phone",
            value_ru="+371 20 000 000",
            data_type="text",
        )
        ContentRepository.set(
            "contacts", "email",
            value_ru="info@oilfusion.lv",
            data_type="text",
        )
        ContentRepository.set(
            "contacts", "address",
            value_ru="Рига, Латвия",
            value_lv="Rīga, Latvija",
            value_en="Riga, Latvia",
            data_type="text",
        )
        
        # Настройки
        SettingRepository.set("default_language", "ru", "string", "Язык по умолчанию")
        SettingRepository.set("auto_translation_enabled", "false", "bool", "Автоматический перевод")
        
        # Видимость секций
        for section in ["hero", "about", "products", "services", "personalization", "reviews", "blog", "contacts"]:
            SettingRepository.set(f"section_visible_{section}", "true", "bool", f"Видимость секции {section}")
        
        logger.info("Дефолтные данные успешно созданы")
        
    except Exception as exc:
        logger.error(f"Ошибка создания дефолтных данных: {exc}")
        db.session.rollback()
        raise
