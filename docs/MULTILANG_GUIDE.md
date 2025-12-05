# Руководство по мультиязычности OilFusion

## Обзор

Система поддерживает 3 языка:
- 🇷🇺 Русский (RU) - основной язык, используется как fallback
- 🇱🇻 Латышский (LV)
- 🇬🇧 Английский (EN)

Все текстовые поля контента хранятся в БД в 3 вариантах: `value_ru`, `value_lv`, `value_en`.

---

## Использование в шаблонах

### Хелпер-функции

В шаблонах доступны 2 функции:

#### 1. `get_content(section, key, default='')`

Получить одно поле контента на текущем языке пользователя.

```jinja
<h1>{{ get_content('hero', 'slogan', 'Balance in every drop') }}</h1>
<p>{{ get_content('hero', 'subtitle') }}</p>
```

#### 2. `get_section_content(section)`

Получить все поля секции на текущем языке.

```jinja
{% set hero = get_section_content('hero') %}
<h1>{{ hero.slogan }}</h1>
<p>{{ hero.subtitle }}</p>
<button>{{ hero.cta_primary }}</button>
```

### Пример обновления шаблона

**Было:**
```jinja
<h1>{{ hero.slogan }}</h1>
```

**Стало:**
```jinja
<h1>{{ get_content('hero', 'slogan') }}</h1>
```

Или:
```jinja
{% set hero = get_section_content('hero') %}
<h1>{{ hero.slogan }}</h1>
```

---

## Админка: Редактирование контента

### Использование готового макроса

Импортируйте макрос в шаблон админки:

```jinja
{% from 'admin/components/multilang_field.html' import input, textarea %}
```

### Текстовое поле (input)

```jinja
{% from 'admin/components/multilang_field.html' import input %}

{{ input(
    name='slogan',
    label='Слоган (заголовок)',
    content_obj=hero_slogan_obj,
    placeholder='Balance in every drop',
    required=true,
    help_text='Основной заголовок на главной странице'
) }}
```

### Многострочное поле (textarea)

```jinja
{% from 'admin/components/multilang_field.html' import textarea %}

{{ textarea(
    name='subtitle',
    label='Подзаголовок',
    content_obj=hero_subtitle_obj,
    rows=3,
    placeholder='Персонализированные масла...',
    help_text='Описание под заголовком'
) }}
```

### Пример полного шаблона админки

```jinja
{% extends "admin/base.html" %}
{% from 'admin/components/multilang_field.html' import input, textarea %}

{% block content %}
<div class="admin-edit-page">
  <h1>Hero секция</h1>
  
  <form method="POST" action="{{ url_for('admin.hero_save', token=token) }}">
    {{ input(
        name='slogan',
        label='Слоган',
        content_obj=hero_slogan,
        required=true
    ) }}
    
    {{ textarea(
        name='subtitle',
        label='Подзаголовок',
        content_obj=hero_subtitle,
        rows=3
    ) }}
    
    <button type="submit">Сохранить</button>
  </form>
</div>
{% endblock %}
```

---

## Админка: Обработка сохранения (Python)

### 1. Получение данных из формы

Каждое поле создаёт 3 input с суффиксами `_ru`, `_lv`, `_en`:

```python
from flask import request
from app.database import ContentRepository

@admin_bp.route('/<token>/admin/hero/save', methods=['POST'])
@require_admin_token
def hero_save(token):
    # Получаем данные для всех языков
    slogan_ru = request.form.get('slogan_ru', '').strip()
    slogan_lv = request.form.get('slogan_lv', '').strip()
    slogan_en = request.form.get('slogan_en', '').strip()
    
    subtitle_ru = request.form.get('subtitle_ru', '').strip()
    subtitle_lv = request.form.get('subtitle_lv', '').strip()
    subtitle_en = request.form.get('subtitle_en', '').strip()
    
    # Сохраняем в БД
    ContentRepository.set(
        section='hero',
        key='slogan',
        value_ru=slogan_ru,
        value_lv=slogan_lv,
        value_en=slogan_en
    )
    
    ContentRepository.set(
        section='hero',
        key='subtitle',
        value_ru=subtitle_ru,
        value_lv=subtitle_lv,
        value_en=subtitle_en
    )
    
    flash('Сохранено!', 'success')
    return redirect(url_for('admin.hero_edit', token=token))
```

### 2. Передача объектов контента в шаблон

```python
from app.database import ContentRepository

@admin_bp.route('/<token>/admin/hero')
@require_admin_token
def hero_edit(token):
    # Получаем объекты Content со всеми языками
    hero_slogan = ContentRepository.get_content_object('hero', 'slogan')
    hero_subtitle = ContentRepository.get_content_object('hero', 'subtitle')
    
    return render_template(
        'admin/hero_edit.html',
        hero_slogan=hero_slogan,
        hero_subtitle=hero_subtitle,
        token=token
    )
```

---

## API ContentRepository

### `ContentRepository.set()`

Сохранить/обновить контент для всех или части языков:

```python
ContentRepository.set(
    section='hero',
    key='slogan',
    value_ru='Balance in every drop',
    value_lv='Līdzsvars katrā pilienā',
    value_en='Balance in every drop'
)
```

### `ContentRepository.get()`

Получить значение для конкретного языка:

