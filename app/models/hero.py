"""
Модель управления Hero секцией (главный баннер).
"""

from datetime import datetime
from typing import Any, Dict

from app.models.content import BaseContentModel


class HeroContent(BaseContentModel):
    """Контент секции Hero (главный баннер)."""

    def __init__(self) -> None:
        super().__init__('data/hero_content.json')
        self._init_default_data()

    def _init_default_data(self) -> None:
        if not self._data:
            self._data = {
                'slogan': 'Balance in every drop',
                'subtitle': 'Персонализированные масла на основе технологий AuraCloud® 3D и ДНК-тестирования',
                'cta_primary': 'Подобрать масло',
                'cta_secondary': 'Записаться',
                'scroll_text': 'Листайте вниз',
                'updated_at': datetime.now().isoformat(),
            }
            self._save_data()

    def get_slogan(self) -> str:
        """Получение слогана."""
        return self.get('slogan', 'Balance in every drop')

    def get_subtitle(self) -> str:
        """Получение подзаголовка."""
        return self.get('subtitle', 'Персонализированные масла на основе технологий AuraCloud® 3D и ДНК-тестирования')

    def get_cta_primary(self) -> str:
        """Получение текста основной кнопки."""
        return self.get('cta_primary', 'Подобрать масло')

    def get_cta_secondary(self) -> str:
        """Получение текста вторичной кнопки."""
        return self.get('cta_secondary', 'Записаться')

    def get_scroll_text(self) -> str:
        """Получение текста скролл индикатора."""
        return self.get('scroll_text', 'Листайте вниз')

    def update_content(self, data: Dict[str, Any]) -> bool:
        """Обновление контента Hero секции."""
        update_data = {
            'slogan': data.get('slogan', self.get_slogan()),
            'subtitle': data.get('subtitle', self.get_subtitle()),
            'cta_primary': data.get('cta_primary', self.get_cta_primary()),
            'cta_secondary': data.get('cta_secondary', self.get_cta_secondary()),
            'scroll_text': data.get('scroll_text', self.get_scroll_text()),
            'updated_at': datetime.now().isoformat(),
        }
        
        for key, value in update_data.items():
            self.set(key, value)
        
        return self._save_data()
