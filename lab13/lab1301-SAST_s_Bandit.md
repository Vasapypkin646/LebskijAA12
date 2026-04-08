# **Лабораторная работа 13. Часть 1: Статический анализ кода (SAST) с Bandit**

## **Тема:** Обнаружение и исправление уязвимостей на уровне исходного кода с использованием инструментов статического анализа.

### **Цель работы:**
Научиться использовать инструменты статического анализа безопасности (SAST) для выявления типовых уязвимостей (SQL-инъекции, hardcoded secrets, небезопасные функции) в Python-коде, интерпретировать отчеты и применять безопасные практики кодирования.

---

## **Задание: Анализ уязвимого веб-приложения на Flask**

Вам предоставлен прототип простого веб-приложения для управления пользователями, содержащий несколько типовых уязвимостей. Ваша задача — проанализировать код с помощью Bandit, найти уязвимости и исправить их.

### **1. Настройка проекта**

Создайте директорию проекта и виртуальное окружение:

```bash
# Создание директории
mkdir lab4-sast
cd lab4-sast

# Создание виртуального окружения Python
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# Установка необходимых пакетов
pip install flask bandit pytest
```

### **2. Базовый код (70% предоставляется)**

**Файл: `app.py`**

```python
from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

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

# Глобальный API ключ (hardcoded — это уязвимость!)
API_KEY = "тут был API_KEY"

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
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
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
    query = f"SELECT * FROM users WHERE username LIKE '%{username}%'"
    cursor.execute(query)
    
    users = cursor.fetchall()
    conn.close()
    
    result = [{"id": u[0], "username": u[1], "email": u[2]} for u in users]
    return jsonify(result)

@app.route('/api/data')
def get_data():
    """Эндпоинт с секретным ключом в коде"""
    # TODO: Убрать hardcoded ключ, использовать переменную окружения
    return jsonify({"api_key": API_KEY, "message": "This is sensitive data"})

@app.route('/execute')
def execute_command():
    """Эндпоинт для выполнения системных команд — содержит Command Injection"""
    cmd = request.args.get('cmd', 'echo "Hello"')
    
    # ❌ УЯЗВИМЫЙ КОД: выполнение пользовательского ввода
    # TODO: Исправить — либо убрать эндпоинт, либо добавить allow-list
    import subprocess
    result = subprocess.check_output(cmd, shell=True)
    
    return jsonify({"output": result.decode()})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### **3. Задания для самостоятельного выполнения (30% дописать)**

#### **A. Запуск Bandit и анализ результатов (обязательно)**

Запустите Bandit для анализа кода и изучите отчет:

```bash
# Запуск Bandit с выводом результатов
bandit app.py -f html -o bandit_report.html

# Или более детальный вывод в консоль
bandit app.py -r -f json -o bandit_report.json
bandit app.py -r -f txt
```

**Вопросы для анализа (ответить в отчете):**
1. Какие уязвимости обнаружил Bandit? Перечислите с указанием строк кода.
2. Какие типы уязвимостей (по классификации Bandit) были найдены?
3. Какие уязвимости Bandit не обнаружил? Почему?

#### **B. Исправление SQL-инъекций (обязательно)**

Исправьте эндпоинты `/user` и `/search`, заменив конкатенацию строк на параметризованные запросы.

```python
# Шаблон для исправления:
@app.route('/user')
def get_user_fixed():
    user_id = request.args.get('id')
    
    if not user_id:
        return jsonify({"error": "Missing id parameter"}), 400
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # TODO: Реализовать параметризованный запрос
    # Используйте ? в качестве плейсхолдера
    # query = "SELECT * FROM users WHERE id = ?"
    # cursor.execute(query, (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"id": user[0], "username": user[1], "email": user[2]})
    return jsonify({"error": "User not found"}), 404
```

**Проверка исправления:**
```bash
# После исправления, попробуйте SQL-инъекцию:
curl "http://localhost:5000/user?id=1 OR 1=1"
# Должен вернуть только пользователя с id=1, а не всех

# Попробуйте некорректный ввод:
curl "http://localhost:5000/user?id=abc"
# Должен вернуть ошибку, а не выполнить SQL-запрос
```

#### **C. Удаление hardcoded секретов (обязательно)**

1. Удалите hardcoded API-ключ из кода.
2. Используйте переменные окружения для хранения секретов.
3. Добавьте проверку наличия переменной окружения при запуске.

```python
# Шаблон для исправления:
import os

# TODO: Заменить hardcoded ключ на чтение из окружения
API_KEY = os.environ.get('API_KEY')

# Добавить проверку при запуске
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

**Запуск с переменной окружения:**
```bash
export API_KEY="your-secure-key-here"
python app.py
```

#### **D. Исправление Command Injection (обязательно)**

Эндпоинт `/execute` выполняет произвольные команды, переданные пользователем. Это критическая уязвимость.

**Варианты исправления:**
1. **Полностью удалить эндпоинт** (если он не нужен).
2. **Ограничить разрешенные команды через allow-list** (если эндпоинт необходим).

