"""
Скрипт миграции данных с одноязычного на мультиязычный контент.
Запустите этот скрипт ОДИН РАЗ после обновления моделей.
"""

from app import create_app
from app.database import db
from app.database.models import Content
from app.utils.logger import get_logger

logger = get_logger()


def migrate_content_to_multilang():
    """
    Миграция существующего контента на мультиязычную структуру.
    Переносит данные из старого поля 'value' в 'value_ru'.
    """
    app = create_app()
    
    with app.app_context():
        logger.info("Начинаем миграцию контента на мультиязычную структуру")
        
        # Проверяем, есть ли уже поля value_ru, value_lv, value_en
        try:
            test = db.session.execute(db.text("SELECT value_ru FROM content LIMIT 1")).fetchone()
            logger.info("Поля для мультиязычности уже существуют, миграция не требуется")
            return
        except Exception:
            logger.info("Поля для мультиязычности не найдены, начинаем миграцию")
        
        # Проверяем, есть ли старое поле 'value' в таблице
        try:
            # Пытаемся прочитать старое поле
            contents = db.session.execute(
                db.text("SELECT id, section, key, value FROM content")
            ).fetchall()
            
            logger.info(f"Найдено {len(contents)} записей для миграции")
            
            # Добавляем новые столбцы
            logger.info("Добавляем столбцы value_ru, value_lv, value_en...")
            db.session.execute(db.text("ALTER TABLE content ADD COLUMN value_ru TEXT"))
            db.session.execute(db.text("ALTER TABLE content ADD COLUMN value_lv TEXT"))
            db.session.execute(db.text("ALTER TABLE content ADD COLUMN value_en TEXT"))
            db.session.commit()
            logger.info("Столбцы добавлены")
            
            # Обновляем каждую запись: переносим value в value_ru
            for row in contents:
                content_id, section, key, old_value = row
                
                db.session.execute(
                    db.text("""
                        UPDATE content 
                        SET value_ru = :value
                        WHERE id = :content_id
                    """),
                    {'value': old_value, 'content_id': content_id}
                )
                logger.info(f"Мигрировано: {section}.{key}")
            
            db.session.commit()
            logger.info("Миграция успешно завершена!")
            
            # Теперь можно удалить старое поле 'value'
            logger.info("Удаляем старое поле 'value'...")
            
            try:
                # SQLite не поддерживает DROP COLUMN напрямую,
                # поэтому создаём новую таблицу без старого поля
                db.session.execute(db.text("""
                    CREATE TABLE content_new (
                        id INTEGER PRIMARY KEY,
                        section VARCHAR(100) NOT NULL,
                        key VARCHAR(255) NOT NULL,
                        value_ru TEXT,
                        value_lv TEXT,
                        value_en TEXT,
                        data_type VARCHAR(50) DEFAULT 'text',
                        created_at DATETIME NOT NULL,
                        updated_at DATETIME NOT NULL,
                        UNIQUE(section, key)
                    )
                """))
                
                # Копируем данные
                db.session.execute(db.text("""
                    INSERT INTO content_new (id, section, key, value_ru, value_lv, value_en, data_type, created_at, updated_at)
                    SELECT id, section, key, value_ru, value_lv, value_en, data_type, created_at, updated_at
                    FROM content
                """))
                
                # Удаляем старую таблицу
                db.session.execute(db.text("DROP TABLE content"))
                
                # Переименовываем новую таблицу
                db.session.execute(db.text("ALTER TABLE content_new RENAME TO content"))
                
                # Создаём индексы
                db.session.execute(db.text("CREATE INDEX ix_content_section ON content (section)"))
                db.session.execute(db.text("CREATE INDEX ix_content_key ON content (key)"))
                
                db.session.commit()
                logger.info("Старое поле 'value' успешно удалено")
                
            except Exception as e:
                logger.warning(f"Не удалось удалить старое поле (возможно, его уже нет): {e}")
                db.session.rollback()
            
        except Exception as e:
            logger.error(f"Ошибка миграции: {e}")
            logger.info("Возможно, миграция уже была выполнена ранее")
            db.session.rollback()


if __name__ == '__main__':
    migrate_content_to_multilang()

