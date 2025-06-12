from celery import Celery

# Настройка Celery с использованием Redis как брокера
app = Celery('myapp', broker='redis://redis:6379/0')  # Используем имя контейнера redis, а не localhost

@app.task
def add(x, y):
    return x + y
