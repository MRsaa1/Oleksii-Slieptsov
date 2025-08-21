#!/usr/bin/env python3
"""
Скрипт для настройки GitHub репозитория
"""

import subprocess
import sys
import os

def run_command(command):
    """Выполнение команды с выводом"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_github_repo():
    """Проверка существования репозитория"""
    print("🔍 Проверка репозитория на GitHub...")
    
    success, stdout, stderr = run_command("git ls-remote origin")
    
    if success:
        print("✅ Репозиторий найден на GitHub!")
        return True
    else:
        print("❌ Репозиторий не найден или недоступен")
        print("�� Нужно создать репозиторий на GitHub")
        return False

def push_to_github():
    """Отправка кода на GitHub"""
    print("📤 Отправка кода на GitHub...")
    
    success, stdout, stderr = run_command("git push -u origin main")
    
    if success:
        print("✅ Код успешно отправлен на GitHub!")
        print("🌐 Репозиторий доступен по адресу:")
        print("   https://github.com/MRsaa1/between-the-lines")
        return True
    else:
        print("❌ Ошибка при отправке кода:")
        print(stderr)
        return False

def main():
    """Основная функция"""
    print("🚀 Настройка GitHub репозитория")
    print("=" * 50)
    
    # Проверяем репозиторий
    if not check_github_repo():
        print("\n📋 Инструкция по созданию репозитория:")
        print("1. Перейдите на https://github.com/new")
        print("2. Repository name: between-the-lines")
        print("3. Description: Автоматизированная система анализа финансово-экономических новостей")
        print("4. Public repository")
        print("5. НЕ ставьте галочки на README, .gitignore, license")
        print("6. Нажмите 'Create repository'")
        print("\nПосле создания репозитория запустите этот скрипт снова")
        return False
    
    # Отправляем код
    if push_to_github():
        print("\n🎉 Настройка завершена успешно!")
        print("\n📋 Следующие шаги:")
        print("1. Перейдите на https://replit.com")
        print("2. Создайте новый Repl")
        print("3. Выберите 'Import from GitHub'")
        print("4. Введите: MRsaa1/between-the-lines")
        print("5. Настройте OPENAI_API_KEY в Secrets")
        print("6. Запустите: python3 web_interface.py")
        return True
    else:
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
