import tkinter as tk
from tkinter import ttk, messagebox

class MainApplication:
    def __init__(self, username, user_data, colors):
        self.username = username
        self.user_data = user_data
        self.colors = colors
        
        self.window = tk.Tk()
        self.window.title(f"Торговая платформа - {self.get_role_name(user_data['role'])}")
        self.window.geometry("900x600")
        self.window.configure(bg='white')
        
        # Центрируем окно
        self.center_window()
        
        # Создаем интерфейс
        self.create_main_interface()
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_main_interface(self):
        """Создание интерфейса главного окна"""
        # Верхняя панель
        header = tk.Frame(self.window, bg=self.colors['primary'], height=70)
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
                 text=f"{self.user_data['name']}",
                 font=('Segoe UI', 11),
                 bg=self.colors['primary'],
                 fg='white').pack(side='top', anchor='e')
        
        tk.Label(user_frame,
                 text=f"Роль: {self.get_role_name(self.user_data['role'])}",
                 font=('Segoe UI', 9),
                 bg=self.colors['primary'],
                 fg='#bdc3c7').pack(side='bottom', anchor='e')
        
        # Основной контент
        content = tk.Frame(self.window, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Приветствие
        welcome_frame = tk.Frame(content, bg='white')
        welcome_frame.pack(fill='x', pady=(0, 30))
        
        tk.Label(welcome_frame,
                 text=f"Добро пожаловать, {self.user_data['name']}!",
                 font=('Segoe UI', 20, 'bold'),
                 fg=self.colors['primary'],
                 bg='white').pack(anchor='w')
        
        tk.Label(welcome_frame,
                 text="Вы вошли в систему управления торговой платформой",
                 font=('Segoe UI', 12),
                 fg=self.colors['gray'],
                 bg='white').pack(anchor='w', pady=(5, 0))
        
        # Доступные функции в зависимости от роли
        self.show_role_functions(content)
        
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
                  command=self.window.destroy).pack(side='bottom', pady=20)
    
    def show_role_functions(self, parent):
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
            'consumer': [
                ("📋", "Каталог", "Просмотр каталога товаров", self.open_catalog),
                ("📝", "Контракт", "Оформление заявки на контракт", self.open_contract_application),
                ("🛒", "Создать заказ", "Создание нового заказа", self.create_order),
                ("📊", "Отслеживание", "Отслеживание статуса заказов", self.track_orders),
                ("📋", "История", "История предыдущих заказов", self.order_history),
                ("💳", "Оплата", "Оплата и финансовые операции", self.payment_section)
            ],
            'agent': [
                ("👥", "Клиенты", "Управление клиентской базой", self.open_clients),
                ("📦", "Заказы", "Управление заказами клиентов", self.manage_orders),
                ("📅", "График", "График вывоза товаров", self.schedule_section),
                ("📄", "Контракты", "Контракты с клиентами", self.client_contracts),
                ("📈", "Статистика", "Статистика продаж", self.sales_statistics)
            ],
            'logistic': [
                ("💰", "Сделка", "Оформление новой сделки", self.new_deal),
                ("📦", "Заказы", "Заказы на сегодня", self.today_orders),
                ("🔄", "Статус", "Изменение статуса заказа", self.change_order_status),
                ("🚚", "Доставка", "График доставки", self.delivery_schedule),
                ("📦", "Отгрузка", "Готовность к отгрузке", self.shipment_readiness),
                ("📊", "Отчеты", "Логистические отчеты", self.logistics_reports),
                ("🗺️", "Маршруты", "Маршруты доставки", self.delivery_routes)
            ],
            'admin': [
                ("📦", "Товары", "Управление товарами", self.manage_products),
                ("👥", "Пользователи", "Управление пользователями", self.manage_users),
                ("⚙️", "Настройки", "Настройки системы", self.system_settings),
                ("📈", "Аналитика", "Аналитика и отчеты", self.analytics_reports),
                ("🔧", "Поддержка", "Техническая поддержка", self.tech_support),
                ("📋", "Логи", "Логи системы", self.system_logs),
                ("💰", "Финансы", "Управление финансами", self.finance_management)
            ]
        }
        
        functions = role_functions.get(self.user_data['role'], [])
        
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
                                 bg=self.get_button_color(self.user_data['role']),
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
                                 bg=self.get_button_color(self.user_data['role']),
                                 fg='white',
                                 relief='flat',
                                 cursor='hand2',
                                 padx=20,
                                 pady=6,
                                 command=command)
            open_btn.pack()
            
            # Эффект наведения на всю карточку
            self.add_card_hover_effect(btn_frame, inner_frame, open_btn, self.user_data['role'])
            
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
    
    # Методы-заглушки для кнопок
    def open_resume_section(self):
        messagebox.showinfo("Резюме", "Раздел 'Резюме' в разработке")
    
    def open_vacancies_section(self):
        messagebox.showinfo("Вакансии", "Раздел 'Вакансии' в разработке")
    
    def open_application_status(self):
        messagebox.showinfo("Статус анкеты", "Раздел 'Статус анкеты' в разработке")
    
    def open_notifications(self):
        messagebox.showinfo("Уведомления", "Раздел 'Уведомления' в разработке")
    
    def open_documents(self):
        messagebox.showinfo("Документы", "Раздел 'Документы' в разработке")
    
    def open_catalog(self):
        messagebox.showinfo("Каталог", "Раздел 'Каталог' в разработке")
    
    def open_contract_application(self):
        messagebox.showinfo("Контракт", "Раздел 'Контракт' в разработке")
    
    def create_order(self):
        messagebox.showinfo("Создание заказа", "Раздел 'Создание заказа' в разработке")
    
    def track_orders(self):
        messagebox.showinfo("Отслеживание", "Раздел 'Отслеживание заказов' в разработке")
    
    def order_history(self):
        messagebox.showinfo("История", "Раздел 'История заказов' в разработке")
    
    def payment_section(self):
        messagebox.showinfo("Оплата", "Раздел 'Оплата' в разработке")
    
    def open_clients(self):
        messagebox.showinfo("Клиенты", "Раздел 'Клиенты' в разработке")
    
    def manage_orders(self):
        messagebox.showinfo("Управление заказами", "Раздел 'Управление заказами' в разработке")
    
    def schedule_section(self):
        messagebox.showinfo("График", "Раздел 'График вывоза' в разработке")
    
    def client_contracts(self):
        messagebox.showinfo("Контракты", "Раздел 'Контракты клиентов' в разработке")
    
    def sales_statistics(self):
        messagebox.showinfo("Статистика", "Раздел 'Статистика' в разработке")
    
    def new_deal(self):
        messagebox.showinfo("Сделка", "Раздел 'Новая сделка' в разработке")
    
    def today_orders(self):
        messagebox.showinfo("Заказы", "Раздел 'Заказы на сегодня' в разработке")
    
    def change_order_status(self):
        messagebox.showinfo("Статус заказа", "Раздел 'Изменение статуса заказа' в разработке")
    
    def delivery_schedule(self):
        messagebox.showinfo("Доставка", "Раздел 'График доставки' в разработке")
    
    def shipment_readiness(self):
        messagebox.showinfo("Отгрузка", "Раздел 'Готовность к отгрузке' в разработке")
    
    def logistics_reports(self):
        messagebox.showinfo("Отчеты", "Раздел 'Логистические отчеты' в разработке")
    
    def delivery_routes(self):
        messagebox.showinfo("Маршруты", "Раздел 'Маршруты доставки' в разработке")
    
    def manage_products(self):
        messagebox.showinfo("Товары", "Раздел 'Управление товарами' в разработке")
    
    def manage_users(self):
        messagebox.showinfo("Пользователи", "Раздел 'Управление пользователями' в разработке")
    
    def system_settings(self):
        messagebox.showinfo("Настройки", "Раздел 'Настройки системы' в разработке")
    
    def analytics_reports(self):
        messagebox.showinfo("Аналитика", "Раздел 'Аналитика' в разработке")
    
    def tech_support(self):
        messagebox.showinfo("Поддержка", "Раздел 'Техническая поддержка' в разработке")
    
    def system_logs(self):
        messagebox.showinfo("Логи", "Раздел 'Логи системы' в разработке")
    
    def finance_management(self):
        messagebox.showinfo("Финансы", "Раздел 'Управление финансами' в разработке")
    
    def run(self):
        """Запуск главного приложения"""
        self.window.mainloop()