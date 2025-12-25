
from .singleton import DatabaseConnection
from .strategy import BonusStrategy, PerformanceBonusStrategy
from .adapter import SalaryCalculatorAdapter
from .repository import EmployeeRepository

__all__ = [
    'DatabaseConnection',
    'BonusStrategy',
    'PerformanceBonusStrategy',
    'SalaryCalculatorAdapter',
    'EmployeeRepository'
]

print(f"Пакет patterns версии {PACKAGE_VERSION} загружен")