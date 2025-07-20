from PIL import Image
from pathlib import Path

# Папка с изображениями
folder = Path("BG")  # <-- укажи путь

# Целевой размер
target_size = (512, 768)

# Форматы изображений, которые обрабатываем
image_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif")

for img_path in folder.iterdir():
    if img_path.suffix.lower() in image_formats and img_path.is_file():
        with Image.open(img_path) as img:
            # Изменяем размер
            resized_img = img.resize(target_size, Image.Resampling.LANCZOS)

            # Сохраняем обратно (перезаписываем)
            resized_img.save(img_path)

        print(f"Обработано: {img_path.name}")
