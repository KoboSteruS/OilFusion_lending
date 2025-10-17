"""
Админские маршруты для управления контентом OilFusion Landing.
Защищены JWT токеном в URL: /<token>/admin/...
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.content import AboutContent, PersonalizationContent, BlogContent
from app.models.products import ProductsContent
from app.models.services import ServicesContent
from app.models.contacts import ContactsContent
from app.utils.logger import get_logger
from app.utils.auth import require_admin_token

logger = get_logger()

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
    background_image_url = request.form.get('background_image_url', '')
    background_overlay_opacity = float(request.form.get('background_overlay_opacity', 0.8))
    background_overlay_color = request.form.get('background_overlay_color', '#FFFFFF')
    
    # Обработка загруженного файла
    if 'background_image' in request.files:
        file = request.files['background_image']
        if file and file.filename:
            from werkzeug.utils import secure_filename
            from datetime import datetime
            from pathlib import Path
            
            # Проверяем расширение файла
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp', 'gif'}:
                filename = secure_filename(file.filename)
                # Создаём уникальное имя файла
                timestamp = int(datetime.now().timestamp())
                unique_filename = f"about_{timestamp}_{filename}"
                
                # Путь для сохранения
                upload_folder = Path('app/static/img')
                upload_folder.mkdir(parents=True, exist_ok=True)
                
                file_path = upload_folder / unique_filename
                file.save(str(file_path))
                
                background_image_url = f"/static/img/{unique_filename}"
                logger.info(f"Загружено изображение для секции 'О компании': {unique_filename}")
    
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
    
    return redirect(url_for('admin.about_edit', token=token))


@admin_bp.route('/<token>/admin/about/feature/add', methods=['POST'])
@require_admin_token
def about_feature_add(token):
    """Добавление новой особенности в секцию О компании."""
    logger.info("Добавление новой особенности")
    
    about_content = AboutContent()
    
    # Обработка изображения особенности
    feature_image_url = request.form.get('feature_image_url', '')
    
    # Обработка загруженного файла
    if 'feature_image' in request.files:
        file = request.files['feature_image']
        if file and file.filename:
            from werkzeug.utils import secure_filename
            from datetime import datetime
            from pathlib import Path
            
            # Проверяем расширение файла
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp', 'gif'}:
                filename = secure_filename(file.filename)
                # Создаём уникальное имя файла
                timestamp = int(datetime.now().timestamp())
                unique_filename = f"feature_{timestamp}_{filename}"
                
                # Путь для сохранения
                upload_folder = Path('app/static/img')
                upload_folder.mkdir(parents=True, exist_ok=True)
                
                file_path = upload_folder / unique_filename
                file.save(str(file_path))
                
                feature_image_url = f"/static/img/{unique_filename}"
                logger.info(f"Загружено изображение для особенности: {unique_filename}")
    
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
    
    return redirect(url_for('admin.about_edit', token=token))


@admin_bp.route('/<token>/admin/about/feature/<int:index>/update', methods=['POST'])
@require_admin_token
def about_feature_update(token, index):
    """Обновление особенности по индексу."""
    logger.info(f"Обновление особенности с индексом {index}")
    
    about_content = AboutContent()
    
    # Обработка изображения особенности
    feature_image_url = request.form.get('feature_image_url', '')
    
    # Обработка загруженного файла
    if 'feature_image' in request.files:
        file = request.files['feature_image']
        if file and file.filename:
            from werkzeug.utils import secure_filename
            from datetime import datetime
            from pathlib import Path
            
            # Проверяем расширение файла
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp', 'gif'}:
                filename = secure_filename(file.filename)
                # Создаём уникальное имя файла
                timestamp = int(datetime.now().timestamp())
                unique_filename = f"feature_{timestamp}_{filename}"
                
                # Путь для сохранения
                upload_folder = Path('app/static/img')
                upload_folder.mkdir(parents=True, exist_ok=True)
                
                file_path = upload_folder / unique_filename
                file.save(str(file_path))
                
                feature_image_url = f"/static/img/{unique_filename}"
                logger.info(f"Загружено изображение для особенности: {unique_filename}")
    
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
    
    # обработка изображений секций
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

    dna_image = _save_image('dna', 'dna_image', 'dna_image_url')
    auracloud_image = _save_image('auracloud', 'auracloud_image', 'auracloud_image_url')

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
