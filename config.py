import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# API ключи
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')  # Опционально

# RSS источники новостей
RSS_SOURCES = {
    'reuters': 'https://feeds.reuters.com/reuters/businessNews',
    'bloomberg': 'https://feeds.bloomberg.com/markets/news.rss',
    'ft': 'https://www.ft.com/rss/home',
    'cnbc': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
    'cbr': 'https://www.cbr.ru/rss/RssNews',  # Банк России
    'sec': 'https://www.sec.gov/news/pressreleases.rss',  # SEC
    'ecb': 'https://www.ecb.europa.eu/press/pr/date/2024/html/index_include.en.rss'  # ECB
}

# Веб-сайты для парсинга
WEBSITE_SOURCES = [
    'https://www.cbr.ru/',
    'https://www.sec.gov/',
    'https://www.ecb.europa.eu/',
    'https://www.fed.gov/',
    'https://www.gov.uk/government/organisations/hm-treasury'
]

# Ключевые слова для определения важности новостей
IMPORTANT_KEYWORDS = [
    'регулирование', 'закон', 'постановление', 'ставка', 'налоги',
    'крупная сделка', 'санкции', 'отчетность', 'комплаенс', 'майнинг',
    'ETF', 'IPO', 'regulation', 'law', 'rate', 'tax', 'sanctions',
    'compliance', 'mining', 'merger', 'acquisition'
]

# Веса источников (чем выше, тем важнее)
SOURCE_WEIGHTS = {
    'cbr': 10,  # Банк России
    'sec': 10,  # SEC
    'ecb': 10,  # ECB
    'fed': 10,  # Federal Reserve
    'reuters': 8,
    'bloomberg': 8,
    'ft': 8,
    'cnbc': 6,
    'coindesk': 5
}

# Промт для AI анализа
AI_SYSTEM_PROMPT = """
Ты — ведущий финансовый аналитик с десятилетиями опыта. Твоя задача — прочитать новость и объяснить её скрытый смысл и потенциальные последствия так, как будто ты объясняешь умному, но не специалисту другу. Избегай жаргона. Будь проницательным, иногда немного саркастичным. Сфокусируйся на "Why" и "So what", а не на "What".

Ответь строго в следующем JSON-формате:
{
  "hidden_meanings": ["Список", "из 2-3", "главных неочевидных выводов"],
  "market_impact": "Краткий прогноз: как это повлияет на рынок акций, облигаций, криптовалют? (1-2 абзаца)",
  "people_impact": "Как это коснется обычных людей? (налоги, цены на товары, ипотека, пр.) (1-2 абзаца)",
  "sector_analysis": "Кто в выигрыше, а кто в проигрыше из секторов экономики?",
  "simple_analogy": "Объясни ситуацию через простую аналогию (например, 'Это как если бы ваш домовладелец...')"
}
"""

# Настройки для генерации контента
OUTPUT_DIR = 'output'
MAX_NEWS_PER_WEEK = 5
DAYS_BACK = 7

# Настройки логирования
LOG_LEVEL = 'INFO'
LOG_FILE = 'between_the_lines.log'
