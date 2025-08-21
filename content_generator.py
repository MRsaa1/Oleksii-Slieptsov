#!/usr/bin/env python3
"""
Module 4: Content Generator
Создание красивого и читаемого дайджеста
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

from config import OUTPUT_DIR

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Класс для генерации итогового дайджеста"""
    
    def __init__(self):
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_digest(self, news: Dict, analysis: Dict) -> str:
        """Основной метод для генерации дайджеста"""
        try:
            logger.info("📝 Начинаем генерацию дайджеста...")
            
            # Создаем содержимое дайджеста
            digest_content = self._create_digest_content(news, analysis)
            
            # Генерируем имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"between_the_lines_{timestamp}.md"
            filepath = self.output_dir / filename
            
            # Сохраняем файл
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(digest_content)
            
            logger.info(f"✅ Дайджест сохранен: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации дайджеста: {str(e)}")
            return None
    
    def generate_telegram_digest(self, news: Dict, analysis: Dict) -> str:
        """Генерация компактной версии для Telegram"""
        try:
            logger.info("📱 Генерация Telegram версии...")
            
            # Создаем содержимое для Telegram
            telegram_content = self._create_telegram_content(news, analysis)
            
            # Генерируем имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"telegram_digest_{timestamp}.md"
            filepath = self.output_dir / filename
            
            # Сохраняем файл
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(telegram_content)
            
            logger.info(f"✅ Telegram версия сохранена: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации Telegram версии: {str(e)}")
            return None
    
    def _create_digest_content(self, news: Dict, analysis: Dict) -> str:
        """Создание содержимого дайджеста"""
        
        # Форматируем дату
        current_date = datetime.now().strftime("%d.%m.%Y")
        
        # Получаем данные из новости
        title = news.get('title', 'Заголовок недоступен')
        description = news.get('description', 'Описание недоступно')
        source = news.get('source', 'Неизвестный источник')
        date = news.get('date')
        
        date_str = ""
        if date:
            date_str = f" ({date.strftime('%d.%m.%Y')})"
        
        # Получаем данные из анализа
        hidden_meanings = analysis.get('hidden_meanings', ['Анализ недоступен'])
        market_impact = analysis.get('market_impact', 'Влияние на рынки не определено')
        people_impact = analysis.get('people_impact', 'Влияние на людей не определено')
        sector_analysis = analysis.get('sector_analysis', 'Анализ секторов не определен')
        simple_analogy = analysis.get('simple_analogy', 'Аналогия не найдена')
        
        # Создаем Markdown контент
        content = f"""# Between The Lines: Итоги недели

*Дайджест от {current_date}*

---

## 🏆 Главная новость: {title}

**Источник:** {source}{date_str}

### 🤔 Что случилось?

{description}

### 🕵️♂️ Что это на самом деле значит?

"""
        
        # Добавляем скрытые смыслы
        for i, meaning in enumerate(hidden_meanings, 1):
            content += f"• **{i}.** {meaning}\n"
        
        content += f"""
### 📈 Влияние на рынки

{market_impact}

### 👥 Что это значит для тебя?

{people_impact}

### 🏆 Проигравшие и победители

{sector_analysis}

### 🧠 Простая аналогия

> "{simple_analogy}"

---

Подготовлено @ReserveOne
"""
        
        return content
    
    def _create_telegram_content(self, news: Dict, analysis: Dict) -> str:
        """Создание компактной версии для Telegram"""
        
        # Получаем данные из новости
        title = news.get('title', 'Заголовок недоступен')
        description = news.get('description', 'Описание недоступно')
        
        # Получаем данные из анализа
        hidden_meanings = analysis.get('hidden_meanings', ['Анализ недоступен'])
        market_impact = analysis.get('market_impact', 'Влияние на рынки не определено')
        people_impact = analysis.get('people_impact', 'Влияние на людей не определено')
        sector_analysis = analysis.get('sector_analysis', 'Анализ секторов не определен')
        simple_analogy = analysis.get('simple_analogy', 'Аналогия не найдена')
        
        # Сокращаем описание для Telegram
        short_description = description[:200] + "..." if len(description) > 200 else description
        
        # Создаем компактный контент для Telegram
        content = f"""📊 **Between The Lines: Итоги недели**

🏆 **ГЛАВНАЯ НОВОСТЬ**
{title}

🤔 **ЧТО СЛУЧИЛОСЬ?**
{short_description}

🕵️♂️ **СКРЫТЫЙ СМЫСЛ**
"""
        
        # Добавляем только первые 2-3 скрытых смысла
        for i, meaning in enumerate(hidden_meanings[:3], 1):
            content += f"• {meaning}\n"
        
        content += f"""
📈 **ВЛИЯНИЕ НА РЫНКИ**
{market_impact[:300]}{"..." if len(market_impact) > 300 else ""}

👥 **ДЛЯ ТЕБЯ**
{people_impact[:300]}{"..." if len(people_impact) > 300 else ""}

🏆 **ПОБЕДИТЕЛИ И ПРОИГРАВШИЕ**
{sector_analysis[:200]}{"..." if len(sector_analysis) > 200 else ""}

🧠 **АНАЛОГИЯ**
"{simple_analogy[:150]}{"..." if len(simple_analogy) > 150 else ""}"

---
Подготовлено @ReserveOne
"""
        
        return content
    
    def generate_summary_report(self, all_scored_news: list) -> str:
        """Генерация краткого отчета по всем новостям"""
        try:
            logger.info("📊 Генерация сводного отчета...")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_summary_{timestamp}.md"
            filepath = self.output_dir / filename
            
            content = f"""# Сводка новостей недели

*Отчет от {datetime.now().strftime("%d.%m.%Y %H:%M")}*

## Топ новости по важности:

"""
            
            for i, news in enumerate(all_scored_news[:10], 1):
                title = news.get('title', 'Заголовок недоступен')
                source = news.get('source', 'Неизвестный источник')
                score = news.get('score', 0)
                
                content += f"""
### {i}. {title}

**Источник:** {source}  
**Оценка важности:** {score:.2f}/10

"""
            
            content += """
---

Подготовлено @ReserveOne
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Сводный отчет сохранен: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации сводного отчета: {str(e)}")
            return None
