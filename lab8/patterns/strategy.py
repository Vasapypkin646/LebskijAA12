from abc import ABC, abstractmethod
from typing import Optional

class BonusStrategy(ABC):
    """Абстрактный класс стратегии расчета бонусов"""
    
    @abstractmethod
    def calculate_bonus(self, employee, **kwargs) -> float:
        pass

class PerformanceBonusStrategy(BonusStrategy):
    """Стратегия расчета бонуса на основе производительности"""
    
    def calculate_bonus(self, employee, **kwargs) -> float:
        performance_score = kwargs.get('performance_score', 1.0)
        
        if hasattr(employee, 'bonus'):
            # Для менеджеров
            base_bonus = employee.bonus
        else:
            # Для остальных сотрудников
            base_bonus = employee.base_salary * 0.1
        
        return base_bonus * performance_score

class SeniorityBonusStrategy(BonusStrategy):
    """Стратегия расчета бонуса на основе стажа"""
    
    def calculate_bonus(self, employee, **kwargs) -> float:
        seniority_years = kwargs.get('seniority_years', 1)
        
        # Определяем множитель уровня
        level_multiplier = 1.0
        if hasattr(employee, '_Developer__seniority_level'):
            # Для разработчиков
            level_multipliers = {
                'junior': 0.5,
                'middle': 1.0,
                'senior': 2.0
            }
            level_multiplier = level_multipliers.get(
                employee._Developer__seniority_level, 1.0
            )
        
        return employee.base_salary * 0.05 * seniority_years * level_multiplier

class ProjectBonusStrategy(BonusStrategy):
    """Стратегия расчета бонуса на основе успешных проектов"""
    
    def calculate_bonus(self, employee, **kwargs) -> float:
        successful_projects = kwargs.get('successful_projects', 0)
        project_importance = kwargs.get('project_importance', 1.0)
        
        base_bonus = 1000  # Базовая сумма за проект
        
        return base_bonus * successful_projects * project_importance

class BonusContext:
    """
    Контекст для использования различных стратегий расчета бонусов.
    Позволяет динамически менять стратегию во время выполнения.
    """
    
    def __init__(self, strategy: Optional[BonusStrategy] = None):
        self._strategy = strategy
    
    @property
    def strategy(self) -> Optional[BonusStrategy]:
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: BonusStrategy):
        self._strategy = strategy
    
    def calculate_bonus(self, employee, **kwargs) -> float:
        """Вычисляет бонус с использованием текущей стратегии"""
        if self._strategy is None:
            raise ValueError("Стратегия не установлена")
        
        return self._strategy.calculate_bonus(employee, **kwargs)