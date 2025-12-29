"""
Модуль класса отдела.
"""

from __future__ import annotations
from typing import List, Dict, Iterator, Optional, Any
import json

from entities.employee import AbstractEmployee
from services.validator import DataValidator
from utils.exceptions import EmployeeNotFoundError
from services.logger import Logger


class Department:
    """Класс отдела компании."""
    
    def __init__(self, name: str):
        """Инициализация отдела.
        
        Args:
            name: Название отдела
        """
        DataValidator.validate_string_not_empty(name, "Название отдела")
        
        self._name = name
        self._employees: List[AbstractEmployee] = []
        self._logger = Logger()
        
        self._logger.log(f"Создан отдел: {name}")
    
    @property
    def name(self) -> str:
        """Название отдела."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Установить название отдела."""
        DataValidator.validate_string_not_empty(value, "Название отдела")
        old_name = self._name
        self._name = value
        self._logger.log(f"Отдел переименован: {old_name} -> {value}")
    
    def add_employee(self, employee: AbstractEmployee) -> None:
        """Добавить сотрудника в отдел.
        
        Args:
            employee: Сотрудник для добавления
            
        Raises:
            ValueError: Если сотрудник уже в отделе
        """
        if employee in self._employees:
            raise ValueError(f"Сотрудник {employee.name} уже в отделе {self.name}")
        
        self._employees.append(employee)
        self._logger.log(f"Сотрудник {employee.name} добавлен в отдел {self.name}")
    
    def remove_employee(self, employee_id: int) -> AbstractEmployee:
        """Удалить сотрудника по ID.
        
        Args:
            employee_id: ID сотрудника
            
        Returns:
            Удаленный сотрудник
            
        Raises:
            EmployeeNotFoundError: Если сотрудник не найден
        """
        for i, employee in enumerate(self._employees):
            if employee.id == employee_id:
                removed = self._employees.pop(i)
                self._logger.log(f"Сотрудник {removed.name} удален из отдела {self.name}")
                return removed
        
        raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в отделе {self.name}")
    
    def get_employees(self) -> List[AbstractEmployee]:
        """Получить список всех сотрудников."""
        return self._employees.copy()
    
    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Найти сотрудника по ID.
        
        Args:
            employee_id: ID сотрудника
            
        Returns:
            Сотрудник или None если не найден
        """
        for employee in self._employees:
            if employee.id == employee_id:
                return employee
        return None
    
    def calculate_total_salary(self) -> float:
        """Рассчитать общую зарплату отдела."""
        return sum(emp.calculate_salary() for emp in self._employees)
    
    def get_employee_count_by_type(self) -> Dict[str, int]:
        """Получить количество сотрудников по типам."""
        counts: Dict[str, int] = {}
        for employee in self._employees:
            emp_type = employee.__class__.__name__
            counts[emp_type] = counts.get(emp_type, 0) + 1
        return counts
    
    def has_employees(self) -> bool:
        """Проверить, есть ли сотрудники в отделе."""
        return len(self._employees) > 0
    
    def __len__(self) -> int:
        """Количество сотрудников в отделе."""
        return len(self._employees)
    
    def __getitem__(self, key: int) -> AbstractEmployee:
        """Получить сотрудника по индексу."""
        return self._employees[key]
    
    def __contains__(self, employee: AbstractEmployee) -> bool:
        """Проверить наличие сотрудника в отделе."""
        return employee in self._employees
    
    def __iter__(self) -> Iterator[AbstractEmployee]:
        """Итерация по сотрудникам отдела."""
        return iter(self._employees)
    
    def __str__(self) -> str:
        """Строковое представление отдела."""
        return f"Отдел: {self.name}, Сотрудников: {len(self)}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь."""
        return {
            'name': self.name,
            'employee_count': len(self),
            'total_salary': self.calculate_total_salary(),
            'employee_count_by_type': self.get_employee_count_by_type(),
            'employees': [emp.to_dict() for emp in self._employees]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Department:
        """Создать из словаря."""
        department = cls(data['name'])
        for emp_data in data['employees']:
            employee = AbstractEmployee.from_dict(emp_data)
            department.add_employee(employee)
        return department
    
    def save_to_file(self, filename: str) -> None:
        """Сохранить отдел в файл."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.to_dict(), file, ensure_ascii=False, indent=2)
            self._logger.log(f"Отдел {self.name} сохранен в файл {filename}")
        except Exception as e:
            self._logger.log(f"Ошибка при сохранении отдела: {e}", level='ERROR')
            raise
    
    @classmethod
    def load_from_file(cls, filename: str) -> Department:
        """Загрузить отдел из файла."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return cls.from_dict(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не найден")
        except Exception as e:
            raise ValueError(f"Ошибка при загрузке отдела: {e}")