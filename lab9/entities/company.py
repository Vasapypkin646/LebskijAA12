"""
Модуль класса компании.
"""

from __future__ import annotations
from typing import List, Dict, Optional, Any
import json
import csv
from datetime import datetime

from entities.department import Department
from entities.project import Project
from entities.employee import AbstractEmployee
from utils.exceptions import (
    DepartmentNotFoundError, ProjectNotFoundError, 
    EmployeeNotFoundError, InvalidInputError
)
from services.logger import Logger


class DepartmentManager:
    """Менеджер отделов компании."""
    
    def __init__(self):
        self._departments: Dict[str, Department] = {}
        self._logger = Logger()
    
    def add_department(self, department: Department) -> None:
        """Добавить отдел.
        
        Args:
            department: Отдел для добавления
            
        Raises:
            ValueError: Если отдел с таким именем уже существует
        """
        if department.name in self._departments:
            raise ValueError(f"Отдел с названием '{department.name}' уже существует")
        
        self._departments[department.name] = department
        self._logger.log(f"Добавлен отдел: {department.name}")
    
    def remove_department(self, name: str) -> Department:
        """Удалить отдел.
        
        Args:
            name: Название отдела
            
        Returns:
            Удаленный отдел
            
        Raises:
            DepartmentNotFoundError: Если отдел не найден
            ValueError: Если в отделе есть сотрудники
        """
        if name not in self._departments:
            raise DepartmentNotFoundError(f"Отдел '{name}' не найден")
        
        department = self._departments[name]
        if department.has_employees():
            raise ValueError(f"Нельзя удалить отдел '{name}': в нем есть сотрудники")
        
        del self._departments[name]
        self._logger.log(f"Удален отдел: {name}")
        return department
    
    def get_department(self, name: str) -> Optional[Department]:
        """Получить отдел по имени."""
        return self._departments.get(name)
    
    def get_all_departments(self) -> List[Department]:
        """Получить все отделы."""
        return list(self._departments.values())
    
    def get_department_names(self) -> List[str]:
        """Получить названия всех отделов."""
        return list(self._departments.keys())
    
    def has_department(self, name: str) -> bool:
        """Проверить наличие отдела."""
        return name in self._departments
    
    def __len__(self) -> int:
        """Количество отделов."""
        return len(self._departments)
    
    def __iter__(self):
        """Итерация по отделам."""
        return iter(self._departments.values())


class ProjectManager:
    """Менеджер проектов компании."""
    
    def __init__(self):
        self._projects: Dict[str, Project] = {}
        self._logger = Logger()
    
    def add_project(self, project: Project) -> None:
        """Добавить проект.
        
        Args:
            project: Проект для добавления
        """
        if project.project_id in self._projects:
            raise ValueError(f"Проект с ID '{project.project_id}' уже существует")
        
        self._projects[project.project_id] = project
        self._logger.log(f"Добавлен проект: {project.name}")
    
    def remove_project(self, project_id: str) -> Project:
        """Удалить проект.
        
        Args:
            project_id: ID проекта
            
        Returns:
            Удаленный проект
            
        Raises:
            ProjectNotFoundError: Если проект не найден
            ValueError: Если в проекте есть участники
        """
        if project_id not in self._projects:
            raise ProjectNotFoundError(f"Проект с ID '{project_id}' не найден")
        
        project = self._projects[project_id]
        if project.has_team_members():
            raise ValueError(f"Нельзя удалить проект '{project.name}': в нем есть участники")
        
        del self._projects[project_id]
        self._logger.log(f"Удален проект: {project.name}")
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Получить проект по ID."""
        return self._projects.get(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """Получить все проекты."""
        return list(self._projects.values())
    
    def get_projects_by_status(self, status: str) -> List[Project]:
        """Получить проекты по статусу."""
        return [p for p in self._projects.values() if p.status == status]
    
    def has_project(self, project_id: str) -> bool:
        """Проверить наличие проекта."""
        return project_id in self._projects
    
    def __len__(self) -> int:
        """Количество проектов."""
        return len(self._projects)
    
    def __iter__(self):
        """Итерация по проектам."""
        return iter(self._projects.values())


class EmployeeManager:
    """Менеджер сотрудников компании."""
    
    def __init__(self, department_manager: DepartmentManager):
        self._department_manager = department_manager
    
    def get_all_employees(self) -> List[AbstractEmployee]:
        """Получить всех сотрудников компании."""
        all_employees = []
        for department in self._department_manager.get_all_departments():
            all_employees.extend(department.get_employees())
        return all_employees
    
    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Найти сотрудника по ID во всех отделах."""
        for department in self._department_manager.get_all_departments():
            employee = department.find_employee_by_id(employee_id)
            if employee:
                return employee
        return None
    
    def remove_employee_from_company(self, employee_id: int) -> AbstractEmployee:
        """Удалить сотрудника из компании.
        
        Args:
            employee_id: ID сотрудника
            
        Returns:
            Удаленный сотрудник
            
        Raises:
            EmployeeNotFoundError: Если сотрудник не найден
        """
        for department in self._department_manager.get_all_departments():
            try:
                return department.remove_employee(employee_id)
            except EmployeeNotFoundError:
                continue
        
        raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в компании")
    
    def get_total_employee_count(self) -> int:
        """Получить общее количество сотрудников."""
        total = 0
        for department in self._department_manager.get_all_departments():
            total += len(department)
        return total


