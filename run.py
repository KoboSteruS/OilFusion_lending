"""
Точка входа для запуска Flask приложения OilFusion Landing.
"""

from app import create_app
from app.config.settings import config_by_name
from app.utils.logger import get_logger
import os

# Определение окружения
environment = os.getenv('FLASK_ENV', 'development')
config = config_by_name.get(environment, config_by_name['default'])

# Создание приложения
app = create_app(config)
logger = get_logger()


if __name__ == '__main__':
    logger.info(f"Запуск приложения в режиме: {environment}")
    logger.info(f"Адрес: http://{app.config['HOST']}:{app.config['PORT']}")
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )





