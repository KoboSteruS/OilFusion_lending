"""
Модели контента для админки.
Простая реализация без базы данных - данные хранятся в JSON файлах.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from werkzeug.utils import secure_filename


class BaseContentModel:
    """
    Базовый класс для моделей контента.
    Обеспечивает сохранение и загрузку данных в JSON файлы.
    """
    
    def __init__(self, data_file: str):
        """
        Инициализация модели.
        
        Args:
            data_file: Путь к JSON файлу для хранения данных
        """
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """
        Загрузка данных из JSON файла.
        
        Returns:
            Словарь с данными или пустой словарь если файл не существует
        """
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_data(self) -> bool:
        """
        Сохранение данных в JSON файл.
        
        Returns:
            True если сохранение прошло успешно, False иначе
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Получение значения по ключу.
        
        Args:
            key: Ключ для поиска
            default: Значение по умолчанию
            
        Returns:
            Значение по ключу или default
        """
        return self._data.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        Установка значения по ключу.
        
        Args:
            key: Ключ
            value: Значение
            
        Returns:
            True если сохранение прошло успешно
        """
        self._data[key] = value
        return self._save_data()
    
    def update(self, data: Dict[str, Any]) -> bool:
        """
        Обновление данных.
        
        Args:
            data: Словарь с новыми данными
            
        Returns:
            True если сохранение прошло успешно
        """
        self._data.update(data)
        return self._save_data()
    
    def get_all(self) -> Dict[str, Any]:
        """
        Получение всех данных.
        
        Returns:
            Словарь со всеми данными
        """
        return self._data.copy()


class AboutContent(BaseContentModel):
    """
    Модель для контента секции "О компании".
    """
    
    def __init__(self):
        super().__init__('data/about_content.json')
        self._init_default_data()
    
    def _init_default_data(self):
        """Инициализация данных по умолчанию."""
        if not self._data:
            default_data = {
                'title': 'О нас',
                'description': 'Мы создаём уникальные масла, основываясь на передовых технологиях AuraCloud® 3D и ДНК-тестирования',
                'philosophy': 'Наша философия - баланс и гармония в каждой капле',
                'background_image_url': '',
                'background_overlay_opacity': 0.8,
                'background_overlay_color': '#FFFFFF',
                'features': [
                    {
                        'title': 'AuraCloud® 3D',
                        'description': 'Передовая технология визуализации энергетической ауры для точного подбора продуктов',
                        'icon': 'aura',
                        'image_url': ''
                    },
                    {
                        'title': 'ДНК-тестирование',
                        'description': 'Индивидуальный подбор масел на основе вашего генетического профиля',
                        'icon': 'dna',
                        'image_url': ''
                    }
                ],
                'updated_at': datetime.now().isoformat()
            }
            self._data = default_data
            self._save_data()
    
    def get_features(self) -> List[Dict[str, str]]:
        """Получение списка особенностей."""
        return self.get('features', [])
    
    def update_feature(self, index: int, feature_data: Dict[str, str]) -> bool:
        """
        Обновление особенности по индексу.
        
        Args:
            index: Индекс особенности
            feature_data: Данные особенности
            
        Returns:
            True если обновление прошло успешно
        """
        features = self.get_features()
        if 0 <= index < len(features):
            features[index] = feature_data
            return self.set('features', features)
        return False
    
    def add_feature(self, feature_data: Dict[str, str]) -> bool:
        """
        Добавление новой особенности.
        
        Args:
            feature_data: Данные особенности
            
        Returns:
            True если добавление прошло успешно
        """
        features = self.get_features()
        features.append(feature_data)
        return self.set('features', features)
    
    def remove_feature(self, index: int) -> bool:
        """
        Удаление особенности по индексу.
        
        Args:
            index: Индекс особенности
            
        Returns:
            True если удаление прошло успешно
        """
        features = self.get_features()
        if 0 <= index < len(features):
            features.pop(index)
            return self.set('features', features)
        return False


