"""
Модуль сервисов.

Содержит вспомогательные классы для работы с данными:
- Валидация
- Расчеты
- Сериализация
- Логирование
- Репозитории
"""

from .validator import (
    DataValidator,
    EmployeeValidator,
    ProjectValidator
)

from .calculator import (
    SalaryCalculationStrategy,
    BonusStrategy,
    BaseSalaryStrategy,
    ManagerSalaryStrategy,
    DeveloperSalaryStrategy,
    SalespersonSalaryStrategy,
    PerformanceBonusStrategy,
    SeniorityBonusStrategy,
    ProjectBonusStrategy,
    BonusContext
)

from .serializer import (
    JSONSerializer,
    CSVExporter
)

from .logger import (
    Logger,
    LogLevel
)

from .repository import (
    IEmployeeRepository,
    EmployeeRepository
)

__all__ = [
    # Валидация
    'DataValidator',
    'EmployeeValidator',
    'ProjectValidator',
    
    # Расчеты
    'SalaryCalculationStrategy',
    'BonusStrategy',
    'BaseSalaryStrategy',
    'ManagerSalaryStrategy',
    'DeveloperSalaryStrategy',
    'SalespersonSalaryStrategy',
    'PerformanceBonusStrategy',
    'SeniorityBonusStrategy',
    'ProjectBonusStrategy',
    'BonusContext',
    
    # Сериализация
    'JSONSerializer',
    'CSVExporter',
    
    # Логирование
    'Logger',
    'LogLevel',
    
    # Репозитории
    'IEmployeeRepository',
    'EmployeeRepository',
]