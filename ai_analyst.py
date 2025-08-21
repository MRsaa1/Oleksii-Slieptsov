#!/usr/bin/env python3
"""
Module 3: AI Analysis Core
Анализ скрытых смыслов и последствий новостей с помощью AI
"""

import json
import logging
from typing import Dict, Optional
import openai
from openai import OpenAI

from config import OPENAI_API_KEY, AI_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class AIAnalyst:
    """Класс для AI анализа новостей"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY не найден в конфигурации")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
    def analyze_news(self, news: Dict) -> Optional[Dict]:
        """Основной метод для анализа новости"""
        try:
            logger.info(f"🤖 Начинаем AI анализ новости: {news.get('title', 'Unknown')[:100]}...")
            
            # Формируем промт для анализа
            user_prompt = self._create_user_prompt(news)
            
            # Выполняем запрос к AI
            analysis_result = self._call_openai_api(user_prompt)
            
            if not analysis_result:
                logger.error("❌ Не удалось получить анализ от AI")
                return None
            
            # Парсим JSON ответ
            parsed_result = self._parse_ai_response(analysis_result)
            
            if not parsed_result:
                logger.error("❌ Не удалось распарсить ответ AI")
                return None
            
            logger.info("✅ AI анализ успешно завершен")
            return parsed_result
            
        except Exception as e:
            logger.error(f"❌ Ошибка при AI анализе: {str(e)}")
            return None
    
    def _create_user_prompt(self, news: Dict) -> str:
        """Создание промта для AI анализа"""
        title = news.get('title', '')
        description = news.get('description', '')
        link = news.get('link', '')
        source = news.get('source', '')
        date = news.get('date')
        
        # Форматируем дату
        date_str = ""
        if date:
            date_str = f"Дата: {date.strftime('%d.%m.%Y')}"
        
        user_prompt = f"""
Проанализируй эту новость:

Заголовок: {title}
Описание: {description}
Источник: {source}
{date_str}
Ссылка: {link}

Пожалуйста, проанализируй скрытый смысл этой новости и её потенциальные последствия.
"""
        
        return user_prompt.strip()
    
    def _call_openai_api(self, user_prompt: str) -> Optional[str]:
        """Вызов OpenAI API"""
        try:
            logger.info("📡 Отправка запроса к OpenAI API...")
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Используем GPT-4o для лучшего анализа
                messages=[
                    {"role": "system", "content": AI_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,  # Баланс между креативностью и точностью
                max_tokens=2000,  # Достаточно для детального анализа
                timeout=60  # Таймаут в секундах
            )
            
            if response.choices and len(response.choices) > 0:
                result = response.choices[0].message.content
                logger.info("✅ Получен ответ от OpenAI API")
                return result
            else:
                logger.error("❌ Пустой ответ от OpenAI API")
                return None
                
        except openai.RateLimitError:
            logger.error("❌ Превышен лимит запросов к OpenAI API")
            return None
        except openai.APIError as e:
            logger.error(f"❌ Ошибка OpenAI API: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка при вызове OpenAI API: {str(e)}")
            return None
    
    def _parse_ai_response(self, response: str) -> Optional[Dict]:
        """Парсинг JSON ответа от AI"""
        try:
            # Очищаем ответ от возможных лишних символов
            cleaned_response = self._clean_json_response(response)
            
            # Парсим JSON
            parsed_data = json.loads(cleaned_response)
            
            # Проверяем структуру ответа
            required_fields = ['hidden_meanings', 'market_impact', 'people_impact', 'sector_analysis', 'simple_analogy']
            
            for field in required_fields:
                if field not in parsed_data:
                    logger.warning(f"⚠️ Отсутствует обязательное поле: {field}")
                    parsed_data[field] = "Информация недоступна"
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Ошибка парсинга JSON: {str(e)}")
            logger.error(f"📄 Полученный ответ: {response[:500]}...")
            
            # Пытаемся извлечь информацию из текстового ответа
            return self._extract_info_from_text(response)
        except Exception as e:
            logger.error(f"❌ Ошибка при парсинге ответа AI: {str(e)}")
            return None
    
    def _clean_json_response(self, response: str) -> str:
        """Очистка JSON ответа от лишних символов"""
        # Ищем JSON в ответе
        start_marker = '{'
        end_marker = '}'
        
        start_idx = response.find(start_marker)
        if start_idx == -1:
            raise ValueError("JSON не найден в ответе")
        
        # Ищем закрывающую скобку с конца
        end_idx = response.rfind(end_marker)
        if end_idx == -1:
            raise ValueError("JSON не найден в ответе")
        
        json_str = response[start_idx:end_idx + 1]
        
        # Убираем возможные escape-символы
        json_str = json_str.replace('\\n', ' ').replace('\\t', ' ')
        
        return json_str
    
    def _extract_info_from_text(self, text: str) -> Dict:
        """Извлечение информации из текстового ответа, если JSON не удалось распарсить"""
        logger.info("🔄 Пытаемся извлечь информацию из текстового ответа...")
        
        # Простая эвристика для извлечения информации
        result = {
            'hidden_meanings': ["Анализ недоступен"],
            'market_impact': "Влияние на рынки не определено",
            'people_impact': "Влияние на людей не определено",
            'sector_analysis': "Анализ секторов не определен",
            'simple_analogy': "Аналогия не найдена"
        }
        
        # Ищем ключевые фразы в тексте
        text_lower = text.lower()
        
        # Ищем скрытые смыслы
        if 'скрытый' in text_lower or 'подтекст' in text_lower or 'на самом деле' in text_lower:
            # Извлекаем предложения с этими словами
            sentences = text.split('.')
            hidden_sentences = [s.strip() for s in sentences if any(word in s.lower() for word in ['скрытый', 'подтекст', 'на самом деле'])]
            if hidden_sentences:
                result['hidden_meanings'] = hidden_sentences[:3]
        
        # Ищем влияние на рынки
        if 'рынок' in text_lower or 'акции' in text_lower or 'облигации' in text_lower:
            market_sentences = [s.strip() for s in text.split('.') if any(word in s.lower() for word in ['рынок', 'акции', 'облигации', 'криптовалют'])]
            if market_sentences:
                result['market_impact'] = '. '.join(market_sentences[:2])
        
        # Ищем влияние на людей
        if 'люди' in text_lower or 'население' in text_lower or 'потребители' in text_lower:
            people_sentences = [s.strip() for s in text.split('.') if any(word in s.lower() for word in ['люди', 'население', 'потребители', 'граждане'])]
            if people_sentences:
                result['people_impact'] = '. '.join(people_sentences[:2])
        
        return result
