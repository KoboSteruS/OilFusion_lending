"""
Модуль настройки логирования с использованием loguru.
Обеспечивает централизованное логирование для всего приложения.
"""

import sys
from pathlib import Path
from loguru import logger
from typing import Any


def setup_logger(
    log_level: str = "INFO",
    log_file: str = "logs/app.log",
    rotation: str = "10 MB",
    retention: str = "1 week",
    compression: str = "zip"
) -> Any:
    """
    Настройка логгера приложения.
    
    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Путь к файлу логов
        rotation: Условие ротации логов
        retention: Время хранения старых логов
        compression: Тип сжатия архивных логов
        
    Returns:
        Настроенный экземпляр логгера
    """
    # Удаляем стандартный handler
    logger.remove()
    
    # Добавляем handler для консоли с цветным выводом
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level
    )
    
    # Создаём директорию для логов если её нет
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Добавляем handler для файла с ротацией
    logger.add(
        log_file,
        rotation=rotation,
        retention=retention,
        compression=compression,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        encoding="utf-8"
    )
    
    logger.info(f"Логгер настроен. Уровень: {log_level}, Файл: {log_file}")
    
    return logger


def get_logger() -> Any:
    """
    Получить настроенный экземпляр логгера.
    
    Returns:
        Экземпляр логгера
    """
    return logger





