FROM python:3.11-slim
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "bot.py"]