class PersonalizationContent(BaseContentModel):
    """
    Модель для контента секции "Персонализация".
    """
    
    def __init__(self):
        super().__init__('data/personalization_content.json')
        self._init_default_data()
    
    def _init_default_data(self):
        """Инициализация данных по умолчанию."""
        if not self._data:
            default_data = {
                'title': 'Персонализация',
                'subtitle': 'Технологии будущего для вашего здоровья сегодня',
                'dna_testing': {
                    'title': 'ДНК-тестирование',
                    'description': 'Индивидуальный подбор масел на основе вашего генетического профиля',
                    'features': [
                        'Анализ генетических маркеров',
                        'Определение индивидуальных потребностей',
                        'Точная формула под ваш организм',
                        'Научно обоснованный подход'
                    ]
                },
                'auracloud': {
                    'title': 'AuraCloud® 3D',
                    'description': 'Визуализация вашей энергетической ауры для точного подбора продуктов',
                    'features': [
                        'Трёхмерная визуализация ауры',
                        'Анализ энергетических центров',
                        'Определение дисбалансов',
                        'Отслеживание динамики изменений'
                    ]
                },
                'info_text': 'Технология AuraCloud® 3D основана на Bio-Well системе',
                'info_description': 'Мы используем передовую технологию Bio-Well для визуализации энергетического поля человека. Эта система позволяет увидеть изменения в вашей ауре и подобрать оптимальные продукты.',
                'bio_well_url': 'https://bio-well.com/en-intl',
                'updated_at': datetime.now().isoformat()
            }
            self._data = default_data
            self._save_data()
    
    def get_dna_features(self) -> List[str]:
        """Получение списка особенностей ДНК-тестирования."""
        return self.get('dna_testing', {}).get('features', [])
    
    def get_auracloud_features(self) -> List[str]:
        """Получение списка особенностей AuraCloud® 3D."""
        return self.get('auracloud', {}).get('features', [])
    
    def update_dna_feature(self, index: int, feature: str) -> bool:
        """
        Обновление особенности ДНК-тестирования.
        
        Args:
            index: Индекс особенности
            feature: Текст особенности
            
        Returns:
            True если обновление прошло успешно
        """
        features = self.get_dna_features()
        if 0 <= index < len(features):
            features[index] = feature
            dna_data = self.get('dna_testing', {})
            dna_data['features'] = features
            return self.set('dna_testing', dna_data)
        return False
    
    def update_auracloud_feature(self, index: int, feature: str) -> bool:
        """
        Обновление особенности AuraCloud® 3D.
        
        Args:
            index: Индекс особенности
            feature: Текст особенности
            
        Returns:
            True если обновление прошло успешно
        """
        features = self.get_auracloud_features()
        if 0 <= index < len(features):
            features[index] = feature
            auracloud_data = self.get('auracloud', {})
            auracloud_data['features'] = features
            return self.set('auracloud', auracloud_data)
        return False


