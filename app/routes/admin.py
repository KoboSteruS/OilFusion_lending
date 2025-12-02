"""
Админские маршруты для управления контентом OilFusion Landing.
Защищены JWT токеном в URL: /<token>/admin/...
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

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
from app.i18n.const import DEFAULT_LANGUAGE, LANGUAGE_LABELS, SUPPORTED_LANGUAGES
from app.i18n.manager import translation_manager
from app.models.auracloud_slider import AuraCloudSlider
from app.models.contacts import ContactsContent
from app.models.content import AboutContent, BlogContent, PersonalizationContent
from app.models.hero import HeroContent
from app.models.products import ProductsContent
from app.models.sections_visibility import SectionsVisibility
from app.models.services import ServicesContent
from app.utils.auth import require_admin_token
from app.utils.logger import get_logger

logger = get_logger()

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}


def _save_uploaded_image(file: FileStorage, prefix: str) -> Optional[str]:
    """
    Сохранение загруженного изображения в папку static/img.

    Args:
        file: Объект FileStorage из Flask.
        prefix: Префикс для формирования имени файла.

    Returns:
        Относительный URL сохранённого файла или None, если файл не загружен.

    Raises:
        ValueError: Если файл имеет недопустимое расширение.
        OSError: Если не удалось сохранить файл.
    """
    if not file or not file.filename:
        return None

    filename = secure_filename(file.filename)
    if '.' not in filename:
        raise ValueError('Файл изображения должен иметь расширение.')

    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError('Недопустимое расширение файла. Разрешены: PNG, JPG, JPEG, WEBP, GIF.')

    upload_folder = Path(current_app.root_path) / 'static' / 'img'
    upload_folder.mkdir(parents=True, exist_ok=True)

    unique_filename = f"{prefix}_{int(datetime.now().timestamp())}_{filename}"
    target_path = upload_folder / unique_filename
    file.save(target_path)

    logger.info(f"Изображение сохранено: {unique_filename}")
    return f"/static/img/{unique_filename}"


# Создание Blueprint для админских маршрутов
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/<token>/admin/')
@require_admin_token
def dashboard(token):
    """Главная страница админки с токеном."""
    logger.info("Запрос главной страницы админки")
    
    about_content = AboutContent()
    personalization_content = PersonalizationContent()
    blog_content = BlogContent()
    
    stats = {
        'about_features': len(about_content.get_features()),
        'dna_features': len(personalization_content.get_dna_features()),
        'auracloud_features': len(personalization_content.get_auracloud_features()),
        'total_articles': len(blog_content.get_articles()),
        'published_articles': len(blog_content.get_published_articles())
    }
    
    return render_template('admin/dashboard.html', stats=stats, token=token)


@admin_bp.route('/<token>/admin/about')
@require_admin_token
def about_edit(token):
    """Редактирование секции О компании."""
    logger.info("Запрос редактирования секции 'О компании'")
    
    about_content = AboutContent()
    content_data = about_content.get_all()
    
    return render_template('admin/about_edit.html', content=content_data, token=token)


@admin_bp.route('/<token>/admin/about/update', methods=['POST'])
@require_admin_token
def about_update(token):
    """Обновление контента секции О компании."""
    logger.info("Обновление контента секции 'О компании'")
    
    about_content = AboutContent()
    
    # Обработка фонового изображения
    background_image_url = (request.form.get('background_image_url') or '').strip()
    if background_image_url.lower() in {'none', 'null', 'undefined'}:
        background_image_url = ''
    background_overlay_opacity_raw = request.form.get('background_overlay_opacity', '0.8')
    try:
        background_overlay_opacity = float(background_overlay_opacity_raw)
    except (TypeError, ValueError):
        background_overlay_opacity = 0.8
    background_overlay_opacity = max(0.0, min(1.0, background_overlay_opacity))
    background_overlay_color = request.form.get('background_overlay_color', '#FFFFFF') or '#FFFFFF'
    
    background_file_error: Optional[str] = None
    uploaded_background = request.files.get('background_image')
    if uploaded_background and uploaded_background.filename:
        try:
            saved_url = _save_uploaded_image(uploaded_background, 'about')
            if saved_url:
                background_image_url = saved_url
        except ValueError as exc:
            background_file_error = str(exc)
        except OSError as exc:
            background_file_error = 'Не удалось сохранить фоновое изображение. Попробуйте загрузить файл ещё раз.'
            logger.exception("Ошибка сохранения фона для секции 'О компании': %s", exc)
    
    update_data = {
        'title': request.form.get('title', ''),
        'description': request.form.get('description', ''),
        'philosophy': request.form.get('philosophy', ''),
        'background_image_url': background_image_url,
        'background_overlay_opacity': background_overlay_opacity,
        'background_overlay_color': background_overlay_color
    }
    
    if about_content.update(update_data):
        flash('Контент успешно обновлен!', 'success')
    else:
        flash('Ошибка при обновлении контента!', 'error')
    
    if background_file_error:
        flash(background_file_error, 'error')
    
    return redirect(url_for('admin.about_edit', token=token))


@admin_bp.route('/<token>/admin/about/feature/add', methods=['POST'])
@require_admin_token
def about_feature_add(token):
    """Добавление новой особенности в секцию О компании."""
    logger.info("Добавление новой особенности")
    
    about_content = AboutContent()
    
    # Обработка изображения особенности
    feature_image_url = (request.form.get('feature_image_url') or '').strip()
    if feature_image_url.lower() in {'none', 'null', 'undefined'}:
        feature_image_url = ''
    
    feature_file_error: Optional[str] = None
    uploaded_feature = request.files.get('feature_image')
    if uploaded_feature and uploaded_feature.filename:
        try:
            saved_url = _save_uploaded_image(uploaded_feature, 'feature')
            if saved_url:
                feature_image_url = saved_url
        except ValueError as exc:
            feature_file_error = str(exc)
        except OSError as exc:
            feature_file_error = 'Не удалось сохранить изображение особенности.'
            logger.exception("Ошибка сохранения изображения особенности: %s", exc)
    
    feature_data = {
        'title': request.form.get('feature_title', ''),
        'description': request.form.get('feature_description', ''),
        'icon': request.form.get('feature_icon', 'default'),
        'image_url': feature_image_url
    }
    
    if about_content.add_feature(feature_data):
        flash('Особенность успешно добавлена!', 'success')
    else:
        flash('Ошибка при добавлении особенности!', 'error')
    
    if feature_file_error:
        flash(feature_file_error, 'error')
    
    return redirect(url_for('admin.about_edit', token=token))


@admin_bp.route('/<token>/admin/about/feature/<int:index>/update', methods=['POST'])
@require_admin_token
def about_feature_update(token, index):
    """Обновление особенности по индексу."""
    logger.info(f"Обновление особенности с индексом {index}")
    
    about_content = AboutContent()
    
    # Обработка изображения особенности
    feature_image_url = (request.form.get('feature_image_url') or '').strip()
    if feature_image_url.lower() in {'none', 'null', 'undefined'}:
        feature_image_url = ''
    
    feature_file_error: Optional[str] = None
    uploaded_feature = request.files.get('feature_image')
    if uploaded_feature and uploaded_feature.filename:
        try:
            saved_url = _save_uploaded_image(uploaded_feature, 'feature')
            if saved_url:
                feature_image_url = saved_url
        except ValueError as exc:
            feature_file_error = str(exc)
        except OSError as exc:
            feature_file_error = 'Не удалось сохранить изображение особенности.'
            logger.exception("Ошибка обновления изображения особенности: %s", exc)
    
    feature_data = {
        'title': request.form.get('feature_title', ''),
        'description': request.form.get('feature_description', ''),
        'icon': request.form.get('feature_icon', 'default'),
        'image_url': feature_image_url
    }
    
    if about_content.update_feature(index, feature_data):
        flash('Особенность успешно обновлена!', 'success')
    else:
        flash('Ошибка при обновлении особенности!', 'error')
    
    if feature_file_error:
        flash(feature_file_error, 'error')
    
    return redirect(url_for('admin.about_edit', token=token))


@admin_bp.route('/<token>/admin/about/feature/<int:index>/delete', methods=['POST'])
@require_admin_token
def about_feature_delete(token, index):
    """Удаление особенности по индексу."""
    logger.info(f"Удаление особенности с индексом {index}")
    
    about_content = AboutContent()
    
    if about_content.remove_feature(index):
        flash('Особенность успешно удалена!', 'success')
    else:
        flash('Ошибка при удалении особенности!', 'error')
    
    return redirect(url_for('admin.about_edit', token=token))


@admin_bp.route('/<token>/admin/personalization')
@require_admin_token
def personalization_edit(token):
    """Редактирование секции Персонализация."""
    logger.info("Запрос редактирования секции 'Персонализация'")
    
    personalization_content = PersonalizationContent()
    content_data = personalization_content.get_all()
    
    return render_template('admin/personalization_edit.html', content=content_data, token=token)


@admin_bp.route('/<token>/admin/personalization/update', methods=['POST'])
@require_admin_token
def personalization_update(token):
    """Обновление контента секции Персонализация."""
    logger.info("Обновление контента секции 'Персонализация'")
    
    personalization_content = PersonalizationContent()
    
    update_data = {
        'title': request.form.get('title', ''),
        'subtitle': request.form.get('subtitle', ''),
        'info_text': request.form.get('info_text', ''),
        'info_description': request.form.get('info_description', ''),
        'bio_well_url': request.form.get('bio_well_url', '')
    }
    
    def resolve_image(prefix: str, file_field: str, url_field: str) -> str:
        file_error: Optional[str] = None
        current_url = (request.form.get(url_field) or '').strip()
        if current_url.lower() in {'none', 'null', 'undefined'}:
            current_url = ''

        uploaded = request.files.get(file_field)
        if uploaded and uploaded.filename:
            try:
                saved_url = _save_uploaded_image(uploaded, prefix)
                if saved_url:
                    return saved_url
            except ValueError as exc:
                file_error = str(exc)
            except OSError as exc:
                file_error = 'Не удалось сохранить изображение. Попробуйте снова.'
                logger.exception("Ошибка сохранения изображения %s: %s", prefix, exc)

        if file_error:
            flash(file_error, 'error')
        return current_url

    dna_image = resolve_image('dna', 'dna_image', 'dna_image_url')
    auracloud_image = resolve_image('auracloud', 'auracloud_image', 'auracloud_image_url')

    dna_data = {
        'title': request.form.get('dna_title', ''),
        'description': request.form.get('dna_description', ''),
        'image_url': dna_image
    }
    update_data['dna_testing'] = dna_data
    
    auracloud_data = {
        'title': request.form.get('auracloud_title', ''),
        'description': request.form.get('auracloud_description', ''),
        'image_url': auracloud_image
    }
    update_data['auracloud'] = auracloud_data
    
    if personalization_content.update(update_data):
        flash('Контент успешно обновлен!', 'success')
    else:
        flash('Ошибка при обновлении контента!', 'error')
    
    return redirect(url_for('admin.personalization_edit', token=token))


@admin_bp.route('/<token>/admin/personalization/dna-feature/<int:index>/update', methods=['POST'])
@require_admin_token
def personalization_dna_feature_update(token, index):
    """Обновление особенности ДНК-тестирования."""
    logger.info(f"Обновление особенности ДНК-тестирования с индексом {index}")
    
    personalization_content = PersonalizationContent()
    action = request.form.get('action', 'update')
    feature_text = request.form.get('feature_text', '')
    
    ok = False
    if action == 'delete':
        ok = personalization_content.remove_dna_feature(index)
    elif action == 'add':
        ok = personalization_content.add_dna_feature(feature_text)
    else:
        ok = personalization_content.update_dna_feature(index, feature_text)
    
    if ok:
        flash('Особенность ДНК-тестирования успешно обновлена!', 'success')
    else:
        flash('Ошибка при обновлении особенности!', 'error')
    
    return redirect(url_for('admin.personalization_edit', token=token))


@admin_bp.route('/<token>/admin/personalization/auracloud-feature/<int:index>/update', methods=['POST'])
@require_admin_token
def personalization_auracloud_feature_update(token, index):
    """Обновление особенности AuraCloud® 3D."""
    logger.info(f"Обновление особенности AuraCloud® 3D с индексом {index}")
    
    personalization_content = PersonalizationContent()
    action = request.form.get('action', 'update')
    feature_text = request.form.get('feature_text', '')
    
    ok = False
    if action == 'delete':
        ok = personalization_content.remove_auracloud_feature(index)
    elif action == 'add':
        ok = personalization_content.add_auracloud_feature(feature_text)
    else:
        ok = personalization_content.update_auracloud_feature(index, feature_text)
    
    if ok:
        flash('Особенность AuraCloud® 3D успешно обновлена!', 'success')
    else:
        flash('Ошибка при обновлении особенности!', 'error')
    
    return redirect(url_for('admin.personalization_edit', token=token))


@admin_bp.route('/<token>/admin/blog')
@require_admin_token
def blog_list(token):
    """Список статей блога."""
    logger.info("Запрос списка статей блога")
    
    blog_content = BlogContent()
    articles = blog_content.get_articles()
    
    return render_template('admin/blog_list.html', articles=articles, token=token)


@admin_bp.route('/<token>/admin/blog/new')
@require_admin_token
def blog_new(token):
    """Создание новой статьи."""
    logger.info("Запрос создания новой статьи")
    
    return render_template('admin/blog_edit.html', article=None, token=token)


@admin_bp.route('/<token>/admin/blog/<int:index>')
@require_admin_token
def blog_edit(token, index):
    """Редактирование статьи по индексу."""
    logger.info(f"Запрос редактирования статьи с индексом {index}")
    
    blog_content = BlogContent()
    article = blog_content.get_article(index)
    
    if article is None:
        flash('Статья не найдена!', 'error')
        return redirect(url_for('admin.blog_list', token=token))
    
    return render_template('admin/blog_edit.html', article=article, article_index=index, token=token)


@admin_bp.route('/<token>/admin/blog/save', methods=['POST'])
@require_admin_token
def blog_save(token):
    """Сохранение статьи (создание или обновление)."""
    logger.info("Сохранение статьи блога")
    
    blog_content = BlogContent()
    article_index = request.form.get('article_index')
    
    article_data = {
        'title': request.form.get('title', ''),
        'content': request.form.get('content', ''),
        'excerpt': request.form.get('excerpt', ''),
        'category': request.form.get('category', ''),
        'read_time': int(request.form.get('read_time', 5)),
        'image': request.form.get('image', ''),
        'published': request.form.get('published') == 'on'
    }
    
    if article_index is not None:
        index = int(article_index)
        if blog_content.update_article(index, article_data):
            flash('Статья успешно обновлена!', 'success')
        else:
            flash('Ошибка при обновлении статьи!', 'error')
    else:
        if blog_content.add_article(article_data):
            flash('Статья успешно создана!', 'success')
        else:
            flash('Ошибка при создании статьи!', 'error')
    
    return redirect(url_for('admin.blog_list', token=token))

# ===================== Products =====================

@admin_bp.route('/<token>/admin/products')
@require_admin_token
def products_list(token):
    products = ProductsContent()
    return render_template('admin/products_list.html', products=products.list(), token=token)


@admin_bp.route('/<token>/admin/products/save', methods=['POST'])
@require_admin_token
def products_save(token):
    from pathlib import Path
    from datetime import datetime
    from werkzeug.utils import secure_filename

    products = ProductsContent()
    index = request.form.get('index')
    name = request.form.get('name', '')
    description = request.form.get('description', '')
    price = request.form.get('price', '')
    category = request.form.get('category', '')
    image_url = request.form.get('image_url', '')
    featured = request.form.get('featured') == 'on'  # Checkbox value

    if 'image_file' in request.files:
        file = request.files['image_file']
        if file and file.filename and '.' in file.filename and file.filename.rsplit('.',1)[1].lower() in {'png','jpg','jpeg','webp','gif'}:
            filename = secure_filename(file.filename)
            unique = f"product_{int(datetime.now().timestamp())}_{filename}"
            folder = Path('app/static/img')
            folder.mkdir(parents=True, exist_ok=True)
            file.save(str(folder / unique))
            image_url = f"/static/img/{unique}"

    item = {
        'name': name,
        'description': description,
        'price': price,
        'category': category,
        'image': image_url,
        'featured': featured,
    }
    if index is not None and index != '':
        ok = ProductsContent().update_item(int(index), item)
    else:
        ok = ProductsContent().add(item)
    flash('Товар сохранён' if ok else 'Ошибка сохранения товара', 'success' if ok else 'error')
    return redirect(url_for('admin.products_list', token=token))


@admin_bp.route('/<token>/admin/products/<int:index>/delete', methods=['POST'])
@require_admin_token
def products_delete(token, index):
    ok = ProductsContent().delete(index)
    flash('Товар удалён' if ok else 'Ошибка удаления товара', 'success' if ok else 'error')
    return redirect(url_for('admin.products_list', token=token))


# ===================== Services =====================

@admin_bp.route('/<token>/admin/services')
@require_admin_token
def services_list(token):
    services = ServicesContent()
    return render_template('admin/services_list.html', services=services.list(), token=token)


@admin_bp.route('/<token>/admin/services/save', methods=['POST'])
@require_admin_token
def services_save(token):
    from pathlib import Path
    from datetime import datetime
    from werkzeug.utils import secure_filename

    services = ServicesContent()
    index = request.form.get('index')
    name = request.form.get('name', '')
    description = request.form.get('description', '')
    price = request.form.get('price', '')
    icon_url = request.form.get('icon_url', '')

    # features as multiline textarea (one per line)
    features_text = request.form.get('features', '')
    features = [f.strip() for f in features_text.split('\n') if f.strip()]

    if 'icon_file' in request.files:
        file = request.files['icon_file']
        if file and file.filename and '.' in file.filename and file.filename.rsplit('.',1)[1].lower() in {'png','jpg','jpeg','webp','gif','svg'}:
            filename = secure_filename(file.filename)
            unique = f"service_{int(datetime.now().timestamp())}_{filename}"
            folder = Path('app/static/img')
            folder.mkdir(parents=True, exist_ok=True)
            file.save(str(folder / unique))
            icon_url = f"/static/img/{unique}"

    item = {
        'name': name,
        'description': description,
        'price': price,
        'icon': icon_url,
        'features': features,
    }
    if index is not None and index != '':
        ok = ServicesContent().update_item(int(index), item)
    else:
        ok = ServicesContent().add(item)
    flash('Услуга сохранена' if ok else 'Ошибка сохранения услуги', 'success' if ok else 'error')
    return redirect(url_for('admin.services_list', token=token))


@admin_bp.route('/<token>/admin/services/<int:index>/delete', methods=['POST'])
@require_admin_token
def services_delete(token, index):
    ok = ServicesContent().delete(index)
    flash('Услуга удалена' if ok else 'Ошибка удаления услуги', 'success' if ok else 'error')
    return redirect(url_for('admin.services_list', token=token))


@admin_bp.route('/<token>/admin/contacts')
@require_admin_token
def contacts_edit(token):
    contacts = ContactsContent()
    return render_template('admin/contacts_edit.html', contacts=contacts.get_all(), token=token)


@admin_bp.route('/<token>/admin/contacts/save', methods=['POST'])
@require_admin_token
def contacts_save(token):
    contacts = ContactsContent()
    data = {
        'email': request.form.get('email', ''),
        'phone': request.form.get('phone', ''),
        'address': request.form.get('address', ''),
        'latitude': request.form.get('latitude'),
        'longitude': request.form.get('longitude'),
        'maps_api_key': request.form.get('maps_api_key', ''),
        'form_title': request.form.get('form_title', ''),
        'form_subtitle': request.form.get('form_subtitle', ''),
        'form_button_text': request.form.get('form_button_text', ''),
        'form_success_message': request.form.get('form_success_message', ''),
    }
    try:
        if data['latitude'] not in (None, ''):
            data['latitude'] = float(data['latitude'])
        if data['longitude'] not in (None, ''):
            data['longitude'] = float(data['longitude'])
    except ValueError:
        pass
    ok = contacts.update(data)
    flash('Контакты сохранены' if ok else 'Ошибка сохранения контактов', 'success' if ok else 'error')
    return redirect(url_for('admin.contacts_edit', token=token))


# ===================== Hero =====================

@admin_bp.route('/<token>/admin/hero')
@require_admin_token
def hero_edit(token):
    from app.database import ContentRepository, ImageRepository
    
    # Получаем объекты контента со всеми языками
    hero_slogan = ContentRepository.get_content_object('hero', 'slogan')
    hero_subtitle = ContentRepository.get_content_object('hero', 'subtitle')
    hero_cta_primary = ContentRepository.get_content_object('hero', 'cta_primary')
    hero_cta_secondary = ContentRepository.get_content_object('hero', 'cta_secondary')
    hero_scroll_text = ContentRepository.get_content_object('hero', 'scroll_text')
    
    # Получаем фоновое изображение
    hero_bg = ImageRepository.get_by_section_field('hero', 'background')
    hero_background = {'image_url': hero_bg.url} if hero_bg else None
    
    return render_template(
        'admin/hero_edit.html',
        hero_slogan=hero_slogan,
        hero_subtitle=hero_subtitle,
        hero_cta_primary=hero_cta_primary,
        hero_cta_secondary=hero_cta_secondary,
        hero_scroll_text=hero_scroll_text,
        hero_background=hero_background,
        token=token
    )


@admin_bp.route('/<token>/admin/hero/save', methods=['POST'])
@require_admin_token
def hero_save(token):
    from app.database import ContentRepository, ImageRepository
    
    # Обработка фонового изображения
    background_image_url = (request.form.get('hero_background_url') or '').strip()
    if background_image_url.lower() in {'none', 'null', 'undefined'}:
        background_image_url = ''

    file_error: Optional[str] = None
    uploaded_file = request.files.get('hero_background_image')
    if uploaded_file and uploaded_file.filename:
        try:
            saved_url = _save_uploaded_image(uploaded_file, 'hero')
            if saved_url:
                background_image_url = saved_url
                
                # Сохраняем в БД
                existing_img = ImageRepository.get_by_section_field('hero', 'background')
                if existing_img:
                    ImageRepository.update_url('hero', 'background', saved_url)
                else:
                    from pathlib import Path
                    filename = Path(saved_url).name
                    ImageRepository.create(
                        filename=filename,
                        original_filename=filename,
                        url=saved_url,
                        section='hero',
                        field='background'
                    )
        except ValueError as exc:
            file_error = str(exc)
        except OSError as exc:
            file_error = 'Не удалось сохранить изображение. Попробуйте ещё раз позже.'
            logger.exception("Ошибка сохранения изображения для Hero секции: %s", exc)
    
    # Сохраняем мультиязычный контент Hero
    try:
        for key in ['slogan', 'subtitle', 'cta_primary', 'cta_secondary', 'scroll_text']:
            ContentRepository.set(
                section='hero',
                key=key,
                value_ru=request.form.get(f'{key}_ru', '').strip(),
                value_lv=request.form.get(f'{key}_lv', '').strip(),
                value_en=request.form.get(f'{key}_en', '').strip()
            )
        
        if file_error:
            flash(file_error, 'error')
        flash('Hero контент сохранён на всех языках!', 'success')
    except Exception as exc:
        logger.exception("Ошибка сохранения Hero контента: %s", exc)
        flash('Ошибка сохранения Hero контента', 'error')
    
    return redirect(url_for('admin.hero_edit', token=token))

@admin_bp.route('/<token>/admin/blog/<int:index>/delete', methods=['POST'])
@require_admin_token
def blog_delete(token, index):
    """Удаление статьи по индексу."""
    logger.info(f"Удаление статьи с индексом {index}")
    
    blog_content = BlogContent()
    
    if blog_content.delete_article(index):
        flash('Статья успешно удалена!', 'success')
    else:
        flash('Ошибка при удалении статьи!', 'error')
    
    return redirect(url_for('admin.blog_list', token=token))


@admin_bp.route('/<token>/admin/sections-visibility')
@require_admin_token
def sections_visibility(token):
    """Управление видимостью разделов сайта."""
    logger.info("Запрос страницы управления видимостью разделов")
    
    sections_visibility = SectionsVisibility()
    sections_data = sections_visibility.get_all_sections()
    
    return render_template('admin/sections_visibility.html', 
                         sections_visibility=sections_data, 
                         token=token)


@admin_bp.route('/<token>/admin/sections-visibility/update', methods=['POST'])
@require_admin_token
def sections_visibility_update(token):
    """Обновление видимости разделов сайта."""
    logger.info("Обновление видимости разделов")
    
    sections_visibility = SectionsVisibility()
    
    # Получаем данные из формы
    sections_data = {
        'hero': 'hero' in request.form,
        'about': 'about' in request.form,
        'products': 'products' in request.form,
        'services': 'services' in request.form,
        'personalization': 'personalization' in request.form,
        'reviews': 'reviews' in request.form,
        'blog': 'blog' in request.form,
        'contacts': 'contacts' in request.form
    }
    
    if sections_visibility.update_sections(sections_data):
        flash('Настройки видимости разделов сохранены!', 'success')
    else:
        flash('Ошибка при сохранении настроек!', 'error')
    
    return redirect(url_for('admin.sections_visibility', token=token))


@admin_bp.route('/<token>/admin/translations')
@require_admin_token
def translations(token):
    """
    Управление переводами контента.
    """
    logger.info("Запрос страницы управления переводами")
    _prime_translation_entries()
    records = translation_manager.list_records()
    return render_template(
        'admin/translations.html',
        records=records,
        token=token,
        languages=[lang for lang in SUPPORTED_LANGUAGES if lang != DEFAULT_LANGUAGE],
        language_labels=LANGUAGE_LABELS,
    )


@admin_bp.route('/<token>/admin/translations/update', methods=['POST'])
@require_admin_token
def translations_update(token):
    """
    Сохранение ручного перевода.
    """
    key = (request.form.get('key') or '').strip()
    locale = (request.form.get('locale') or '').lower()
    value = request.form.get('value', '')

    if not key or locale not in SUPPORTED_LANGUAGES or locale == DEFAULT_LANGUAGE:
        flash('Некорректные данные для сохранения перевода', 'error')
    else:
        translation_manager.set_manual_translation(key, locale, value)
        flash('Перевод обновлён', 'success')

    return redirect(url_for('admin.translations', token=token))


@admin_bp.route('/<token>/admin/translations/auto', methods=['POST'])
@require_admin_token
def translations_auto(token):
    """
    Принудительный автоперевод для выбранного ключа.
    """
    key = (request.form.get('key') or '').strip()
    locale = (request.form.get('locale') or '').lower()

    if not key or locale not in SUPPORTED_LANGUAGES or locale == DEFAULT_LANGUAGE:
        flash('Невозможно выполнить автоперевод для выбранных параметров', 'error')
    else:
        result = translation_manager.auto_translate(key, locale)
        if result is None:
            flash('Автоматический перевод отключён', 'error')
        else:
            flash('Автоперевод выполнен', 'success')

    return redirect(url_for('admin.translations', token=token))


@admin_bp.route('/<token>/admin/auracloud-slider')
@require_admin_token
def auracloud_slider(token):
    """Управление AuraCloud слайдером."""
    logger.info("Запрос страницы управления AuraCloud слайдером")
    
    slider = AuraCloudSlider()
    slider_data = slider.get_all()
    
    return render_template('admin/auracloud_slider.html', 
                         slider=slider_data, 
                         token=token)


@admin_bp.route('/<token>/admin/auracloud-slider/update', methods=['POST'])
@require_admin_token
def auracloud_slider_update(token):
    """Обновление настроек AuraCloud слайдера."""
    logger.info("Обновление настроек AuraCloud слайдера")
    
    slider = AuraCloudSlider()
    
    # Обработка изображений
    from pathlib import Path
    from datetime import datetime
    from werkzeug.utils import secure_filename
    
    def _save_image(prefix: str, file_field: str, fallback_url: str) -> str:
        url = request.form.get(fallback_url, '')
        if file_field in request.files:
            file = request.files[file_field]
            if file and file.filename and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'png','jpg','jpeg','webp','gif'}:
                filename = secure_filename(file.filename)
                unique = f"{prefix}_{int(datetime.now().timestamp())}_{filename}"
                folder = Path('app/static/img')
                folder.mkdir(parents=True, exist_ok=True)
                file.save(str(folder / unique))
                return f"/static/img/{unique}"
        return url

    before_image = _save_image('aura_before', 'before_image', 'before_image_url')
    after_image = _save_image('aura_after', 'after_image', 'after_image_url')
    
    # Обновляем данные
    update_data = {
        'title': request.form.get('title', ''),
        'subtitle': request.form.get('subtitle', ''),
        'description': request.form.get('description', ''),
        'before_label': request.form.get('before_label', ''),
        'after_label': request.form.get('after_label', ''),
        'before_image': before_image,
        'after_image': after_image,
        'enabled': 'enabled' in request.form
    }
    
    if slider.update(update_data):
        flash('Настройки AuraCloud слайдера сохранены!', 'success')
    else:
        flash('Ошибка при сохранении настроек!', 'error')
    
    return redirect(url_for('admin.auracloud_slider', token=token))


def _prime_translation_entries() -> None:
    """
    Подготавливает ключи переводов на основе текущего контента.
    """
    backgrounds = SectionBackgrounds()

    hero_content = HeroContent()
    hero_data = {
        'slogan': hero_content.get_slogan(),
        'subtitle': hero_content.get_subtitle(),
        'cta_primary': hero_content.get_cta_primary(),
        'cta_secondary': hero_content.get_cta_secondary(),
        'scroll_text': hero_content.get_scroll_text(),
        'background': backgrounds.get_section_background('hero'),
    }
    translate_hero(hero_data, DEFAULT_LANGUAGE)

    about_content = AboutContent()
    about_data = about_content.get_all()
    about_data['background'] = backgrounds.get_section_background('about')
    translate_about(about_data, DEFAULT_LANGUAGE)

    products_store = ProductsContent()
    products_data = {
        'title': 'Наша продукция',
        'products_list': products_store.list(),
        'background': backgrounds.get_section_background('products'),
    }
    translate_products(products_data, DEFAULT_LANGUAGE)

    services_store = ServicesContent()
    services_data = {
        'title': 'Наши услуги',
        'services_list': services_store.list(),
    }
    translate_services(services_data, DEFAULT_LANGUAGE)

    personalization_content = PersonalizationContent()
    personalization_data = personalization_content.get_all()
    translate_personalization(personalization_data, DEFAULT_LANGUAGE)

    blog_content = BlogContent()
    blog_data = {
        'title': blog_content.get('title', 'Блог'),
        'subtitle': blog_content.get('subtitle', ''),
        'articles_list': blog_content.get_published_articles(),
    }
    translate_blog(blog_data, DEFAULT_LANGUAGE)

    contacts_store = ContactsContent()
    contacts_data = contacts_store.get_all()
    translate_contacts(contacts_data, DEFAULT_LANGUAGE)

    auracloud_slider_store = AuraCloudSlider()
    translate_auracloud_slider(auracloud_slider_store.get_all(), DEFAULT_LANGUAGE)

    reviews_data = {
        'title': 'Отзывы наших клиентов',
        'reviews_list': [],
    }
    translate_reviews(reviews_data, DEFAULT_LANGUAGE)
