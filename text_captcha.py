# text_captcha.py
import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from PIL import Image, ImageTk
import string

class TextImageCaptcha:
    def __init__(self, parent_window, on_success_callback):
        self.parent = parent_window
        self.on_success = on_success_callback
        
        self.window = tk.Toplevel(parent_window)
        self.window.title("Введите текст с картинки")
        self.window.geometry("500x500")
        self.window.configure(bg='white')
        self.window.resizable(False, False)
        # Центрирование окна (самый простой способ)
        # Устанавливаем размер окна
        window_width = 500
        window_height = 500
    
        # Получаем размеры экрана
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
    
        # Вычисляем координаты для центрирования
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
    
        # Устанавливаем geometry с позиционированием
        self.window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        # Блокируем родительское окно
        self.window.transient(parent_window)
        self.window.grab_set()
        
        # Инициализация
        self.captcha_folder = "captcha_images"
        self.correct_text = ""
        self.load_captcha_data()
        
        # Цвета
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'light': '#ecf0f1'
        }
        
        # Сохраняем ссылку на изображение
        self.photo_ref = None
        
        # Создаем интерфейс
        self.create_interface()
    
    def load_captcha_data(self):
        """Загружает случайное изображение капчи"""
        try:
            # Получаем список всех изображений
            if not os.path.exists(self.captcha_folder):
                print(f"❌ Папка {self.captcha_folder} не существует!")
                return
            
            images = []
            for file in os.listdir(self.captcha_folder):
                if file.endswith('.png'):
                    images.append(file)
            
            if not images:
                print("❌ Нет изображений капчи!")
                return
            
            # Выбираем случайное изображение
            self.selected_image = random.choice(images)
            image_path = os.path.join(self.captcha_folder, self.selected_image)
            
            # Загружаем соответствующий текст
            text_file = self.selected_image.replace('.png', '.txt')
            text_path = os.path.join(self.captcha_folder, text_file)
            
            if os.path.exists(text_path):
                with open(text_path, 'r') as f:
                    self.correct_text = f.read().strip()
                    print(f"✅ Текст капчи: {self.correct_text}")
            else:
                # Если текстового файла нет, генерируем случайный
                self.correct_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                print(f"⚠️ Создан случайный текст: {self.correct_text}")
            
            # Загружаем изображение
            self.captcha_image = Image.open(image_path)
            return True
            
        except Exception as e:
            print(f"❌ Ошибка загрузки капчи: {e}")
            # Создаем заглушку
            self.correct_text = "TEST"
            self.captcha_image = None
            return False
    
    def create_interface(self):
        """Создание интерфейса текстовой капчи"""
        main_frame = tk.Frame(self.window, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Заголовок
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame,
                 text="🔒 ВВЕДИТЕ ТЕКСТ С КАРТИНКИ",
                 font=('Arial', 16, 'bold'),
                 fg=self.colors['primary'],
                 bg='white').pack(anchor='center')
        
        tk.Label(header_frame,
                 text="Введите текст который видите на изображении",
                 font=('Arial', 11),
                 fg='#7f8c8d',
                 bg='white').pack(anchor='center', pady=(5, 0))
        
        # Изображение капчи
        image_frame = tk.Frame(main_frame, bg='white')
        image_frame.pack(pady=20)
        
        if self.captcha_image:
            try:
                # Увеличиваем изображение для лучшей видимости
                img = self.captcha_image.resize((200, 200), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.photo_ref = self.photo  # Сохраняем ссылку
                
                image_label = tk.Label(image_frame, image=self.photo, bg='white')
                image_label.pack()
                
            except Exception as e:
                print(f"❌ Ошибка отображения изображения: {e}")
                self.show_fallback_image(image_frame)
        else:
            self.show_fallback_image(image_frame)
        
        # Поле для ввода текста
        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(input_frame,
                 text="Введите текст:",
                 font=('Arial', 11),
                 fg=self.colors['primary'],
                 bg='white').pack(anchor='w', pady=(0, 5))
        
        self.text_entry = ttk.Entry(input_frame, 
                                   font=('Arial', 14),
                                   justify='center')
        self.text_entry.pack(fill='x', pady=(0, 10))
        self.text_entry.focus()
        
        # Подсказка
        tk.Label(input_frame,
                 text="Введите текст заглавными буквами и цифрами как на картинке",
                 font=('Arial', 9),
                 fg='#95a5a6',
                 bg='white').pack(anchor='w')
        
        # Кнопки
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill='x')
        
        # Кнопка проверки
        check_btn = tk.Button(button_frame,
                             text="ПРОВЕРИТЬ",
                             font=('Arial', 12, 'bold'),
                             bg=self.colors['success'],
                             fg='white',
                             relief='flat',
                             cursor='hand2',
                             padx=30,
                             pady=12,
                             command=self.verify_captcha)
        check_btn.pack(fill='x', pady=(0, 10))
        
        # Кнопка обновления
        refresh_btn = tk.Button(button_frame,
                               text="🔄 ОБНОВИТЬ КАРТИНКУ",
                               font=('Arial', 10),
                               bg=self.colors['secondary'],
                               fg='white',
                               relief='flat',
                               cursor='hand2',
                               padx=30,
                               pady=10,
                               command=self.refresh_captcha)
        refresh_btn.pack(fill='x')
    
    def show_fallback_image(self, parent):
        """Показывает заглушку если изображение не загрузилось"""
        fallback_frame = tk.Frame(parent, bg='white', 
                                 highlightbackground='#bdc3c7',
                                 highlightthickness=2,
                                 width=200, height=200)
        fallback_frame.pack_propagate(False)
        fallback_frame.pack()
        
        tk.Label(fallback_frame,
                 text="КАПЧА",
                 font=('Arial', 24, 'bold'),
                 fg='#34495e',
                 bg='white').pack(expand=True)
        
        tk.Label(fallback_frame,
                 text="Текст: TEST",
                 font=('Arial', 16),
                 fg='#2c3e50',
                 bg='white').pack()
    
    def verify_captcha(self):
        """Проверка введенного текста"""
        user_input = self.text_entry.get().strip().upper()
        
        if not user_input:
            messagebox.showwarning("Внимание", "Введите текст с картинки!")
            self.text_entry.focus()
            return
        
        if user_input == self.correct_text:
            messagebox.showinfo("Успех", "✓ Капча пройдена успешно!")
            self.window.destroy()
            self.on_success()
        else:
            messagebox.showerror("Ошибка", 
                               f"❌ Неверный текст!\n"
                               f"Вы ввели: {user_input}\n"
                               f"Правильно: {self.correct_text}")
            self.text_entry.delete(0, tk.END)
            self.text_entry.focus()
    
    def refresh_captcha(self):
        """Обновление капчи"""
        self.load_captcha_data()
        
        # Обновляем изображение
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        # Нашли фрейм с изображением
                        for subchild in child.winfo_children():
                            if isinstance(subchild, tk.Label) and hasattr(subchild, 'image'):
                                # Обновляем изображение
                                if self.captcha_image:
                                    img = self.captcha_image.resize((200, 200), Image.Resampling.LANCZOS)
                                    new_photo = ImageTk.PhotoImage(img)
                                    self.photo_ref = new_photo  # Обновляем ссылку
                                    subchild.config(image=new_photo)
                                break
                        break
        
        # Очищаем поле ввода
        self.text_entry.delete(0, tk.END)
        self.text_entry.focus()


# Тестирование
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Тест текстовой капчи")
    root.geometry("300x200")
    
    def on_success():
        print("✅ Капча пройдена!")
        messagebox.showinfo("Тест", "Капча пройдена успешно!")
    
    def test_captcha():
        TextImageCaptcha(root, on_success)
    
    tk.Label(root, text="Тест текстовой капчи", font=('Arial', 14)).pack(pady=20)
    tk.Button(root, text="Запустить капчу", command=test_captcha, 
              font=('Arial', 12)).pack(pady=10)
    
    root.mainloop()