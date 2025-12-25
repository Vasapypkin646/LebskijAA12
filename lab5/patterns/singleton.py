import sqlite3
from typing import Optional

class DatabaseConnection:
    """
    Паттерн Singleton для управления подключением к базе данных.
    Гарантирует единственное подключение к SQLite БД в рамках приложения.
    """
    _instance = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.database_file = "employees.db"
        return cls._instance
    
    def get_connection(self) -> sqlite3.Connection:
        """Возвращает соединение с базой данных (создает при необходимости)"""
        if self._connection is None:
            self._connection = sqlite3.connect(self.database_file, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            self._create_tables()
        return self._connection
    
    def _create_tables(self):
        """Создает необходимые таблицы в БД"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица сотрудников
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                base_salary REAL NOT NULL,
                type TEXT NOT NULL,
                bonus REAL,
                tech_stack TEXT,
                seniority_level TEXT,
                commission_rate REAL,
                sales_volume REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
    
    def close_connection(self):
        """Закрывает соединение с базой данных"""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
    
    def __del__(self):
        """Деструктор для автоматического закрытия соединения"""
        self.close_connection()