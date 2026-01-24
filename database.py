import pyodbc
import hashlib
import logging
from datetime import datetime

class DatabaseManager:
    def __init__(self, server='DESKTOP-HKB5J94', database='TradingPlatformDB'):
        """
        Инициализация подключения к SQL Server
        
        Args:
            server: Имя сервера (DESKTOP-HKB5J94)
            database: Имя базы данных (TradingPlatformDB)
        """
        self.server = server
        self.database = database
        self.connection = None
        self.cursor = None
        
        # Настройка логирования
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Строка подключения для Windows Authentication
        self.connection_string = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'Trusted_Connection=yes;'
        )
        
        # Подключаемся к базе
        self.connect()
    
    def connect(self):
        """Установка подключения к SQL Server"""
        try:
            self.connection = pyodbc.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            self.logger.info(f"Успешное подключение к SQL Server {self.server}, база {self.database}")
            
        except Exception as e:
            self.logger.error(f"Ошибка подключения к SQL Server: {e}")
            raise
    
    def disconnect(self):
        """Закрытие подключения"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.logger.info("Соединение с базой данных закрыто")
    
    def hash_password(self, password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, full_name, email, role, phone=None):
        """
        Регистрация нового пользователя в таблице users
        
        Args:
            username: Имя пользователя
            password: Пароль (будет хеширован)
            full_name: Полное имя
            email: Email
            role: Роль пользователя
            phone: Телефон (опционально)
        
        Returns:
            tuple: (success, message, user_id)
        """
        try:
            # Проверяем существование пользователя
            self.cursor.execute(
                "SELECT id FROM users WHERE username = ? OR email = ?",
                (username, email)
            )
            
            if self.cursor.fetchone():
                return False, "Пользователь с таким именем или email уже существует", None
            
            # Хешируем пароль
            password_hash = self.hash_password(password)
            
            # Вставляем нового пользователя
            insert_query = """
            INSERT INTO users (username, password_hash, full_name, email, role, phone, created_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, GETDATE(), 1)
            """
            
            self.cursor.execute(insert_query, 
                              (username, password_hash, full_name, email, role, phone))
            
            # Получаем ID нового пользователя
            self.cursor.execute("SELECT SCOPE_IDENTITY()")
            user_id = self.cursor.fetchone()[0]
            
            # Логируем регистрацию
            self.log_auth_action(None, username, 'registration')
            
            self.connection.commit()
            
            self.logger.info(f"Зарегистрирован новый пользователь: {username} (ID: {user_id})")
            
            return True, "Регистрация успешно завершена", user_id
            
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка регистрации пользователя: {e}")
            return False, f"Ошибка базы данных: {str(e)}", None
    
    def authenticate_user(self, username, password):
        """
        Аутентификация пользователя
        
        Args:
            username: Имя пользователя
            password: Пароль
        
        Returns:
            tuple: (success, message, user_data)
        """
        try:
            # Ищем пользователя
            query = """
            SELECT id, username, password_hash, full_name, email, role, is_active
            FROM users 
            WHERE username = ?
            """
            
            self.cursor.execute(query, (username,))
            user = self.cursor.fetchone()
            
            if not user:
                self.log_auth_action(None, username, 'login_failed')
                return False, "Пользователь не найден", None
            
            user_id, db_username, db_password_hash, full_name, email, role, is_active = user
            
            # Проверяем активность аккаунта
            if not is_active:
                return False, "Аккаунт деактивирован. Обратитесь к администратору", None
            
            # Проверяем пароль
            input_password_hash = self.hash_password(password)
            
            if input_password_hash != db_password_hash:
                self.log_auth_action(user_id, username, 'login_failed')
                return False, "Неверный пароль", None
            
            # Обновляем время последнего входа
            update_query = """
            UPDATE users 
            SET last_login = GETDATE()
            WHERE id = ?
            """
            self.cursor.execute(update_query, (user_id,))
            
            # Логируем успешный вход
            self.log_auth_action(user_id, username, 'login_success')
            
            self.connection.commit()
            
            # Формируем данные пользователя
            user_data = {
                'id': user_id,
                'username': db_username,
                'name': full_name,
                'email': email,
                'role': role,
                'is_active': is_active
            }
            
            self.logger.info(f"Успешная аутентификация пользователя: {username}")
            
            return True, "Аутентификация успешна", user_data
            
        except Exception as e:
            self.logger.error(f"Ошибка аутентификации: {e}")
            return False, f"Ошибка базы данных: {str(e)}", None
    
    def get_all_users(self):
        """Получение списка всех пользователей"""
        try:
            query = """
            SELECT id, username, full_name, email, role, 
                   CONVERT(varchar, created_at, 120) as created_at,
                   CONVERT(varchar, last_login, 120) as last_login,
                   is_active
            FROM users
            ORDER BY created_at DESC
            """
            
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            users = []
            
            for row in self.cursor.fetchall():
                user_dict = dict(zip(columns, row))
                users.append(user_dict)
            
            return users
            
        except Exception as e:
            self.logger.error(f"Ошибка получения пользователей: {e}")
            return []
    
    def get_user_by_username(self, username):
        """Получение информации о пользователе по имени"""
        try:
            query = """
            SELECT id, username, full_name, email, role, phone,
                   CONVERT(varchar, created_at, 120) as created_at,
                   CONVERT(varchar, last_login, 120) as last_login,
                   is_active
            FROM users 
            WHERE username = ?
            """
            
            self.cursor.execute(query, (username,))
            row = self.cursor.fetchone()
            
            if row:
                columns = [column[0] for column in self.cursor.description]
                return dict(zip(columns, row))
            return None
            
        except Exception as e:
            self.logger.error(f"Ошибка получения пользователя: {e}")
            return None
    
    def update_user_profile(self, user_id, **kwargs):
        """Обновление профиля пользователя"""
        try:
            # Формируем SQL запрос
            set_clauses = []
            params = []
            
            for key, value in kwargs.items():
                if value is not None:
                    set_clauses.append(f"{key} = ?")
                    params.append(value)
            
            if not set_clauses:
                return False, "Нет данных для обновления"
            
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = ?"
            
            self.cursor.execute(query, params)
            self.connection.commit()
            
            return True, "Профиль успешно обновлен"
            
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка обновления профиля: {e}")
            return False, f"Ошибка обновления: {str(e)}"
    
    def log_auth_action(self, user_id, username, action):
        """
        Логирование действий авторизации
        (Предполагаем, что у вас есть таблица auth_logs)
        """
        try:
            # Проверяем существование таблицы auth_logs
            self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='auth_logs' AND xtype='U')
            CREATE TABLE auth_logs (
                id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT NULL,
                username VARCHAR(50),
                ip_address VARCHAR(45),
                action VARCHAR(20),
                timestamp DATETIME DEFAULT GETDATE()
            )
            """)
            
            # Вставляем запись в логи
            insert_query = """
            INSERT INTO auth_logs (user_id, username, action)
            VALUES (?, ?, ?)
            """
            
            self.cursor.execute(insert_query, (user_id, username, action))
            self.connection.commit()
            
        except Exception as e:
            self.logger.error(f"Ошибка логирования: {e}")
    
    def check_user_exists(self, username, email):
        """Проверка существования пользователя"""
        try:
            self.cursor.execute(
                "SELECT id FROM users WHERE username = ? OR email = ?",
                (username, email)
            )
            return self.cursor.fetchone() is not None
        except Exception as e:
            self.logger.error(f"Ошибка проверки пользователя: {e}")
            return False
    
    def get_user_stats(self):
        """Получение статистики пользователей"""
        try:
            stats = {}
            
            # Общее количество пользователей
            self.cursor.execute("SELECT COUNT(*) FROM users")
            stats['total_users'] = self.cursor.fetchone()[0]
            
            # Количество по ролям
            self.cursor.execute("""
            SELECT role, COUNT(*) as count 
            FROM users 
            WHERE is_active = 1 
            GROUP BY role
            """)
            
            role_stats = {}
            for row in self.cursor.fetchall():
                role_stats[row[0]] = row[1]
            stats['by_role'] = role_stats
            
            # Активные пользователи
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            stats['active_users'] = self.cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Ошибка получения статистики: {e}")
            return {}
    
    def __del__(self):
        """Деструктор - закрываем соединение"""
        self.disconnect()


