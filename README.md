# OilFusion Landing

Современный лендинг для компании OilFusion - персонализированные масла на основе технологий AuraCloud® 3D и ДНК-тестирования.

## 🌟 Особенности

- **Hero секция** с главным слоганом "Balance in every drop"
- **О компании** с философией и технологиями AuraCloud® 3D и ДНК-тестирования
- **Продукция** - каталог продуктов
- **Услуги** - описание предоставляемых услуг
- **Персонализация** - визуализация технологий подбора
- **Отзывы** - слайдер отзывов клиентов
- **Блог** - актуальные статьи
- **Контакты** - карта Google Maps и контактная информация

## 🛠 Технологический стек

- **Backend**: Flask 3.0.0
- **Логирование**: Loguru
- **WSGI**: Gunicorn
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)

## 📦 Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd OilFusion_Lending
```

### 2. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env` и заполните необходимые значения:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Отредактируйте `.env` файл:

```env
SECRET_KEY=your-secure-secret-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
COMPANY_EMAIL=info@oilfusion.com
# ... остальные настройки
```

## 🚀 Запуск

### Режим разработки

```bash
python run.py
```

Приложение будет доступно по адресу: `http://localhost:5000`

### Production режим

```bash
# Установить переменную окружения
set FLASK_ENV=production  # Windows
export FLASK_ENV=production  # Linux/Mac

# Запуск через Gunicorn (Linux/Mac)
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Запуск через waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 run:app
```

## 📁 Структура проекта

```
OilFusion_Lending/
├── app/
│   ├── __init__.py              # Инициализация Flask приложения
│   ├── config/                  # Конфигурация
│   │   ├── __init__.py
│   │   └── settings.py          # Настройки приложения
│   ├── routes/                  # Маршруты
│   │   ├── __init__.py
│   │   └── main.py              # Основные маршруты
│   ├── static/                  # Статические файлы
│   │   ├── css/                 # Стили
│   │   ├── js/                  # JavaScript
│   │   └── images/              # Изображения
│   ├── templates/               # HTML шаблоны
│   │   ├── base.html            # Базовый шаблон
│   │   ├── index.html           # Главная страница
│   │   └── sections/            # Секции лендинга
│   └── utils/                   # Утилиты
│       ├── __init__.py
│       └── logger.py            # Настройка логирования
├── logs/                        # Логи приложения
├── .env.example                 # Пример файла окружения
├── .gitignore                   # Git ignore файл
├── requirements.txt             # Python зависимости
├── run.py                       # Точка входа
└── README.md                    # Документация

```

## 🔧 Конфигурация

### Настройки окружения

Приложение поддерживает три режима работы:
- `development` - режим разработки (по умолчанию)
- `production` - production режим
- `testing` - режим тестирования

Настройка режима через переменную окружения `FLASK_ENV`.

### Логирование

Используется библиотека `loguru` для логирования:
- Логи в консоль с цветным выводом
- Логи в файл с автоматической ротацией (10 MB)
- Автоматическое сжатие старых логов
- Хранение логов в течение 1 недели

## 🏗 Архитектура

Проект построен на основе паттерна **Application Factory**:
- Разделение на модули (blueprints)
- Централизованная конфигурация
- Масштабируемая структура
- Легкое тестирование

## 📝 Разработка

### Добавление новых маршрутов

1. Создайте новый blueprint в `app/routes/`
2. Зарегистрируйте его в `app/__init__.py`
3. Добавьте соответствующие шаблоны в `app/templates/`

### Стилизация

- CSS файлы размещаются в `app/static/css/`
- JavaScript файлы в `app/static/js/`
- Изображения в `app/static/images/`

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'feat: Добавлена новая функция'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

### Формат коммитов

Используйте [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` - новая функциональность
- `fix:` - исправление ошибок
- `docs:` - документация
- `style:` - форматирование
- `refactor:` - рефакторинг
- `test:` - тесты
- `chore:` - технические работы

## 📄 Лицензия

Этот проект является частной разработкой для OilFusion.

## 📞 Контакты

- Email: info@oilfusion.com
- Website: [oilfusion.com](https://oilfusion.com)

---

**Balance in every drop** ✨





