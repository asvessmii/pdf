# Telegram Bot "Анна Герц" - Полное руководство по запуску

## 📋 Описание проекта

Telegram бот для натуропата Анны Герц с системой тестирования и отправкой PDF рациона.

**Основные функции:**
- Приветствие с фото Анны (с задержкой 5 секунд между сообщениями)
- **РЕАЛЬНАЯ** проверка подписки на канал @anna_gertssss
- Тест из 5 вопросов с системой баллов
- 5 вариантов результатов (60%, 70%, 80%, 90%, 100%)
- Отправка PDF рациона
- Сохранение данных пользователей в MongoDB
- API для мониторинга

**Bot Username:** @AnnaGertsBot  
**Bot Name:** "Анна Герц Нутрициолог | Натуропат"  
**Channel:** @anna_gertssss

## 🛠 Требования к системе

### Минимальные требования:
- **OS:** Linux/Ubuntu (рекомендуется Ubuntu 20.04+)
- **Python:** 3.8+
- **RAM:** 2GB+
- **Disk:** 10GB+ свободного места
- **Network:** Стабильное интернет-соединение

## 🚀 ПОШАГОВАЯ УСТАНОВКА (ПРОВЕРЕННАЯ ИНСТРУКЦИЯ)

### ВАЖНО: Подготовка бота в Telegram

**ОБЯЗАТЕЛЬНО ПЕРЕД ЗАПУСКОМ:**
1. Убедитесь, что бот @AnnaGertsBot добавлен как **администратор** в канал @anna_gertssss
2. Без этого проверка подписки работать не будет!

### Шаг 1: Подготовка сервера

```bash
# Обновляем систему
apt update && apt upgrade -y

# Устанавливаем необходимые пакеты
apt install -y python3 python3-pip python3-venv git curl supervisor mongodb
```

### Шаг 2: Клонирование проекта

```bash
# Переходим в рабочую директорию (например /app или /opt)
cd /app

# Клонируем репозиторий
git clone https://github.com/asvessmii/pdf.git pdf_project

# Переключаемся на ветку с проектом
cd pdf_project
git checkout conflict_130725_2306
```

### Шаг 3: Копирование файлов проекта

```bash
# Возвращаемся в /app
cd /app

# Копируем backend файлы
cp -r pdf_project/backend/* backend/

# Создаем директории для ресурсов
mkdir -p telegram_bot_images telegram_bot_pdfs

# Копируем ресурсы из проекта
cp pdf_project/telegram_bot_images/* telegram_bot_images/
cp pdf_project/telegram_bot_pdfs/* telegram_bot_pdfs/

# Получаем ресурсы из main ветки
cd pdf_project
git checkout main
cd /app
cp "pdf_project/Кето Анна Герц.pdf" telegram_bot_pdfs/
cp pdf_project/photo_5443093706300320460_y.jpg telegram_bot_images/anna_photo.jpg
```

### Шаг 4: Настройка переменных окружения

```bash
# Создаем .env файл в backend директории
cat > backend/.env << 'EOF'
# MongoDB настройки
MONGO_URL=mongodb://localhost:27017
DB_NAME=anna_hertz_bot

# Telegram Bot Token
TELEGRAM_BOT_TOKEN=7550832092:AAHepUzpoxjrNjm2uB5xn1DafBrQ6WFQN7E
EOF
```

### Шаг 5: Установка Python зависимостей

```bash
# Переходим в backend директорию
cd /app/backend

# Устанавливаем зависимости
pip install -r requirements.txt
```

### Шаг 6: Проверка MongoDB

```bash
# Запускаем MongoDB (если не запущен)
systemctl start mongodb
systemctl enable mongodb

# Проверяем подключение
python3 -c "
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'anna_hertz_bot')

try:
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    db.command('ping')
    print('✅ MongoDB подключение успешно!')
except Exception as e:
    print(f'❌ Ошибка подключения к MongoDB: {e}')
"
```

### Шаг 7: Настройка Supervisor

```bash
# Создаем конфигурацию для supervisor
cat > /etc/supervisor/conf.d/telegram-bot.conf << 'EOF'
[program:telegram-bot]
command=python3 server.py
directory=/app/backend
user=root
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/telegram-bot.out.log
stderr_logfile=/var/log/supervisor/telegram-bot.err.log
environment=PATH="/root/.venv/bin"
EOF

# Останавливаем старый backend (если запущен)
supervisorctl stop backend || true

# Обновляем конфигурацию supervisor
supervisorctl reread
supervisorctl update

# Запускаем telegram-bot
supervisorctl start telegram-bot
```

### Шаг 8: Проверка запуска

```bash
# Проверяем статус
supervisorctl status telegram-bot

# Должно показать: telegram-bot RUNNING

# Проверяем логи
tail -f /var/log/supervisor/telegram-bot.out.log

# Ожидаемые строки в логах:
# INFO:__main__:Запуск FastAPI сервера...
# INFO:__main__:Telegram бот запущен в фоновом режиме
# INFO:telegram_bot:Запуск Telegram бота...
# INFO:telegram.ext.Application:Application started
```

