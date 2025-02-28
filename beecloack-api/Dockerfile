# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY . .

# Проверяем структуру проекта (для отладки)
RUN ls -la

# Открываем порт 8000
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:8000", "wsgi:app"]