```python
# Получить на русском
slogan_ru = ContentRepository.get('hero', 'slogan', locale='ru')

# Получить на латышском (с fallback на русский)
slogan_lv = ContentRepository.get('hero', 'slogan', locale='lv', default='')
```

### `ContentRepository.get_section()`

Получить все поля секции для конкретного языка:

```python
hero_content_ru = ContentRepository.get_section('hero', locale='ru')
# {'slogan': '...', 'subtitle': '...', ...}
```

### `ContentRepository.get_content_object()`

Получить объект Content со всеми языками (для админки):

```python
content_obj = ContentRepository.get_content_object('hero', 'slogan')
# content_obj.value_ru, content_obj.value_lv, content_obj.value_en
```

---

## Миграция существующих JSON данных

Скрипт `migrate_to_multilang.py` уже был запущен и перенёс все данные из старого поля `value` в `value_ru`.

Если нужно добавить переводы:

1. Откройте админку
2. Отредактируйте контент, переключаясь между языками 🇷🇺🇱🇻🇬🇧
3. Сохраните

---

## Чеклист обновления секции

### Для фронтенда (шаблон секции):

- [ ] Импортировать хелпер `get_section_content()`
- [ ] Заменить прямые обращения к данным на вызов хелпера
- [ ] Проверить отображение на всех языках

### Для админки (редактирование):

- [ ] Импортировать макросы `multilang_field.html`
- [ ] Заменить обычные input/textarea на мультиязычные макросы
- [ ] Обновить роут GET: передавать объекты Content через `get_content_object()`
- [ ] Обновить роут POST: получать данные с суффиксами `_ru`, `_lv`, `_en`
- [ ] Сохранять через `ContentRepository.set()` с тремя параметрами

---

## Пример: Полное обновление Hero секции

### 1. Шаблон фронтенда (`sections/hero.html`)

```jinja
{% set hero = get_section_content('hero') %}

<section id="hero">
    <h1>{{ hero.slogan }}</h1>
    <p>{{ hero.subtitle }}</p>
    <button>{{ hero.cta_primary }}</button>
    <button>{{ hero.cta_secondary }}</button>
</section>
```

### 2. Шаблон админки (`admin/hero_edit.html`)

```jinja
{% extends "admin/base.html" %}
{% from 'admin/components/multilang_field.html' import input, textarea %}

{% block content %}
<form method="POST" action="{{ url_for('admin.hero_save', token=token) }}">
    {{ input(name='slogan', label='Слоган', content_obj=hero_slogan, required=true) }}
    {{ textarea(name='subtitle', label='Подзаголовок', content_obj=hero_subtitle, rows=3) }}
    {{ input(name='cta_primary', label='Основная кнопка', content_obj=hero_cta_primary) }}
    {{ input(name='cta_secondary', label='Вторичная кнопка', content_obj=hero_cta_secondary) }}
    
    <button type="submit">Сохранить</button>
</form>
{% endblock %}
```

### 3. Роуты админки (`routes/admin.py`)

```python
from app.database import ContentRepository

@admin_bp.route('/<token>/admin/hero')
@require_admin_token
def hero_edit(token):
    return render_template(
        'admin/hero_edit.html',
        hero_slogan=ContentRepository.get_content_object('hero', 'slogan'),
        hero_subtitle=ContentRepository.get_content_object('hero', 'subtitle'),
        hero_cta_primary=ContentRepository.get_content_object('hero', 'cta_primary'),
        hero_cta_secondary=ContentRepository.get_content_object('hero', 'cta_secondary'),
        token=token
    )

@admin_bp.route('/<token>/admin/hero/save', methods=['POST'])
@require_admin_token
def hero_save(token):
    # Сохраняем каждое поле с тремя языками
    for key in ['slogan', 'subtitle', 'cta_primary', 'cta_secondary']:
        ContentRepository.set(
            section='hero',
            key=key,
            value_ru=request.form.get(f'{key}_ru', '').strip(),
            value_lv=request.form.get(f'{key}_lv', '').strip(),
            value_en=request.form.get(f'{key}_en', '').strip()
        )
    
    flash('Сохранено!', 'success')
    return redirect(url_for('admin.hero_edit', token=token))
```

---

## Fallback логика

Если перевод для языка не указан, автоматически используется русский:

```python
# В БД:
# value_ru = "Баланс в каждой капле"
# value_lv = NULL
# value_en = "Balance in every drop"

# При запросе LV:
ContentRepository.get('hero', 'slogan', locale='lv')
# Вернёт: "Баланс в каждой капле" (fallback на RU)
```

---

## Тестирование

1. Откройте сайт
2. Переключите язык через sidebar (🇷🇺🇱🇻🇬🇧)
3. Проверьте, что весь контент меняется
4. Откройте админку
5. Отредактируйте контент на разных языках
6. Сохраните и проверьте на фронтенде

---

## FAQ

**Q: Можно ли оставить перевод пустым?**  
A: Да, в этом случае будет использован русский текст.

**Q: Нужно ли обновлять все секции сразу?**  
A: Нет, можно обновлять постепенно. Старые секции продолжат работать.

**Q: Как добавить новый язык?**  
A: Нужно добавить столбец в БД (`value_xx`), обновить модель `Content` и макросы.

**Q: Где хранятся переводы интерфейса (кнопок, меню)?**  
A: В таблице `translations`. Они работают через систему i18n.




