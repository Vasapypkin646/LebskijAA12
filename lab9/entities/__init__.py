"""
Модуль сущностей предметной области.

Содержит основные классы бизнес-логики системы:
- Сотрудники разных типов
- Отделы компании
- Проекты
- Компания
"""

from .employee import (
    AbstractEmployee,
    Employee,
    Manager,
    Developer,
    Salesperson,
    EmployeeData,
    ISalaryCalculable,
    IInfoProvidable,
    ISkillManageable,
    ISalesManageable
)

from .department import Department
from .project import Project
from .company import Company

__all__ = [
    'AbstractEmployee',
    'Employee',
    'Manager', 
    'Developer',
    'Salesperson',
    'EmployeeData',
    'ISalaryCalculable',
    'IInfoProvidable', 
    'ISkillManageable',
    'ISalesManageable',
    'Department',
    'Project',
    'Company',
]