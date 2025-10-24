"""
Модель управления услугами. Поддерживает список карточек с иконкой/изображением,
ценой, описанием и списком особенностей.
"""

from datetime import datetime
from typing import Any, Dict, List

from app.models.base import BaseContentModel


class ServicesContent(BaseContentModel):
    """Контент секции "Услуги"."""

    def __init__(self) -> None:
        super().__init__('data/services_content.json')
        self._init_default_data()

    def _init_default_data(self) -> None:
        if not self._data:
            default_services = [
                {
                    'name': 'ДНК-тестирование',
                    'description': 'Комплексный анализ генетических особенностей для подбора идеального масла.',
                    'price': 'от 5 000 ₽',
                    'icon': '/static/img/service1.png',
                    'features': [
                        'Анализ 50+ генетических маркеров',
                        'Персональные рекомендации',
                        'Подробный отчет с результатами',
                        'Консультация специалиста'
                    ]
                },
                {
                    'name': 'AuraCloud® 3D диагностика',
                    'description': 'Современная технология визуализации энергетического поля человека.',
                    'price': 'от 3 500 ₽',
                    'icon': '/static/img/service2.png',
                    'features': [
                        '3D-модель ауры в реальном времени',
                        'Анализ энергетических центров',
                        'Рекомендации по балансировке',
                        'Сравнение до и после'
                    ]
                },
                {
                    'name': 'Персональная консультация',
                    'description': 'Индивидуальная встреча с экспертом для подбора оптимального ухода.',
                    'price': 'от 2 000 ₽',
                    'icon': '/static/img/service3.png',
                    'features': [
                        'Анализ состояния кожи',
                        'Подбор продуктов',
                        'План ухода на месяц',
                        'Последующее сопровождение'
                    ]
                }
            ]
            
            self._data = {
                'title': 'Наши услуги',
                'services': default_services,
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

