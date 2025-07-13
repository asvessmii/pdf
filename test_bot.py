#!/usr/bin/env python3
"""
Скрипт для тестирования Telegram бота Анны Герц
"""
import os
import sys
import requests
import time
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv('/app/backend/.env')

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def test_bot_info():
    """Тест получения информации о боте"""
    print("🤖 Тестирование информации о боте...")
    
    try:
        response = requests.get(f"{API_BASE}/getMe")
        data = response.json()
        
        if data.get("ok"):
            bot_info = data.get("result", {})
            print(f"✅ Бот активен!")
            print(f"   Имя: {bot_info.get('first_name')}")
            print(f"   Username: @{bot_info.get('username')}")
            print(f"   ID: {bot_info.get('id')}")
            return True
        else:
            print(f"❌ Ошибка получения информации о боте: {data}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения к Telegram API: {e}")
        return False

def test_api_endpoints():
    """Тест API endpoints нашего сервера"""
    print("\n🌐 Тестирование API endpoints...")
    
    endpoints = [
        ("/", "Корневой endpoint"),
        ("/api/bot/status", "Статус бота"),
        ("/api/health", "Проверка здоровья"),
        ("/api/users/count", "Количество пользователей"),
        ("/api/test-results/count", "Количество тестов")
    ]
    
    all_passed = True
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:8001{endpoint}")
            if response.status_code == 200:
                print(f"✅ {description}: OK")
                if endpoint == "/api/bot/status":
                    data = response.json()
                    print(f"   Статус: {data.get('status')}")
            else:
                print(f"❌ {description}: HTTP {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ {description}: Ошибка {e}")
            all_passed = False
    
    return all_passed

def test_files():
    """Тест наличия необходимых файлов"""
    print("\n📁 Тестирование файлов...")
    
    files = [
        ("/app/telegram_bot_images/anna_photo.jpg", "Фото Анны"),
        ("/app/telegram_bot_pdfs/Кето Анна Герц.pdf", "PDF рацион")
    ]
    
    all_passed = True
    
    for file_path, description in files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {description}: OK (размер: {size} байт)")
        else:
            print(f"❌ {description}: Файл не найден")
            all_passed = False
    
    return all_passed

def test_mongodb():
    """Тест подключения к MongoDB"""
    print("\n🗄️ Тестирование MongoDB...")
    
    try:
        from pymongo import MongoClient
        
        MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
        DB_NAME = os.getenv('DB_NAME', 'anna_hertz_bot')
        
        client = MongoClient(MONGO_URL)
        db = client[DB_NAME]
        
        # Проверяем подключение
        db.command('ping')
        print(f"✅ MongoDB подключение: OK")
        print(f"   База данных: {DB_NAME}")
        
        # Проверяем коллекции
        collections = db.list_collection_names()
        print(f"   Коллекции: {collections if collections else 'Пусто (норм для нового бота)'}")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB: Ошибка {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 ТЕСТИРОВАНИЕ TELEGRAM БОТА АННЫ ГЕРЦ")
    print("=" * 50)
    
    tests = [
        ("Информация о боте", test_bot_info),
        ("API endpoints", test_api_endpoints),
        ("Файлы ресурсов", test_files),
        ("MongoDB", test_mongodb)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed_tests += 1
        else:
            print(f"💥 Тест '{test_name}' не прошел!")
    
    print("\n" + "=" * 50)
    print(f"📊 РЕЗУЛЬТАТЫ: {passed_tests}/{total_tests} тестов прошли успешно")
    
    if passed_tests == total_tests:
        print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ! Бот готов к использованию!")
        print("\n🤖 Найдите бота в Telegram: @AnnaGertsBot")
        print("💬 Отправьте команду: /start")
    else:
        print("⚠️ Некоторые тесты не прошли. Проверьте логи.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)