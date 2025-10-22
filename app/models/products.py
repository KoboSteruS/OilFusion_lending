"""
Модель управления продукцией (карточки продуктов) с хранением в JSON.
Поддержка изображений, цены, категории и описания.
"""

from datetime import datetime
from typing import Any, Dict, List

from app.models.content import BaseContentModel


class ProductsContent(BaseContentModel):
    """Контент секции "Продукция"."""

    def __init__(self) -> None:
        super().__init__('data/products_content.json')
        self._init_default_data()

    def _init_default_data(self) -> None:
        if not self._data:
            default_products = [
                {
                    'name': 'Масло для лица "Баланс"',
                    'category': 'Уход за лицом',
                    'description': 'Персонализированное масло для нормализации работы сальных желез и восстановления естественного баланса кожи.',
                    'price': 'от 3 500 ₽',
                    'image': '/static/img/product1.jpg',
                    'featured': True
                },
                {
                    'name': 'Масло для тела "Гармония"',
                    'category': 'Уход за телом',
                    'description': 'Увлажняющее масло с натуральными экстрактами для поддержания упругости и эластичности кожи.',
                    'price': 'от 2 800 ₽',
                    'image': '/static/img/product2.jpg',
                    'featured': True
                },
                {
                    'name': 'Масло для волос "Сила"',
                    'category': 'Уход за волосами',
                    'description': 'Восстанавливающее масло для укрепления волосяных фолликулов и придания блеска.',
                    'price': 'от 2 200 ₽',
                    'image': '/static/img/product3.jpg',
                    'featured': False
                },
                {
                    'name': 'Масло для ауры "Энергия"',
                    'category': 'Энергетика',
                    'description': 'Специальная смесь для гармонизации энергетического поля и восстановления баланса.',
                    'price': 'от 4 200 ₽',
                    'image': '/static/img/product4.jpg',
                    'featured': True
                },
                {
                    'name': 'Комплексная программа "Полная"',
                    'category': 'Комплекты',
                    'description': 'Полный набор продуктов с индивидуальным сопровождением и консультацией.',
                    'price': 'от 12 000 ₽',
                    'image': '/static/img/product5.jpg',
                    'featured': True
                },
                {
                    'name': 'Масло для массажа "Релакс"',
                    'category': 'Массаж',
                    'description': 'Расслабляющее масло с ароматерапевтическими свойствами для глубокого восстановления.',
                    'price': 'от 2 500 ₽',
                    'image': '/static/img/product6.jpg',
                    'featured': False
                }
            ]
            
            self._data = {
                'title': 'Наша продукция',
                'products': default_products,
                'updated_at': datetime.now().isoformat(),
            }
            self._save_data()

    # CRUD
    def list(self) -> List[Dict[str, Any]]:
        return self.get('products', [])

    def get_featured(self, limit: int = 6) -> List[Dict[str, Any]]:
        """Получить избранные товары (с флагом featured=True)."""
        all_products = self.list()
        featured = [p for p in all_products if p.get('featured', False)]
        return featured[:limit]

    def add(self, product: Dict[str, Any]) -> bool:
        items = self.list()
        items.append(product)
        return self.set('products', items)

    def update_item(self, index: int, product: Dict[str, Any]) -> bool:
        items = self.list()
        if 0 <= index < len(items):
            items[index] = product
            return self.set('products', items)
        return False

    def delete(self, index: int) -> bool:
        items = self.list()
        if 0 <= index < len(items):
            items.pop(index)
            return self.set('products', items)
        return False

