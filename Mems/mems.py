import random
from moviepy.editor import *
from pathlib import Path
import os
import re

# --- Функция определения следующего номера файла ---
def ger(folder, prefix="output", ext=".mp4"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    files = os.listdir(folder)
    pattern = re.compile(rf"{re.escape(prefix)}(\d+){re.escape(ext)}")
    numbers = [int(m.group(1)) for f in files if (m := pattern.fullmatch(f))]

    next_number = max(numbers) + 1 if numbers else 1
    return next_number, os.path.join(folder, f"{prefix}{next_number}{ext}")

# --- Определяем корневую директорию ---
current_file = Path(__file__).resolve()
parent_dir = current_file.parent.parent

# --- Папки ---
bg_folder = parent_dir / "BG"
m_folder = parent_dir / "MEM"
output_folder = parent_dir / "OUTPUT"
music_folder = parent_dir / "music"

# --- Проверка наличия изображений ---
bg_images = [f for f in os.listdir(bg_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
m_images = [f for f in os.listdir(m_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

if not bg_images:
    raise FileNotFoundError("Нет фоновых изображений в папке BG.")
if len(m_images) < 2:
    raise ValueError("В папке M должно быть как минимум 2 изображения.")

# --- Выбор изображений ---
bg_path = bg_folder / random.choice(bg_images)
img1, img2 = random.sample(m_images, 2)
path1 = m_folder / img1
path2 = m_folder / img2

# --- Настройки ---
video_duration = 10  # секунд
fps = 3

# --- Создание фонового клипа ---
bg_clip = ImageClip(str(bg_path)).set_duration(video_duration)
w, h = bg_clip.size

# --- Создание двух картинок поверх ---
img_size = 256  # предполагается 256x256

# Позиции: одна сверху, другая ниже (по центру горизонтально)
y1 = h // 2 - img_size - 10  # верхняя картинка
y2 = h // 2 + 10             # нижняя картинка

clip1 = ImageClip(str(path1)).set_duration(video_duration).resize((img_size, img_size)).set_position(("center", y1))
clip2 = ImageClip(str(path2)).set_duration(video_duration).resize((img_size, img_size)).set_position(("center", y2))

# --- Наложение на фон ---
final = CompositeVideoClip([bg_clip, clip1, clip2])

# --- Музыка ---
music_path = music_folder / f"MUSIC{random.randint(1, 8)}.mp3"
audio = AudioFileClip(str(music_path)).subclip(0, video_duration)
final = final.set_audio(audio)

# --- Сохраняем ---
_, output_path = ger(str(output_folder))
final.write_videofile(output_path, fps=fps)
