#!/usr/bin/env python3
"""
Module 2: Relevance & Impact Scorer
Определение важности и релевантности новостей
"""

import re
import logging
from typing import List, Dict
from datetime import datetime

from config import IMPORTANT_KEYWORDS, SOURCE_WEIGHTS, MAX_NEWS_PER_WEEK

logger = logging.getLogger(__name__)

class RelevanceScorer:
    """Класс для оценки релевантности и важности новостей"""
    
    def __init__(self):
        self.keyword_patterns = [re.compile(rf'\b{keyword}\b', re.IGNORECASE) 
                               for keyword in IMPORTANT_KEYWORDS]
    
    def score_news(self, news_list: List[Dict]) -> List[Dict]:
        """Основной метод для оценки новостей"""
        try:
            logger.info(f"🎯 Начинаем оценку {len(news_list)} новостей...")
            
            scored_news = []
            
            for news in news_list:
                try:
                    score = self._calculate_score(news)
                    news_with_score = news.copy()
                    news_with_score['score'] = score
                    scored_news.append(news_with_score)
                    
                except Exception as e:
                    logger.warning(f"⚠️ Ошибка оценки новости '{news.get('title', 'Unknown')}': {str(e)}")
                    continue
            
            # Сортируем по убыванию оценки
            scored_news.sort(key=lambda x: x['score'], reverse=True)
            
            # Возвращаем топ новости
            top_news = scored_news[:MAX_NEWS_PER_WEEK]
            
            logger.info(f"✅ Оценено {len(scored_news)} новостей, выбрано {len(top_news)} лучших")
            
            # Логируем топ-3 новости для отладки
            for i, news in enumerate(top_news[:3]):
                logger.info(f"🏆 #{i+1}: {news['title'][:100]}... (оценка: {news['score']:.2f})")
            
            return top_news
            
        except Exception as e:
            logger.error(f"❌ Ошибка при оценке новостей: {str(e)}")
            return []
    
    def _calculate_score(self, news: Dict) -> float:
        """Расчет оценки для одной новости"""
        score = 0.0
        
        # Базовые компоненты оценки
        keyword_score = self._calculate_keyword_score(news)
        source_score = self._calculate_source_score(news)
        content_score = self._calculate_content_score(news)
        recency_score = self._calculate_recency_score(news)
        
        # Взвешенная сумма всех компонентов
        score = (
            keyword_score * 0.4 +      # 40% - ключевые слова
            source_score * 0.3 +       # 30% - источник
            content_score * 0.2 +      # 20% - качество контента
            recency_score * 0.1        # 10% - свежесть
        )
        
        return round(score, 2)
    
    def _calculate_keyword_score(self, news: Dict) -> float:
        """Оценка по ключевым словам"""
        score = 0.0
        text_to_check = f"{news.get('title', '')} {news.get('description', '')}"
        
        # Подсчитываем количество совпадений ключевых слов
        keyword_matches = 0
        for pattern in self.keyword_patterns:
            if pattern.search(text_to_check):
                keyword_matches += 1
        
        # Нормализуем оценку (0-10 баллов)
        if keyword_matches == 0:
            score = 0.0
        elif keyword_matches == 1:
            score = 3.0
        elif keyword_matches == 2:
            score = 6.0
        elif keyword_matches >= 3:
            score = 10.0
        
        return score
    
    def _calculate_source_score(self, news: Dict) -> float:
        """Оценка по источнику новости"""
        source = news.get('source', '').lower()
        
        # Получаем вес источника из конфигурации
        source_weight = SOURCE_WEIGHTS.get(source, 1.0)
        
        # Нормализуем к шкале 0-10
        max_weight = max(SOURCE_WEIGHTS.values())
        normalized_score = (source_weight / max_weight) * 10
        
        return round(normalized_score, 2)
    
    def _calculate_content_score(self, news: Dict) -> float:
        """Оценка качества контента"""
        score = 0.0
        
        title = news.get('title', '')
        description = news.get('description', '')
        
        # Оценка по длине заголовка (оптимальная длина 30-100 символов)
        title_length = len(title)
        if 30 <= title_length <= 100:
            score += 3.0
        elif 20 <= title_length <= 150:
            score += 2.0
        else:
            score += 1.0
        
        # Оценка по наличию описания
        if description and len(description) > 50:
            score += 3.0
        elif description and len(description) > 20:
            score += 2.0
        else:
            score += 1.0
        
        # Оценка по качеству текста (наличие цифр, дат, имен)
        quality_indicators = 0
        
        # Проверяем наличие цифр (возможные суммы, проценты, даты)
        if re.search(r'\d+', title + description):
            quality_indicators += 1
        
        # Проверяем наличие заглавных букв (возможные имена, названия компаний)
        if re.search(r'[A-ZА-Я]', title + description):
            quality_indicators += 1
        
        # Проверяем наличие специальных символов (валюты, проценты)
        if re.search(r'[\$€£¥%]', title + description):
            quality_indicators += 1
        
        score += quality_indicators * 1.5
        
        return min(score, 10.0)  # Ограничиваем максимумом 10
    
    def _calculate_recency_score(self, news: Dict) -> float:
        """Оценка по свежести новости"""
        news_date = news.get('date')
        
        if not news_date:
            return 5.0  # Средняя оценка для новостей без даты
        
        now = datetime.now()
        days_old = (now - news_date).days
        
        # Оценка по свежести (новые новости получают больше баллов)
        if days_old == 0:
            score = 10.0
        elif days_old == 1:
            score = 9.0
        elif days_old == 2:
            score = 8.0
        elif days_old == 3:
            score = 7.0
        elif days_old <= 7:
            score = 6.0
        elif days_old <= 14:
            score = 4.0
        else:
            score = 2.0
        
        return score
    
    def get_score_breakdown(self, news: Dict) -> Dict:
        """Получение детальной разбивки оценки для отладки"""
        return {
            'keyword_score': self._calculate_keyword_score(news),
            'source_score': self._calculate_source_score(news),
            'content_score': self._calculate_content_score(news),
            'recency_score': self._calculate_recency_score(news),
            'total_score': self._calculate_score(news)
        }
