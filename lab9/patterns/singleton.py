"""
Паттерн Singleton.
"""

import sqlite3
from typing import Optional


class DatabaseConnection:
    """Singleton для подключения к базе данных."""
    
    _instance: Optional['DatabaseConnection'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.database_file = "company_database.db"
            self._connection: Optional[sqlite3.Connection] = None
            self._initialized = True
    
    def connect(self) -> sqlite3.Connection:
        """Получить подключение к базе данных."""
        if self._connection is None:
            self._connection = sqlite3.connect(self.database_file)
        return self._connection
    
    def close(self) -> None:
        """Закрыть подключение."""
        if self._connection:
            self._connection.close()
            self._connection = None