#!/usr/bin/env python3
"""
Between The Lines - Главный оркестратор системы
Автоматизированная система анализа финансово-экономических новостей
"""

import os
import sys
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path

# Добавляем текущую директорию в путь для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import *
from news_gatherer import NewsGatherer
from scorer import RelevanceScorer
from ai_analyst import AIAnalyst
from content_generator import ContentGenerator

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BetweenTheLines:
    """Главный класс для оркестрации всего процесса анализа новостей"""
    
    def __init__(self):
        self.news_gatherer = NewsGatherer()
        self.scorer = RelevanceScorer()
        self.ai_analyst = AIAnalyst()
        self.content_generator = ContentGenerator()
        
        # Создаем директорию для выходных файлов
        Path(OUTPUT_DIR).mkdir(exist_ok=True)
        
    def run_weekly_analysis(self):
        """Основной метод для запуска еженедельного анализа"""
        try:
            logger.info("🚀 Запуск еженедельного анализа Between The Lines")
            
            # Шаг 1: Сбор новостей
            logger.info("📰 Сбор новостей из различных источников...")
            news_list = self.news_gatherer.gather_news()
            
            if not news_list:
                logger.error("❌ Не удалось собрать новости")
                return False
                
            logger.info(f"✅ Собрано {len(news_list)} новостей")
            
            # Шаг 2: Оценка релевантности и важности
            logger.info("🎯 Оценка релевантности новостей...")
            scored_news = self.scorer.score_news(news_list)
            
            if not scored_news:
                logger.error("❌ Не удалось оценить новости")
                return False
                
            logger.info(f"✅ Оценено {len(scored_news)} новостей")
            
            # Шаг 3: Выбор топ новости для анализа
            top_news = scored_news[0] if scored_news else None
            if not top_news:
                logger.error("❌ Нет подходящих новостей для анализа")
                return False
                
            logger.info(f"🏆 Выбрана главная новость: {top_news['title'][:100]}...")
            
            # Шаг 4: AI анализ
            logger.info("🤖 Запуск AI анализа...")
            analysis_result = self.ai_analyst.analyze_news(top_news)
            
            if not analysis_result:
                logger.error("❌ Не удалось проанализировать новость")
                return False
                
            logger.info("✅ AI анализ завершен")
            
            # Шаг 5: Генерация контента
            logger.info("�� Генерация итогового дайджеста...")
            digest_path = self.content_generator.generate_digest(top_news, analysis_result)
            
            # Генерация Telegram версии
            logger.info("📱 Генерация Telegram версии...")
            telegram_path = self.content_generator.generate_telegram_digest(top_news, analysis_result)
            digest_path = self.content_generator.generate_digest(top_news, analysis_result)
            
            if not digest_path:
                logger.error("❌ Не удалось сгенерировать дайджест")
                return False
                
            logger.info(f"✅ Дайджест сохранен: {digest_path}")
            
            # Шаг 6: Сохранение дополнительной информации
            self._save_analysis_data(top_news, analysis_result, scored_news)
            
            logger.info("🎉 Еженедельный анализ успешно завершен!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {str(e)}")
            return False
    
    def _save_analysis_data(self, top_news, analysis_result, scored_news):
        """Сохранение дополнительных данных анализа"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Сохраняем полные данные анализа
            analysis_data = {
                'timestamp': timestamp,
                'top_news': top_news,
                'analysis_result': analysis_result,
                'all_scored_news': scored_news[:10]  # Топ-10 новостей
            }
            
            analysis_file = Path(OUTPUT_DIR) / f"analysis_data_{timestamp}.json"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"📊 Данные анализа сохранены: {analysis_file}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения данных анализа: {str(e)}")

def main():
    """Точка входа в приложение"""
    try:
        # Проверяем наличие API ключа
        if not OPENAI_API_KEY:
            logger.error("❌ Не найден OPENAI_API_KEY в переменных окружения")
            logger.info("💡 Создайте файл .env с переменной OPENAI_API_KEY=your_key_here")
            return False
        
        # Создаем экземпляр системы
        btl = BetweenTheLines()
        
        # Запускаем анализ
        success = btl.run_weekly_analysis()
        
        if success:
            logger.info("✅ Система Between The Lines завершила работу успешно")
            return True
        else:
            logger.error("❌ Система Between The Lines завершила работу с ошибками")
            return False
            
    except KeyboardInterrupt:
        logger.info("⏹️ Работа прервана пользователем")
        return False
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
