"""
Упрощенный скрипт для генерации JWT токена.
Автоматически генерирует токен на 1 год.
"""

import os
import sys
from pathlib import Path

# Настройка кодировки
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')

sys.path.insert(0, str(Path(__file__).parent))

from app.config.settings import Config
from app.utils.auth import generate_admin_token, get_token_info
from datetime import datetime

def main():
    print("=" * 70)
    print("ГЕНЕРАТОР JWT ТОКЕНА ДЛЯ АДМИНКИ OILFUSION")
    print("=" * 70)
    print()
    
    # Получаем SECRET_KEY
    secret_key = os.getenv('SECRET_KEY') or Config.SECRET_KEY
    
    # Генерируем токен на 1 год
    expires_hours = 8760  # 1 год
    
    print("Генерация токена (срок действия: 1 год)...")
    token = generate_admin_token(secret_key, expires_hours)
    
    # Получаем информацию о токене
    token_info = get_token_info(token, secret_key)
    
    print()
    print("=" * 70)
    print("ТОКЕН УСПЕШНО СГЕНЕРИРОВАН!")
    print("=" * 70)
    print()
    print("ВАШ ТОКЕН:")
    print("-" * 70)
    print(token)
    print("-" * 70)
    print()
    
    if token_info.get('valid'):
        print("ИНФОРМАЦИЯ О ТОКЕНЕ:")
        print(f"  Создан:   {token_info.get('issued_at', 'N/A')}")
        print(f"  Истекает: {token_info.get('expires_at', 'N/A')}")
        print()
    
    print("URL ДЛЯ ДОСТУПА К АДМИНКЕ:")
    print()
    print(f"  Дашборд:       http://localhost:5000/{token}/admin/")
    print(f"  О компании:    http://localhost:5000/{token}/admin/about")
    print(f"  Персонализ.:   http://localhost:5000/{token}/admin/personalization")
    print(f"  Блог:          http://localhost:5000/{token}/admin/blog")
    print()
    
    # Сохранение в файл
    filename = 'admin_token.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"OilFusion Admin Token\n")
        f.write(f"Сгенерирован: {datetime.now().isoformat()}\n")
        f.write(f"Истекает: {token_info.get('expires_at', 'N/A')}\n")
        f.write(f"\n")
        f.write(f"Токен:\n")
        f.write(f"{token}\n")
        f.write(f"\n")
        f.write(f"URL для доступа:\n")
        f.write(f"http://localhost:5000/{token}/admin/\n")
    
    print(f"Токен сохранён в файл: {filename}")
    print()
    
    print("=" * 70)
    print("ГОТОВО! Используйте токен для доступа к админке")
    print("=" * 70)
    print()
    print("ВАЖНО:")
    print("  1. Сохраните этот токен в безопасном месте")
    print("  2. Не передавайте токен третьим лицам")
    print("  3. Для production установите надёжный SECRET_KEY в .env")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nОШИБКА при генерации токена: {str(e)}")
        sys.exit(1)

