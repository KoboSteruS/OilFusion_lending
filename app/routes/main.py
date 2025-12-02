"""
Основные маршруты лендинга OilFusion.
Обрабатывает все запросы к главной странице и её секциям.
"""

from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.database import ContentRepository, ImageRepository, SettingRepository
from app.i18n.const import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
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

    # Получаем контент на текущем языке из БД
    hero_data = ContentRepository.get_section("hero", locale)
    about_data = ContentRepository.get_section("about", locale)
    products_data = ContentRepository.get_section("products", locale)
    services_data = ContentRepository.get_section("services", locale)
    personalization_data = ContentRepository.get_section("personalization", locale)
    blog_data = ContentRepository.get_section("blog", locale)
    contacts_data = ContentRepository.get_section("contacts", locale)
    auracloud_slider_data = ContentRepository.get_section("auracloud_slider", locale)
    
    # Получаем настройки видимости секций
    sections_visibility = {}
    for section in ['hero', 'about', 'products', 'services', 'personalization', 'reviews', 'blog', 'contacts']:
        visible = SettingRepository.get(f'section_visible_{section}', 'true')
        sections_visibility[section] = visible.lower() == 'true'
    
    # Получаем изображения
    hero_bg = ImageRepository.get_by_section_field('hero', 'background')
    about_bg = ImageRepository.get_by_section_field('about', 'background')
    products_bg = ImageRepository.get_by_section_field('products', 'background')
    
    if hero_bg:
        hero_data['background'] = {'image_url': hero_bg.url}
    if about_bg:
        about_data['background'] = {'image_url': about_bg.url}
    if products_bg:
        products_data['background'] = {'image_url': products_bg.url}
    
    # Reviews заглушка
    reviews_data = {
        "title": ContentRepository.get("reviews", "title", locale, "Отзывы наших клиентов"),
        "reviews_list": [],
    }

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
        sections_visibility=sections_visibility,
        auracloud_slider=auracloud_slider_data,
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
    
    # Получаем продукты из БД
    products_data = ContentRepository.get_section("products", locale)
    catalog_products = products_data.get('products', [])
    
    # Получаем фон
    products_bg = ImageRepository.get_by_section_field('products', 'background')
    catalog_background = {'image_url': products_bg.url} if products_bg else None
    
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


