"""
Базовый класс для всех моделей контента.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class BaseContentModel:
    """Базовый класс для управления контентом через JSON файлы."""

    def __init__(self, file_path: str):
        """
        Инициализация модели.
        
        Args:
            file_path: Путь к JSON файлу для хранения данных
        """
        self.file_path = file_path
        self._data = {}
        self._load_data()

    def _load_data(self) -> None:
        """Загрузка данных из JSON файла."""
        try:
            if Path(self.file_path).exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            else:
                self._data = {}
                self._init_default_data()
        except (json.JSONDecodeError, FileNotFoundError):
            self._data = {}
            self._init_default_data()

    def _save_data(self) -> bool:
        """Сохранение данных в JSON файл."""
        try:
            # Создаем директорию если не существует
            Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def _init_default_data(self) -> None:
        """Инициализация данных по умолчанию. Переопределяется в наследниках."""
        pass

    def get(self, key: str, default: Any = None) -> Any:
        """Получить значение по ключу."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """Установить значение по ключу."""
        self._data[key] = value
        self._data['updated_at'] = datetime.now().isoformat()
        return self._save_data()

    def get_all(self) -> Dict[str, Any]:
        """Получить все данные."""
        return self._data.copy()

    def update(self, data: Dict[str, Any]) -> bool:
        """Обновить данные."""
        self._data.update(data)
        self._data['updated_at'] = datetime.now().isoformat()
        return self._save_data()

    def delete(self, key: str) -> bool:
        """Удалить ключ из данных."""
        if key in self._data:
            del self._data[key]
            self._data['updated_at'] = datetime.now().isoformat()
            return self._save_data()
        return False
