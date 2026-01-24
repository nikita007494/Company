import tkinter as tk
from tkinter import ttk, font
import tkinter.messagebox as messagebox

class TradingAuthForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Торговая платформа | Авторизация")
        self.root.geometry('450x600')
        self.root.resizable(False, False)
        self.root.configure(bg='#1e1e2e')
        
        # Стилизация
        self.setup_styles()
        self.create_widgets()
        self.center_window()
        
    def setup_styles(self):
        """Настройка стилей виджетов"""
        self.custom_font = font.Font(family="Segoe UI", size=10)
        self.title_font = font.Font(family="Segoe UI", size=20, weight="bold")
        
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Создание всех виджетов формы"""
        
        # Главный контейнер
        main_container = tk.Frame(self.root, bg='#1e1e2e', padx=40, pady=40)
        main_container.pack(fill='both', expand=True)
        
        # Логотип/Заголовок платформы
        logo_frame = tk.Frame(main_container, bg='#1e1e2e')
        logo_frame.pack(pady=(0, 30))
        
        tk.Label(logo_frame, text="📈", font=("Arial", 48), 
                bg='#1e1e2e', fg='#89b4fa').pack()
        
        tk.Label(logo_frame, text="TRADE PRO", font=self.title_font,
                bg='#1e1e2e', fg='#cdd6f4').pack(pady=(10, 5))
        
        tk.Label(logo_frame, text="Торговая платформа для профессионалов", 
                font=self.custom_font, bg='#1e1e2e', fg='#a6adc8').pack()
        
        # Фрейм формы
        form_frame = tk.Frame(main_container, bg='#313244', 
                             relief='flat', padx=30, pady=30)
        form_frame.pack(fill='x', pady=(0, 20))
        
        # Заголовок формы
        tk.Label(form_frame, text="Вход в систему", 
                font=("Segoe UI", 14, "bold"),
                bg='#313244', fg='#cdd6f4').pack(pady=(0, 25))
        
        # Поле логина
        login_frame = tk.Frame(form_frame, bg='#313244')
        login_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(login_frame, text="Имя пользователя", 
                font=self.custom_font, bg='#313244', fg='#a6adc8',
                anchor='w').pack(fill='x')
        
        self.login_entry = tk.Entry(login_frame, font=self.custom_font,
                                   bg='#45475a', fg='#cdd6f4',
                                   insertbackground='#cdd6f4',
                                   relief='flat', highlightthickness=1,
                                   highlightbackground='#585b70',
                                   highlightcolor='#89b4fa')
        self.login_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.login_entry.bind('<FocusIn>', lambda e: self.entry_focus_in(e, self.login_entry))
        self.login_entry.bind('<FocusOut>', lambda e: self.entry_focus_out(e, self.login_entry))
        
        # Поле пароля
        pass_frame = tk.Frame(form_frame, bg='#313244')
        pass_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(pass_frame, text="Пароль", 
                font=self.custom_font, bg='#313244', fg='#a6adc8',
                anchor='w').pack(fill='x')
        
        self.pass_entry = tk.Entry(pass_frame, font=self.custom_font,
                                  bg='#45475a', fg='#cdd6f4',
                                  insertbackground='#cdd6f4',
                                  relief='flat', highlightthickness=1,
                                  highlightbackground='#585b70',
                                  highlightcolor='#89b4fa',
                                  show='•')
        self.pass_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.pass_entry.bind('<FocusIn>', lambda e: self.entry_focus_in(e, self.pass_entry))
        self.pass_entry.bind('<FocusOut>', lambda e: self.entry_focus_out(e, self.pass_entry))
        
        # Кнопка показать/скрыть пароль
        self.show_pass_var = tk.BooleanVar()
        self.show_pass_btn = tk.Checkbutton(pass_frame, 
                                          text="Показать пароль",
                                          variable=self.show_pass_var,
                                          command=self.toggle_password,
                                          font=("Segoe UI", 9),
                                          bg='#313244', fg='#a6adc8',
                                          activebackground='#313244',
                                          activeforeground='#a6adc8',
                                          selectcolor='#313244')
        self.show_pass_btn.pack(anchor='w', pady=(5, 0))
        
        # Чекбокс "Запомнить меня"
        self.remember_var = tk.BooleanVar()
        tk.Checkbutton(form_frame, 
                      text="Запомнить меня",
                      variable=self.remember_var,
                      font=("Segoe UI", 9),
                      bg='#313244', fg='#a6adc8',
                      activebackground='#313244',
                      activeforeground='#a6adc8',
                      selectcolor='#313244').pack(anchor='w', pady=(0, 25))
        
        # Кнопка входа
        self.login_btn = tk.Button(form_frame, text="ВОЙТИ",
                                 font=("Segoe UI", 11, "bold"),
                                 bg='#89b4fa', fg='#1e1e2e',
                                 activebackground='#74c7ec',
                                 activeforeground='#1e1e2e',
                                 relief='flat',
                                 cursor='hand2',
                                 padx=30, pady=10,
                                 command=self.authenticate)
        self.login_btn.pack(fill='x', pady=(0, 15))
        
        # Ссылка "Забыли пароль?"
        tk.Label(form_frame, text="Забыли пароль?", 
                font=("Segoe UI", 9, "underline"),
                bg='#313244', fg='#89b4fa',
                cursor='hand2').pack()
        
        # Фрейм для дополнительных опций
        options_frame = tk.Frame(main_container, bg='#1e1e2e')
        options_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(options_frame, text="Нет аккаунта?", 
                font=self.custom_font, bg='#1e1e2e', fg='#a6adc8').pack(side='left')
        
        tk.Label(options_frame, text=" Зарегистрироваться", 
                font=("Segoe UI", 9, "bold", "underline"),
                bg='#1e1e2e', fg='#89b4fa',
                cursor='hand2').pack(side='left')
        
        # Информация о версии
        tk.Label(main_container, text="© 2024 Trade Pro Platform v2.1.4", 
                font=("Segoe UI", 8), bg='#1e1e2e', fg='#6c7086').pack(side='bottom', pady=10)
        
        # Стилизация при наведении
        self.setup_hover_effects()
        
        # Установить фокус на поле логина
        self.login_entry.focus_set()
        
    def setup_hover_effects(self):
        """Настройка эффектов при наведении"""
        self.login_btn.bind('<Enter>', lambda e: self.login_btn.config(bg='#74c7ec'))
        self.login_btn.bind('<Leave>', lambda e: self.login_btn.config(bg='#89b4fa'))
        
    def entry_focus_in(self, event, entry):
        """Эффект при фокусе на поле ввода"""
        entry.config(highlightbackground='#89b4fa')
        
    def entry_focus_out(self, event, entry):
        """Эффект при потере фокуса"""
        entry.config(highlightbackground='#585b70')
        
    def toggle_password(self):
        """Показать/скрыть пароль"""
        if self.show_pass_var.get():
            self.pass_entry.config(show='')
        else:
            self.pass_entry.config(show='•')
            
    def authenticate(self):
        """Аутентификация пользователя"""
        username = self.login_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Внимание", "Пожалуйста, заполните все поля")
            return
            
        # Здесь должна быть реальная логика аутентификации
        if username == "demo" and password == "demo123":
            messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
            # Здесь можно открыть основное окно торговой платформы
            self.open_trading_platform(username)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")
            
    def open_trading_platform(self, username):
        """Открытие основной платформы"""
        # Закрыть окно авторизации
        self.root.destroy()
        
        # Создать новое окно торговой платформы
        platform_root = tk.Tk()
        platform_root.title(f"Trade Pro Platform | {username}")
        platform_root.geometry('1200x800')
        platform_root.configure(bg='#1e1e2e')
        
        # Здесь можно добавить интерфейс торговой платформы
        tk.Label(platform_root, text=f"Добро пожаловать в торговую платформу, {username}!",
                font=("Segoe UI", 16, "bold"),
                bg='#1e1e2e', fg='#cdd6f4').pack(pady=50)
        
        platform_root.mainloop()

def main():
    root = tk.Tk()
    app = TradingAuthForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()