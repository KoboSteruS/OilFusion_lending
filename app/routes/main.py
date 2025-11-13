"""
Основные маршруты лендинга OilFusion.
Обрабатывает все запросы к главной странице и её секциям.
"""

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

from app.i18n.adapters import (
    translate_about,
    translate_auracloud_slider,
    translate_blog,
    translate_contacts,
    translate_hero,
    translate_personalization,
    translate_products,
    translate_reviews,
    translate_services,
)
from app.i18n.const import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from app.models.auracloud_slider import AuraCloudSlider
from app.models.contacts import ContactsContent
from app.models.content import AboutContent, BlogContent, PersonalizationContent
from app.models.hero import HeroContent
from app.models.images import SectionBackgrounds
from app.models.products import ProductsContent
from app.models.sections_visibility import SectionsVisibility
from app.models.services import ServicesContent
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
    logger.info("Запрос главной страницы")

    locale = getattr(g, "locale", DEFAULT_LANGUAGE)

    backgrounds = SectionBackgrounds()
    sections_visibility = SectionsVisibility()
    auracloud_slider_store = AuraCloudSlider()
    slider_data = auracloud_slider_store.get_all()

    hero_content = HeroContent()
    hero_data = {
        "slogan": hero_content.get_slogan(),
        "subtitle": hero_content.get_subtitle(),
        "cta_primary": hero_content.get_cta_primary(),
        "cta_secondary": hero_content.get_cta_secondary(),
        "scroll_text": hero_content.get_scroll_text(),
        "background": backgrounds.get_section_background("hero"),
    }

    about_content = AboutContent()
    about_data = about_content.get_all()
    about_data["background"] = backgrounds.get_section_background("about")

    products_store = ProductsContent()
    products_data = {
        "title": "Наша продукция",
        "products_list": products_store.list(),
        "background": backgrounds.get_section_background("products"),
    }

    services_store = ServicesContent()
    services_data = {
        "title": "Наши услуги",
        "services_list": services_store.list(),
    }

    personalization_content = PersonalizationContent()
    personalization_data = personalization_content.get_all()

    reviews_data = {
        "title": "Отзывы наших клиентов",
        "reviews_list": [],
    }

    blog_content = BlogContent()
    blog_data = {
        "title": blog_content.get("title", "Блог"),
        "subtitle": blog_content.get(
            "subtitle", "Полезная информация о здоровье и персонализации"
        ),
        "articles_list": blog_content.get_published_articles(),
    }

    contacts_store = ContactsContent()
    contacts_data = contacts_store.get_all()

    # Применяем переводы
    hero_data = translate_hero(hero_data, locale)
    about_data = translate_about(about_data, locale)
    products_data = translate_products(products_data, locale)
    services_data = translate_services(services_data, locale)
    personalization_data = translate_personalization(personalization_data, locale)
    reviews_data = translate_reviews(reviews_data, locale)
    blog_data = translate_blog(blog_data, locale)
    contacts_data = translate_contacts(contacts_data, locale)
    slider_data = translate_auracloud_slider(slider_data, locale)

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
    
    backgrounds = SectionBackgrounds()
    products_store = ProductsContent()
    
    catalog_products = products_store.list()
    catalog_background = backgrounds.get_section_background('products')
    
    return render_template(
        'catalog.html',
        products=catalog_products,
        background=catalog_background
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


