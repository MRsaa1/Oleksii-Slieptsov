#!/usr/bin/env python3
"""
Module 1: News Aggregator
Сбор новостей из разнообразных источников
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import time
import random

from config import RSS_SOURCES, WEBSITE_SOURCES, DAYS_BACK

logger = logging.getLogger(__name__)

class NewsGatherer:
    """Класс для сбора новостей из различных источников"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def gather_news(self) -> List[Dict]:
        """Основной метод для сбора всех новостей"""
        all_news = []
        
        try:
            # Собираем новости из RSS источников
            logger.info("📡 Сбор новостей из RSS источников...")
            rss_news = self._gather_rss_news()
            all_news.extend(rss_news)
            
            # Собираем новости с веб-сайтов
            logger.info("🌐 Сбор новостей с веб-сайтов...")
            website_news = self._gather_website_news()
            all_news.extend(website_news)
            
            # Фильтруем новости по дате
            cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)
            filtered_news = []
            
            for news in all_news:
                if news.get('date') and news['date'] >= cutoff_date:
                    filtered_news.append(news)
                elif not news.get('date'):  # Если дата не указана, включаем
                    filtered_news.append(news)
            
            logger.info(f"✅ Собрано {len(filtered_news)} новостей за последние {DAYS_BACK} дней")
            return filtered_news
            
        except Exception as e:
            logger.error(f"❌ Ошибка при сборе новостей: {str(e)}")
            return []
    
    def _gather_rss_news(self) -> List[Dict]:
        """Сбор новостей из RSS источников"""
        rss_news = []
        
        for source_name, rss_url in RSS_SOURCES.items():
            try:
                logger.info(f"📡 Обработка RSS: {source_name}")
                
                # Добавляем случайную задержку для избежания блокировки
                time.sleep(random.uniform(1, 3))
                
                feed = feedparser.parse(rss_url)
                
                if feed.bozo:
                    logger.warning(f"⚠️ Проблемы с RSS {source_name}: {feed.bozo_exception}")
                    continue
                
                for entry in feed.entries:
                    try:
                        # Парсим дату
                        date = self._parse_date(entry.get('published', ''))
                        
                        news_item = {
                            'title': entry.get('title', ''),
                            'description': entry.get('summary', ''),
                            'link': entry.get('link', ''),
                            'date': date,
                            'source': source_name,
                            'source_type': 'rss'
                        }
                        
                        # Добавляем только если есть заголовок и ссылка
                        if news_item['title'] and news_item['link']:
                            rss_news.append(news_item)
                            
                    except Exception as e:
                        logger.warning(f"⚠️ Ошибка обработки RSS записи {source_name}: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.error(f"❌ Ошибка при обработке RSS {source_name}: {str(e)}")
                continue
        
        logger.info(f"📡 Собрано {len(rss_news)} новостей из RSS источников")
        return rss_news
    
    def _gather_website_news(self) -> List[Dict]:
        """Сбор новостей с веб-сайтов"""
        website_news = []
        
        for website_url in WEBSITE_SOURCES:
            try:
                logger.info(f"🌐 Обработка сайта: {website_url}")
                
                # Добавляем случайную задержку
                time.sleep(random.uniform(2, 5))
                
                response = self.session.get(website_url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем новости на странице (базовая эвристика)
                news_links = self._extract_news_links(soup, website_url)
                
                for link in news_links[:10]:  # Ограничиваем количество
                    try:
                        news_item = self._extract_news_from_page(link)
                        if news_item:
                            website_news.append(news_item)
                            
                    except Exception as e:
                        logger.warning(f"⚠️ Ошибка обработки страницы {link}: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.error(f"❌ Ошибка при обработке сайта {website_url}: {str(e)}")
                continue
        
        logger.info(f"🌐 Собрано {len(website_news)} новостей с веб-сайтов")
        return website_news
    
    def _extract_news_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Извлечение ссылок на новости со страницы"""
        news_links = []
        
        # Ищем ссылки, которые могут быть новостями
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # Проверяем, похоже ли это на новость
            if self._looks_like_news_link(href, text):
                # Преобразуем относительные ссылки в абсолютные
                if href.startswith('/'):
                    full_url = base_url.rstrip('/') + href
                elif href.startswith('http'):
                    full_url = href
                else:
                    full_url = base_url.rstrip('/') + '/' + href
                
                news_links.append(full_url)
        
        return list(set(news_links))  # Убираем дубликаты
    
    def _looks_like_news_link(self, href: str, text: str) -> bool:
        """Проверка, похожа ли ссылка на новость"""
        news_keywords = ['news', 'press', 'release', 'announcement', 'новости', 'пресс', 'релиз']
        
        href_lower = href.lower()
        text_lower = text.lower()
        
        # Проверяем ключевые слова в ссылке и тексте
        for keyword in news_keywords:
            if keyword in href_lower or keyword in text_lower:
                return True
        
        # Проверяем длину текста (новости обычно имеют осмысленные заголовки)
        if len(text) > 20 and len(text) < 200:
            return True
        
        return False
    
    def _extract_news_from_page(self, url: str) -> Optional[Dict]:
        """Извлечение информации о новости со страницы"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Извлекаем заголовок
            title = self._extract_title(soup)
            if not title:
                return None
            
            # Извлекаем описание
            description = self._extract_description(soup)
            
            # Извлекаем дату
            date = self._extract_date(soup)
            
            # Определяем источник из URL
            source = self._extract_source_from_url(url)
            
            return {
                'title': title,
                'description': description,
                'link': url,
                'date': date,
                'source': source,
                'source_type': 'website'
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Ошибка извлечения новости с {url}: {str(e)}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Извлечение заголовка со страницы"""
        # Пробуем различные селекторы для заголовка
        title_selectors = [
            'h1',
            '.title',
            '.headline',
            '.article-title',
            'title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 10:
                    return title
        
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Извлечение описания со страницы"""
        # Пробуем различные селекторы для описания
        desc_selectors = [
            '.description',
            '.summary',
            '.excerpt',
            '.article-summary',
            'meta[name="description"]',
            'p'
        ]
        
        for selector in desc_selectors:
            if selector == 'meta[name="description"]':
                element = soup.select_one(selector)
                if element:
                    return element.get('content', '')
            else:
                element = soup.select_one(selector)
                if element:
                    desc = element.get_text(strip=True)
                    if desc and len(desc) > 50:
                        return desc[:500]  # Ограничиваем длину
        
        return ""
    
    def _extract_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Извлечение даты со страницы"""
        # Пробуем различные селекторы для даты
        date_selectors = [
            '.date',
            '.published',
            '.timestamp',
            'time',
            'meta[property="article:published_time"]'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                if selector == 'meta[property="article:published_time"]':
                    date_str = element.get('content', '')
                else:
                    date_str = element.get_text(strip=True)
                
                if date_str:
                    parsed_date = self._parse_date(date_str)
                    if parsed_date:
                        return parsed_date
        
        return None
    
    def _extract_source_from_url(self, url: str) -> str:
        """Извлечение названия источника из URL"""
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Убираем www. и домен верхнего уровня
        source = domain.replace('www.', '').split('.')[0]
        
        return source
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Парсинг даты из строки"""
        if not date_str:
            return None
        
        # Список форматов дат для парсинга
        date_formats = [
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
            '%d.%m.%Y',
            '%d/%m/%Y',
            '%B %d, %Y',
            '%b %d, %Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # Если не удалось распарсить, возвращаем None
        return None
