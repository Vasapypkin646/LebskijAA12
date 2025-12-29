"""
Модуль класса проекта.
"""

from __future__ import annotations
from typing import List, Set, Iterator, Optional
from datetime import datetime

from entities.employee import AbstractEmployee
from services.validator import ProjectValidator, DataValidator
from utils.exceptions import ProjectNotFoundError, InvalidStatusError
from services.logger import Logger


class Project:
    """Класс проекта компании."""
    
    _existing_project_ids: Set[str] = set()
    _valid_statuses = ["planning", "active", "completed", "cancelled"]
    
    def __init__(self, project_id: str, name: str, description: str, 
                 deadline: str, status: str = "planning"):
        """Инициализация проекта.
        
        Args:
            project_id: Уникальный идентификатор проекта
            name: Название проекта
            description: Описание проекта
            deadline: Срок выполнения (YYYY-MM-DD)
            status: Статус проекта
            
        Raises:
            DuplicateIdError: Если ID проекта уже существует
            InvalidDateError: Если дата в некорректном формате
            InvalidStatusError: Если статус недопустимый
        """
        # Валидация данных
        ProjectValidator.validate_project_id(project_id, self._existing_project_ids)
        DataValidator.validate_string_not_empty(name, "Название проекта")
        DataValidator.validate_string_not_empty(description, "Описание проекта")
        ProjectValidator.validate_date(deadline)
        ProjectValidator.validate_status(status, self._valid_statuses)
        
        # Сохранение данных
        self._project_id = project_id
        self._name = name
        self._description = description
        self._deadline = deadline
        self._status = status
        self._team: List[AbstractEmployee] = []
        self._logger = Logger()
        
        # Регистрация ID
        self._existing_project_ids.add(project_id)
        self._logger.log(f"Создан проект: {name} (ID: {project_id})")
    
    @property
    def project_id(self) -> str:
        """ID проекта."""
        return self._project_id
    
    @property
    def name(self) -> str:
        """Название проекта."""
        return self._name
    
    @property
    def description(self) -> str:
        """Описание проекта."""
        return self._description
    
    @property
    def deadline(self) -> str:
        """Срок выполнения."""
        return self._deadline
    
    @property
    def status(self) -> str:
        """Статус проекта."""
        return self._status
    
    def add_team_member(self, employee: AbstractEmployee) -> None:
        """Добавить сотрудника в команду проекта.
        
        Args:
            employee: Сотрудник для добавления
        """
        if self.is_employee_in_project(employee.id):
            raise ValueError(f"Сотрудник {employee.name} уже в команде проекта")
        
        self._team.append(employee)
        self._logger.log(f"Сотрудник {employee.name} добавлен в проект {self.name}")
    
    def remove_team_member(self, employee_id: int) -> AbstractEmployee:
        """Удалить сотрудника из команды проекта.
        
        Args:
            employee_id: ID сотрудника
            
        Returns:
            Удаленный сотрудник
            
        Raises:
            ValueError: Если сотрудник не найден
        """
        for i, employee in enumerate(self._team):
            if employee.id == employee_id:
                removed = self._team.pop(i)
                self._logger.log(f"Сотрудник {removed.name} удален из проекта {self.name}")
                return removed
        
        raise ValueError(f"Сотрудник с ID {employee_id} не найден в проекте")
    
    def get_team(self) -> List[AbstractEmployee]:
        """Получить команду проекта."""
        return self._team.copy()
    
    def get_team_size(self) -> int:
        """Получить размер команды."""
        return len(self._team)
    
    def calculate_total_salary(self) -> float:
        """Рассчитать общую зарплату команды проекта."""
        return sum(emp.calculate_salary() for emp in self._team)
    
    def change_status(self, new_status: str) -> None:
        """Изменить статус проекта.
        
        Args:
            new_status: Новый статус
            
        Raises:
            InvalidStatusError: Если статус недопустимый
            ValueError: Если переход статуса невозможен
        """
        ProjectValidator.validate_status(new_status, self._valid_statuses)
        
        old_status = self._status
        
        # Проверка логики переходов
        if old_status in ["completed", "cancelled"]:
            raise ValueError(f"Нельзя изменить статус проекта с '{old_status}'")
        
        self._status = new_status
        self._logger.log(f"Статус проекта {self.name} изменен: {old_status} -> {new_status}")
    
    def is_employee_in_project(self, employee_id: int) -> bool:
        """Проверить, участвует ли сотрудник в проекте."""
        return any(emp.id == employee_id for emp in self._team)
    
    def has_team_members(self) -> bool:
        """Проверить, есть ли участники в проекте."""
        return len(self._team) > 0
    
    def get_days_until_deadline(self) -> int:
        """Получить количество дней до дедлайна."""
        try:
            target_date = datetime.strptime(self._deadline, "%Y-%m-%d")
            current_date = datetime.now()
            return (target_date - current_date).days
        except ValueError:
            return 9999
    
    def get_project_info(self) -> str:
        """Получить информацию о проекте."""
        return (f"Проект: {self.name} (ID: {self.project_id})\n"
                f"Описание: {self.description}\n"
                f"Дедлайн: {self.deadline} ({self.get_days_until_deadline()} дней)\n"
                f"Статус: {self.status}\n"
                f"Команда: {self.get_team_size()} сотрудников")
    
    def __len__(self) -> int:
        """Размер команды проекта."""
        return len(self._team)
    
    def __contains__(self, employee: AbstractEmployee) -> bool:
        """Проверить наличие сотрудника в проекте."""
        return self.is_employee_in_project(employee.id)
    
    def __iter__(self) -> Iterator[AbstractEmployee]:
        """Итерация по команде проекта."""
        return iter(self._team)
    
    def __str__(self) -> str:
        """Строковое представление проекта."""
        return f"Проект: {self.name} (Статус: {self.status}, Команда: {len(self)})"
    
    def to_dict(self) -> dict:
        """Конвертировать в словарь."""
        return {
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'deadline': self.deadline,
            'status': self.status,
            'team_size': self.get_team_size(),
            'team_member_ids': [emp.id for emp in self._team],
            'total_salary_cost': self.calculate_total_salary()
        }
    
    @classmethod
    def from_dict(cls, data: dict, employee_map: dict) -> Project:
        """Создать из словаря."""
        project = cls(
            project_id=data['project_id'],
            name=data['name'],
            description=data['description'],
            deadline=data['deadline'],
            status=data['status']
        )
        
        # Восстановление команды
        for emp_id in data.get('team_member_ids', []):
            if emp_id in employee_map:
                project.add_team_member(employee_map[emp_id])
        
        return project
    
    @classmethod
    def reset_ids(cls) -> None:
        """Сбросить статическую коллекцию ID (для тестирования)."""
        cls._existing_project_ids.clear()