"""
Модель управления контактами компании.
"""

from datetime import datetime
from typing import Any, Dict

from app.models.base import BaseContentModel


class ContactsContent(BaseContentModel):
    """Контент секции "Контакты"."""

    def __init__(self) -> None:
        super().__init__('data/contacts_content.json')
        self._init_default_data()

    def _init_default_data(self) -> None:
        if not self._data:
            self._data = {
                'email': 'info@oilfusion.example',
                'phone': '+1-555-0100',
                'address': 'New York, NY',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'maps_api_key': '',
                'form_title': 'Записаться на консультацию',
                'form_subtitle': 'Оставьте заявку и мы свяжемся с вами',
                'form_button_text': 'Отправить',
                'form_success_message': 'Спасибо! Мы свяжемся с вами в ближайшее время.',
                'updated_at': datetime.now().isoformat(),
            }
            self._save_data()


