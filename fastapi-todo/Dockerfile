FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Создаём нового пользователя
RUN useradd -m celeryuser

# Устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install celery[redis]

# Копируем весь код приложения
COPY ./app ./app

# Даем привилегии пользователю celeryuser на директорию
RUN chown -R celeryuser:celeryuser /app

# Переключаемся на нового пользователя
USER celeryuser

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем приложение через Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
