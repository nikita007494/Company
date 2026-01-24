# update_captcha_images.py
import os
import random
import string
from PIL import Image, ImageDraw, ImageFont

def update_captcha_images():
    """Обновляет изображения капчи с сохранением текста"""
    captcha_folder = "captcha_images"
    
    # Создаем папку если её нет
    if not os.path.exists(captcha_folder):
        os.makedirs(captcha_folder)
        print(f"✅ Создана папка: {captcha_folder}")
    
    # Удаляем старые файлы
    for file in os.listdir(captcha_folder):
        file_path = os.path.join(captcha_folder, file)
        try:
            os.remove(file_path)
            print(f"🗑️ Удален: {file}")
        except:
            pass
    
    # Создаем новые изображения
    print("🖼️ Создаю новые изображения капчи...")
    
    for i in range(12):  # Создаем 12 разных капч
        # Генерируем текст (4 символа: буквы и цифры)
        text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        # Создаем изображение
        img = Image.new('RGB', (200, 100), color=(245, 245, 245))
        draw = ImageDraw.Draw(img)
        
        # Пробуем разные шрифты
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 40)
            except:
                font = ImageFont.load_default()
        
        # Рисуем текст с тенью для лучшей читаемости
        # Тень
        draw.text((53, 33), text, fill=(150, 150, 150), font=font)
        # Основной текст
        draw.text((50, 30), text, fill=(50, 50, 50), font=font)
        
        # Добавляем шумные линии
        for _ in range(8):
            x1 = random.randint(0, 199)
            y1 = random.randint(0, 99)
            x2 = random.randint(0, 199)
            y2 = random.randint(0, 99)
            draw.line([(x1, y1), (x2, y2)], 
                     fill=(random.randint(180, 220), 
                           random.randint(180, 220), 
                           random.randint(180, 220)), 
                     width=1)
        
        # Сохраняем изображение
        img_path = os.path.join(captcha_folder, f'captcha_{i}.png')
        img.save(img_path)
        
        # Сохраняем текст
        text_path = os.path.join(captcha_folder, f'captcha_{i}.txt')
        with open(text_path, 'w') as f:
            f.write(text)
        
        print(f"✅ Создано: captcha_{i}.png (текст: {text})")
    
    print("\n🎉 Обновление завершено!")
    print(f"📁 Папка: {os.path.abspath(captcha_folder)}")
    print(f"📊 Создано: 12 изображений с текстом")

if __name__ == "__main__":
    update_captcha_images()