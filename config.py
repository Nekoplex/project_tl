import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Переменные окружения
TOKEN = os.getenv('VK_GROUP_TOKEN')  # Токен вашего VK-бота
