#!/usr/bin/env python3
"""
Скрипт для запуска Between The Lines на Replit
"""

import os
import sys
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Проверка настроек окружения"""
    logger.info("🔍 Проверка настроек окружения...")
    
    # Проверяем наличие API ключа
    if not os.getenv('OPENAI_API_KEY'):
        logger.error("❌ OPENAI_API_KEY не найден в переменных окружения")
        logger.info("💡 Установите переменную OPENAI_API_KEY в настройках Replit")
        return False
    
    logger.info("✅ Настройки окружения корректны")
    return True

def setup_directories():
    """Создание необходимых директорий"""
    logger.info("📁 Создание директорий...")
    
    # Создаем директорию для выходных файлов
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    logger.info("✅ Директории созданы")
    return True

def main():
    """Основная функция"""
    logger.info("🚀 Запуск Between The Lines на Replit")
    
    # Проверяем окружение
    if not check_environment():
        return False
    
    # Создаем директории
    if not setup_directories():
        return False
    
    # Импортируем и запускаем основную систему
    try:
        from main import main as run_system
        success = run_system()
        
        if success:
            logger.info("✅ Система завершила работу успешно")
            return True
        else:
            logger.error("❌ Система завершила работу с ошибками")
            return False
            
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
