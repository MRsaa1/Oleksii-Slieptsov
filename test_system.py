#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы системы Between The Lines
"""

import sys
import logging
from pathlib import Path

# Добавляем текущую директорию в путь
sys.path.append(str(Path(__file__).parent))

from config import *
from news_gatherer import NewsGatherer
from scorer import RelevanceScorer

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_news_gathering():
    """Тест сбора новостей"""
    print("🧪 Тестирование сбора новостей...")
    
    try:
        gatherer = NewsGatherer()
        news_list = gatherer.gather_news()
        
        if news_list:
            print(f"✅ Собрано {len(news_list)} новостей")
            
            # Показываем первые 3 новости
            for i, news in enumerate(news_list[:3], 1):
                print(f"\n{i}. {news.get('title', 'Нет заголовка')[:100]}...")
                print(f"   Источник: {news.get('source', 'Неизвестно')}")
                print(f"   Дата: {news.get('date', 'Не указана')}")
            
            return news_list
        else:
            print("❌ Не удалось собрать новости")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при сборе новостей: {str(e)}")
        return []

def test_scoring(news_list):
    """Тест оценки новостей"""
    print("\n🧪 Тестирование оценки новостей...")
    
    if not news_list:
        print("❌ Нет новостей для оценки")
        return []
    
    try:
        scorer = RelevanceScorer()
        scored_news = scorer.score_news(news_list)
        
        if scored_news:
            print(f"✅ Оценено {len(scored_news)} новостей")
            
            # Показываем топ-3 с оценками
            for i, news in enumerate(scored_news[:3], 1):
                print(f"\n{i}. Оценка: {news.get('score', 0):.2f}/10")
                print(f"   {news.get('title', 'Нет заголовка')[:100]}...")
                print(f"   Источник: {news.get('source', 'Неизвестно')}")
            
            return scored_news
        else:
            print("❌ Не удалось оценить новости")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при оценке новостей: {str(e)}")
        return []

def test_config():
    """Тест конфигурации"""
    print("🧪 Тестирование конфигурации...")
    
    try:
        print(f"✅ RSS источников: {len(RSS_SOURCES)}")
        print(f"✅ Веб-сайтов: {len(WEBSITE_SOURCES)}")
        print(f"✅ Ключевых слов: {len(IMPORTANT_KEYWORDS)}")
        print(f"✅ Весов источников: {len(SOURCE_WEIGHTS)}")
        
        if OPENAI_API_KEY:
            print("✅ OpenAI API ключ настроен")
        else:
            print("⚠️ OpenAI API ключ не настроен")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {str(e)}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования системы Between The Lines")
    print("=" * 50)
    
    # Тест конфигурации
    if not test_config():
        return False
    
    # Тест сбора новостей
    news_list = test_news_gathering()
    
    # Тест оценки новостей
    if news_list:
        scored_news = test_scoring(news_list)
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
