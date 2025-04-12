# Используем официальный Python-образ как основу
FROM python:3.12-slim

# Устанавливаем FFmpeg и другие зависимости
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Указываем команду запуска
CMD ["python", "main.py"]
