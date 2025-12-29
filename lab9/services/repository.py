"""
Паттерн Repository.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import sqlite3
from entities.employee import AbstractEmployee
from patterns.singleton import DatabaseConnection


class IEmployeeRepository(ABC):
    """Интерфейс репозитория сотрудников."""
    
    @abstractmethod
    def add(self, employee: AbstractEmployee) -> bool:
        """Добавить сотрудника."""
        pass
    
    @abstractmethod
    def get(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Получить сотрудника по ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[AbstractEmployee]:
        """Получить всех сотрудников."""
        pass
    
    @abstractmethod
    def update(self, employee: AbstractEmployee) -> bool:
        """Обновить данные сотрудника."""
        pass
    
    @abstractmethod
    def delete(self, employee_id: int) -> bool:
        """Удалить сотрудника."""
        pass


class EmployeeRepository(IEmployeeRepository):
    """Реализация репозитория сотрудников."""
    
    def __init__(self):
        self._db = DatabaseConnection()
        self._init_database()
    
    def _init_database(self) -> None:
        """Инициализировать таблицу сотрудников."""
        conn = self._db.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                base_salary REAL NOT NULL,
                type TEXT NOT NULL,
                bonus REAL DEFAULT 0,
                tech_stack TEXT DEFAULT '',
                seniority_level TEXT DEFAULT 'junior',
                commission_rate REAL DEFAULT 0,
                sales_volume REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
    
    def add(self, employee: AbstractEmployee) -> bool:
        """Добавить сотрудника в БД."""
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            data = employee.to_dict()
            
            cursor.execute('''
                INSERT OR REPLACE INTO employees 
                (id, name, department, base_salary, type, bonus, tech_stack, 
                 seniority_level, commission_rate, sales_volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['id'],
                data['name'],
                data['department'],
                data['base_salary'],
                data['type'],
                data.get('bonus', 0),
                ','.join(data.get('tech_stack', [])),
                data.get('seniority_level', 'junior'),
                data.get('commission_rate', 0),
                data.get('sales_volume', 0)
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении сотрудника: {e}")
            return False
    
    def get(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Получить сотрудника из БД."""
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            data = {
                'id': row[0],
                'name': row[1],
                'department': row[2],
                'base_salary': row[3],
                'type': row[4],
                'bonus': row[5],
                'tech_stack': row[6].split(',') if row[6] else [],
                'seniority_level': row[7],
                'commission_rate': row[8],
                'sales_volume': row[9]
            }
            
            from patterns.factory import EmployeeFactory
            return EmployeeFactory.create_from_dict(data)
            
        except Exception as e:
            print(f"Ошибка при получении сотрудника: {e}")
            return None
    
    def get_all(self) -> List[AbstractEmployee]:
        """Получить всех сотрудников из БД."""
        employees = []
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM employees')
            rows = cursor.fetchall()
            
            from patterns.factory import EmployeeFactory
            
            for row in rows:
                data = {
                    'id': row[0],
                    'name': row[1],
                    'department': row[2],
                    'base_salary': row[3],
                    'type': row[4],
                    'bonus': row[5],
                    'tech_stack': row[6].split(',') if row[6] else [],
                    'seniority_level': row[7],
                    'commission_rate': row[8],
                    'sales_volume': row[9]
                }
                
                employee = EmployeeFactory.create_from_dict(data)
                employees.append(employee)
                
        except Exception as e:
            print(f"Ошибка при получении всех сотрудников: {e}")
        
        return employees
    
    def update(self, employee: AbstractEmployee) -> bool:
        """Обновить данные сотрудника в БД."""
        # Используем add с REPLACE
        return self.add(employee)
    
    def delete(self, employee_id: int) -> bool:
        """Удалить сотрудника из БД."""
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
            conn.commit()
            
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Ошибка при удалении сотрудника: {e}")
            return False