"""
WSGI-энтрипоинт для деплоя на Render/Heroku/Gunicorn.
Экспортирует переменную `app`, которую ожидает gunicorn.
"""

from app import create_app

app = create_app()

# Опционально: точка входа для локального запуска `python wsgi.py`
if __name__ == "__main__":
    # Render предоставляет переменную PORT, но для локали используем 5000
    import os
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)