### Шаг 9: Тестирование API

```bash
# Тест статуса бота
curl -s http://localhost:8001/api/bot/status | python3 -m json.tool

# Должен вернуть:
# {
#   "status": "running",
#   "message": "Telegram бот запущен"
# }

# Тест здоровья системы
curl -s http://localhost:8001/api/health | python3 -m json.tool

# Должен вернуть:
# {
#   "status": "healthy",
#   "mongodb": "connected", 
#   "telegram_bot": "running",
#   "message": "API is working properly"
# }
```

### Шаг 10: Финальная настройка в Telegram

**КРИТИЧЕСКИ ВАЖНО:**
1. Найдите канал @anna_gertssss в Telegram
2. Добавьте бота @AnnaGertsBot как **администратора** канала
3. Дайте ему права "Просматривать сообщения" (чтобы мог проверять подписку)

### Шаг 11: Тестирование бота

```bash
# Создаем тестовый скрипт
cat > /app/test_bot.py << 'EOF'
#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def test_bot():
    # Проверяем информацию о боте
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
        print(f"❌ Ошибка: {data}")
        return False

if __name__ == "__main__":
    test_bot()
EOF

# Запускаем тест
python3 /app/test_bot.py
```

## 🎯 Использование бота

1. **Найдите бота в Telegram**: @AnnaGertsBot
2. **Отправьте команду**: /start
3. **Проследите весь процесс**:
   - Получите приветствие с фото Анны
   - Через 5 секунд получите предложение подписаться
   - Подпишитесь на канал @anna_gertssss
   - Нажмите "Проверка подписки" (должна пройти успешно)
   - Пройдите тест из 5 вопросов
   - Получите персональный результат
   - Скачайте PDF рацион

## 🔧 Управление и мониторинг

### Команды управления:
```bash
# Статус
supervisorctl status telegram-bot

# Перезапуск
supervisorctl restart telegram-bot

# Остановка
supervisorctl stop telegram-bot

# Логи в реальном времени
tail -f /var/log/supervisor/telegram-bot.out.log

# Ошибки
tail -f /var/log/supervisor/telegram-bot.err.log
```

### API мониторинг:
```bash
# Статус бота
curl http://localhost:8001/api/bot/status

# Здоровье системы
curl http://localhost:8001/api/health

# Количество пользователей
curl http://localhost:8001/api/users/count

# Количество тестов
curl http://localhost:8001/api/test-results/count
```

## 🚨 Решение проблем

### Проблема: Бот не запускается
```bash
# Проверьте логи
tail -n 50 /var/log/supervisor/telegram-bot.err.log

# Проверьте токен
echo $TELEGRAM_BOT_TOKEN

# Проверьте интернет
ping api.telegram.org
```

### Проблема: Проверка подписки не работает
```bash
# Убедитесь, что бот добавлен как админ в канал @anna_gertssss
# Проверьте логи на ошибки проверки подписки
grep "Ошибка при проверке подписки" /var/log/supervisor/telegram-bot.out.log
```

### Проблема: MongoDB не подключается
```bash
# Проверьте статус MongoDB
systemctl status mongodb

# Тест подключения
mongo --eval "db.adminCommand('ping')"
```

### Проблема: PDF не отправляется
```bash
# Проверьте наличие файла
ls -la /app/telegram_bot_pdfs/

# Проверьте права
chmod 644 /app/telegram_bot_pdfs/*
```

## 🔄 Обновление проекта

```bash
# Остановка
supervisorctl stop telegram-bot

# Получение обновлений
cd /app/pdf_project
git pull origin conflict_130725_2306

# Копирование новых файлов
cp -r backend/* /app/backend/

# Установка новых зависимостей
cd /app/backend
pip install -r requirements.txt

# Запуск
supervisorctl start telegram-bot
```

## 📊 Статистика использования

Чтобы посмотреть статистику использования бота:

```bash
# API статистика
curl -s http://localhost:8001/api/users/count | python3 -m json.tool
curl -s http://localhost:8001/api/test-results/count | python3 -m json.tool

# Детальные данные
curl -s http://localhost:8001/api/users | python3 -m json.tool
curl -s http://localhost:8001/api/test-results | python3 -m json.tool
```

## ✅ Контрольный список готовности

- [ ] Сервер подготовлен и обновлен
- [ ] Проект склонирован и файлы скопированы
- [ ] Зависимости установлены
- [ ] .env файл настроен с правильным токеном
- [ ] MongoDB запущен и работает
- [ ] Supervisor настроен и бот запущен
- [ ] **БОТ ДОБАВЛЕН КАК АДМИН В КАНАЛ @anna_gertssss**
- [ ] API тесты проходят успешно
- [ ] Тест бота в Telegram выполнен полностью

## 🎉 После успешной установки

**Бот готов к использованию!**
- Username: @AnnaGertsBot
- Канал: @anna_gertssss
- Все функции работают
- Данные сохраняются в MongoDB
- API доступно для мониторинга

---

**Версия инструкции:** Проверена и обновлена по результатам реального развертывания