import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from datetime import datetime
import json
import os

class EnhancedLoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🔐 Торговая платформа - Авторизация")
        self.window.geometry("560x700")
        self.window.configure(bg='#f0f2f5')
        self.window.resizable(False, False)
        
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
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.time_label.config(text=current_time)
        self.window.after(1000, self.update_time)
    
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
        """Обработка входа"""
        if not self.validate_input():
            return
        
        username = self.username_var.get().strip()
        password = self.password_entry.get().strip()
        hashed_password = self.hash_password(password)
        
        # Проверка учетных данных
        if username in self.users and self.users[username]['password'] == hashed_password:
            # Успешный вход
            self.on_login_success(username)
        else:
            # Неудачная попытка
            self.on_login_failure(username)
    
    def on_login_success(self, username):
        """Действия при успешном входе"""
        user_data = self.users[username]
        
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
        
        # Закрываем окно авторизации и открываем главное
        self.window.destroy()
        
        # Здесь будет запуск главного приложения
        self.launch_main_app(username, user_data)
    
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
        # Импортируем здесь, чтобы избежать циклических импортов
        import sys
        
        # Создаем простое главное окно для демонстрации
        main_window = tk.Tk()
        main_window.title(f"Торговая платформа - {self.get_role_name(user_data['role'])}")
        main_window.geometry("900x600")
        main_window.configure(bg='white')
        
        # Центрируем
        main_window.update_idletasks()
        width = main_window.winfo_width()
        height = main_window.winfo_height()
        x = (main_window.winfo_screenwidth() // 2) - (width // 2)
        y = (main_window.winfo_screenheight() // 2) - (height // 2)
        main_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Создаем интерфейс главного окна
        self.create_main_interface(main_window, username, user_data)
        
        main_window.mainloop()
    
    def create_main_interface(self, window, username, user_data):
        """Создание интерфейса главного окна"""
        # Верхняя панель
        header = tk.Frame(window, bg=self.colors['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Лого и название
        logo_frame = tk.Frame(header, bg=self.colors['primary'])
        logo_frame.pack(side='left', padx=20)
        
        tk.Label(logo_frame,
                text="🛒",
                font=('Segoe UI', 24),
                bg=self.colors['primary'],
                fg='white').pack(side='left', padx=(0, 10))
        
        tk.Label(logo_frame,
                text="Торговая платформа",
                font=('Segoe UI', 16, 'bold'),
                bg=self.colors['primary'],
                fg='white').pack(side='left')
        
        # Информация о пользователе
        user_frame = tk.Frame(header, bg=self.colors['primary'])
        user_frame.pack(side='right', padx=20)
        
        tk.Label(user_frame,
                text=f"{user_data['name']}",
                font=('Segoe UI', 11),
                bg=self.colors['primary'],
                fg='white').pack(side='top', anchor='e')
        
        tk.Label(user_frame,
                text=f"Роль: {self.get_role_name(user_data['role'])}",
                font=('Segoe UI', 9),
                bg=self.colors['primary'],
                fg='#bdc3c7').pack(side='bottom', anchor='e')
        
        # Основной контент
        content = tk.Frame(window, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Приветствие
        welcome_frame = tk.Frame(content, bg='white')
        welcome_frame.pack(fill='x', pady=(0, 30))
        
        tk.Label(welcome_frame,
                text=f"Добро пожаловать, {user_data['name']}!",
                font=('Segoe UI', 20, 'bold'),
                fg=self.colors['primary'],
                bg='white').pack(anchor='w')
        
        tk.Label(welcome_frame,
                text="Вы вошли в систему управления торговой платформой",
                font=('Segoe UI', 12),
                fg=self.colors['gray'],
                bg='white').pack(anchor='w', pady=(5, 0))
        
        # Доступные функции в зависимости от роли
        self.show_role_functions(content, user_data['role'])
        
        # Кнопка выхода
        tk.Button(content,
                 text="Выйти из системы",
                 font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['accent'],
                 fg='white',
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=window.destroy).pack(side='bottom', pady=20)
    
def show_role_functions(self, parent, role):
    """Показать функции доступные для роли в виде кнопок с иконками"""
    
    # Функции с подробным описанием
    role_functions = {
        'candidate': [
            ("📝", "Резюме", "Заполнение и редактирование резюме", self.open_resume_section),
            ("👁‍🗨", "Вакансии", "Просмотр активных вакансий компании", self.open_vacancies_section),
            ("📊", "Статус", "Отслеживание статуса своей анкеты", self.open_application_status),
            ("🔔", "Уведомления", "Уведомления о новых вакансиях", self.open_notifications),
            ("📄", "Документы", "Мои загруженные документы", self.open_documents)
        ],
        # ... остальные роли ...
    }
    
    functions = role_functions.get(role, [])
    
    # Создаем основной фрейм
    main_frame = tk.Frame(parent, bg='white')
    main_frame.pack(fill='both', expand=True)
    
    # Заголовок
    header_frame = tk.Frame(main_frame, bg='white')
    header_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(header_frame,
            text="🚀 ДОСТУПНЫЕ РАЗДЕЛЫ",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['primary'],
            bg='white').pack(anchor='w')
    
    tk.Label(header_frame,
            text="Выберите нужный раздел для работы",
            font=('Segoe UI', 11),
            fg=self.colors['gray'],
            bg='white').pack(anchor='w', pady=(5, 0))
    
    if not functions:
        tk.Label(main_frame,
                text="Нет доступных функций для данной роли",
                font=('Segoe UI', 12),
                fg=self.colors['gray'],
                bg='white').pack(pady=50)
        return
    
    # Создаем Canvas для прокрутки
    canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    
    scrollable_frame = tk.Frame(canvas, bg='white')
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Сетка для кнопок
    grid_frame = tk.Frame(scrollable_frame, bg='white')
    grid_frame.pack(fill='both', expand=True, padx=5, pady=5)
    
    # Создаем стилизованные кнопки
    for i, (icon, title, description, command) in enumerate(functions):
        row = i // 2
        col = i % 2
        
        btn_frame = tk.Frame(grid_frame, 
                            bg=self.get_button_color(role),
                            relief='flat',
                            highlightthickness=0)
        btn_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Внутренний фрейм для отступов
        inner_frame = tk.Frame(btn_frame, bg='white', padx=15, pady=15)
        inner_frame.pack(fill='both', expand=True)
        
        # Иконка и заголовок
        icon_frame = tk.Frame(inner_frame, bg='white')
        icon_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(icon_frame,
                text=icon,
                font=('Segoe UI', 24),
                bg='white').pack(side='left', padx=(0, 10))
        
        tk.Label(icon_frame,
                text=title,
                font=('Segoe UI', 13, 'bold'),
                fg=self.colors['primary'],
                bg='white').pack(side='left')
        
        # Описание
        tk.Label(inner_frame,
                text=description,
                font=('Segoe UI', 10),
                fg=self.colors['dark'],
                bg='white',
                wraplength=200,
                justify='left').pack(fill='x', pady=(0, 15))
        
        # Кнопка "Открыть"
        open_btn = tk.Button(inner_frame,
                           text="ОТКРЫТЬ →",
                           font=('Segoe UI', 9, 'bold'),
                           bg=self.get_button_color(role),
                           fg='white',
                           relief='flat',
                           cursor='hand2',
                           padx=20,
                           pady=6,
                           command=command)
        open_btn.pack()
        
        # Эффект наведения на всю карточку
        self.add_card_hover_effect(btn_frame, inner_frame, open_btn, role)
        
        # Настраиваем размеры
        btn_frame.config(width=250, height=180)
        btn_frame.pack_propagate(False)
    
    # Настройка сетки
    grid_frame.columnconfigure(0, weight=1)
    grid_frame.columnconfigure(1, weight=1)
    
    # Размещаем Canvas и Scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Настраиваем прокрутку колесиком мыши
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def open_resume_section(self):
        """Заглушка для раздела резюме"""
        messagebox.showinfo("Резюме", "Раздел 'Резюме' в разработке")
    
    def open_vacancies_section(self):
        """Заглушка для раздела вакансий"""
        messagebox.showinfo("Вакансии", "Раздел 'Вакансии' в разработке")
    
    def open_application_status(self):
        """Заглушка для раздела статуса анкеты"""
        messagebox.showinfo("Статус анкеты", "Раздел 'Статус анкеты' в разработке")
    
    def open_notifications(self):
        """Заглушка для раздела уведомлений"""
        messagebox.showinfo("Уведомления", "Раздел 'Уведомления' в разработке")
    
    def open_documents(self):
        """Заглушка для раздела документов"""
        messagebox.showinfo("Документы", "Раздел 'Документы' в разработке")
    
    def open_catalog(self):
        """Заглушка для раздела каталога"""
        messagebox.showinfo("Каталог", "Раздел 'Каталог' в разработке")
    
    def open_contract_application(self):
        """Заглушка для раздела контракта"""
        messagebox.showinfo("Контракт", "Раздел 'Контракт' в разработке")
    
    def create_order(self):
        """Заглушка для создания заказа"""
        messagebox.showinfo("Создание заказа", "Раздел 'Создание заказа' в разработке")
    
    def track_orders(self):
        """Заглушка для отслеживания заказов"""
        messagebox.showinfo("Отслеживание", "Раздел 'Отслеживание заказов' в разработке")
    
    def order_history(self):
        """Заглушка для истории заказов"""
        messagebox.showinfo("История", "Раздел 'История заказов' в разработке")
    
    def payment_section(self):
        """Заглушка для раздела оплаты"""
        messagebox.showinfo("Оплата", "Раздел 'Оплата' в разработке")
    
    def open_clients(self):
        """Заглушка для раздела клиентов"""
        messagebox.showinfo("Клиенты", "Раздел 'Клиенты' в разработке")
    
    def manage_orders(self):
        """Заглушка для управления заказами"""
        messagebox.showinfo("Управление заказами", "Раздел 'Управление заказами' в разработке")
    
    def schedule_section(self):
        """Заглушка для раздела графика"""
        messagebox.showinfo("График", "Раздел 'График вывоза' в разработке")
    
    def client_contracts(self):
        """Заглушка для контрактов клиентов"""
        messagebox.showinfo("Контракты", "Раздел 'Контракты клиентов' в разработке")
    
    def sales_statistics(self):
        """Заглушка для статистики"""
        messagebox.showinfo("Статистика", "Раздел 'Статистика' в разработке")
    
    def new_deal(self):
        """Заглушка для новой сделки"""
        messagebox.showinfo("Сделка", "Раздел 'Новая сделка' в разработке")
    
    def today_orders(self):
        """Заглушка для заказов на сегодня"""
        messagebox.showinfo("Заказы", "Раздел 'Заказы на сегодня' в разработке")
    
    def change_order_status(self):
        """Заглушка для изменения статуса"""
        messagebox.showinfo("Статус заказа", "Раздел 'Изменение статуса заказа' в разработке")
    
    def delivery_schedule(self):
        """Заглушка для графика доставки"""
        messagebox.showinfo("Доставка", "Раздел 'График доставки' в разработке")
    
    def shipment_readiness(self):
        """Заглушка для готовности к отгрузке"""
        messagebox.showinfo("Отгрузка", "Раздел 'Готовность к отгрузке' в разработке")
    
    def logistics_reports(self):
        """Заглушка для логистических отчетов"""
        messagebox.showinfo("Отчеты", "Раздел 'Логистические отчеты' в разработке")
    
    def delivery_routes(self):
        """Заглушка для маршрутов доставки"""
        messagebox.showinfo("Маршруты", "Раздел 'Маршруты доставки' в разработке")
    
    def manage_products(self):
        """Заглушка для управления товарами"""
        messagebox.showinfo("Товары", "Раздел 'Управление товарами' в разработке")
    
    def manage_users(self):
        """Заглушка для управления пользователями"""
        messagebox.showinfo("Пользователи", "Раздел 'Управление пользователями' в разработке")
    
    def system_settings(self):
        """Заглушка для настроек системы"""
        messagebox.showinfo("Настройки", "Раздел 'Настройки системы' в разработке")
    
    def analytics_reports(self):
        """Заглушка для аналитики"""
        messagebox.showinfo("Аналитика", "Раздел 'Аналитика' в разработке")
    
    def tech_support(self):
        """Заглушка для техподдержки"""
        messagebox.showinfo("Поддержка", "Раздел 'Техническая поддержка' в разработке")
    
    def system_logs(self):
        """Заглушка для логов системы"""
        messagebox.showinfo("Логи", "Раздел 'Логи системы' в разработке")
    
    def finance_management(self):
        """Заглушка для управления финансами"""
        messagebox.showinfo("Финансы", "Раздел 'Управление финансами' в разработке")
    
    
def get_button_color(self, role):
     """Возвращает цвет кнопки в зависимости от роли"""
     colors = {
        'candidate': '#3498db',      # Синий
        'consumer': '#2ecc71',       # Зеленый
        'agent': '#9b59b6',          # Фиолетовый
        'logistic': '#e67e22',       # Оранжевый
        'admin': '#e74c3c'           # Красный
     }
     return colors.get(role, '#3498db')

def darken_color(self, color, percent):
    """Затемняет цвет на указанный процент"""
    if isinstance(color, str) and color.startswith('#'):
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        darkened = tuple(max(0, int(c * (100 - percent) / 100)) for c in rgb)
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'
    return color

def add_card_hover_effect(self, card_frame, inner_frame, button, role):
    """Добавляет эффект наведения на карточку"""
    original_bg = self.get_button_color(role)
    darkened_bg = self.darken_color(original_bg, 15)
    
    def on_enter(e):
        card_frame.config(bg=darkened_bg)
        button.config(bg=darkened_bg)
    
    def on_leave(e):
        card_frame.config(bg=original_bg)
        button.config(bg=original_bg)
    
    # Привязываем события ко всем виджетам внутри карточки
    for widget in [card_frame, inner_frame, button]:
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)    
# Запуск приложения
if __name__ == "__main__":
    try:
        app = EnhancedLoginWindow()
        # Просто вызываем метод mainloop напрямую
        app.window.mainloop()
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        messagebox.showerror("Ошибка", f"Не удалось запустить приложение:\n{str(e)}")