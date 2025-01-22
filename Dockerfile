# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /bewise-ai
ENV PYTHONPATH=/bewise-ai

# Копируем requirements.txt в контейнер и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое папки app в контейнер
COPY . .

# Команда для запуска FastAPI приложения через entrypoint скрипт
CMD ["uvicorn", "app.main:app", "--reload", "--workers", "3", "--host", "0.0.0.0", "--port", "8000"]