# Синглтон для доступа к базе данных
class DatabaseConnection:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DatabaseManager(
                server='DESKTOP-HKB5J94',
                database='TradingPlatformDB'
            )
        return cls._instance
    
    @classmethod
    def close_connection(cls):
        if cls._instance:
            cls._instance.disconnect()
            cls._instance = None


# Функция для тестирования подключения
def test_connection():
    """Тестирование подключения к базе данных"""
    try:
        db = DatabaseManager()
        print(f"✅ Успешное подключение к SQL Server!")
        
        # Проверяем структуру таблицы users
        db.cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'users'
        ORDER BY ORDINAL_POSITION
        """)
        
        print("\n📊 Структура таблицы users:")
        columns = db.cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        # Проверяем количество пользователей
        db.cursor.execute("SELECT COUNT(*) FROM users")
        count = db.cursor.fetchone()[0]
        print(f"\n👥 Количество пользователей в базе: {count}")
        
        db.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print(f"Строка подключения: {db.connection_string if 'db' in locals() else 'Не создана'}")
        return False


if __name__ == "__main__":
    # Тестирование подключения
    if test_connection():
        # Тест регистрации (закомментируйте, если не нужно)
        try:
            db = DatabaseManager()
            success, message, user_id = db.register_user(
                username='test_user_py',
                password='Test123!',
                full_name='Тест Python',
                email='test_py@example.com',
                role='candidate',
                phone='+79991234567'
            )
            
            if success:
                print(f"✅ Тестовая регистрация успешна! ID: {user_id}")
            else:
                print(f"⚠️ Тестовая регистрация не удалась: {message}")
            
            db.disconnect()
            
        except Exception as e:
            print(f"❌ Ошибка тестирования: {e}")