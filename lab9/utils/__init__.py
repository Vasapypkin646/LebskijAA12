# lab9_refactored/utils/__init__.py
"""
Модуль вспомогательных утилит.

Содержит:
- Классы исключений
- Вспомогательные функции
- Утилиты для работы с данными
"""

from .exceptions import (
    EmployeeNotFoundError,
    DepartmentNotFoundError,
    ProjectNotFoundError,
    InvalidStatusError,
    DuplicateIdError,
    InvalidDateError,
    InvalidSalaryError,
    InvalidInputError
)

from .helpers import (
    sort_by_key,
    compare_employees_by_name,
    compare_employees_by_salary,
    get_name_key,
    get_salary_key,
    get_department_name_key
)

__all__ = [
    
    'EmployeeNotFoundError',
    'DepartmentNotFoundError',
    'ProjectNotFoundError',
    'InvalidStatusError',
    'DuplicateIdError',
    'InvalidDateError',
    'InvalidSalaryError',
    'InvalidInputError',
    
    'sort_by_key',
    'compare_employees_by_name',
    'compare_employees_by_salary',
    'get_name_key',
    'get_salary_key',
    'get_department_name_key',
]