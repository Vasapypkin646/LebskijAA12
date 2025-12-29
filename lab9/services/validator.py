"""
Модуль валидации данных.
"""

from datetime import datetime
from typing import Set, List, Any
from utils.exceptions import (
    DuplicateIdError, InvalidSalaryError, InvalidDateError,
    InvalidStatusError, InvalidInputError
)


class DataValidator:
    """Базовый класс валидации данных."""
    
    @staticmethod
    def validate_not_none(value: Any, field_name: str) -> None:
        """Проверка, что значение не None."""
        if value is None:
            raise InvalidInputError(f"{field_name} не может быть None")
    
    @staticmethod
    def validate_string_not_empty(value: str, field_name: str) -> None:
        """Проверка, что строка не пустая."""
        if not value or not isinstance(value, str) or value.strip() == "":
            raise InvalidInputError(f"{field_name} должен быть непустой строкой")
    
    @staticmethod
    def validate_positive_integer(value: int, field_name: str) -> None:
        """Проверка положительного целого числа."""
        if not isinstance(value, int) or value <= 0:
            raise InvalidInputError(f"{field_name} должен быть положительным целым числом")


class EmployeeValidator(DataValidator):
    """Валидатор данных сотрудника."""
    
    @staticmethod
    def validate_employee_id(employee_id: int, existing_ids: Set[int]) -> None:
        """Валидация ID сотрудника."""
        DataValidator.validate_positive_integer(employee_id, "ID сотрудника")
        
        if employee_id in existing_ids:
            raise DuplicateIdError(f"Сотрудник с ID {employee_id} уже существует")
    
    @staticmethod
    def validate_name(name: str) -> None:
        """Валидация имени сотрудника."""
        DataValidator.validate_string_not_empty(name, "Имя сотрудника")
    
    @staticmethod
    def validate_salary(salary: float) -> None:
        """Валидация зарплаты."""
        if not isinstance(salary, (int, float)) or salary < 0:
            raise InvalidSalaryError(f"Некорректная зарплата: {salary}")
        
        if salary > 1_000_000:
            raise InvalidSalaryError(f"Зарплата {salary} превышает максимально допустимую")
    
    @staticmethod
    def validate_department(department: str) -> None:
        """Валидация отдела."""
        DataValidator.validate_string_not_empty(department, "Отдел")


class ProjectValidator(DataValidator):
    """Валидатор данных проекта."""
    
    @staticmethod
    def validate_project_id(project_id: str, existing_ids: Set[str]) -> None:
        """Валидация ID проекта."""
        DataValidator.validate_string_not_empty(project_id, "ID проекта")
        
        if project_id in existing_ids:
            raise DuplicateIdError(f"Проект с ID {project_id} уже существует")
    
    @staticmethod
    def validate_date(date_str: str) -> None:
        """Валидация даты."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise InvalidDateError(f"Некорректный формат даты: {date_str}. Ожидается YYYY-MM-DD")
    
    @staticmethod
    def validate_status(status: str, valid_statuses: List[str]) -> None:
        """Валидация статуса."""
        if status not in valid_statuses:
            raise InvalidStatusError(f"Недопустимый статус: '{status}'. Допустимые статусы: {valid_statuses}")