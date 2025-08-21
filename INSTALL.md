# Быстрая установка Between The Lines

## 1. Установка зависимостей

```bash
pip3 install -r requirements.txt
```

## 2. Настройка API ключей

Отредактируйте файл `.env`:

```env
OPENAI_API_KEY=your_actual_openai_api_key_here
NEWS_API_KEY=your_news_api_key_here  # Опционально
```

## 3. Тестирование системы

```bash
python3 test_system.py
```

## 4. Запуск анализа

```bash
python3 main.py
```

## 5. Автоматический запуск по расписанию

```bash
python3 scheduler.py
```

## Структура проекта

```
between_the_lines/
├── main.py                 # Главный оркестратор
├── config.py              # Конфигурация
├── news_gatherer.py       # Сбор новостей
├── scorer.py              # Оценка важности
├── ai_analyst.py          # AI анализ
├── content_generator.py   # Генерация контента
├── scheduler.py           # Планировщик
├── test_system.py         # Тестирование
├── requirements.txt       # Зависимости
├── .env                   # API ключи
├── README.md             # Полная документация
└── output/               # Выходные файлы (создается автоматически)
```

## Требования

- Python 3.7+
- OpenAI API ключ
- Интернет-соединение
