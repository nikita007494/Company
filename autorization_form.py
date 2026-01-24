import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from datetime import datetime
import json
import os
from captcha import CaptchaWindow
# Импортируем класс из второго файла
import main_form
from main_form import MainApplication
import registration
from database import DatabaseConnection
from text_captcha import TextImageCaptcha
class EnhancedLoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🔐 Торговая платформа - Авторизация")
        self.window.geometry("560x800")
        self.window.configure(bg='#f0f2f5')
        self.window.resizable(False, False)
        self.locked_until = None
        # Флаг прохождения капчи
        #self.captcha_passed = False
        
         # Счетчик неудачных попыток и флаг капчи
        self.failed_attempts = 0
        self.max_attempts = 0  # Максимальное количество попыток до капчи
        #self.captcha_passed = False
        # Иконка (если есть файл icon.ico)
        try:
            self.window.iconbitmap('icon.ico')
        except:
            pass
        
        # Центрирование
        self.center_window()
        
        # Загружаем сохраненные данные
        self.load_config()
        
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
        
        # Тестовые пользователи
        self.users = self.load_users()
        
        # ID таймера для отмены
        self.timer_id = None
        
        # Создаем интерфейс
        self.create_interface()
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y-50}')  # Немного выше центра
    
    def load_config(self):
        """Загрузка конфигурации из файла"""
        self.config_file = 'login_config.json'
        self.config = {
            'last_username': '',
            'remember_me': False,
            'login_attempts': {}
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                pass
    
    def save_config(self):
        """Сохранение конфигурации в файл"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def load_users(self):
        """Загрузка пользователей (в реальном приложении - из БД)"""
        return {
            'candidate': {
                'password': self.hash_password('candidate123'),
                'role': 'candidate',
                'name': 'Иван Петров',
                'email': 'candidate@example.com'
            },
            'consumer': {
                'password': self.hash_password('consumer123'),
                'role': 'consumer',
                'name': 'ООО "Ромашка"',
                'email': 'consumer@example.com'
            },
            'agent': {
                'password': self.hash_password('agent123'),
                'role': 'agent',
                'name': 'Алексей Смирнов',
                'email': 'agent@example.com'
            },
            'logistic': {
                'password': self.hash_password('logistic123'),
                'role': 'logistic',
                'name': 'Мария Иванова',
                'email': 'logistic@example.com'
            },
            'admin': {
                'password': self.hash_password('admin123'),
                'role': 'admin',
                'name': 'Администратор Системы',
                'email': 'admin@example.com'
            }
        }
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_interface(self):
        """Создание интерфейса"""
        # Главный контейнер с прокруткой
        main_canvas = tk.Canvas(self.window, bg='#f0f2f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg='#f0f2f5')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Заголовок
        self.create_header(scrollable_frame)
        
        # Карточка входа
        self.create_login_card(scrollable_frame)
        
        # Информационная панель
        self.create_info_panel(scrollable_frame)
        
        # Футер
        self.create_footer(scrollable_frame)
        
        # Автозаполнение, если было "Запомнить меня"
        if self.config.get('remember_me') and self.config.get('last_username'):
            self.username_var.set(self.config['last_username'])
            self.remember_var.set(True)
            self.password_entry.focus_set()
    
    def create_header(self, parent):
        """Создание заголовка"""
        header_frame = tk.Frame(parent, bg='#f0f2f5')
        header_frame.pack(pady=(20, 10))
        
        # Логотип и название
        logo_frame = tk.Frame(header_frame, bg='#f0f2f5')
        logo_frame.pack()
        
        # Эмуляция логотипа
        logo_canvas = tk.Canvas(logo_frame, width=80, height=80, bg='#f0f2f5', highlightthickness=0)
        logo_canvas.pack()
        
        # Рисуем простой логотип
        logo_canvas.create_oval(10, 10, 70, 70, fill=self.colors['secondary'], outline='')
        logo_canvas.create_text(40, 40, text="TP", font=('Arial', 24, 'bold'), fill='white')
        
        # Название системы
        tk.Label(header_frame,
                text="ТОРГОВАЯ ПЛАТФОРМА",
                font=('Segoe UI', 26, 'bold'),
                fg=self.colors['primary'],
                bg='#f0f2f5').pack(pady=(10, 5))
        
        tk.Label(header_frame,
                text="Единая система управления продажами, логистикой и кадрами",
                font=('Segoe UI', 11),
                fg=self.colors['gray'],
                bg='#f0f2f5',
                wraplength=600).pack()
        
        # Текущая дата и время
        time_frame = tk.Frame(header_frame, bg='#f0f2f5')
        time_frame.pack(pady=(10, 0))
        
        self.time_label = tk.Label(time_frame,
                                  text=datetime.now().strftime("%d.%m.%Y %H:%M"),
                                  font=('Segoe UI', 9),
                                  fg=self.colors['gray'],
                                  bg='#f0f2f5')
        self.time_label.pack()
        
        # Обновление времени
        self.update_time()
    
    def update_time(self):
        """Обновление времени в реальном времени"""
        try:
            current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            self.time_label.config(text=current_time)
            # Сохраняем ID таймера для отмены
            self.timer_id = self.window.after(1000, self.update_time)
        except Exception as e:
            print(f"Ошибка обновления времени: {e}")
    
    def create_login_card(self, parent):
        """Создание карточки входа"""
        self.login_card = tk.Frame(parent,
                                  bg='white',
                                  relief='flat',
                                  highlightbackground='#dfe6e9',
                                  highlightthickness=1)
        self.login_card.pack(fill='x', padx=20, pady=10)
        
        # Заголовок карточки
        card_header = tk.Frame(self.login_card, 
                              bg=self.colors['primary'], 
                              height=45)
        card_header.pack(fill='x')
        card_header.pack_propagate(False)
        
        tk.Label(card_header,
                text="🔐 АВТОРИЗАЦИЯ В СИСТЕМЕ",
                font=('Segoe UI', 11, 'bold'),
                fg='white',
                bg=self.colors['primary']).pack(expand=True)
        
        # Тело карточки
        card_body = tk.Frame(self.login_card, bg='white', padx=30, pady=25)
        card_body.pack(fill='both', expand=True)
        
        # Переменные
        self.username_var = tk.StringVar()
        self.remember_var = tk.BooleanVar(value=False)
        
        # Поле логина
        tk.Label(card_body,
                text="Имя пользователя",
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['dark'],
                bg='white',
                anchor='w').pack(fill='x', pady=(0, 8))
        
        username_frame = tk.Frame(card_body, bg='white')
        username_frame.pack(fill='x', pady=(0, 15))
        
        self.username_entry = ttk.Entry(username_frame,
                                      textvariable=self.username_var,
                                      font=('Segoe UI', 11))
        self.username_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Иконка пользователя
        tk.Label(username_frame,
                text="👤",
                font=('Segoe UI', 14),
                bg='white').pack(side='right')
        
        # Поле пароля
        tk.Label(card_body,
                text="Пароль",
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['dark'],
                bg='white',
                anchor='w').pack(fill='x', pady=(0, 8))
        
        password_frame = tk.Frame(card_body, bg='white')
        password_frame.pack(fill='x', pady=(0, 20))
        
        self.password_entry = ttk.Entry(password_frame,
                                      font=('Segoe UI', 11),
                                      show='•')
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
        
        # Кнопка входа
        self.login_btn = tk.Button(card_body,
                                  text="ВОЙТИ В СИСТЕМУ",
                                  font=('Segoe UI', 11, 'bold'),
                                  bg=self.colors['secondary'],
                                  fg='white',
                                  relief='flat',
                                  cursor='hand2',
                                  padx=30,
                                  pady=12,
                                  command=self.login)
        self.login_btn.pack(fill='x', pady=(0, 15))

        self.regist_btn = tk.Button(card_body,
                                  text="РЕГИСТРАЦИЯ",
                                  font=('Segoe UI', 11, 'bold'),
                                  bg=self.colors['secondary'],
                                  fg='white',
                                  relief='flat',
                                  cursor='hand2',
                                  padx=30,
                                  pady=12,
                                  command=self.show_registration
                                  )
        self.regist_btn.pack(fill='x', pady=(0, 15))
        # Дополнительные опции
        options_frame = tk.Frame(card_body, bg='white')
        options_frame.pack(fill='x')
        
        # Запомнить меня
        remember_check = tk.Checkbutton(options_frame,
                                       text="Запомнить меня",
                                       variable=self.remember_var,
                                       font=('Segoe UI', 9),
                                       fg=self.colors['dark'],
                                       bg='white',
                                       selectcolor='white',
                                       activebackground='white',
                                       cursor='hand2')
        remember_check.pack(side='left')
        
        # Забыли пароль? (заглушка)
        forgot_btn = tk.Button(options_frame,
                              text="Забыли пароль?",
                              font=('Segoe UI', 9),
                              fg=self.colors['secondary'],
                              bg='white',
                              relief='flat',
                              cursor='hand2',
                              command=self.show_password_recovery)
        forgot_btn.pack(side='right')
        
        # Разделитель
        separator = tk.Frame(card_body, height=1, bg='#dfe6e9')
        separator.pack(fill='x', pady=20)
        
        # Быстрый вход
        self.create_quick_login(card_body)
        
        # Бинды клавиш
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def toggle_password(self):
        """Показать/скрыть пароль"""
        if self.password_entry.cget('show') == '•':
            self.password_entry.config(show='')
            self.show_pass_btn.config(text='🔒')
        else:
            self.password_entry.config(show='•')
            self.show_pass_btn.config(text='👁')
    
    def create_quick_login(self, parent):
        """Создание панели быстрого входа"""
        tk.Label(parent,
                text="🚀 Быстрый вход (для тестирования):",
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['dark'],
                bg='white',
                anchor='w').pack(fill='x', pady=(0, 10))
        
        accounts_grid = tk.Frame(parent, bg='white')
        accounts_grid.pack(fill='x')
        
        accounts = [
            ('👤 Кандидат', 'candidate', '#e3f2fd'),
            ('🛒 Потребитель', 'consumer', '#f3e5f5'),
            ('📊 Агент', 'agent', '#e8f5e8'),
            ('🚚 Логист', 'logistic', '#fff3e0'),
            ('⚙️ Админ', 'admin', '#ffebee')
        ]
        
        for i, (text, username, color) in enumerate(accounts):
            btn = tk.Button(accounts_grid,
                          text=text,
                          font=('Segoe UI', 9),
                          bg=color,
                          fg=self.colors['dark'],
                          relief='flat',
                          cursor='hand2',
                          padx=15,
                          pady=8,
                          command=lambda u=username: self.fill_test_account(u))
            
            # Располагаем в две колонки
            if i % 2 == 0:
                btn.grid(row=i//2, column=0, padx=(0, 5), pady=2, sticky='ew')
            else:
                btn.grid(row=i//2, column=1, padx=(5, 0), pady=2, sticky='ew')
        
        # Настройка веса колонок
        accounts_grid.columnconfigure(0, weight=1)
        accounts_grid.columnconfigure(1, weight=1)
    
    def create_info_panel(self, parent):
        """Создание информационной панели"""
        info_frame = tk.Frame(parent, bg='#e8f4fc', relief='flat')
        info_frame.pack(fill='x', padx=20, pady=15)
        
        info_text = tk.Text(info_frame,
                           height=4,
                           font=('Segoe UI', 9),
                           fg='#2c5282',
                           bg='#e8f4fc',
                           wrap='word',
                           relief='flat',
                           padx=15,
                           pady=10)
        info_text.pack(fill='x')
        
        # Создаем тег для центрирования
        info_text.tag_configure("center", justify='center')

        # Вставляем текст с тегом центрирования
        info_text.insert('1.0', 
                 "💡 Информация о ролях:\n"
                 "• Кандидат – доступ к вакансиям и резюме\n"
                 "• Потребитель – заказы товаров и контракты\n"
                 "• Агент – управление клиентами и статистика\n"
                 "• Логист – управление доставкой и статусами\n"
                 "• Админ – полный доступ ко всем функциям")

        # Применяем центрирование ко всему тексту
        info_text.tag_add("center", "1.0", "end")

        info_text.config(state='disabled')
    
    def create_footer(self, parent):
        """Создание футера"""
        footer_frame = tk.Frame(parent, bg='#f0f2f5')
        footer_frame.pack(fill='x', pady=(10, 20))
        
        # Версия и копирайт
        tk.Label(footer_frame,
                text="Торговая платформа • Версия 1.1.0 • © 2026",
                font=('Segoe UI', 9),
                fg=self.colors['gray'],
                bg='#f0f2f5').pack(pady=(0, 5))
        
        # Статус системы
        status_frame = tk.Frame(footer_frame, bg='#f0f2f5')
        status_frame.pack()
        
        # Индикатор подключения (заглушка)
        tk.Label(status_frame,
                text="●",
                font=('Arial', 12),
                fg=self.colors['success'],
                bg='#f0f2f5').pack(side='left', padx=(0, 5))
        
        tk.Label(status_frame,
                text="Подключено к базе данных",
                font=('Segoe UI', 8),
                fg=self.colors['gray'],
                bg='#f0f2f5').pack(side='left')
    
    def fill_test_account(self, username):
        """Заполнение тестового аккаунта"""
        self.username_var.set(username)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, f"{username}123")
        
        # Анимация подсветки
        self.highlight_field(self.username_entry, '#e8f4fc')
        self.highlight_field(self.password_entry, '#e8f4fc')
        
        # Фокус на кнопке входа
        self.login_btn.focus_set()
    
    def highlight_field(self, widget, color):
        """Подсветка поля ввода"""
        original_color = widget.cget('background')
        widget.config(background=color)
        self.window.after(800, lambda: widget.config(background=original_color))
    
    def show_password_recovery(self):
        """Восстановление пароля (заглушка)"""
        messagebox.showinfo("Восстановление пароля",
                          "Для восстановления пароля обратитесь к системному администратору.\n"
                          "Телефон: +7 (XXX) XXX-XX-XX\n"
                          "Email: support@trading-platform.ru")
    
    def validate_input(self):
        """Валидация ввода"""
        username = self.username_var.get().strip()
        password = self.password_entry.get().strip()
        
        errors = []
        
        if not username:
            errors.append("Введите имя пользователя")
            self.highlight_field(self.username_entry, '#ffebee')
        
        if not password:
            errors.append("Введите пароль")
            self.highlight_field(self.password_entry, '#ffebee')
        
        if errors:
            messagebox.showwarning("Ошибка заполнения", "\n".join(errors))
            return False
        
        # Проверка количества попыток
        attempts = self.config.get('login_attempts', {})
        user_attempts = attempts.get(username, 0)
        
        if user_attempts >= 5:
            messagebox.showerror("Доступ заблокирован",
                               f"Слишком много неудачных попыток входа для пользователя '{username}'.\n"
                               "Обратитесь к администратору.")
            return False
        
        return True
    
    def login(self):
        """Обработка входа с капчей"""
        if not self.validate_input():
            return
    
        username = self.username_var.get().strip()
        password = self.password_entry.get().strip()
    
        # ВСЕГДА показываем капчу
        self.show_captcha_window()
    
        # Сначала пробуем БД
        try:
            from database import DatabaseConnection
            db = DatabaseConnection.get_instance()
    
            print(f"DEBUG: Пробуем аутентификацию через БД для {username}")
            success, message, user_data = db.authenticate_user(username, password)
    
            if success:
                print(f"DEBUG: Успешная аутентификация через БД")
                # Сбрасываем счетчик неудачных попыток при успешном входе
                self.failed_attempts = 0
                self.captcha_passed = False
            
                # Обновляем статус капчи
                if hasattr(self, 'update_captcha_status'):
                    self.update_captcha_status()
            
                # Проверяем, есть ли метод on_login_success
                if hasattr(self, 'on_login_success'):
                    print(f"DEBUG: Вызываем on_login_success с user_data")
                    self.on_login_success(username, user_data)
                else:
                    print(f"ERROR: Метод on_login_success не найден!")
                    messagebox.showerror("Ошибка", "Метод on_login_success не найден в классе")
                return
            else:
                print(f"DEBUG: Ошибка аутентификации в БД: {message}")
                # Увеличиваем счетчик неудачных попыток
                self.failed_attempts += 1
            
                # Обновляем статус капчи
                if hasattr(self, 'update_captcha_status'):
                    self.update_captcha_status()
            
                # Проверяем, нужна ли капча после неудачной попытки
                if self.failed_attempts >= self.max_attempts:
                    self.show_captcha_required()
            
                # Проверяем, есть ли метод on_login_failure
                if hasattr(self, 'on_login_failure'):
                    self.on_login_failure(username)
                else:
                    print(f"ERROR: Метод on_login_failure не найден!")
                    messagebox.showerror("Ошибка", f"Неверные данные: {message}")
                return
        
        except AttributeError as e:
            print(f"DEBUG: AttributeError - проверяем наличие методов: {e}")
            # Проверяем наличие методов
            methods = ['on_login_success', 'on_login_failure', 'hash_password']
            for method in methods:
                if not hasattr(self, method):
                    print(f"ERROR: Отсутствует метод {method}")
    
            # Fallback на локальные данные
            print("DEBUG: Используем fallback...")
    
        except Exception as e:
            print(f"DEBUG: Ошибка подключения к БД: {e}")
            # Увеличиваем счетчик неудачных попыток
            self.failed_attempts += 1
        
            # Обновляем статус капчи
            if hasattr(self, 'update_captcha_status'):
                self.update_captcha_status()
        
            # Fallback на локальные данные
            pass
    
        # Fallback на локальные данные (если БД недоступна или ошибка)
        print(f"DEBUG: Используем локальные данные...")
        hashed_password = self.hash_password(password)
    
        if username in self.users and self.users[username]['password'] == hashed_password:
            # Сбрасываем счетчик неудачных попыток при успешном входе
            self.failed_attempts = 0
            self.captcha_passed = False
        
            # Обновляем статус капчи
            if hasattr(self, 'update_captcha_status'):
                self.update_captcha_status()
        
            # Создаем user_data из локальных данных
            user_data = self.users[username]
    
            if hasattr(self, 'on_login_success'):
                self.on_login_success(username, user_data)
            else:
                print("ERROR: Метод on_login_success не найден для локальных данных!")
                messagebox.showerror("Ошибка", "Внутренняя ошибка приложения")
        else:
            # Увеличиваем счетчик неудачных попыток
            self.failed_attempts += 1
        
            # Обновляем статус капчи
            if hasattr(self, 'update_captcha_status'):
                self.update_captcha_status()
        
            # Проверяем, нужна ли капча после неудачной попытки
            if self.failed_attempts >= self.max_attempts:
                self.show_captcha_required()
        
            if hasattr(self, 'on_login_failure'):
                self.on_login_failure(username)
            else:
                messagebox.showerror("Ошибка авторизации", 
                           "Неверное имя пользователя или пароль")
    def on_login_success(self, username, user_data=None):
        """Действия при успешном входе"""
        # Если user_data не передан, используем локальные данные
        if user_data is None and username in self.users:
         user_data = self.users[username]
    
        if not user_data:
            messagebox.showerror("Ошибка", "Данные пользователя не найдены")
            return
    
        # Сохраняем конфигурацию
        if self.remember_var.get():
            self.config['last_username'] = username
            self.config['remember_me'] = True
        else:
            self.config['last_username'] = ''
            self.config['remember_me'] = False
    
        # Сбрасываем счетчик попыток
        if username in self.config.get('login_attempts', {}):
            del self.config['login_attempts'][username]
       
        self.save_config()
    
        # Показываем сообщение
        role_name = self.get_role_name(user_data['role'])
        messagebox.showinfo("Вход выполнен",
                       f"✅ Успешная авторизация!\n\n"
                       f"Добро пожаловать, {user_data['name']}!\n"
                       f"Роль: {role_name}\n"
                       f"Логин: {username}")
    
        #    Останавливаем таймер перед уничтожением окна
        if hasattr(self, 'timer_id') and self.timer_id:
            self.window.after_cancel(self.timer_id)
    
        # Закрываем окно авторизации
        self.window.destroy()
    
        # Запускаем главное приложение
        self.launch_main_app(username, user_data)
    def update_captcha_status(self):
        """Обновление статуса капчи"""
        if self.failed_attempts >= self.max_attempts and not self.captcha_passed:
            self.captcha_status_label.config(
                text=f"Требуется проверка капчи ({self.failed_attempts}/{self.max_attempts} попыток)"
            )
        else:
            self.captcha_status_label.config(text="")
    
 
    def show_registration(self):
        """Показать форму регистрации"""
        # Создаем окно регистрации как дочернее
        registration_window = registration.RegistrationForm(self.window)

    def show_captcha_required(self):
        """Показ сообщения о необходимости капчи"""
        if self.failed_attempts >= self.max_attempts and not self.captcha_passed:
            response = messagebox.askyesno(
                "Требуется проверка безопасности",
                #f"Обнаружено {self.failed_attempts} неудачных попыток входа.\n"
                "Для продолжения требуется пройти проверку.\n\n"
                "Пройти проверку сейчас?"
            )
        
            if response:
                self.show_captcha_window()
                return True
        return False
    def show_captcha_window(self):
        """Показать окно текстовой капчи"""
        try:
            from text_captcha import TextImageCaptcha
        
            def on_captcha_success():
                """Обработка успешного прохождения капчи"""
                self.captcha_passed = True
                self.update_captcha_status()
                messagebox.showinfo("Успех", 
                              "✓ Проверка пройдена успешно!\n"
                              "Теперь вы можете попробовать войти снова.")
        
            # Открываем окно текстовой капчи
            TextImageCaptcha(self.window, on_captcha_success)
        
        except ImportError as e:
            print(f"❌ Не удалось импортировать текстовую капчу: {e}")
            # Fallback на простую математическую капчу
            self.show_simple_captcha()

    def show_simple_captcha(self):
        """Простая текстовая капча (fallback)"""
        import random
    
        # Создаем окно капчи
        captcha_window = tk.Toplevel(self.window)
        captcha_window.title("Проверка безопасности")
        captcha_window.geometry("400x300")
        captcha_window.configure(bg='white')
        captcha_window.resizable(False, False)
    
        # Блокируем родительское окно
        captcha_window.transient(self.window)
        captcha_window.grab_set()
    
        # Генерируем случайный пример
        operations = ['+', '-', '*']
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(operations)
    
        if op == '+':
            correct_answer = a + b
        elif op == '-':
            correct_answer = a - b
        else:
            correct_answer = a * b
    
        # Интерфейс
        # Центрирование окна (самый простой способ)
        captcha_window.update_idletasks()
        width = captcha_window.winfo_width()
        height = captcha_window.winfo_height()
        x = (captcha_window.winfo_screenwidth() // 2) - (width // 2)
        y = (captcha_window.winfo_screenheight() // 2) - (height // 2)
        captcha_window.geometry(f'+{x}+{y}')
        main_frame = tk.Frame(captcha_window, bg='white', padx=30, pady=30)
        main_frame.pack(fill='both', expand=True)
    
        tk.Label(main_frame,
             text="🔒 ПРОВЕРКА БЕЗОПАСНОСТИ",
             font=('Arial', 14, 'bold'),
             fg='#2c3e50',
             bg='white').pack(pady=(0, 20))
    
        tk.Label(main_frame,
             text=f"Решите пример: {a} {op} {b} = ?",
             font=('Arial', 16),
             fg='#34495e',
             bg='white').pack(pady=(0, 20))
    
        answer_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=answer_var, 
              font=('Arial', 14)).pack(pady=(0, 20), fill='x')
    
        def verify():
            try:
                user_answer = int(answer_var.get().strip())
                if user_answer == correct_answer:
                    self.captcha_passed = True
                    self.update_captcha_status()
                    messagebox.showinfo("Успех", "Проверка пройдена!")
                    captcha_window.destroy()
                else:
                    messagebox.showerror("Ошибка", "Неверный ответ!")
                    answer_var.set("")
            except:
                messagebox.showerror("Ошибка", "Введите число!")
    
        tk.Button(main_frame,
                text="ПРОВЕРИТЬ",
                bg='#27ae60',
                fg='white',
                font=('Arial', 12, 'bold'),
                command=verify,
                padx=30, pady=10).pack()

    def update_captcha_status(self):
        """Обновление статуса капчи в интерфейсе"""
        if hasattr(self, 'captcha_status_label'):
            if self.failed_attempts >= self.max_attempts and not self.captcha_passed:
                self.captcha_status_label.config(
                    text=f"⚠️ Требуется проверка ({self.failed_attempts}/{self.max_attempts})",
                    fg='#e74c3c'
                )
            elif self.captcha_passed:
                self.captcha_status_label.config(
                    text="✓ Проверка пройдена",
                    fg='#27ae60'
                )
            else:
                remaining = max(0, self.max_attempts - self.failed_attempts)
                self.captcha_status_label.config(
                    text=f"Осталось попыток: {remaining}",
                    fg='#7f8c8d'
                )
    def increment_failed_attempts(self):
        """Увеличивает счетчик неудачных попыток"""
        self.failed_attempts += 1
        self.update_captcha_status()
    
        # Проверяем, нужна ли капча
        if self.failed_attempts >= self.max_attempts and not self.captcha_passed:
            self.show_captcha_required()

    def reset_login_attempts(self):
        """Сбрасывает счетчик попыток при успешном входе"""
        self.failed_attempts = 0
        self.captcha_passed = False
        self.update_captcha_status()

    
    def on_login_failure(self, username):
        """Действия при неудачном входе"""
        # Увеличиваем счетчик попыток
        if 'login_attempts' not in self.config:
         self.config['login_attempts'] = {}
    
        self.config['login_attempts'][username] = self.config['login_attempts'].get(username, 0) + 1
        self.save_config()
    
        attempts = self.config['login_attempts'][username]
        remaining = 5 - attempts
    
        if remaining > 0:
         messagebox.showerror("Ошибка авторизации",
                           f"❌ Неверное имя пользователя или пароль\n\n"
                           f"Неудачных попыток: {attempts}\n"
                           f"Осталось попыток: {remaining}")
        else:
            messagebox.showerror("Доступ заблокирован",
                           f"❌ Превышено максимальное количество попыток\n\n"
                           f"Доступ для пользователя '{username}' временно заблокирован.\n"
                           "Обратитесь к системному администратору.")
    
        # Сброс пароля и фокус
        self.password_entry.delete(0, tk.END)
        self.password_entry.focus_set()
    
        # Анимация тряски
        self.shake_window()
    
    def shake_window(self):
        """Анимация тряски окна при ошибке"""
        x = self.window.winfo_x()
        y = self.window.winfo_y()
    
        for i in range(5):
            offset = 5 if i % 2 == 0 else -5
            self.window.geometry(f"+{x + offset}+{y}")
            self.window.update()
            self.window.after(50)
    
        self.window.geometry(f"+{x}+{y}")
    
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
    
    def launch_main_app(self, username, user_data):
        """Запуск главного приложения"""
        # Создаем экземпляр главного приложения
        main_app = MainApplication(username, user_data, self.colors)
        main_app.run()
    
    def run(self):
        """Запуск приложения"""
        self.window.mainloop()


# Запуск приложения
if __name__ == "__main__":
    try:
        app = EnhancedLoginWindow()
        app.run()
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        messagebox.showerror("Ошибка", f"Не удалось запустить приложение:\n{str(e)}")