```python
# Шаблон для исправления:
@app.route('/execute')
def execute_command_fixed():
    cmd = request.args.get('cmd', '')
    
    # TODO: Реализовать allow-list разрешенных команд
    # ALLOWED_COMMANDS = ['echo', 'date', 'whoami']
    # Проверить, что cmd начинается с разрешенной команды
    # Никогда не использовать shell=True с пользовательским вводом
    
    # Небезопасно:
    # result = subprocess.check_output(cmd, shell=True)
    
    # Безопасно (с allow-list и без shell):
    # result = subprocess.check_output(cmd.split())
```

#### **E. Дополнительное задание: Настройка Bandit в CI/CD (дополнительно)**

Создайте конфигурационный файл для Bandit, который будет игнорировать определенные уязвимости или устанавливать пороги.

**Файл: `.bandit`**
```yaml
# TODO: Создать конфигурацию для Bandit
# - Установить порог серьезности (например, MEDIUM)
# - Исключить определенные проверки (skips)
# - Указать пути для исключения
```

Запустите Bandit с конфигурацией:
```bash
bandit -c .bandit app.py
```

### **4. Запуск и проверка**

```bash
# Запуск приложения
python app.py

# Тестирование исправленных эндпоинтов
# Проверка SQL-инъекции
curl "http://localhost:5000/user?id=1 OR 1=1"

# Проверка поиска
curl "http://localhost:5000/search?username=admin"

# Проверка API эндпоинта (должен требовать API_KEY)
curl "http://localhost:5000/api/data"

# Проверка исправленного command injection
curl "http://localhost:5000/execute?cmd=ls"  # Должен быть заблокирован или ограничен

# Повторный запуск Bandit для проверки исправлений
bandit app.py
```

### **5. Что должно быть в отчёте:**

1. **Исходный код:**
   - Файл `app.py` с исправленными уязвимостями.
   - Файл `.bandit` (если выполнено доп. задание).

2. **Скриншоты:**
   - Отчет Bandit до исправлений (bandit_report.html или вывод в консоли).
   - Отчет Bandit после исправлений (показать, что количество уязвимостей уменьшилось).
   - Примеры успешных запросов к исправленному API.

3. **Ответы на вопросы:**
   - Какие уязвимости обнаружил Bandit в исходном коде? Укажите конкретные строки и типы уязвимостей.
   - Почему параметризованные запросы защищают от SQL-инъекций? Объясните механизм.
   - В чем разница между `subprocess.run(cmd, shell=True)` и `subprocess.run(cmd.split())` с точки зрения безопасности?
   - Какие уязвимости статический анализатор (SAST) не может обнаружить? Приведите примеры.

### **6. Критерии оценивания:**

#### **Обязательные требования (минимум для зачета):**
- **SQL-инъекции исправлены:** Эндпоинты `/user` и `/search` используют параметризованные запросы.
- **Hardcoded secrets удалены:** API-ключ читается из переменной окружения, проверка наличия ключа при запуске.
- **Command Injection устранен:** Эндпоинт `/execute` либо удален, либо использует allow-list и не использует `shell=True`.
- **Bandit запущен:** Предоставлен отчет до и после исправлений.

#### **Дополнительные критерии (для повышения оценки):**
- **Конфигурация Bandit:** Создан файл `.bandit` с настройкой порога серьезности.
- **Дополнительные проверки:** Добавлены обработка ошибок и валидация входных данных.
- **Документация:** В коде добавлены комментарии, объясняющие безопасные практики.

#### **Неприемлемые ошибки:**
- Оставлены SQL-инъекции в коде.
- Использование `shell=True` с пользовательским вводом.
- Hardcoded секреты в коде.

### **7. Полезные команды для Ubuntu:**

```bash
# Запуск Bandit в разных форматах
bandit app.py -f html -o report.html
bandit app.py -f json -o report.json
bandit app.py -f txt

# Запуск с определенным уровнем серьезности
bandit app.py -ll  # только низкий уровень
bandit app.py -l   # только средний и выше

# Исключение определенных проверок
bandit app.py -s B608  # исключить проверку B608 (hardcoded sql)

# Просмотр всех доступных проверок
bandit -l

# Управление переменными окружения
echo $API_KEY
export API_KEY="new-key"
unset API_KEY

# Проверка SQL-инъекции через curl
curl -v "http://localhost:5000/user?id=1' OR '1'='1"
```

### **8. Структура проекта:**

```
lab4-sast/
├── venv/
├── app.py
├── users.db (создается автоматически)
├── .bandit (опционально)
└── bandit_report.html (создается при запуске)
```

### **9. Советы по выполнению:**

1. **Запускайте Bandit после каждого изменения**, чтобы видеть прогресс.
2. **Не удаляйте эндпоинты без необходимости** — лучше исправлять, но если эндпоинт не нужен по заданию, его можно удалить с комментарием.
3. **Используйте переменные окружения** для хранения ключей — это стандартная практика в продакшене.
4. **Тестируйте SQL-инъекции вручную**, чтобы убедиться, что исправление работает.
5. **Обратите внимание на импорты** — после исправления убедитесь, что все необходимые модули импортированы.

**Примечание:** В задании предоставлено ~70% кода. Ваша задача — понять логику работы, выявить уязвимости с помощью Bandit и дописать недостающие ~30% безопасных решений.