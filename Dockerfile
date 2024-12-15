# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт, на котором будет работать FastAPI
EXPOSE 7000

# Запускаем сервер FastAPI с помощью uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
