# 🚀 Инструкция по первому запуску OilFusion Landing

## Предварительные требования

- Python 3.8+
- pip (менеджер пакетов Python)
- Git (опционально)

## 📋 Шаги по установке и запуску

### 1. Создание виртуального окружения

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения

# Windows (CMD)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Отредактируйте `.env` файл и укажите свои значения:

```env
SECRET_KEY=ваш-секретный-ключ-для-production
GOOGLE_MAPS_API_KEY=ваш-ключ-google-maps-api
COMPANY_EMAIL=info@oilfusion.com
# ... остальные параметры
```

### 4. Запуск приложения

```bash
python run.py
```

Приложение будет доступно по адресу: **http://localhost:5000**

## 🔧 Режимы запуска

### Режим разработки (по умолчанию)

```bash
set FLASK_ENV=development
python run.py
```

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
├── app/                          # Основное приложение
│   ├── __init__.py              # Инициализация Flask
│   ├── config/                  # Конфигурация
│   │   ├── __init__.py
│   │   └── settings.py          # Настройки приложения
│   ├── routes/                  # Маршруты
│   │   ├── __init__.py
│   │   └── main.py              # Основные маршруты
│   ├── static/                  # Статические файлы
│   │   ├── css/                 # Стили
│   │   │   ├── main.css         # Основные стили
│   │   │   ├── sections.css     # Стили секций
│   │   │   └── responsive.css   # Адаптивные стили
│   │   ├── js/                  # JavaScript
│   │   │   ├── main.js          # Основной JS
│   │   │   ├── slider.js        # Слайдер отзывов
│   │   │   └── smooth-scroll.js # Плавная прокрутка
│   │   └── images/              # Изображения
│   ├── templates/               # HTML шаблоны
│   │   ├── base.html            # Базовый шаблон
│   │   ├── index.html           # Главная страница
│   │   └── sections/            # Секции лендинга
│   │       ├── hero.html        # Hero секция
│   │       ├── about.html       # О компании
│   │       ├── products.html    # Продукция
│   │       ├── services.html    # Услуги
│   │       ├── personalization.html  # Персонализация
│   │       ├── reviews.html     # Отзывы
│   │       ├── blog.html        # Блог
│   │       ├── contacts.html    # Контакты
│   │       └── footer.html      # Подвал
│   └── utils/                   # Утилиты
│       ├── __init__.py
│       └── logger.py            # Логирование
├── logs/                        # Логи приложения
├── .gitignore                   # Git ignore
├── requirements.txt             # Python зависимости
├── run.py                       # Точка входа
├── README.md                    # Документация
└── SETUP.md                     # Инструкция по запуску
```

## 🎨 Секции лендинга

1. **Hero** - Главная секция со слоганом "Balance in every drop"
2. **О компании** - Философия, технологии AuraCloud® 3D и ДНК-тестирование
3. **Продукция** - Каталог продуктов с карточками
4. **Услуги** - Описание предоставляемых услуг
5. **Персонализация** - Детальное описание технологий
6. **Отзывы** - Слайдер отзывов клиентов
7. **Блог** - Статьи и полезная информация
8. **Контакты** - Карта Google Maps и форма обратной связи
9. **Подвал** - Ссылки, соцсети, форма подписки

## 🔑 Ключевые функции

### Логирование
- Используется библиотека **loguru**
- Логи выводятся в консоль и файл `logs/app.log`
- Автоматическая ротация логов (10 MB)
- Сжатие старых логов

### Навигация
- Плавная прокрутка к секциям
- Адаптивное мобильное меню
- Кнопка "Наверх"

### Интерактивность
- Слайдер "До/После" для визуализации ауры
- Слайдер отзывов с автопрокруткой
- Формы обратной связи и подписки
- Анимации при прокрутке

## 🛠 Технологии

- **Backend**: Flask 3.0.0
- **Логирование**: Loguru
- **WSGI**: Gunicorn
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)

## ✅ Проверка работоспособности

После запуска откройте браузер и перейдите по адресу:

```
http://localhost:5000
```

Также доступен health check endpoint:

```
http://localhost:5000/health
```

## 📝 Дальнейшая разработка

### Добавление контента

1. **Изображения**: Разместите изображения в `app/static/images/`
2. **Продукты**: Добавьте данные в `app/routes/main.py` в функции `index()`
3. **Услуги**: Аналогично продуктам
4. **Отзывы**: Добавьте данные отзывов
5. **Статьи блога**: Добавьте статьи

### Настройка Google Maps

1. Получите API ключ: https://developers.google.com/maps/documentation/javascript/get-api-key
2. Добавьте ключ в `.env` файл:
   ```
   GOOGLE_MAPS_API_KEY=ваш-ключ
   ```
3. Укажите координаты офиса:
   ```
   COMPANY_LATITUDE=55.751244
   COMPANY_LONGITUDE=37.618423
   ```

### Стилизация

- Измените цветовую схему в `app/static/css/main.css` (переменные CSS)
- Добавьте свои шрифты
- Настройте адаптивность в `app/static/css/responsive.css`

## 🐛 Устранение проблем

### Ошибка импорта модулей

```bash
pip install -r requirements.txt --upgrade
```

### Проблемы с логами

Убедитесь, что директория `logs/` существует:

```bash
mkdir logs
```

### Порт уже занят

Измените порт в `.env` файле:

```
PORT=8000
```

## 📞 Поддержка

При возникновении проблем создайте issue в репозитории или свяжитесь с командой разработки.

---

**Balance in every drop** ✨





