"""
Скрипт для генерации JWT токена для доступа к админке OilFusion.
Запустите этот скрипт для получения токена доступа к админке.
"""

import os
import sys
from pathlib import Path

# Настройка кодировки для Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')  # UTF-8
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Добавляем путь к приложению
sys.path.insert(0, str(Path(__file__).parent))

from app.config.settings import Config
from app.utils.auth import generate_admin_token, get_token_info
from datetime import datetime


def main():
    """Главная функция для генерации токена."""
    print("=" * 60)
    print("🔐 ГЕНЕРАТОР JWT ТОКЕНА ДЛЯ АДМИНКИ OILFUSION")
    print("=" * 60)
    print()
    
    # Получаем SECRET_KEY
    secret_key = os.getenv('SECRET_KEY') or Config.SECRET_KEY
    
    if not secret_key or secret_key == 'dev-secret-key-change-in-production':
        print("⚠️  ВНИМАНИЕ: Используется стандартный SECRET_KEY")
        print("   Для production рекомендуется установить свой SECRET_KEY в .env")
        print()
    
    # Запрашиваем срок действия
    print("📅 Срок действия токена:")
    print("   1. 1 день")
    print("   2. 1 неделя")
    print("   3. 1 месяц")
    print("   4. 1 год (по умолчанию)")
    print("   5. Навсегда (не рекомендуется)")
    print()
    
    choice = input("Выберите вариант (1-5) или нажмите Enter для варианта 4: ").strip()
    
    # Определяем срок действия в часах
    expires_hours_map = {
        '1': 24,           # 1 день
        '2': 168,          # 1 неделя
        '3': 720,          # 1 месяц (30 дней)
        '4': 8760,         # 1 год
        '5': 876000,       # 100 лет (практически навсегда)
        '': 8760           # по умолчанию 1 год
    }
    
    expires_hours = expires_hours_map.get(choice, 8760)
    
    # Генерируем токен
    print()
    print("⏳ Генерация токена...")
    token = generate_admin_token(secret_key, expires_hours)
    
    # Получаем информацию о токене
    token_info = get_token_info(token, secret_key)
    
    print()
    print("=" * 60)
    print("✅ ТОКЕН УСПЕШНО СГЕНЕРИРОВАН!")
    print("=" * 60)
    print()
    print("🔑 ВАШ ТОКЕН:")
    print("-" * 60)
    print(token)
    print("-" * 60)
    print()
    
    # Информация о токене
    if token_info.get('valid'):
        print("📊 ИНФОРМАЦИЯ О ТОКЕНЕ:")
        print(f"   Создан:        {token_info.get('issued_at', 'N/A')}")
        print(f"   Истекает:      {token_info.get('expires_at', 'N/A')}")
        print(f"   ID токена:     {token_info.get('jti', 'N/A')}")
        print()
    
    # URL для доступа
    print("🌐 URL ДЛЯ ДОСТУПА К АДМИНКЕ:")
    print()
    print(f"   Дашборд:       http://localhost:5000/{token}/admin/")
    print(f"   О компании:    http://localhost:5000/{token}/admin/about")
    print(f"   Персонализ.:   http://localhost:5000/{token}/admin/personalization")
    print(f"   Блог:          http://localhost:5000/{token}/admin/blog")
    print()
    
    # Сохранение в файл
    save_choice = input("💾 Сохранить токен в файл? (y/n): ").strip().lower()
    
    if save_choice in ['y', 'yes', 'д', 'да']:
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
        
        print(f"✅ Токен сохранён в файл: {filename}")
        print()
    
    # Предупреждения
    print("⚠️  ВАЖНО:")
    print("   1. Сохраните этот токен в безопасном месте")
    print("   2. Не передавайте токен третьим лицам")
    print("   3. При компрометации токена сгенерируйте новый")
    print("   4. Для production установите надёжный SECRET_KEY в .env")
    print()
    
    print("=" * 60)
    print("🎉 Готово! Используйте токен для доступа к админке")
    print("=" * 60)
    print()
    
    # Автокопирование в буфер обмена (опционально)
    try:
        import pyperclip
        copy_choice = input("📋 Скопировать URL в буфер обмена? (y/n): ").strip().lower()
        if copy_choice in ['y', 'yes', 'д', 'да']:
            pyperclip.copy(f"http://localhost:5000/{token}/admin/")
            print("✅ URL скопирован в буфер обмена!")
    except ImportError:
        pass  # pyperclip не установлен - пропускаем


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Генерация токена отменена пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Ошибка при генерации токена: {str(e)}")
        sys.exit(1)

