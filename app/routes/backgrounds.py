"""
Маршруты для управления фоновыми изображениями секций.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import os
from app.models.images import SectionBackgrounds
from app.utils.logger import get_logger
from app.utils.auth import require_admin_token

logger = get_logger()

# Создание Blueprint для управления фонами
backgrounds_bp = Blueprint('backgrounds', __name__)

# Разрешённые расширения для изображений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}


def allowed_file(filename: str) -> bool:
    """Проверка расширения файла."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@backgrounds_bp.route('/<token>/admin/backgrounds')
@require_admin_token
def backgrounds_list(token):
    """
    Управление фоновыми изображениями всех секций.
    
    Args:
        token: JWT токен
        
    Returns:
        Отрендеренный шаблон управления фонами
    """
    logger.info("Запрос управления фоновыми изображениями")
    
    backgrounds = SectionBackgrounds()
    all_backgrounds = backgrounds.get_all_backgrounds()
    
    # Список секций для управления
    sections = {
        'hero': 'Hero (Главная секция)',
        'about': 'О компании',
        'products': 'Продукция',
        'services': 'Услуги',
        'personalization': 'Персонализация',
        'reviews': 'Отзывы',
        'blog': 'Блог',
        'contacts': 'Контакты'
    }
    
    return render_template(
        'admin/backgrounds.html', 
        backgrounds=all_backgrounds,
        sections=sections,
        token=token
    )


@backgrounds_bp.route('/<token>/admin/backgrounds/<section>/update', methods=['POST'])
@require_admin_token
def background_update(token, section):
    """
    Обновление фона секции.
    
    Args:
        token: JWT токен
        section: Название секции
        
    Returns:
        Редирект на страницу управления фонами
    """
    logger.info(f"Обновление фона секции {section}")
    
    backgrounds = SectionBackgrounds()
    
    bg_type = request.form.get('bg_type', 'white')
    image_url = request.form.get('image_url', '')
    gradient = request.form.get('gradient', '')
    overlay_opacity = float(request.form.get('overlay_opacity', 0.3))
    overlay_color = request.form.get('overlay_color', '#000000')
    
    # Обработка загруженного файла
    if 'image_file' in request.files:
        file = request.files['image_file']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Создаём уникальное имя файла
            timestamp = int(datetime.now().timestamp())
            unique_filename = f"{section}_{timestamp}_{filename}"
            
            # Путь для сохранения
            upload_folder = Path('app/static/img')
            upload_folder.mkdir(parents=True, exist_ok=True)
            
            file_path = upload_folder / unique_filename
            file.save(str(file_path))
            
            image_url = f"/static/img/{unique_filename}"
            logger.info(f"Загружено изображение: {unique_filename}")
    
    if backgrounds.update_section_background(
        section, bg_type, image_url, gradient, overlay_opacity, overlay_color
    ):
        flash(f'Фон секции "{section}" успешно обновлён!', 'success')
    else:
        flash('Ошибка при обновлении фона!', 'error')
    
    return redirect(url_for('backgrounds.backgrounds_list', token=token))


@backgrounds_bp.route('/<token>/admin/backgrounds/<section>/reset', methods=['POST'])
@require_admin_token
def background_reset(token, section):
    """
    Сброс фона секции к настройкам по умолчанию.
    
    Args:
        token: JWT токен
        section: Название секции
        
    Returns:
        Редирект на страницу управления фонами
    """
    logger.info(f"Сброс фона секции {section} к настройкам по умолчанию")
    
    backgrounds = SectionBackgrounds()
    
    if backgrounds.reset_section_to_default(section):
        flash(f'Фон секции "{section}" сброшен к настройкам по умолчанию!', 'success')
    else:
        flash('Ошибка при сбросе фона!', 'error')
    
    return redirect(url_for('backgrounds.backgrounds_list', token=token))

