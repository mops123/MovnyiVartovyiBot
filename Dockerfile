# Вибираємо офіційний Python 3.11 образ
FROM python:3.11-slim

# Оновлюємо pip
RUN pip install --upgrade pip

# Копіюємо файл з вимогами (створи requirements.txt з потрібними бібліотеками)
COPY requirements.txt /app/requirements.txt

WORKDIR /app

# Встановлюємо залежності
RUN pip install -r requirements.txt

# Копіюємо весь код в контейнер
COPY . /app

# Запускаємо бота
CMD ["python", "bot.py"]
