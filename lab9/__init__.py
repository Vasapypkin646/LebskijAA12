
"""
Система учета сотрудников компании.

Модуль предоставляет функциональность для управления сотрудниками, отделами,
проектами и компанией с применением принципов SOLID и паттернов проектирования.
"""

from entities.employee import Employee, Manager, Developer, Salesperson, AbstractEmployee
from entities.department import Department
from entities.project import Project
from entities.company import Company
from patterns.factory import EmployeeFactory
from patterns.repository import EmployeeRepository
from services.calculator import BonusContext, PerformanceBonusStrategy

__all__ = [

    'AbstractEmployee',
    'Employee', 
    'Manager',
    'Developer',
    'Salesperson',
    'Department',
    'Project',
    'Company',
    
    'EmployeeFactory',
    'EmployeeRepository',
    'BonusContext',
    'PerformanceBonusStrategy'
]