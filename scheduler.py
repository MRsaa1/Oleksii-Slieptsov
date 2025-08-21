#!/usr/bin/env python3
"""
Scheduler для автоматического запуска Between The Lines
"""

import schedule
import time
import logging
import sys
from datetime import datetime
from pathlib import Path

# Добавляем текущую директорию в путь
sys.path.append(str(Path(__file__).parent))

from main import main

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_analysis():
    """Запуск анализа с логированием"""
    logger.info("🕐 Запуск запланированного анализа...")
    
    try:
        success = main()
        if success:
            logger.info("✅ Запланированный анализ завершен успешно")
        else:
            logger.error("❌ Запланированный анализ завершен с ошибками")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка в запланированном анализе: {str(e)}")

def setup_schedule():
    """Настройка расписания"""
    # Запуск каждый понедельник в 9:00
    schedule.every().monday.at("09:00").do(run_analysis)
    
    # Запуск каждый день в 9:00 (для тестирования)
    # schedule.every().day.at("09:00").do(run_analysis)
    
    # Запуск каждые 6 часов (для тестирования)
    # schedule.every(6).hours.do(run_analysis)
    
    logger.info("📅 Расписание настроено: каждый понедельник в 9:00")

def main_scheduler():
    """Основная функция планировщика"""
    logger.info("🚀 Запуск планировщика Between The Lines")
    
    # Настраиваем расписание
    setup_schedule()
    
    # Запускаем анализ сразу при старте (опционально)
    # run_analysis()
    
    logger.info("⏰ Планировщик запущен. Ожидание следующего запуска...")
    
    # Бесконечный цикл для выполнения запланированных задач
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту
        except KeyboardInterrupt:
            logger.info("⏹️ Планировщик остановлен пользователем")
            break
        except Exception as e:
            logger.error(f"❌ Ошибка в планировщике: {str(e)}")
            time.sleep(300)  # Ждем 5 минут перед повторной попыткой

if __name__ == "__main__":
    main_scheduler()
