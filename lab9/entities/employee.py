"""
Модуль классов сотрудников.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Set, List, Optional, Dict, Any
from dataclasses import dataclass
from decimal import Decimal

from services.validator import EmployeeValidator
from services.calculator import (
    SalaryCalculationStrategy, BaseSalaryStrategy,
    ManagerSalaryStrategy, DeveloperSalaryStrategy, SalespersonSalaryStrategy
)
from utils.exceptions import InvalidSalaryError, DuplicateIdError
from services.logger import Logger


@dataclass
class EmployeeData:
    """DTO для данных сотрудника."""
    id: int
    name: str
    department: str
    base_salary: float
    
    def __post_init__(self):
        """Пост-инициализация для валидации."""
        if self.base_salary < 0:
            raise InvalidSalaryError(f"Зарплата не может быть отрицательной: {self.base_salary}")


class ISalaryCalculable(ABC):
    """Интерфейс для объектов, у которых можно рассчитать зарплату."""
    
    @abstractmethod
    def calculate_salary(self) -> float:
        """Рассчитать зарплату."""
        pass


class IInfoProvidable(ABC):
    """Интерфейс для объектов, предоставляющих информацию."""
    
    @abstractmethod
    def get_info(self) -> str:
        """Получить информацию."""
        pass


class ISkillManageable(ABC):
    """Интерфейс для управления навыками."""
    
    @abstractmethod
    def add_skill(self, skill: str) -> None:
        """Добавить навык."""
        pass
    
    @abstractmethod
    def get_skills(self) -> List[str]:
        """Получить список навыков."""
        pass


class ISalesManageable(ABC):
    """Интерфейс для управления продажами."""
    
    @abstractmethod
    def update_sales(self, amount: float) -> None:
        """Обновить объем продаж."""
        pass


class AbstractEmployee(ABC, ISalaryCalculable, IInfoProvidable):
    """Абстрактный базовый класс сотрудника."""
    
    _existing_ids: Set[int] = set()
    _logger: Logger = Logger()
    
    def __init__(self, data: EmployeeData, salary_strategy: Optional[SalaryCalculationStrategy] = None):
        """Инициализация сотрудника.
        
        Args:
            data: Данные сотрудника
            salary_strategy: Стратегия расчета зарплаты
        """
        # Валидация данных
        EmployeeValidator.validate_employee_id(data.id, self._existing_ids)
        EmployeeValidator.validate_name(data.name)
        EmployeeValidator.validate_salary(data.base_salary)
        EmployeeValidator.validate_department(data.department)
        
        # Сохранение данных
        self._id = data.id
        self._name = data.name
        self._department = data.department
        self._base_salary = float(data.base_salary)
        self._salary_strategy = salary_strategy or BaseSalaryStrategy()
        
        # Регистрация ID и логирование
        self._existing_ids.add(data.id)
        self._logger.log(f"Создан сотрудник: {self._name} (ID: {self._id})")
    
    @property
    def id(self) -> int:
        """Уникальный идентификатор сотрудника."""
        return self._id
    
    @property
    def name(self) -> str:
        """Имя сотрудника."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Установить имя сотрудника."""
        EmployeeValidator.validate_name(value)
        old_name = self._name
        self._name = value
        self._logger.log(f"Изменено имя сотрудника {self._id}: {old_name} -> {value}")
    
    @property
    def department(self) -> str:
        """Отдел сотрудника."""
        return self._department
    
    @department.setter
    def department(self, value: str) -> None:
        """Установить отдел сотрудника."""
        EmployeeValidator.validate_department(value)
        old_dept = self._department
        self._department = value
        self._logger.log(f"Сотрудник {self._name} переведен из {old_dept} в {value}")
    
    @property
    def base_salary(self) -> float:
        """Базовая зарплата."""
        return self._base_salary
    
    @base_salary.setter
    def base_salary(self, value: float) -> None:
        """Установить базовую зарплату."""
        EmployeeValidator.validate_salary(value)
        old_salary = self._base_salary
        self._base_salary = value
        self._logger.log(f"Изменена зарплата сотрудника {self._name}: {old_salary} -> {value}")
    
    def calculate_salary(self) -> float:
        """Рассчитать зарплату сотрудника."""
        return self._salary_strategy.calculate(self)
    
    def get_info(self) -> str:
        """Получить информацию о сотруднике."""
        return f"{self.__class__.__name__}: {self._name} (ID: {self._id}, Отдел: {self._department})"
    
    def __str__(self) -> str:
        """Строковое представление сотрудника."""
        return f"Сотрудник id: {self.id}, имя: {self.name}, отдел: {self.department}"
    
    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}')"
    
    def __eq__(self, other: object) -> bool:
        """Проверка равенства по ID."""
        if not isinstance(other, AbstractEmployee):
            return False
        return self.id == other.id
    
    def __lt__(self, other: AbstractEmployee) -> bool:
        """Сравнение по зарплате."""
        return self.calculate_salary() < other.calculate_salary()
    
    def __hash__(self) -> int:
        """Хэш на основе ID."""
        return hash(self.id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь."""
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'base_salary': self.base_salary,
            'type': self.__class__.__name__
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AbstractEmployee:
        """Создать из словаря."""
        from patterns.factory import EmployeeFactory
        return EmployeeFactory.create_from_dict(data)
    
    @classmethod
    def reset_ids(cls) -> None:
        """Сбросить статическую коллекцию ID (для тестирования)."""
        cls._existing_ids.clear()


class Employee(AbstractEmployee):
    """Базовый класс сотрудника."""
    
    def __init__(self, data: EmployeeData):
        """Инициализация базового сотрудника."""
        super().__init__(data, BaseSalaryStrategy())


class Manager(AbstractEmployee):
    """Класс менеджера."""
    
    def __init__(self, data: EmployeeData, bonus: float = 0.0):
        """Инициализация менеджера."""
        super().__init__(data, ManagerSalaryStrategy())
        self._bonus = float(bonus)
    
    @property
    def bonus(self) -> float:
        """Бонус менеджера."""
        return self._bonus
    
    @bonus.setter
    def bonus(self, value: float) -> None:
        """Установить бонус менеджера."""
        if value < 0:
            raise InvalidSalaryError(f"Бонус не может быть отрицательным: {value}")
        self._bonus = value
    
    def calculate_salary(self) -> float:
        """Рассчитать зарплату менеджера."""
        return self.base_salary + self.bonus
    
    def get_info(self) -> str:
        """Получить информацию о менеджере."""
        base_info = super().get_info()
        return f"{base_info}, Бонус: {self.bonus:.2f}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь."""
        data = super().to_dict()
        data['bonus'] = self.bonus
        return data


class Developer(AbstractEmployee, ISkillManageable):
    """Класс разработчика."""
    
    def __init__(self, data: EmployeeData, tech_stack: List[str], seniority_level: str):
        """Инициализация разработчика."""
        super().__init__(data, DeveloperSalaryStrategy())
        self._tech_stack = set(tech_stack)
        self._seniority_level = seniority_level
    
    @property
    def seniority_level(self) -> str:
        """Уровень разработчика."""
        return self._seniority_level
    
    @seniority_level.setter
    def seniority_level(self, value: str) -> None:
        """Установить уровень разработчика."""
        valid_levels = {"junior", "middle", "senior"}
        if value not in valid_levels:
            raise ValueError(f"Недопустимый уровень: {value}. Допустимые: {valid_levels}")
        self._seniority_level = value
    
    def add_skill(self, skill: str) -> None:
        """Добавить навык."""
        self._tech_stack.add(skill)
        self._logger.log(f"Разработчик {self.name} получил навык: {skill}")
    
    def get_skills(self) -> List[str]:
        """Получить список навыков."""
        return list(self._tech_stack)
    
    def calculate_salary(self) -> float:
        """Рассчитать зарплату разработчика."""
        strategy = DeveloperSalaryStrategy()
        return strategy.calculate(self)
    
    def get_info(self) -> str:
        """Получить информацию о разработчике."""
        base_info = super().get_info()
        return f"{base_info}, Уровень: {self.seniority_level}, Навыки: {', '.join(self.get_skills())}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь."""
        data = super().to_dict()
        data['tech_stack'] = list(self._tech_stack)
        data['seniority_level'] = self.seniority_level
        return data
    
    def __iter__(self):
        """Итерация по навыкам."""
        return iter(self._tech_stack)


class Salesperson(AbstractEmployee, ISalesManageable):
    """Класс продавца."""
    
    def __init__(self, data: EmployeeData, commission_rate: float, sales_volume: float = 0.0):
        """Инициализация продавца."""
        super().__init__(data, SalespersonSalaryStrategy())
        self._commission_rate = float(commission_rate)
        self._sales_volume = float(sales_volume)
    
    @property
    def commission_rate(self) -> float:
        """Ставка комиссии."""
        return self._commission_rate
    
    @property
    def sales_volume(self) -> float:
        """Объем продаж."""
        return self._sales_volume
    
    def update_sales(self, amount: float) -> None:
        """Обновить объем продаж."""
        if amount < 0:
            raise ValueError(f"Объем продаж не может быть отрицательным: {amount}")
        self._sales_volume += amount
        self._logger.log(f"Продавец {self.name} увеличил объем продаж на {amount}")
    
    def calculate_salary(self) -> float:
        """Рассчитать зарплату продавца."""
        return self.base_salary + (self.commission_rate * self.sales_volume)
    
    def get_info(self) -> str:
        """Получить информацию о продавце."""
        base_info = super().get_info()
        return f"{base_info}, Комиссия: {self.commission_rate:.1%}, Продажи: {self.sales_volume:.2f}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь."""
        data = super().to_dict()
        data['commission_rate'] = self.commission_rate
        data['sales_volume'] = self.sales_volume
        return data