"""
Модель для управления фоновыми изображениями секций лендинга.
Позволяет выбирать между изображением и градиентным фоном.
"""

from app.models.base import BaseContentModel
from datetime import datetime
from typing import Dict, Any, Optional


class SectionBackgrounds(BaseContentModel):
    """
    Модель для управления фоновыми изображениями секций.
    Поддерживает выбор между изображением и градиентом/цветом.
    """
    
    def __init__(self):
        super().__init__('data/section_backgrounds.json')
        self._init_default_data()
    
    def _init_default_data(self):
        """Инициализация данных по умолчанию."""
        if not self._data:
            default_data = {
                'hero': {
                    'type': 'image',  # image или gradient
                    'image_url': '/static/img/hero.png',
                    'gradient': 'linear-gradient(135deg, #FFA48F 0%, #FFF4BB 100%)',
                    'overlay_opacity': 0.3,  # Прозрачность наложения (0-1)
                    'overlay_color': '#000000'
                },
                'about': {
                    'type': 'gradient',
                    'image_url': '',
                    'gradient': 'linear-gradient(135deg, #FFA48F 0%, #FFF4BB 100%)',
                    'overlay_opacity': 0.8,
                    'overlay_color': '#FFFFFF'
                },
                'products': {
                    'type': 'gradient',
                    'image_url': '',
                    'gradient': 'linear-gradient(135deg, #FFA48F 0%, #FFF4BB 100%)',
                    'overlay_opacity': 0.8,
                    'overlay_color': '#FFFFFF'
                },
                'services': {
                    'type': 'white',
                    'image_url': '',
                    'gradient': '',
                    'overlay_opacity': 0,
                    'overlay_color': '#FFFFFF'
                },
                'personalization': {
                    'type': 'gradient',
                    'image_url': '',
                    'gradient': 'linear-gradient(135deg, #FFA48F 0%, #FFF4BB 100%)',
                    'overlay_opacity': 0.8,
                    'overlay_color': '#FFFFFF'
                },
                'reviews': {
                    'type': 'white',
                    'image_url': '',
                    'gradient': '',
                    'overlay_opacity': 0,
                    'overlay_color': '#FFFFFF'
                },
                'blog': {
                    'type': 'gradient',
                    'image_url': '',
                    'gradient': 'linear-gradient(135deg, #FFA48F 0%, #FFF4BB 100%)',
                    'overlay_opacity': 0.8,
                    'overlay_color': '#FFFFFF'
                },
                'contacts': {
                    'type': 'white',
                    'image_url': '',
                    'gradient': '',
                    'overlay_opacity': 0,
                    'overlay_color': '#FFFFFF'
                },
                'updated_at': datetime.now().isoformat()
            }
            self._data = default_data
            self._save_data()
    
    def get_section_background(self, section: str) -> Dict[str, Any]:
        """
        Получение настроек фона для секции.
        
        Args:
            section: Название секции (hero, about, products и т.д.)
            
        Returns:
            Словарь с настройками фона
        """
        return self.get(section, {
            'type': 'white',
            'image_url': '',
            'gradient': '',
            'overlay_opacity': 0,
            'overlay_color': '#FFFFFF'
        })
    
    def update_section_background(self, section: str, bg_type: str, 
                                  image_url: str = '', gradient: str = '',
                                  overlay_opacity: float = 0.3,
                                  overlay_color: str = '#000000') -> bool:
        """
        Обновление настроек фона секции.
        
        Args:
            section: Название секции
            bg_type: Тип фона (image, gradient, white)
            image_url: URL изображения
            gradient: CSS градиент
            overlay_opacity: Прозрачность наложения
            overlay_color: Цвет наложения
            
        Returns:
            True если обновление прошло успешно
        """
        background_data = {
            'type': bg_type,
            'image_url': image_url,
            'gradient': gradient,
            'overlay_opacity': overlay_opacity,
            'overlay_color': overlay_color
        }
        
        return self.set(section, background_data)
    
    def get_all_backgrounds(self) -> Dict[str, Dict[str, Any]]:
        """
        Получение всех фоновых настроек.
        
        Returns:
            Словарь со всеми настройками фонов
        """
        return self.get_all()
    
    def reset_section_to_default(self, section: str) -> bool:
        """
        Сброс секции к настройкам по умолчанию.
        
        Args:
            section: Название секции
            
        Returns:
            True если сброс прошёл успешно
        """
        default_backgrounds = {
            'hero': {
                'type': 'gradient',
                'image_url': '',
                'gradient': 'linear-gradient(135deg, #FFA48F 0%, #FFF4BB 100%)',
                'overlay_opacity': 0.3,
                'overlay_color': '#000000'
            },
            'about': {
                'type': 'gradient',
                'image_url': '',
                'gradient': 'linear-gradient(135deg, #FFA48F 0%, #FFF4BB 100%)',
                'overlay_opacity': 0.8,
                'overlay_color': '#FFFFFF'
            },
            'products': {
                'type': 'gradient',
                'image_url': '',
                'gradient': 'linear-gradient(135deg, #FFA48F 0%, #FFF4BB 100%)',
                'overlay_opacity': 0.8,
                'overlay_color': '#FFFFFF'
            }
        }
        
        if section in default_backgrounds:
            return self.set(section, default_backgrounds[section])
        
        return False