class Company:
    """Класс компании."""
    
    def __init__(self, name: str):
        """Инициализация компании.
        
        Args:
            name: Название компании
        """
        self._name = name
        self._department_manager = DepartmentManager()
        self._project_manager = ProjectManager()
        self._employee_manager = EmployeeManager(self._department_manager)
        self._logger = Logger()
        
        self._logger.log(f"Создана компания: {name}")
    
    @property
    def name(self) -> str:
        """Название компании."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Установить название компании."""
        if not value or not isinstance(value, str):
            raise InvalidInputError("Название компании должно быть непустой строкой")
        self._name = value
    
    # Делегирование методов DepartmentManager
    def add_department(self, department: Department) -> None:
        """Добавить отдел."""
        self._department_manager.add_department(department)
    
    def remove_department(self, name: str) -> Department:
        """Удалить отдел."""
        return self._department_manager.remove_department(name)
    
    def get_department(self, name: str) -> Optional[Department]:
        """Получить отдел."""
        return self._department_manager.get_department(name)
    
    def get_all_departments(self) -> List[Department]:
        """Получить все отделы."""
        return self._department_manager.get_all_departments()
    
    # Делегирование методов ProjectManager
    def add_project(self, project: Project) -> None:
        """Добавить проект."""
        self._project_manager.add_project(project)
    
    def remove_project(self, project_id: str) -> Project:
        """Удалить проект."""
        return self._project_manager.remove_project(project_id)
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Получить проект."""
        return self._project_manager.get_project(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """Получить все проекты."""
        return self._project_manager.get_all_projects()
    
    # Делегирование методов EmployeeManager
    def get_all_employees(self) -> List[AbstractEmployee]:
        """Получить всех сотрудников."""
        return self._employee_manager.get_all_employees()
    
    def find_employee_by_id(self, employee_id: int) -> AbstractEmployee:
        """Найти сотрудника по ID."""
        employee = self._employee_manager.find_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")
        return employee
    
    def remove_employee_from_company(self, employee_id: int) -> AbstractEmployee:
        """Удалить сотрудника из компании."""
        return self._employee_manager.remove_employee_from_company(employee_id)
    
    # Бизнес-методы
    def calculate_total_monthly_cost(self) -> float:
        """Рассчитать общие месячные затраты."""
        total = 0.0
        for department in self.get_all_departments():
            total += department.calculate_total_salary()
        return total
    
    def assign_employee_to_project(self, employee_id: int, project_id: str) -> None:
        """Назначить сотрудника на проект.
        
        Args:
            employee_id: ID сотрудника
            project_id: ID проекта
        """
        employee = self.find_employee_by_id(employee_id)
        project = self.get_project(project_id)
        
        if not project:
            raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")
        
        project.add_team_member(employee)
        self._logger.log(f"Сотрудник {employee.name} назначен на проект {project.name}")
    
    def get_department_stats(self) -> Dict[str, Dict[str, Any]]:
        """Получить статистику по отделам."""
        stats = {}
        
        for department in self.get_all_departments():
            employees = department.get_employees()
            salaries = [emp.calculate_salary() for emp in employees]
            
            dept_stats = {
                'name': department.name,
                'total_employees': len(department),
                'total_salary': department.calculate_total_salary(),
                'employee_count_by_type': department.get_employee_count_by_type(),
                'average_salary': sum(salaries) / len(salaries) if salaries else 0,
                'salary_distribution': {
                    'min': min(salaries) if salaries else 0,
                    'max': max(salaries) if salaries else 0,
                    'median': sorted(salaries)[len(salaries) // 2] if salaries else 0
                }
            }
            
            stats[department.name] = dept_stats
        
        return stats
    
    def __str__(self) -> str:
        """Строковое представление компании."""
        dept_count = len(self._department_manager)
        project_count = len(self._project_manager)
        employee_count = self._employee_manager.get_total_employee_count()
        
        return (f"Компания: {self.name}\n"
                f"Отделов: {dept_count}, Проектов: {project_count}, Сотрудников: {employee_count}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь."""
        return {
            'company_name': self.name,
            'departments': [dept.to_dict() for dept in self.get_all_departments()],
            'projects': [proj.to_dict() for proj in self.get_all_projects()],
            'metadata': {
                'total_employees': self._employee_manager.get_total_employee_count(),
                'total_projects': len(self._project_manager),
                'total_monthly_cost': self.calculate_total_monthly_cost(),
                'export_date': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
    
    def save_to_json(self, filename: str) -> None:
        """Сохранить компанию в JSON файл."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.to_dict(), file, ensure_ascii=False, indent=2)
            self._logger.log(f"Компания '{self.name}' сохранена в {filename}")
        except Exception as e:
            self._logger.log(f"Ошибка при сохранении компании: {e}", level='ERROR')
            raise
    
    @classmethod
    def load_from_json(cls, filename: str) -> Company:
        """Загрузить компанию из JSON файла."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Создание компании
            company = cls(data['company_name'])
            
            # Создание карты сотрудников
            employee_map = {}
            
            # Создание отделов и сотрудников
            for dept_data in data['departments']:
                department = Department.from_dict(dept_data)
                company.add_department(department)
                
                # Добавление сотрудников в карту
                for emp in department.get_employees():
                    employee_map[emp.id] = emp
            
            # Создание проектов
            for proj_data in data['projects']:
                project = Project.from_dict(proj_data, employee_map)
                company.add_project(project)
            
            return company
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не найден")
        except Exception as e:
            raise ValueError(f"Ошибка при загрузке компании: {e}")