"""
Паттерн Strategy для расчета бонусов.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from entities.employee import AbstractEmployee


class BonusStrategy(ABC):
    """Абстрактный класс стратегии расчета бонусов"""
    
    @abstractmethod
    def calculate_bonus(self, employee: AbstractEmployee, **kwargs) -> float:
        pass


class PerformanceBonusStrategy(BonusStrategy):
    """Стратегия расчета бонуса на основе производительности"""
    
    def calculate_bonus(self, employee: AbstractEmployee, **kwargs) -> float:
        performance_score = kwargs.get('performance_score', 1.0)
        employee_data = employee.to_dict()
        
        # Используем единый подход с adapter.py
        if employee_data.get('type') == 'Manager':
            # Для менеджеров
            base_bonus = employee_data.get('bonus', 0)
        else:
            # Для остальных сотрудников
            base_bonus = employee_data.get('base_salary', 0) * 0.1
        
        return base_bonus * performance_score


class SeniorityBonusStrategy(BonusStrategy):
    """Стратегия расчета бонуса на основе стажа"""
    
    def calculate_bonus(self, employee: AbstractEmployee, **kwargs) -> float:
        seniority_years = kwargs.get('seniority_years', 1)
        employee_data = employee.to_dict()
        
        base_salary = employee_data.get('base_salary', 0)
        level_multiplier = 1.0
        
        if employee_data.get('type') == 'Developer':
            # Для разработчиков
            level_multipliers = {
                'junior': 0.5,
                'middle': 1.0,
                'senior': 2.0
            }
            level = employee_data.get('seniority_level', 'junior')
            level_multiplier = level_multipliers.get(level, 1.0)
        
        return base_salary * 0.05 * seniority_years * level_multiplier


class ProjectBonusStrategy(BonusStrategy):
    """Стратегия расчета бонуса на основе успешных проектов"""
    
    def calculate_bonus(self, employee: AbstractEmployee, **kwargs) -> float:
        successful_projects = kwargs.get('successful_projects', 0)
        project_importance = kwargs.get('project_importance', 1.0)
        
        employee_data = employee.to_dict()
        
        
        base_bonus = 1000
        if employee_data.get('type') == 'Manager':
            base_bonus = 1500
        elif employee_data.get('type') == 'Developer':
            base_bonus = 1200
        
        return base_bonus * successful_projects * project_importance


class BonusContext:
    """
    Калькулятор бонусов с поддержкой стратегий.
    Аналогично SalaryCalculatorAdapter, но для бонусов.
    """
    
    def __init__(self, strategy: Optional[BonusStrategy] = None):
        self._strategy = strategy
    
    @property
    def strategy(self) -> Optional[BonusStrategy]:
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: BonusStrategy):
        self._strategy = strategy
    
    def calculate_bonus(self, employee: AbstractEmployee, **kwargs) -> float:
        """Рассчитать бонус с использованием текущей стратегии"""
        if self._strategy is None:
            raise ValueError("Стратегия не установлена")
        
        return self._strategy.calculate_bonus(employee, **kwargs)
    
    def calculate_total_bonus(self, employee: AbstractEmployee, 
                             strategies: list[BonusStrategy], **kwargs) -> float:
        """Рассчитать общий бонус по нескольким стратегиям"""
        total = 0.0
        for strategy in strategies:
            self._strategy = strategy
            total += self.calculate_bonus(employee, **kwargs)
        return total
