import requests
import os
import subprocess
from vkbottle.user import User, Message
from vkbottle import VideoUploader
from config import TOKEN  # Импорт токена из config.py

user = User(token=TOKEN)  # Используем токен из config.py
video_uploader = VideoUploader(user.api)

CACHE_FOLDER = os.path.join(os.getcwd(), "cached_images")
VIDEO_PATH = os.path.join(os.getcwd(), "timelapse.mp4")

# Кэширование изображений
@user.on.message(text="!закэшируй <time1> <time2>")
async def cache_images_handler(message: Message, time1: str, time2: str):
    await message.answer("Процесс кеширования запущен✅")
    
    time1, time2 = int(time1), int(time2)
    os.makedirs(CACHE_FOLDER, exist_ok=True)

    for i in range(time1, time2 + 1000, 1000):
        url = f"https://xn----8sbwxcrbj4g.xn--80aa3a2f.xn--p1ai/mp/server/images/history/picture/{i}.png"
        filename = os.path.join(CACHE_FOLDER, f"{i}.png")
        r = requests.get(url, allow_redirects=True)

        if r.status_code == 200 and not os.path.exists(filename):
            with open(filename, 'wb') as file:
                file.write(r.content)

    await message.answer("Процесс кеширования завершён✅")

# Создание таймлапса с использованием FFmpeg
@user.on.message(text="!таймлапс <time3> <time4>")
async def art_handler(message: Message, time3: str, time4: str):
    await message.answer("Создание таймлапса запущено✅")

    time3, time4 = int(time3), int(time4)
    images = [img for img in os.listdir(CACHE_FOLDER)
              if img.endswith(".png") and time3 <= int(img.split('.')[0]) <= time4]
    images.sort(key=lambda x: int(x.split('.')[0]))

    if not images:
        await message.answer("Нет изображений для создания таймлапса.")
        return

    # Генерация списка файлов для FFmpeg
    file_list_path = os.path.join(CACHE_FOLDER, "images.txt")
    with open(file_list_path, "w") as file_list:
        for image in images:
            file_list.write(f"file '{os.path.join(CACHE_FOLDER, image)}'\n")

    # Генерация видео с помощью FFmpeg
    try:
        ffmpeg_command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", file_list_path,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            VIDEO_PATH
        ]
        subprocess.run(ffmpeg_command, check=True)

        # Проверяем, что видео действительно записалось
        if not os.path.exists(VIDEO_PATH) or os.path.getsize(VIDEO_PATH) == 0:
            await message.answer("Ошибка: видеофайл не был создан или пустой.")
            return

        # Загрузка видео в VK
        ready_video = await video_uploader.upload(file_source=VIDEO_PATH)
        await message.answer(f"Таймлапс {time3}-{time4} готов✅", attachment=ready_video)
    except subprocess.CalledProcessError as e:
        await message.answer(f"Ошибка при создании видео с помощью FFmpeg: {e}")
    except Exception as e:
        await message.answer(f"Ошибка при отправке видео: {e}")

user.run_forever()
