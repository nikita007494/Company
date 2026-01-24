import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import json
import os
import pyodbc
from datetime import datetime

class RegistrationForm:
    def __init__(self, parent_window=None):
        self.parent_window = parent_window  # Ссылка на окно авторизации
        
        self.window = tk.Toplevel() if parent_window else tk.Tk()
        self.window.title("Торговая платформа - Регистрация")
        self.window.geometry("500x650")
        self.window.configure(bg='white')
        self.window.resizable(False, False)
        
        # Блокируем родительское окно
        if parent_window:
            self.window.transient(parent_window)
            self.window.grab_set()
        
        # Цветовая схема
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'accent': '#e74c3c',
            'success': '#27ae60',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e',
            'gray': '#95a5a6'
        }
        
        # Центрируем окно
        self.center_window()
        
        # Создаем интерфейс
        self.create_interface()
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_interface(self):
        """Создание интерфейса регистрации"""
        # Главный контейнер
        main_frame = tk.Frame(self.window, bg='white', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Заголовок
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame,
                 text="📝 РЕГИСТРАЦИЯ",
                 font=('Segoe UI', 18, 'bold'),
                 fg=self.colors['primary'],
                 bg='white').pack(anchor='w')
        
        tk.Label(header_frame,
                 text="Создайте новый аккаунт",
                 font=('Segoe UI', 11),
                 fg=self.colors['gray'],
                 bg='white').pack(anchor='w', pady=(5, 0))
        
        # Поля для регистрации
        self.create_registration_fields(main_frame)
        
        # Кнопки
        self.create_registration_buttons(main_frame)
    
    def create_registration_fields(self, parent):
        """Создание полей для регистрации"""
        fields_frame = tk.Frame(parent, bg='white')
        fields_frame.pack(fill='both', expand=True)
        
        # ФИО
        tk.Label(fields_frame,
                 text="ФИО*",
                 font=('Segoe UI', 10, 'bold'),
                 fg=self.colors['dark'],
                 bg='white').pack(anchor='w', pady=(10, 5))
        
        self.fullname_entry = ttk.Entry(fields_frame, font=('Segoe UI', 11))
        self.fullname_entry.pack(fill='x', pady=(0, 15))
        
        # Email
        tk.Label(fields_frame,
                 text="Email*",
                 font=('Segoe UI', 10, 'bold'),
                 fg=self.colors['dark'],
                 bg='white').pack(anchor='w', pady=(5, 5))
        
        self.email_entry = ttk.Entry(fields_frame, font=('Segoe UI', 11))
        self.email_entry.pack(fill='x', pady=(0, 15))
        
        # Имя пользователя
        tk.Label(fields_frame,
                 text="Имя пользователя*",
                 font=('Segoe UI', 10, 'bold'),
                 fg=self.colors['dark'],
                 bg='white').pack(anchor='w', pady=(5, 5))
        
        self.username_entry = ttk.Entry(fields_frame, font=('Segoe UI', 11))
        self.username_entry.pack(fill='x', pady=(0, 15))
        
        # Пароль
        tk.Label(fields_frame,
                 text="Пароль*",
                 font=('Segoe UI', 10, 'bold'),
                 fg=self.colors['dark'],
                 bg='white').pack(anchor='w', pady=(5, 5))
        
        password_frame = tk.Frame(fields_frame, bg='white')
        password_frame.pack(fill='x', pady=(0, 15))
        
        self.password_entry = ttk.Entry(password_frame, font=('Segoe UI', 11), show='•')
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Кнопка показать/скрыть пароль
        self.show_pass_btn = tk.Button(password_frame,
                                      text="👁",
                                      font=('Segoe UI', 10),
                                      bg='white',
                                      fg=self.colors['gray'],
                                      relief='flat',
                                      cursor='hand2',
                                      command=self.toggle_password)
        self.show_pass_btn.pack(side='right')
        
        # Подтверждение пароля
        tk.Label(fields_frame,
                 text="Подтвердите пароль*",
                 font=('Segoe UI', 10, 'bold'),
                 fg=self.colors['dark'],
                 bg='white').pack(anchor='w', pady=(5, 5))
        
        self.confirm_password_entry = ttk.Entry(fields_frame, font=('Segoe UI', 11), show='•')
        self.confirm_password_entry.pack(fill='x', pady=(0, 15))
        
        # Роль
        tk.Label(fields_frame,
                 text="Выберите роль*",
                 font=('Segoe UI', 10, 'bold'),
                 fg=self.colors['dark'],
                 bg='white').pack(anchor='w', pady=(5, 5))
        
        self.role_var = tk.StringVar(value='candidate')
        role_frame = tk.Frame(fields_frame, bg='white')
        role_frame.pack(fill='x', pady=(0, 10))
        
        roles = [
            ('👤 Кандидат', 'candidate'),
            ('🛒 Потребитель', 'consumer'), 
            ('📊 Агент', 'agent'),
            ('🚚 Логист', 'logistic')
        ]
        
        for text, value in roles:
            rb = tk.Radiobutton(role_frame,
                               text=text,
                               variable=self.role_var,
                               value=value,
                               font=('Segoe UI', 10),
                               fg=self.colors['dark'],
                               bg='white',
                               selectcolor='white',
                               activebackground='white')
            rb.pack(side='left', padx=(0, 15))
    
    def toggle_password(self):
        """Показать/скрыть пароль"""
        if self.password_entry.cget('show') == '•':
            self.password_entry.config(show='')
            self.confirm_password_entry.config(show='')
            self.show_pass_btn.config(text='🔒')
        else:
            self.password_entry.config(show='•')
            self.confirm_password_entry.config(show='•')
            self.show_pass_btn.config(text='👁')
    
    def create_registration_buttons(self, parent):
        """Создание кнопок регистрации"""
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill='x', pady=(20, 0))
        
        # Кнопка регистрации
        self.register_btn = tk.Button(button_frame,
                                     text="ЗАРЕГИСТРИРОВАТЬСЯ",
                                     font=('Segoe UI', 11, 'bold'),
                                     bg=self.colors['success'],
                                     fg='white',
                                     relief='flat',
                                     cursor='hand2',
                                     padx=30,
                                     pady=12,
                                     command=self.register_user)
        self.register_btn.pack(fill='x', pady=(0, 10))
        
        # Кнопка отмены
        self.cancel_btn = tk.Button(button_frame,
                                   text="ОТМЕНА",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=self.colors['accent'],
                                   fg='white',
                                   relief='flat',
                                   cursor='hand2',
                                   padx=30,
                                   pady=12,
                                   command=self.cancel_registration)
        self.cancel_btn.pack(fill='x')
    
    def create_db_connection(self):
        """Создание подключения к базе данных"""
        try:
            # Параметры подключения
            server = 'DESKTOP-HKB5J94'
            database = 'TradingPlatformDB'
            
            # Строка подключения
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
            
            # Создаем подключение
            connection = pyodbc.connect(connection_string)
            return connection
        except Exception as e:
            print(f"❌ Ошибка подключения к БД: {e}")
            return None
    
    def hash_password(self, password):
        """Хеширование пароля"""
        # Используем SHA-256 для хеширования
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_user_exists(self, connection, username, email):
        """Проверка существования пользователя"""
        try:
            cursor = connection.cursor()
            
            # Проверяем по username и email
            query = """
            SELECT COUNT(*) FROM Users 
            WHERE username = ? OR email = ?
            """
            cursor.execute(query, (username, email))
            count = cursor.fetchone()[0]
            
            return count > 0
        except Exception as e:
            print(f"❌ Ошибка при проверке пользователя: {e}")
            return True  # Если ошибка, считаем что пользователь существует
    
    def register_user_in_db(self, connection, username, password, full_name, email, role):
        """Регистрация пользователя в базе данных - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        try:
            cursor = connection.cursor()
            
            # Хешируем пароль
            hashed_password = self.hash_password(password)
            
            # Вставляем нового пользователя (используем правильные имена столбцов)
            query = """
            INSERT INTO Users (username, password_hash, full_name, email, role, created_at, is_active)
            VALUES (?, ?, ?, ?, ?, GETDATE(), 1)
            """
            
            cursor.execute(query, (username, hashed_password, full_name, email, role))
            connection.commit()
            
            # Получаем ID нового пользователя
            cursor.execute("SELECT SCOPE_IDENTITY()")
            user_id = cursor.fetchone()[0]
            
            return True, "Пользователь успешно зарегистрирован", user_id
        except Exception as e:
            print(f"❌ Ошибка при регистрации пользователя: {e}")
            connection.rollback()  # Откатываем изменения при ошибке
            return False, f"Ошибка при регистрации: {str(e)}", None
    
    def register_user(self):
        """Обработка регистрации пользователя"""
        # Получаем данные из полей
        fullname = self.fullname_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        role = self.role_var.get()
        
        print(f"\n=== ДЕБАГ РЕГИСТРАЦИИ ===")
        print(f"ФИО: '{fullname}'")
        print(f"Email: '{email}'")
        print(f"Username: '{username}'")
        print(f"Password: {'*' * len(password)}")
        print(f"Confirm: {'*' * len(confirm_password)}")
        print(f"Role: '{role}'")
        
        # Валидация
        errors = []
        
        if not fullname:
            errors.append("Введите ФИО")
        if not email or '@' not in email:
            errors.append("Введите корректный email")
        if not username:
            errors.append("Введите имя пользователя")
        if len(password) < 6:
            errors.append("Пароль должен содержать минимум 6 символов")
        if password != confirm_password:
            errors.append("Пароли не совпадают")
        
        if errors:
            print(f"Ошибки валидации: {errors}")
            messagebox.showerror("Ошибка заполнения", "\n".join(errors))
            return
        
        try:
            print("1. Создаем подключение к БД...")
            connection = self.create_db_connection()
            
            if connection is None:
                print("❌ Подключение не установлено!")
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных")
                return
            
            print(f"✅ Подключение установлено")
            
            # Проверяем существование пользователя
            print(f"2. Проверяем существование пользователя '{username}'...")
            if self.check_user_exists(connection, username, email):
                print(f"❌ Пользователь уже существует")
                messagebox.showerror("Ошибка", "Пользователь с таким именем или email уже существует")
                connection.close()
                return
            
            print("✅ Пользователь не существует")
            
            # Регистрируем пользователя
            print(f"3. Регистрируем пользователя '{username}'...")
            success, message, user_id = self.register_user_in_db(
                connection, username, password, fullname, email, role
            )
            
            # Закрываем подключение
            connection.close()
            
            print(f"Результат регистрации:")
            print(f"   success: {success}")
            print(f"   message: {message}")
            print(f"   user_id: {user_id}")
            
            if success:
                print(f"✅ Регистрация успешна!")
                
                # Показываем информацию о пользователе
                role_name = self.get_role_name(role)
                
                messagebox.showinfo("Успешно", 
                              f"Регистрация завершена успешно!\n\n"
                              f"Имя пользователя: {username}\n"
                              f"ФИО: {fullname}\n"
                              f"Email: {email}\n"
                              f"Роль: {role_name}\n"
                              f"ID пользователя: {user_id}\n\n"
                              f"Теперь вы можете войти в систему.")
                
                # Закрываем окно регистрации
                self.window.destroy()
            else:
                print(f"❌ Ошибка регистрации: {message}")
                messagebox.showerror("Ошибка", message)
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Ошибка базы данных", 
                           f"Не удалось выполнить регистрацию:\n{str(e)}")
    
    def get_role_name(self, role):
        """Получение названия роли"""
        role_names = {
            'candidate': 'Кандидат',
            'consumer': 'Потребитель',
            'agent': 'Торговый агент',
            'logistic': 'Логист',
            'admin': 'Администратор'
        }
        return role_names.get(role, role)
    
    def cancel_registration(self):
        """Отмена регистрации"""
        self.window.destroy()
    
    def run(self):
        """Запуск окна регистрации"""
        self.window.mainloop()


# Для тестирования отдельно
if __name__ == "__main__":
    app = RegistrationForm()
    app.run()