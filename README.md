# 🇺🇦 MovnyiVartovyiBot

Telegram-бот, що стежить за дотриманням мовного правила в групі: приєднання можливе лише за згодою спілкуватись українською. Побудований на `aiogram` з `aiohttp` вебсервером — оптимізований для деплою на Render.

---

## 📦 Основні функції

- Блокує нових учасників одразу після входу
- Виводить привітальне повідомлення з кнопками
- Розблоковує лише тих, хто погоджується з правилом
- Видаляє тих, хто не згоден
- Має HTTP-сервер на `/` для підтримки Render Free Tier у активному стані

---

## 🚀 Швидкий старт

### 🔧 Варіант A: Локально (без Docker)

1. Клонуй репозиторій:

```
git clone https://github.com/your-username/MovnyiVartovyiBot.git
cd MovnyiVartovyiBot
```

2. Встанови залежності:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Створи ```.env``` файл:

```
BOT_TOKEN=your_token_here
```

4. Запусти бота:

```
python bot.py
```

### 🐳 Варіант B: Запуск через Docker

1. Побудуй Docker-образ:

```
docker build -t movnyi-vartovyi-bot .
```

2. Запусти контейнер, передавши токен бота:

```
docker run -d \
  --name vartovyi \
  -e BOT_TOKEN=123456789:ABCDEF_your_token_here \
  -p 8080:8080 \
  movnyi-vartovyi-bot
```

Контейнер відкриє порт 8080 (для keep-alive), а Telegram бот запуститься у режимі polling.

## ☁️ Деплой на Render

Проєкт готовий до розгортання як Web Service:

1. Завантаж проект у GitHub

2. На https://render.com створи новий Web Service

3. Обери:

```
Environment: Docker

Build Command: (необов’язково, Render сам використовує Dockerfile)

Start Command: (необов’язково, визначено у Dockerfile)

Environment Variable → додай: BOT_TOKEN
```

4. Після деплою — налаштуй UptimeRobot для пінгування кожні 5 хвилин, щоб уникнути «засинання»:

```https://your-bot-service.onrender.com/```


## 📄 Залежності
```aiogram``` — Telegram Bot фреймворк

```aiohttp``` — легкий HTTP-сервер

```python-dotenv``` — підвантаження змінних з .env


Усе встановлюється з:

```
pip install -r requirements.txt
```

## 🧠 Логіка

При вході нового користувача він автоматично блокується.

Йому надсилається привітальне повідомлення з кнопками "Так" / "Нєт".

✅ Якщо погоджується — бот знімає обмеження.

❌ Якщо ні — користувача видаляє з групи.


## 🔐 Безпека
Не заливай свій BOT_TOKEN до GitHub. Додай .env до .gitignore.


## 📝 Ліцензія
MIT License — використовуй, змінюй, поширюй з вказанням автора.


## 🤝 Співпраця
PR-и, покращення та багрепорти — дуже вітаються!

