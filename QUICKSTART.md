# ⚡ Быстрый старт OilFusion Landing

## За 3 минуты до запуска

### 1️⃣ Установка зависимостей

```bash
# Создать и активировать виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Установить пакеты
pip install -r requirements.txt
```

### 2️⃣ Создать .env файл (опционально)

```bash
# Скопировать пример
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

Или использовать настройки по умолчанию.

### 3️⃣ Запустить приложение

```bash
python run.py
```

### 🎉 Готово!

Откройте браузер: **http://localhost:5000**

---

## 📱 Что вы увидите

1. **Hero секция** - "Balance in every drop"
2. **О компании** - Философия и технологии
3. **Продукция** - Каталог (заглушки)
4. **Услуги** - Описание услуг
5. **Персонализация** - ДНК и AuraCloud® 3D
6. **Отзывы** - Слайдер отзывов
7. **Блог** - Статьи (заглушки)
8. **Контакты** - Форма и карта
9. **Подвал** - Ссылки и соцсети

---

## 🛠 Следующие шаги

### Добавить контент

1. **Изображения** → `app/static/images/`
2. **Продукты** → `app/routes/main.py` (переменная `products_data`)
3. **Услуги** → `app/routes/main.py` (переменная `services_data`)
4. **Отзывы** → `app/routes/main.py` (переменная `reviews_data`)
5. **Статьи** → `app/routes/main.py` (переменная `blog_data`)

### Настроить Google Maps

В `.env` файле:
```env
GOOGLE_MAPS_API_KEY=ваш-ключ
COMPANY_LATITUDE=55.751244
COMPANY_LONGITUDE=37.618423
```

### Изменить цвета

В `app/static/css/main.css` измените CSS переменные:
```css
:root {
    --primary-color: #2C7A7B;  /* Основной цвет */
    --secondary-color: #D69E2E; /* Акцентный цвет */
    /* ... */
}
```

---

## 💡 Полезные команды

```bash
# Проверка здоровья приложения
curl http://localhost:5000/health

# Просмотр логов
type logs\app.log  # Windows
# cat logs/app.log  # Linux/Mac

# Остановка сервера
Ctrl + C
```

---

## 📚 Документация

- **README.md** - Полное описание проекта
- **SETUP.md** - Детальная инструкция по установке
- **PROJECT_STRUCTURE.md** - Структура и архитектура
- **COMMIT_MESSAGE.md** - Шаблон для Git коммита

---

## 🐛 Проблемы?

### Порт занят
```bash
# В .env измените порт
PORT=8000
```

### Ошибка импорта
```bash
pip install -r requirements.txt --upgrade
```

### Нет директории logs
```bash
mkdir logs
```

---

**Готово! Удачной разработки!** 🚀

*Balance in every drop* ✨





