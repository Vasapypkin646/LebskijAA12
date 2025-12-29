"""
Фабрика сотрудников.
"""

from typing import Dict, Any
from entities.employee import (
    Employee, Manager, Developer, Salesperson, 
    EmployeeData, AbstractEmployee
)
from utils.exceptions import InvalidInputError


class EmployeeFactory:
    """Фабрика для создания сотрудников."""
    
    @staticmethod
    def create_employee(employee_type: str, **kwargs) -> AbstractEmployee:
        """Создать сотрудника указанного типа.
        
        Args:
            employee_type: Тип сотрудника ('employee', 'manager', 'developer', 'salesperson')
            **kwargs: Параметры сотрудника
            
        Returns:
            Созданный сотрудник
        """
        # Базовые данные
        data = EmployeeData(
            id=kwargs.get('id'),
            name=kwargs.get('name'),
            department=kwargs.get('department'),
            base_salary=kwargs.get('base_salary', 0.0)
        )
        
        if employee_type == 'employee':
            return Employee(data)
        
        elif employee_type == 'manager':
            bonus = kwargs.get('bonus', 0.0)
            return Manager(data, bonus)
        
        elif employee_type == 'developer':
            tech_stack = kwargs.get('tech_stack', [])
            seniority_level = kwargs.get('seniority_level', 'junior')
            return Developer(data, tech_stack, seniority_level)
        
        elif employee_type == 'salesperson':
            commission_rate = kwargs.get('commission_rate', 0.0)
            sales_volume = kwargs.get('sales_volume', 0.0)
            return Salesperson(data, commission_rate, sales_volume)
        
        else:
            raise ValueError(f"Неизвестный тип сотрудника: {employee_type}")
    
    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> AbstractEmployee:
        """Создать сотрудника из словаря.
        
        Args:
            data: Словарь с данными сотрудника
            
        Returns:
            Созданный сотрудник
        """
        employee_type = data.get('type', 'Employee')
        
        base_data = EmployeeData(
            id=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary']
        )
        
        if employee_type == 'Manager':
            return Manager(base_data, data.get('bonus', 0.0))
        
        elif employee_type == 'Developer':
            return Developer(
                base_data,
                data.get('tech_stack', []),
                data.get('seniority_level', 'junior')
            )
        
        elif employee_type == 'Salesperson':
            return Salesperson(
                base_data,
                data.get('commission_rate', 0.0),
                data.get('sales_volume', 0.0)
            )
        
        else:  # Employee или неизвестный тип
            return Employee(base_data)