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
            self._data = {
                'title': 'Наша продукция',
                'products': [],
                'updated_at': datetime.now().isoformat(),
            }
            self._save_data()

    # CRUD
    def list(self) -> List[Dict[str, Any]]:
        return self.get('products', [])

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

