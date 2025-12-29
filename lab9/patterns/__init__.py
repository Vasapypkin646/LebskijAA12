"""
Модуль паттернов проектирования.

Содержит реализации основных паттернов проектирования:
- Singleton
- Factory
- Strategy
- Adapter
- Repository
"""

from .singleton import DatabaseConnection
from .factory import EmployeeFactory
from .strategy import (
    PerformanceBonusStrategy,
    SeniorityBonusStrategy,
    ProjectBonusStrategy,
    BonusContext
)
from .adapter import (
    ExternalSalarySystem,
    SalaryCalculatorAdapter
)
from .repository import (
    IEmployeeRepository,
    EmployeeRepository
)

__all__ = [
    'DatabaseConnection',
    'EmployeeFactory',
    'PerformanceBonusStrategy',
    'SeniorityBonusStrategy',
    'ProjectBonusStrategy',
    'BonusContext',
    'ExternalSalarySystem',
    'SalaryCalculatorAdapter',
    'IEmployeeRepository',
    'EmployeeRepository',
]