"""
Основные маршруты лендинга OilFusion.
Обрабатывает все запросы к главной странице и её секциям.
"""

import json

from flask import (
    Blueprint,
    current_app,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.database import ContentRepository
from app.i18n.const import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from app.models.images import SectionBackgrounds
from app.models.sections_visibility import SectionsVisibility
from app.utils.logger import get_logger

logger = get_logger()

# Создание Blueprint для основных маршрутов
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """
    Главная страница лендинга.
    Отображает все секции: Hero, О компании, Продукция, Услуги,
    Персонализация, Отзывы, Блог, Контакты.

    Returns:
        Отрендеренный HTML шаблон главной страницы
    """
    locale = getattr(g, "locale", DEFAULT_LANGUAGE)
    logger.info("Запрос главной страницы, локаль: {}", locale)

    backgrounds = SectionBackgrounds()
    sections_visibility = SectionsVisibility()

    # Получаем контент напрямую из БД на нужном языке
    hero_data = ContentRepository.get_section("hero", locale)
    hero_data["background"] = backgrounds.get_section_background("hero")

    about_data = ContentRepository.get_section("about", locale)
    about_data["background"] = backgrounds.get_section_background("about")
    
    # Парсим JSON для features (только если это строка)
    if about_data.get('features') and isinstance(about_data['features'], str):
        try:
            about_data['features'] = json.loads(about_data['features'])
        except json.JSONDecodeError:
            about_data['features'] = []

    products_data = ContentRepository.get_section("products", locale)
    products_data["background"] = backgrounds.get_section_background("products")
    # products - это уже распарсенный JSON из БД благодаря get_section()

    services_data = ContentRepository.get_section("services", locale)
    
    # Парсим JSON для services_list (только если это строка)
    if services_data.get('services_list') and isinstance(services_data['services_list'], str):
        try:
            services_data['services_list'] = json.loads(services_data['services_list'])
        except json.JSONDecodeError:
            services_data['services_list'] = []

    personalization_data = ContentRepository.get_section("personalization", locale)
    
    # Парсим JSON для dna_testing и auracloud (только если это строки)
    if personalization_data.get('dna_testing') and isinstance(personalization_data['dna_testing'], str):
        try:
            personalization_data['dna_testing'] = json.loads(personalization_data['dna_testing'])
        except json.JSONDecodeError:
            pass
    
    if personalization_data.get('auracloud') and isinstance(personalization_data['auracloud'], str):
        try:
            personalization_data['auracloud'] = json.loads(personalization_data['auracloud'])
        except json.JSONDecodeError:
            pass

    reviews_data = ContentRepository.get_section("reviews", locale)
    if not reviews_data.get("title"):
        reviews_data["title"] = "Отзывы наших клиентов"
    reviews_data["reviews_list"] = []

    blog_data = ContentRepository.get_section("blog", locale)
    blog_data["articles_list"] = blog_data.get("articles", [])

    contacts_data = ContentRepository.get_section("contacts", locale)

    slider_data = ContentRepository.get_section("auracloud_slider", locale)

    return render_template(
        "index.html",
        hero=hero_data,
        about=about_data,
        products=products_data,
        services=services_data,
        personalization=personalization_data,
        reviews=reviews_data,
        blog=blog_data,
        contacts=contacts_data,
        sections_visibility=sections_visibility.get_all_sections(),
        auracloud_slider=slider_data,
    )


@main_bp.route("/set_language/<lang>", methods=["GET", "POST"])
def set_language(lang: str):
    """
    Переключение языка интерфейса.
    """
    if lang not in SUPPORTED_LANGUAGES:
        logger.warning("Попытка выбрать неподдерживаемый язык: {}", lang)
        return {"status": "error", "message": "Unsupported language"}, 400
    else:
        session["locale"] = lang
        g.locale = lang
        logger.info("Локаль обновлена пользователем: {}", lang)

    if request.method == "POST":
        return {"status": "success", "language": lang}, 200

    next_url = request.args.get("next") or request.referrer or url_for("main.index")
    return redirect(next_url)


@main_bp.route('/catalog')
def catalog():
    """
    Каталог продукции.
    
    Returns:
        Отрендеренный HTML каталог с полным списком продуктов
    """
    logger.info("Запрос страницы каталога продукции")
    
    locale = getattr(g, "locale", DEFAULT_LANGUAGE)
    backgrounds = SectionBackgrounds()
    
    # Получаем продукты из БД
    products_data = ContentRepository.get_section("products", locale)
    
    # Парсим JSON для products (только если это строка)
    if products_data.get('products') and isinstance(products_data['products'], str):
        try:
            products_data['products'] = json.loads(products_data['products'])
        except json.JSONDecodeError:
            products_data['products'] = []
    
    catalog_products = products_data.get('products', [])
    catalog_background = backgrounds.get_section_background('products')
    
    return render_template(
        'catalog.html',
        products=catalog_products,
        background=catalog_background,
        products_title=products_data.get('title', 'Каталог продукции'),
        products_subtitle=products_data.get('subtitle', '')
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


