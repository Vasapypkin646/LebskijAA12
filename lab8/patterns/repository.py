from typing import List, Optional, Dict, Any
from .singleton import DatabaseConnection

class EmployeeRepository:
    """
    Реализация паттерна Repository для работы с данными сотрудников.
    Инкапсулирует логику доступа к базе данных.
    """
    
    def __init__(self):
        self._db = DatabaseConnection()
    
    def _employee_to_dict(self, employee) -> Dict[str, Any]:
        """Конвертирует объект сотрудника в словарь для БД"""
        employee_dict = employee.to_dict()
        
        # Добавляем специальные поля для разных типов сотрудников
        if hasattr(employee, 'bonus'):
            employee_dict['bonus'] = employee.bonus
        
        if hasattr(employee, '_Developer__tech_stack'):
            employee_dict['tech_stack'] = ', '.join(employee._Developer__tech_stack)
        
        if hasattr(employee, '_Developer__seniority_level'):
            employee_dict['seniority_level'] = employee._Developer__seniority_level
        
        if hasattr(employee, '_Saleperson__commission_rate'):
            employee_dict['commission_rate'] = employee._Saleperson__commission_rate
        
        if hasattr(employee, '_Saleperson__sales_volume'):
            employee_dict['sales_volume'] = employee._Saleperson__sales_volume
        
        return employee_dict
    
    def _dict_to_employee(self, row: Dict[str, Any]):
        """Создает объект сотрудника из данных БД"""
        # Импортируем классы из вашего Zadanie.py
        import sys
        sys.path.append('.')
        
        # Используем абсолютный импорт
        employee_data = {
            'id': row['id'],
            'name': row['name'],
            'department': row['department'],
            'base_salary': row['base_salary'],
            'type': row['type'],
            'skip_validation': True
        }
        
        employee_type = row['type']
        
        if employee_type == 'Manager' and row['bonus'] is not None:
            employee_data['bonus'] = row['bonus']
            # Создаем объект Manager динамически
            from Zadanie import Manager
            return Manager(**employee_data)
        
        elif employee_type == 'Developer':
            if row['tech_stack']:
                employee_data['tech_stack'] = row['tech_stack'].split(', ')
            if row['seniority_level']:
                employee_data['seniority_level'] = row['seniority_level']
            # Создаем объект Developer динамически
            from Zadanie import Developer
            return Developer(**employee_data)
        
        elif employee_type == 'Saleperson':
            if row['commission_rate'] is not None:
                employee_data['commission_rate'] = row['commission_rate']
            if row['sales_volume'] is not None:
                employee_data['sales_volume'] = row['sales_volume']
            # Создаем объект Saleperson динамически
            from Zadanie import Saleperson
            return Saleperson(**employee_data)
        
        else:
            # Создаем объект Employee динамически
            from Zadanie import Employee
            return Employee(**employee_data)
    
    def add(self, employee) -> bool:
        """Добавляет сотрудника в БД"""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            
            employee_dict = self._employee_to_dict(employee)
            
            cursor.execute('''
                INSERT OR REPLACE INTO employees 
                (id, name, department, base_salary, type, bonus, tech_stack, seniority_level, commission_rate, sales_volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                employee_dict['id'],
                employee_dict['name'],
                employee_dict['department'],
                employee_dict['base_salary'],
                employee_dict['type'],
                employee_dict.get('bonus'),
                employee_dict.get('tech_stack'),
                employee_dict.get('seniority_level'),
                employee_dict.get('commission_rate'),
                employee_dict.get('sales_volume')
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении сотрудника: {e}")
            return False
    
    def get(self, employee_id: int) -> Optional[Any]:
        """Получает сотрудника по ID"""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
            row = cursor.fetchone()
            
            if row:
                return self._dict_to_employee(dict(row))
            return None
            
        except Exception as e:
            print(f"Ошибка при получении сотрудника: {e}")
            return None
    
    def get_all(self) -> List[Any]:
        """Получает всех сотрудников"""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM employees ORDER BY id')
            rows = cursor.fetchall()
            
            return [self._dict_to_employee(dict(row)) for row in rows]
            
        except Exception as e:
            print(f"Ошибка при получении всех сотрудников: {e}")
            return []
    
    def update(self, employee) -> bool:
        """Обновляет данные сотрудника"""
        return self.add(employee)  # Используем INSERT OR REPLACE
    
    def delete(self, employee_id: int) -> bool:
        """Удаляет сотрудника по ID"""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Ошибка при удалении сотрудника: {e}")
            return False
    
    def find_by_department(self, department_name: str) -> List[Any]:
        """Находит сотрудников по отделу"""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM employees WHERE department = ? ORDER BY id', (department_name,))
            rows = cursor.fetchall()
            
            return [self._dict_to_employee(dict(row)) for row in rows]
            
        except Exception as e:
            print(f"Ошибка при поиске по отделу: {e}")
            return []
    
    def find_by_type(self, employee_type: str) -> List[Any]:
        """Находит сотрудников по типу"""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM employees WHERE type = ? ORDER BY id', (employee_type,))
            rows = cursor.fetchall()
            
            return [self._dict_to_employee(dict(row)) for row in rows]
            
        except Exception as e:
            print(f"Ошибка при поиске по типу: {e}")
            return []
    
    def get_total_salary_expenses(self) -> float:
        """Вычисляет общие затраты на зарплаты"""
        try:
            employees = self.get_all()
            return sum(emp.calculate_salary() for emp in employees)
            
        except Exception as e:
            print(f"Ошибка при расчете затрат: {e}")
            return 0.0