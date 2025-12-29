"""
Модуль стратегий расчета зарплаты и бонусов.
"""

from abc import ABC, abstractmethod
from typing import Protocol, Optional
from decimal import Decimal


class SalaryCalculationStrategy(Protocol):
    """Протокол стратегии расчета зарплаты."""
    
    def calculate(self, employee: 'AbstractEmployee') -> float:
        """Рассчитать зарплату сотрудника."""
        ...


class BonusStrategy(Protocol):
    """Протокол стратегии расчета бонусов."""
    
    def calculate_bonus(self, employee: 'AbstractEmployee', **kwargs) -> float:
        """Рассчитать бонус сотрудника."""
        ...


class BaseSalaryStrategy:
    """Базовая стратегия расчета зарплаты."""
    
    def calculate(self, employee: 'AbstractEmployee') -> float:
        """Рассчитать базовую зарплату."""
        return employee.base_salary


class ManagerSalaryStrategy:
    """Стратегия расчета зарплаты менеджера."""
    
    def calculate(self, employee: 'Manager') -> float:
        """Рассчитать зарплату менеджера (базовая + бонус)."""
        return employee.base_salary + employee.bonus


class DeveloperSalaryStrategy:
    """Стратегия расчета зарплаты разработчика."""
    
    def __init__(self):
        self._multipliers = {
            "junior": 1.0,
            "middle": 1.5,
            "senior": 2.0
        }
    
    def calculate(self, employee: 'Developer') -> float:
        """Рассчитать зарплату разработчика."""
        multiplier = self._multipliers.get(employee.seniority_level, 1.0)
        return employee.base_salary * multiplier


class SalespersonSalaryStrategy:
    """Стратегия расчета зарплаты продавца."""
    
    def calculate(self, employee: 'Salesperson') -> float:
        """Рассчитать зарплату продавца (базовая + комиссия)."""
        return employee.base_salary + (employee.commission_rate * employee.sales_volume)


class PerformanceBonusStrategy:
    """Стратегия расчета бонуса по производительности."""
    
    def calculate_bonus(self, employee: 'AbstractEmployee', performance_score: float = 1.0) -> float:
        """Рассчитать бонус по производительности."""
        if performance_score < 0.5:
            return 0.0
        elif performance_score < 1.0:
            return employee.base_salary * 0.1 * performance_score
        elif performance_score < 1.5:
            return employee.base_salary * 0.2 * performance_score
        else:
            return employee.base_salary * 0.3 * min(performance_score, 2.0)


class SeniorityBonusStrategy:
    """Стратегия расчета бонуса за стаж."""
    
    def calculate_bonus(self, employee: 'AbstractEmployee', seniority_years: int = 0) -> float:
        """Рассчитать бонус за стаж."""
        if seniority_years < 1:
            return 0.0
        elif seniority_years < 3:
            return employee.base_salary * 0.05
        elif seniority_years < 5:
            return employee.base_salary * 0.1
        elif seniority_years < 10:
            return employee.base_salary * 0.15
        else:
            return employee.base_salary * 0.2


class ProjectBonusStrategy:
    """Стратегия расчета проектного бонуса."""
    
    def calculate_bonus(self, employee: 'AbstractEmployee', project_complexity: float = 1.0) -> float:
        """Рассчитать проектный бонус."""
        return employee.base_salary * 0.1 * project_complexity


class BonusContext:
    """Контекст для использования стратегии расчета бонусов."""
    
    def __init__(self, strategy: Optional[BonusStrategy] = None):
        self._strategy = strategy
    
    @property
    def strategy(self) -> Optional[BonusStrategy]:
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: BonusStrategy) -> None:
        self._strategy = strategy
    
    def calculate_bonus(self, employee: 'AbstractEmployee', **kwargs) -> float:
        """Рассчитать бонус с использованием текущей стратегии."""
        if self._strategy is None:
            return 0.0
        return self._strategy.calculate_bonus(employee, **kwargs)