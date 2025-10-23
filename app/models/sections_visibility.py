"""
Модель для управления видимостью разделов сайта.
"""
from datetime import datetime
from typing import Dict, Any, List
from .base import BaseContentModel


class SectionsVisibility(BaseContentModel):
    """Управление видимостью разделов сайта."""

    def __init__(self) -> None:
        super().__init__('data/sections_visibility.json')
        self._init_default_data()

    def _init_default_data(self) -> None:
        """Инициализация данных по умолчанию."""
        if not self._data:
            self._data = {
                'sections': {
                    'hero': True,
                    'about': True,
                    'products': True,
                    'services': True,
                    'personalization': True,
                    'reviews': True,
                    'blog': True,
                    'contacts': True
                },
                'updated_at': datetime.now().isoformat(),
            }
            self._save_data()

    def is_visible(self, section_name: str) -> bool:
        """Проверить видимость раздела."""
        return self.get('sections', {}).get(section_name, True)

    def set_visibility(self, section_name: str, visible: bool) -> bool:
        """Установить видимость раздела."""
        sections = self.get('sections', {})
        sections[section_name] = visible
        return self.set('sections', sections)

    def get_all_sections(self) -> Dict[str, bool]:
        """Получить видимость всех разделов."""
        return self.get('sections', {})

    def update_sections(self, sections_data: Dict[str, bool]) -> bool:
        """Обновить видимость всех разделов."""
        return self.set('sections', sections_data)
