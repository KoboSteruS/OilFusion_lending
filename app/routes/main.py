"""
Основные маршруты лендинга OilFusion.
Обрабатывает все запросы к главной странице и её секциям.
"""

from flask import Blueprint, render_template, current_app
from app.utils.logger import get_logger
from app.models.content import AboutContent, PersonalizationContent, BlogContent
from app.models.products import ProductsContent
from app.models.services import ServicesContent
from app.models.images import SectionBackgrounds
from app.models.contacts import ContactsContent
from app.models.hero import HeroContent

logger = get_logger()

# Создание Blueprint для основных маршрутов
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    Главная страница лендинга.
    Отображает все секции: Hero, О компании, Продукция, Услуги, 
    Персонализация, Отзывы, Блог, Контакты.
    
    Returns:
        Отрендеренный HTML шаблон главной страницы
    """
    logger.info("Запрос главной страницы")
    
    # Получаем настройки фонов
    backgrounds = SectionBackgrounds()
    
    # Данные для Hero секции
    # Данные Hero секции из модели
    hero_content = HeroContent()
    hero_data = {
        'slogan': hero_content.get_slogan(),
        'subtitle': hero_content.get_subtitle(),
        'cta_primary': hero_content.get_cta_primary(),
        'cta_secondary': hero_content.get_cta_secondary(),
        'scroll_text': hero_content.get_scroll_text(),
        'background': backgrounds.get_section_background('hero')
    }
    
    # Данные о компании из модели
    about_content = AboutContent()
    about_data = about_content.get_all()
    about_data['background'] = backgrounds.get_section_background('about')
    
    # Данные о продукции
    products_store = ProductsContent()
    products_data = {
        'title': 'Наша продукция',
        'products_list': products_store.list(),
        'background': backgrounds.get_section_background('products')
    }
    
    # Данные об услугах
    services_store = ServicesContent()
    services_data = {
        'title': 'Наши услуги',
        'services_list': services_store.list()
    }
    
    # Данные о персонализации из модели
    personalization_content = PersonalizationContent()
    personalization_data = personalization_content.get_all()
    
    # Данные отзывов (заглушка)
    reviews_data = {
        'title': 'Отзывы наших клиентов',
        'reviews_list': []  # Будет заполнено позже
    }
    
    # Данные блога из модели
    blog_content = BlogContent()
    blog_data = {
        'title': blog_content.get('title', 'Блог'),
        'subtitle': blog_content.get('subtitle', 'Полезная информация о здоровье и персонализации'),
        'articles_list': blog_content.get_published_articles()
    }
    
    # Контактные данные
    contacts_store = ContactsContent()
    contacts_data = contacts_store.get_all()
    
    return render_template(
        'index.html',
        hero=hero_data,
        about=about_data,
        products=products_data,
        services=services_data,
        personalization=personalization_data,
        reviews=reviews_data,
        blog=blog_data,
        contacts=contacts_data
    )


@main_bp.route('/health')
def health_check():
    """
    Проверка здоровья приложения.
    Используется для мониторинга.
    
    Returns:
        JSON с статусом приложения
    """
    return {'status': 'healthy', 'service': 'OilFusion Landing'}, 200


