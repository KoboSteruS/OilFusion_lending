"""
Подключение к базе данных SQLite.
"""

from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def init_db(app: Flask) -> None:
    """
    Инициализация базы данных.
    Создаёт таблицы и выполняет миграцию данных из JSON при первом запуске.
    
    Args:
        app: Экземпляр Flask приложения
    """
    from app.utils.logger import get_logger
    logger = get_logger()
    
    # Путь к БД в папке data
    data_dir = Path(app.config['BASE_DIR']) / 'data'
    db_path = data_dir / 'oilfusion.db'
    data_dir.mkdir(parents=True, exist_ok=True)
    
    is_new_db = not db_path.exists()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Создаём все таблицы
        db.create_all()
        logger.info("Таблицы базы данных созданы")
        
        # Если БД новая или миграция не выполнена, запускаем миграцию
        from app.database.migrations import migrate_json_to_db, create_default_data
        from app.database.repositories import SettingRepository
        
        migration_completed = SettingRepository.get('migration_completed')
        
        if is_new_db or migration_completed != 'true':
            logger.info("Запуск миграции данных из JSON в SQLite")
            try:
                migrate_json_to_db(data_dir)
            except Exception as e:
                logger.warning(f"Ошибка миграции JSON: {e}")
                logger.info("Создание дефолтных данных")
                create_default_data()

