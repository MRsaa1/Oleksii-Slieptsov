#!/usr/bin/env python3
"""
Скрипт для создания репозитория на GitHub
"""

import requests
import json
import os

def create_github_repo():
    """Создание репозитория на GitHub"""
    
    # Настройки репозитория
    repo_name = "between-the-lines"
    description = "Автоматизированная система анализа финансово-экономических новостей"
    
    # Данные для создания репозитория
    repo_data = {
        "name": repo_name,
        "description": description,
        "private": False,
        "has_issues": True,
        "has_wiki": True,
        "has_downloads": True,
        "auto_init": False
    }
    
    print("🔧 Для создания репозитория на GitHub нужно:")
    print("1. Перейти на https://github.com/new")
    print("2. Создать репозиторий 'between-the-lines'")
    print("3. НЕ инициализировать с README (оставьте пустым)")
    print("4. Скопировать URL репозитория")
    print()
    print("После создания репозитория выполните:")
    print("git remote add origin https://github.com/MRsaa1/between-the-lines.git")
    print("git branch -M main")
    print("git push -u origin main")
    print()
    print("Или если используете SSH:")
    print("git remote add origin git@github.com:MRsaa1/between-the-lines.git")
    print("git branch -M main")
    print("git push -u origin main")

if __name__ == "__main__":
    create_github_repo()
