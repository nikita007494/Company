# generate_hashes.py
import hashlib

# Тестовые пользователи и пароли
users = [
    ('candidate', 'candidate123'),
    ('consumer', 'consumer123'),
    ('agent', 'agent123'),
    ('logistic', 'logistic123'),
    ('admin', 'admin123')
]

print("SQL-команды для обновления паролей в базе:\n")
print("-- Копируйте и выполняйте в SSMS\n")

for username, password in users:
    # Генерируем SHA-256 хеш
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    sql = f"""
-- Для пользователя: {username} (пароль: {password})
UPDATE users 
SET password_hash = '{password_hash}'
WHERE username = '{username}';

-- ИЛИ если пользователя нет:
IF NOT EXISTS (SELECT 1 FROM users WHERE username = '{username}')
BEGIN
    INSERT INTO users (username, password_hash, full_name, email, role, created_at, is_active)
    VALUES (
        '{username}',
        '{password_hash}',
        'Тестовый {username}',
        '{username}@example.com',
        '{username if username != "admin" else "admin"}',
        GETDATE(),
        1
    );
END
GO
"""
    print(sql)
    print("-" * 80)

print("\nГотовые хеши SHA-256:")
print("-" * 50)
for username, password in users:
    hash_value = hashlib.sha256(password.encode()).hexdigest()
    print(f"{username:10} | {hash_value}")