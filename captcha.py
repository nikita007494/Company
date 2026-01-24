# captcha_fixed2.py
import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
import string

def ensure_captcha_folder():
    """Гарантирует создание папки и изображений капчи"""
    captcha_folder = "captcha_images"
    
    # Создаем папку если её нет
    if not os.path.exists(captcha_folder):
        print(f"Создаем папку: {captcha_folder}")
        os.makedirs(captcha_folder)
    
    # Проверяем есть ли изображения
    image_count = 0
    for file in os.listdir(captcha_folder):
        if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_count += 1
    
    # Если изображений меньше 4, генерируем новые
    if image_count < 4:
        print(f"Изображений найдено: {image_count}. Генерируем новые...")
        generate_captcha_images(captcha_folder)
    
    return captcha_folder

def generate_captcha_images(captcha_folder):
    """Генерация изображений для капчи"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        print("Генерация изображений капчи...")
        
        # Создаем 9 изображений с разными текстами
        for i in range(9):
            img = Image.new('RGB', (120, 120), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            
            # Генерируем случайный текст (2-3 символа)
            text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(2, 3)))
            
            # Используем системный шрифт или стандартный
            try:
                font = ImageFont.truetype("arial.ttf", 40)
                print(f"  Используем шрифт Arial для изображения {i}")
            except:
                try:
                    font = ImageFont.truetype("DejaVuSans.ttf", 40)
                    print(f"  Используем шрифт DejaVuSans для изображения {i}")
                except:
                    font = ImageFont.load_default()
                    print(f"  Используем стандартный шрифт для изображения {i}")
            
            # Рисуем текст
            d.text((30, 40), text, fill=(0, 0, 0), font=font)
            
            # Добавляем шум
            for _ in range(30):
                x = random.randint(0, 119)
                y = random.randint(0, 119)
                d.point((x, y), fill=(
                    random.randint(0, 255), 
                    random.randint(0, 255), 
                    random.randint(0, 255)
                ))
            
            # Добавляем линии
            for _ in range(3):
                x1 = random.randint(0, 119)
                y1 = random.randint(0, 119)
                x2 = random.randint(0, 119)
                y2 = random.randint(0, 119)
                d.line([(x1, y1), (x2, y2)], 
                      fill=(random.randint(100, 200), 
                            random.randint(100, 200), 
                            random.randint(100, 200)), 
                      width=2)
            
            # Сохраняем изображение
            img_path = os.path.join(captcha_folder, f'captcha_{i}.png')
            img.save(img_path)
            print(f"  Создано: {img_path}")
        
        print("✅ Генерация завершена!")
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка: PIL не установлен: {e}")
        print("Установите: pip install pillow")
        return False
    except Exception as e:
        print(f"❌ Ошибка при генерации изображений: {e}")
        return False

class ImageCaptcha:
    def __init__(self):
        # Гарантируем создание папки и изображений
        print("Инициализация ImageCaptcha...")
        self.captcha_folder = ensure_captcha_folder()
        
        self.captcha_images = []
        self.correct_image_index = None
        self.selected_images = []
        self.captcha_text = ""
        
        # Загружаем изображения
        self.load_captcha_images()
        
        print("✅ ImageCaptcha инициализирован")
    
    def load_captcha_images(self):
        """Загрузка изображений для капчи"""
        self.captcha_images = []
        
        try:
            from PIL import Image
            
            # Загружаем все изображения из папки
            for i in range(9):
                img_path = os.path.join(self.captcha_folder, f'captcha_{i}.png')
                if os.path.exists(img_path):
                    try:
                        img = Image.open(img_path)
                        self.captcha_images.append(img)
                        print(f"  Загружено: captcha_{i}.png")
                    except Exception as e:
                        print(f"  Ошибка загрузки {img_path}: {e}")
                else:
                    print(f"  Файл не найден: {img_path}")
            
            if not self.captcha_images:
                print("❌ Не удалось загрузить изображения капчи")
                # Пробуем сгенерировать заново
                if generate_captcha_images(self.captcha_folder):
                    self.load_captcha_images()
                
        except ImportError:
            print("❌ PIL не установлен, изображения недоступны")
        except Exception as e:
            print(f"❌ Ошибка при загрузке изображений: {e}")
    
    def generate_captcha(self):
        """Генерация новой капчи"""
        if not self.captcha_images:
            print("⚠️ Нет изображений для капчи")
            # Создаем заглушки
            return list(range(4)), "Выберите любое изображение"
        
        # Выбираем 4 случайных изображения
        available_indices = list(range(len(self.captcha_images)))
        selected_indices = random.sample(available_indices, min(4, len(available_indices)))
        
        # Если изображений меньше 4, добавляем дубликаты
        while len(selected_indices) < 4:
            selected_indices.append(random.choice(available_indices))
        
        # Выбираем одно изображение как правильное
        self.correct_image_index = random.choice(selected_indices)
        
        # Определяем текст на правильном изображении
        self.captcha_text = f"Выберите изображение #{self.correct_image_index + 1}"
        
        print(f"Сгенерирована капча: правильное изображение #{self.correct_image_index}")
        return selected_indices, self.captcha_text
    
    def check_captcha(self, selected_index):
        """Проверка выбранного изображения"""
        result = selected_index == self.correct_image_index
        print(f"Проверка капчи: выбрано #{selected_index}, правильно #{self.correct_image_index} -> {'✓' if result else '✗'}")
        return result


class CaptchaWindow:
    def __init__(self, parent_window, on_success_callback):
        print("Создание CaptchaWindow...")
        self.parent_window = parent_window
        self.on_success_callback = on_success_callback
        self.captcha = ImageCaptcha()  # Это создаст папку и изображения!
        
        self.window = tk.Toplevel(parent_window)
        self.window.title("Подтверждение капчи")
        self.window.geometry("550x600")
        self.window.configure(bg='white')
        self.window.resizable(False, False)
        
        # Блокируем родительское окно
        self.window.transient(parent_window)
        self.window.grab_set()
        
        # Генерируем новую капчу
        self.selected_indices, self.captcha_text = self.captcha.generate_captcha()
        self.selected_index = None
        
        # Сохраняем ссылки на изображения
        self.photo_references = []
        
        # Создаем интерфейс
        self.create_interface()
        
        print("✅ CaptchaWindow создан")
    
    def create_interface(self):
        """Создание интерфейса капчи"""
        # Главный контейнер
        main_frame = tk.Frame(self.window, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Заголовок
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame,
                 text="🔒 ПОДТВЕРЖДЕНИЕ",
                 font=('Arial', 16, 'bold'),
                 fg='#2c3e50',
                 bg='white').pack(anchor='w')
        
        tk.Label(header_frame,
                 text="Выберите указанное изображение",
                 font=('Arial', 11),
                 fg='#7f8c8d',
                 bg='white').pack(anchor='w', pady=(5, 0))
        
        # Инструкция
        instruction_frame = tk.Frame(main_frame, bg='white', pady=10)
        instruction_frame.pack(fill='x')
        
        tk.Label(instruction_frame,
                 text="Выберите изображение:",
                 font=('Arial', 11, 'bold'),
                 fg='#2c3e50',
                 bg='white').pack(anchor='w')
        
        # Текст капчи
        self.captcha_label = tk.Label(instruction_frame,
                                      text=self.captcha_text,
                                      font=('Arial', 14, 'bold'),
                                      fg='#27ae60',
                                      bg='white')
        self.captcha_label.pack(anchor='w', pady=(5, 0))
        
        # Изображения капчи
        self.create_captcha_images(main_frame)
        
        # Кнопки
        self.create_buttons(main_frame)
    
    def create_captcha_images(self, parent):
        """Создание сетки с изображениями капчи"""
        try:
            from PIL import ImageTk
            
            images_frame = tk.Frame(parent, bg='white')
            images_frame.pack(fill='both', expand=True, pady=20)
            
            # Сетка 2x2
            self.image_buttons = []
            
            for i in range(4):
                row = i // 2
                col = i % 2
                
                frame = tk.Frame(images_frame, bg='white', highlightbackground='#ecf0f1', 
                               highlightthickness=2, relief='ridge')
                frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
                
                # Загружаем изображение
                img_index = self.selected_indices[i]
                
                try:
                    if img_index < len(self.captcha.captcha_images):
                        img = self.captcha.captcha_images[img_index]
                        img = img.resize((160, 160))
                        
                        # Конвертируем в PhotoImage
                        photo = ImageTk.PhotoImage(img)
                        self.photo_references.append(photo)  # ВАЖНО: сохраняем ссылку!
                        
                        # Создаем кнопку с изображением
                        btn = tk.Button(frame, image=photo, bg='white', relief='flat',
                                      cursor='hand2', command=lambda idx=i: self.select_image(idx))
                        btn.pack(fill='both', expand=True, padx=5, pady=5)
                        
                        # Индикатор выбора
                        selection_indicator = tk.Label(frame, text="", bg='white', 
                                                      font=('Arial', 16, 'bold'))
                        selection_indicator.pack()
                        
                        self.image_buttons.append({
                            'button': btn,
                            'indicator': selection_indicator,
                            'selected': False,
                            'index': img_index
                        })
                        print(f"  Создана кнопка для изображения #{img_index}")
                    else:
                        print(f"  ⚠️ Индекс {img_index} вне диапазона")
                        # Создаем заглушку
                        self.create_fallback_button(frame, i)
                except Exception as e:
                    print(f"  ❌ Ошибка при создании кнопки {i}: {e}")
                    self.create_fallback_button(frame, i)
            
            # Настраиваем веса строк и столбцов
            images_frame.grid_rowconfigure(0, weight=1)
            images_frame.grid_rowconfigure(1, weight=1)
            images_frame.grid_columnconfigure(0, weight=1)
            images_frame.grid_columnconfigure(1, weight=1)
            
        except ImportError:
            print("❌ PIL не установлен, создаем текстовые кнопки")
            self.create_text_buttons(parent)
    
    def create_fallback_button(self, frame, index):
        """Создает текстовую кнопку если изображение не загрузилось"""
        btn = tk.Button(frame, text=f"Изображение {index+1}", 
                       font=('Arial', 14), bg='#ecf0f1', fg='#2c3e50',
                       relief='raised', cursor='hand2',
                       command=lambda idx=index: self.select_image(idx),
                       width=15, height=6)
        btn.pack(fill='both', expand=True, padx=5, pady=5)
        
        selection_indicator = tk.Label(frame, text="", bg='white', 
                                      font=('Arial', 16, 'bold'))
        selection_indicator.pack()
        
        self.image_buttons.append({
            'button': btn,
            'indicator': selection_indicator,
            'selected': False,
            'index': index
        })
    
    def create_text_buttons(self, parent):
        """Создает текстовые кнопки если PIL не установлен"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='both', expand=True, pady=20)
        
        self.image_buttons = []
        
        for i in range(4):
            btn = tk.Button(frame, text=f"Вариант {i+1}", 
                           font=('Arial', 14), bg='#3498db', fg='white',
                           relief='raised', cursor='hand2',
                           command=lambda idx=i: self.select_image(idx),
                           width=20, height=3)
            btn.pack(pady=10)
            
            selection_indicator = tk.Label(frame, text="", bg='white', 
                                          font=('Arial', 16, 'bold'))
            selection_indicator.pack()
            
            self.image_buttons.append({
                'button': btn,
                'indicator': selection_indicator,
                'selected': False,
                'index': i
            })
    
    def select_image(self, button_index):
        """Обработка выбора изображения"""
        print(f"Выбрано изображение #{button_index}")
        
        # Сбрасываем все выделения
        for btn_info in self.image_buttons:
            btn_info['selected'] = False
            btn_info['indicator'].config(text="")
            btn_info['button'].config(bg='white' if hasattr(btn_info['button'], 'cget') and btn_info['button'].cget('bg') != '#3498db' else '#3498db')
        
        # Выделяем выбранное
        self.image_buttons[button_index]['selected'] = True
        self.image_buttons[button_index]['indicator'].config(text="✓", fg='#27ae60')
        
        # Меняем цвет кнопки если это текстовая кнопка
        if self.image_buttons[button_index]['button'].cget('text').startswith('Вариант'):
            self.image_buttons[button_index]['button'].config(bg='#2ecc71')
        
        # Сохраняем индекс выбранного изображения
        self.selected_index = self.selected_indices[button_index]
    
    def create_buttons(self, parent):
        """Создание кнопок"""
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Кнопка подтверждения
        self.confirm_btn = tk.Button(button_frame,
                                    text="ПОДТВЕРДИТЬ",
                                    font=('Arial', 12, 'bold'),
                                    bg='#27ae60',
                                    fg='white',
                                    relief='flat',
                                    cursor='hand2',
                                    padx=30,
                                    pady=12,
                                    command=self.verify_captcha)
        self.confirm_btn.pack(fill='x', pady=(0, 10))
        
        # Кнопка обновления капчи
        self.refresh_btn = tk.Button(button_frame,
                                    text="🔄 ОБНОВИТЬ КАПЧУ",
                                    font=('Arial', 10),
                                    bg='#3498db',
                                    fg='white',
                                    relief='flat',
                                    cursor='hand2',
                                    padx=30,
                                    pady=10,
                                    command=self.refresh_captcha)
        self.refresh_btn.pack(fill='x')
    
    def verify_captcha(self):
        """Проверка капчи"""
        # Проверяем, выбрано ли изображение
        selected = False
        for btn_info in self.image_buttons:
            if btn_info['selected']:
                selected = True
                break
        
        if not selected:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите изображение")
            return
        
        # Проверяем правильность выбора
        if self.captcha.check_captcha(self.selected_index):
            messagebox.showinfo("Успех", "✓ Капча пройдена успешно!")
            self.window.destroy()
            self.on_success_callback()
        else:
            messagebox.showerror("Ошибка", "✗ Выбрано неправильное изображение. Попробуйте снова.")
            self.refresh_captcha()
    
    def refresh_captcha(self):
        """Обновление капчи"""
        print("Обновление капчи...")
        
        # Генерируем новую капчу
        self.selected_indices, self.captcha_text = self.captcha.generate_captcha()
        
        # Обновляем текст
        self.captcha_label.config(text=self.captcha_text)
        
        # Сбрасываем выделения
        self.selected_index = None
        for btn_info in self.image_buttons:
            btn_info['selected'] = False
            btn_info['indicator'].config(text="")
            # Возвращаем исходный цвет
            if btn_info['button'].cget('text').startswith('Вариант'):
                btn_info['button'].config(bg='#3498db')
            else:
                btn_info['button'].config(bg='white')


# Тестирование
if __name__ == "__main__":
    print("=" * 50)
    print("ТЕСТ КАПЧИ")
    print("=" * 50)
    
    root = tk.Tk()
    root.title("Тест капчи")
    root.geometry("400x300")
    
    def on_captcha_success():
        print("✅ Капча пройдена успешно!")
        messagebox.showinfo("Успех", "Капча пройдена!")
        root.destroy()
    
    def test_captcha():
        print("\nЗапуск теста капчи...")
        CaptchaWindow(root, on_captcha_success)
    
    tk.Label(root, text="Тестирование системы капчи", 
             font=('Arial', 14, 'bold')).pack(pady=20)
    
    tk.Button(root, text="Запустить капчу", 
              command=test_captcha, font=('Arial', 12),
              bg='#3498db', fg='white', padx=20, pady=10).pack(pady=10)
    
    tk.Button(root, text="Проверить папку captcha_images", 
              command=lambda: print(f"Папка существует: {os.path.exists('captcha_images')}"),
              font=('Arial', 10)).pack(pady=5)
    
    tk.Button(root, text="Выход", command=root.quit).pack(pady=20)
    
    root.mainloop()