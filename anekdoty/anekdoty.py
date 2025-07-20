import random
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import os
import re
import textwrap

# --- Функция определения следующего номера файла ---
def ger(folder, prefix="т", ext=".txt"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    files = os.listdir(folder)
    pattern = re.compile(rf"{re.escape(prefix)}(\d+){re.escape(ext)}")
    numbers = []

    for file in files:
        match = pattern.fullmatch(file)
        if match:
            numbers.append(int(match.group(1)))

    next_number = max(numbers) + 1 if numbers else 1
    next_filename = f"{prefix}{next_number}{ext}"
    full_path = os.path.join(folder, next_filename)
    return next_number, full_path

# --- Определяем корневую директорию ---
current_file = Path(__file__)
parent_dir = current_file.parent.parent

# --- Чтение анекдотов ---
with open("ee.txt", "r", encoding="utf-8") as a:
    t = a.read().split("---\n")

text = random.choice(t).strip()

# --- Выбор случайного фонового изображения ---
bg_folder = parent_dir / "BG"
bg_images = [f for f in os.listdir(bg_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

if not bg_images:
    raise FileNotFoundError(f"В папке {bg_folder} нет ни одного изображения!")

background_image = bg_folder / random.choice(bg_images)

# --- Настройки вывода ---
output_folder = parent_dir / "OUTPUT"
num, output_video = ger(str(output_folder), "output", ".mp4")

font_path = "C:/Windows/Fonts/arial.ttf"
font_size = 20
video_duration = 10
fps = 3

# --- Загружаем фото ---
clip = ImageClip(str(background_image)).set_duration(video_duration)
w, h = clip.size

# --- Текст в изображение ---
def wrap_text_by_pixel_width(text, font, draw, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def create_text_image(text, font_path, font_size, img_size, max_width_ratio=0.8):
    img = Image.new("RGBA", img_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)

    max_text_width = int(img_size[0] * max_width_ratio)

    lines = []
    for paragraph in text.split('\n'):
        lines.extend(wrap_text_by_pixel_width(paragraph, font, draw, max_text_width))

    line_heights = []
    text_width = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        text_width = max(text_width, w)
        line_heights.append(h)

    total_text_height = sum(line_heights) + (len(lines) - 1) * 10

    padding = 20
    bg_width = text_width + padding * 2
    bg_height = total_text_height + padding * 2
    bg_x = (img_size[0] - bg_width) // 2
    bg_y = img_size[1] - bg_height - 50

    draw.rectangle([bg_x, bg_y, bg_x + bg_width, bg_y + bg_height], fill=(0, 0, 0, 180))

    y = bg_y + padding
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (img_size[0] - line_width) // 2
        draw.text((x, y), line, font=font, fill="white")
        y += line_heights[i] + 10

    return np.array(img)

# --- Генерация текста ---
text_img = create_text_image(text, font_path, font_size, clip.size)
text_clip = ImageClip(text_img).set_duration(video_duration)

# --- Объединяем видео и текст ---
final = CompositeVideoClip([clip, text_clip])

# --- Подключаем случайную музыку ---
music_path = parent_dir / f"music/MUSIC{random.randint(1, 3)}.mp3"
audio_clip = AudioFileClip(str(music_path)).subclip(0, video_duration)
final = final.set_audio(audio_clip)

# --- Сохраняем видео ---
final.write_videofile(output_video, fps=fps)
