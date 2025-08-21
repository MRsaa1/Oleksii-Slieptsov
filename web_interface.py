#!/usr/bin/env python3
"""
Веб-интерфейс для Between The Lines на Replit
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Создаем папку для шаблонов
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

# Создаем HTML шаблон
html_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Between The Lines - Анализ новостей</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
            transition: transform 0.2s;
        }
        .button:hover {
            transform: translateY(-2px);
        }
        .button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .status {
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .status.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status.info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .files-list {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .file-item {
            padding: 10px;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .file-item:last-child {
            border-bottom: none;
        }
        .download-link {
            color: #667eea;
            text-decoration: none;
        }
        .download-link:hover {
            text-decoration: underline;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Between The Lines</h1>
        <p>Автоматический анализ финансово-экономических новостей</p>
    </div>
    
    <div class="container">
        <h2>🚀 Управление системой</h2>
        
        <div id="status"></div>
        
        <button class="button" onclick="runAnalysis()">🔍 Запустить анализ</button>
        <button class="button" onclick="refreshFiles()">📁 Обновить список файлов</button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Выполняется анализ новостей...</p>
        </div>
        
        <div class="files-list">
            <h3>📄 Созданные файлы</h3>
            <div id="filesList">
                <p>Нажмите "Обновить список файлов" для просмотра</p>
            </div>
        </div>
    </div>
    
    <script>
        function showStatus(message, type) {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = `<div class="status ${type}">${message}</div>`;
        }
        
        function showLoading(show) {
            const loading = document.getElementById('loading');
            loading.style.display = show ? 'block' : 'none';
        }
        
        async function runAnalysis() {
            showLoading(true);
            showStatus('Запуск анализа новостей...', 'info');
            
            try {
                const response = await fetch('/run_analysis', {
                    method: 'POST'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showStatus('✅ Анализ завершен успешно!', 'success');
                    refreshFiles();
                } else {
                    showStatus('❌ Ошибка: ' + result.error, 'error');
                }
            } catch (error) {
                showStatus('❌ Ошибка соединения: ' + error.message, 'error');
            } finally {
                showLoading(false);
            }
        }
        
        async function refreshFiles() {
            try {
                const response = await fetch('/list_files');
                const files = await response.json();
                
                const filesList = document.getElementById('filesList');
                
                if (files.length === 0) {
                    filesList.innerHTML = '<p>Файлы не найдены</p>';
                    return;
                }
                
                let html = '';
                files.forEach(file => {
                    const downloadUrl = `/download/${encodeURIComponent(file)}`;
                    html += `
                        <div class="file-item">
                            <span>�� ${file}</span>
                            <a href="${downloadUrl}" class="download-link" download>⬇️ Скачать</a>
                        </div>
                    `;
                });
                
                filesList.innerHTML = html;
            } catch (error) {
                showStatus('❌ Ошибка загрузки файлов: ' + error.message, 'error');
            }
        }
        
        // Загружаем файлы при загрузке страницы
        window.onload = function() {
            refreshFiles();
        };
    </script>
</body>
</html>
"""

# Сохраняем HTML шаблон
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/run_analysis', methods=['POST'])
def run_analysis():
    """Запуск анализа новостей"""
    try:
        logger.info("Запуск анализа через веб-интерфейс")
        
        # Проверяем наличие API ключа
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({
                'success': False,
                'error': 'OPENAI_API_KEY не настроен'
            })
        
        # Импортируем и запускаем систему
        from main import main as run_system
        success = run_system()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Анализ завершен успешно'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Ошибка при выполнении анализа'
            })
            
    except Exception as e:
        logger.error(f"Ошибка при запуске анализа: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/list_files')
def list_files():
    """Список созданных файлов"""
    try:
        output_dir = Path("output")
        if not output_dir.exists():
            return jsonify([])
        
        files = []
        for file_path in output_dir.glob("*.md"):
            files.append(file_path.name)
        
        # Сортируем по дате создания (новые сначала)
        files.sort(reverse=True)
        
        return jsonify(files)
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка файлов: {str(e)}")
        return jsonify([])

@app.route('/download/<filename>')
def download_file(filename):
    """Скачивание файла"""
    try:
        file_path = Path("output") / filename
        
        if not file_path.exists():
            return "Файл не найден", 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Ошибка при скачивании файла: {str(e)}")
        return "Ошибка скачивания", 500

@app.route('/health')
def health_check():
    """Проверка состояния системы"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'openai_key_configured': bool(os.getenv('OPENAI_API_KEY'))
    })

if __name__ == '__main__':
    # Получаем порт из переменных окружения Replit
    port = int(os.environ.get('PORT', 8080))
    
    logger.info(f"Запуск веб-интерфейса на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
