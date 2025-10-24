"""
Модель для управления слайдером AuraCloud До/После.
"""
from datetime import datetime
from typing import Dict, Any
from .base import BaseContentModel


class AuraCloudSlider(BaseContentModel):
    """Управление слайдером AuraCloud До/После."""

    def __init__(self) -> None:
        super().__init__('data/auracloud_slider.json')
        self._init_default_data()

    def _init_default_data(self) -> None:
        """Инициализация данных по умолчанию."""
        if not self._data:
            self._data = {
                'title': 'AuraCloud® 3D - До и После',
                'subtitle': 'Посмотрите, как меняется ваша аура после использования наших масел',
                'before_image': '',
                'after_image': '',
                'before_label': 'До',
                'after_label': 'После',
                'description': 'Интерактивный слайдер показывает трансформацию энергетического поля человека',
                'enabled': True,
                'updated_at': datetime.now().isoformat(),
            }
            self._save_data()

    def get_all(self) -> Dict[str, Any]:
        """Получить все данные слайдера."""
        return self._data

    def update(self, data: Dict[str, Any]) -> bool:
        """Обновить данные слайдера."""
        self._data.update(data)
        self._data['updated_at'] = datetime.now().isoformat()
        return self._save_data()

    def set_before_image(self, image_url: str) -> bool:
        """Установить изображение 'До'."""
        self._data['before_image'] = image_url
        self._data['updated_at'] = datetime.now().isoformat()
        return self._save_data()

    def set_after_image(self, image_url: str) -> bool:
        """Установить изображение 'После'."""
        self._data['after_image'] = image_url
        self._data['updated_at'] = datetime.now().isoformat()
        return self._save_data()

    def set_enabled(self, enabled: bool) -> bool:
        """Включить/выключить слайдер."""
        self._data['enabled'] = enabled
        self._data['updated_at'] = datetime.now().isoformat()
        return self._save_data()

