from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os


# TODO: Заменить hardcoded ключ на чтение из окружения
API_KEY = os.environ.get('API_KEY')

# Добавить проверку при запуске
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
    
app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Добавляем тестового пользователя
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password) VALUES (1, 'admin', 'admin@example.com', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password) VALUES (2, 'user', 'user@example.com', 'user123')")
    
    conn.commit()
    conn.close()

# HTML шаблон для главной страницы
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>User Management</title>
</head>
<body>
    <h1>User Management System</h1>
    <form action="/user" method="GET">
        <label>User ID:</label>
        <input type="text" name="id">
        <button type="submit">Get User</button>
    </form>
    
    <form action="/search" method="GET">
        <label>Search by username:</label>
        <input type="text" name="username">
        <button type="submit">Search</button>
    </form>
    
    <div id="result">
        {content}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE.format(content="<p>Enter user ID or search by username</p>"))

@app.route('/user')
def get_user():
    """Получение пользователя по ID — содержит SQL-инъекцию"""
    user_id = request.args.get('id')
    
    if not user_id:
        return jsonify({"error": "Missing id parameter"}), 400
    
    # ❌ УЯЗВИМЫЙ КОД: прямая конкатенация строк
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # TODO: Исправить SQL-инъекцию, используя параметризованный запрос
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"id": user[0], "username": user[1], "email": user[2]})
    return jsonify({"error": "User not found"}), 404

@app.route('/search')
def search_users():
    """Поиск пользователей по имени — содержит SQL-инъекцию"""
    username = request.args.get('username', '')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # ❌ УЯЗВИМЫЙ КОД: прямая конкатенация строк
    # TODO: Исправить SQL-инъекцию
    
    query = "SELECT * FROM users WHERE username LIKE ?"
    cursor.execute(query, (f'%{username}%',))
    
    users = cursor.fetchall()
    conn.close()
    
    result = [{"id": u[0], "username": u[1], "email": u[2]} for u in users]
    return jsonify(result)

@app.route('/api/data')
def get_data():
    """Эндпоинт с секретным ключом в коде"""
    # TODO: Убрать hardcoded ключ, использовать переменную окружения
    return jsonify({"message": "This is sensitive data"})

@app.route('/execute')
def execute_command():
    """Эндпоинт для выполнения системных команд — содержит Command Injection"""
    cmd = request.args.get('cmd', 'echo "Hello"')
    
    # ❌ УЯЗВИМЫЙ КОД: выполнение пользовательского ввода
    # TODO: Исправить — либо убрать эндпоинт, либо добавить allow-list
    
    ALLOWED_COMMANDS = ['echo', 'date', 'whoami']
    cmd_parts = cmd.split()
    if not cmd_parts or cmd_parts[0] not in ALLOWED_COMMANDS:
        return jsonify({"error": "Command not allowed"}), 403

    import subprocess
    try:
        result = subprocess.check_output(cmd_parts, stderr=subprocess.STDOUT, timeout=5)
        return jsonify({"output": result.decode()})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output.decode()}), 400

if __name__ == '__main__':
    init_db()
    import os

if __name__ == '__main__':
    init_db()
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    app.run(debug=False, host=host, port=5000)