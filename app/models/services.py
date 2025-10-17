"""
Модель управления услугами. Поддерживает список карточек с иконкой/изображением,
ценой, описанием и списком особенностей.
"""

from datetime import datetime
from typing import Any, Dict, List

from app.models.content import BaseContentModel


class ServicesContent(BaseContentModel):
    """Контент секции "Услуги"."""

    def __init__(self) -> None:
        super().__init__('data/services_content.json')
        self._init_default_data()

    def _init_default_data(self) -> None:
        if not self._data:
            self._data = {
                'title': 'Наши услуги',
                'services': [],
                'updated_at': datetime.now().isoformat(),
            }
            self._save_data()

    # CRUD
    def list(self) -> List[Dict[str, Any]]:
        return self.get('services', [])

    def add(self, service: Dict[str, Any]) -> bool:
        items = self.list()
        items.append(service)
        return self.set('services', items)

    def update_item(self, index: int, service: Dict[str, Any]) -> bool:
        items = self.list()
        if 0 <= index < len(items):
            items[index] = service
            return self.set('services', items)
        return False

    def delete(self, index: int) -> bool:
        items = self.list()
        if 0 <= index < len(items):
            items.pop(index)
            return self.set('services', items)
        return False