class BlogArticle:
    """
    Модель для статьи блога.
    """
    
    def __init__(self, title: str = '', content: str = '', excerpt: str = '', 
                 category: str = '', read_time: int = 5, image: str = '', 
                 published: bool = True, created_at: str = None):
        self.title = title
        self.content = content
        self.excerpt = excerpt
        self.category = category
        self.read_time = read_time
        self.image = image
        self.published = published
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь."""
        return {
            'title': self.title,
            'content': self.content,
            'excerpt': self.excerpt,
            'category': self.category,
            'read_time': self.read_time,
            'image': self.image,
            'published': self.published,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BlogArticle':
        """Создание из словаря."""
        return cls(
            title=data.get('title', ''),
            content=data.get('content', ''),
            excerpt=data.get('excerpt', ''),
            category=data.get('category', ''),
            read_time=data.get('read_time', 5),
            image=data.get('image', ''),
            published=data.get('published', True),
            created_at=data.get('created_at', datetime.now().isoformat())
        )


class BlogContent(BaseContentModel):
    """
    Модель для контента блога.
    """
    
    def __init__(self):
        super().__init__('data/blog_content.json')
        self._init_default_data()
    
    def _init_default_data(self):
        """Инициализация данных по умолчанию."""
        if not self._data:
            default_articles = [
                {
                    'title': 'Как работает ДНК-тестирование для подбора масел',
                    'content': 'Полное содержание статьи о ДНК-тестировании...',
                    'excerpt': 'Узнайте о научных основах генетического тестирования и как это помогает подобрать идеальное масло именно для вас.',
                    'category': 'Технологии',
                    'read_time': 5,
                    'image': '/static/images/blog/dna-testing.jpg',
                    'published': True,
                    'created_at': datetime.now().isoformat()
                },
                {
                    'title': 'AuraCloud® 3D: революция в энергетической диагностике',
                    'content': 'Полное содержание статьи о AuraCloud® 3D...',
                    'excerpt': 'Погрузитесь в мир передовых технологий визуализации ауры и узнайте, как это помогает улучшить ваше самочувствие.',
                    'category': 'Здоровье',
                    'read_time': 7,
                    'image': '/static/images/blog/auracloud.jpg',
                    'published': True,
                    'created_at': datetime.now().isoformat()
                },
                {
                    'title': '10 правил использования персонализированных масел',
                    'content': 'Полное содержание статьи о правилах использования...',
                    'excerpt': 'Практические рекомендации по применению наших продуктов для достижения максимального эффекта и долгосрочного результата.',
                    'category': 'Советы',
                    'read_time': 4,
                    'image': '/static/images/blog/oil-usage.jpg',
                    'published': True,
                    'created_at': datetime.now().isoformat()
                }
            ]
            
            default_data = {
                'title': 'Блог',
                'subtitle': 'Полезная информация о здоровье и персонализации',
                'articles': default_articles,
                'updated_at': datetime.now().isoformat()
            }
            self._data = default_data
            self._save_data()
    
    def get_articles(self) -> List[Dict[str, Any]]:
        """Получение списка статей."""
        return self.get('articles', [])
    
    def get_published_articles(self) -> List[Dict[str, Any]]:
        """Получение опубликованных статей."""
        articles = self.get_articles()
        return [article for article in articles if article.get('published', True)]
    
    def get_article(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Получение статьи по индексу.
        
        Args:
            index: Индекс статьи
            
        Returns:
            Словарь с данными статьи или None
        """
        articles = self.get_articles()
        if 0 <= index < len(articles):
            return articles[index]
        return None
    
    def add_article(self, article_data: Dict[str, Any]) -> bool:
        """
        Добавление новой статьи.
        
        Args:
            article_data: Данные статьи
            
        Returns:
            True если добавление прошло успешно
        """
        articles = self.get_articles()
        article_data['created_at'] = datetime.now().isoformat()
        articles.append(article_data)
        return self.set('articles', articles)
    
    def update_article(self, index: int, article_data: Dict[str, Any]) -> bool:
        """
        Обновление статьи по индексу.
        
        Args:
            index: Индекс статьи
            article_data: Новые данные статьи
            
        Returns:
            True если обновление прошло успешно
        """
        articles = self.get_articles()
        if 0 <= index < len(articles):
            # Сохраняем дату создания
            if 'created_at' not in article_data:
                article_data['created_at'] = articles[index].get('created_at', datetime.now().isoformat())
            articles[index] = article_data
            return self.set('articles', articles)
        return False
    
    def delete_article(self, index: int) -> bool:
        """
        Удаление статьи по индексу.
        
        Args:
            index: Индекс статьи
            
        Returns:
            True если удаление прошло успешно
        """
        articles = self.get_articles()
        if 0 <= index < len(articles):
            articles.pop(index)
            return self.set('articles', articles)
        return False

