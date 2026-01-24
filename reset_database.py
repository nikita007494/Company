# reset_database.py
from database import DatabaseManager
import hashlib

def reset_database():
    """Сброс базы данных до тестового состояния"""
    db = DatabaseManager()
    
    print("Сброс базы данных...")
    
    # Удаляем всех пользователей (осторожно!)
    db.cursor.execute("DELETE FROM users")
    print("Удалены все пользователи")
    
    # Добавляем тестовых пользователей
    test_users = [
        ('candidate', 'candidate123', 'Кандидат Тестовый', 'candidate@test.com', 'candidate'),
        ('consumer', 'consumer123', 'Потребитель Тест', 'consumer@test.com', 'consumer'),
        ('agent', 'agent123', 'Агент Тестов', 'agent@test.com', 'agent'),
        ('logistic', 'logistic123', 'Логист Тест', 'logistic@test.com', 'logistic'),
        ('admin', 'admin123', 'Администратор', 'admin@test.com', 'admin')
    ]
    
    for username, password, full_name, email, role in test_users:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        db.cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, email, role, created_at, is_active)
        VALUES (?, ?, ?, ?, ?, GETDATE(), 1)
        """, (username, password_hash, full_name, email, role))
        
        print(f"✅ Создан {username}: {password}")
    
    db.connection.commit()
    db.disconnect()
    print("\n✅ База данных сброшена!")
    print("\nТестовые учетные данные:")
    print("-" * 40)
    for username, password, _, _, _ in test_users:
        print(f"{username:10} / {password}")

if __name__ == "__main__":
    reset_database()