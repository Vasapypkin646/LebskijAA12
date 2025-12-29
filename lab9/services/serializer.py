"""
Сериализация и десериализация данных.
"""

import json
import csv
from typing import List, Dict, Any
from datetime import datetime
from entities.employee import AbstractEmployee
from entities.department import Department
from entities.company import Company


class JSONSerializer:
    """Сериализатор в JSON."""
    
    @staticmethod
    def serialize_employee(employee: AbstractEmployee) -> str:
        """Сериализовать сотрудника в JSON."""
        return json.dumps(employee.to_dict(), ensure_ascii=False, indent=2)
    
    @staticmethod
    def serialize_department(department: Department) -> str:
        """Сериализовать отдел в JSON."""
        return json.dumps(department.to_dict(), ensure_ascii=False, indent=2)
    
    @staticmethod
    def serialize_company(company: Company) -> str:
        """Сериализовать компанию в JSON."""
        return json.dumps(company.to_dict(), ensure_ascii=False, indent=2)


class CSVExporter:
    """Экспортер в CSV."""
    
    @staticmethod
    def export_employees_to_csv(employees: List[AbstractEmployee], filename: str) -> None:
        """Экспортировать сотрудников в CSV."""
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Заголовки
            writer.writerow([
                'ID', 'Имя', 'Отдел', 'Должность', 'Базовая зарплата',
                'Итоговая зарплата', 'Дополнительная информация'
            ])
            
            # Данные
            for employee in employees:
                emp_type = employee.__class__.__name__
                additional_info = ""
                
                if hasattr(employee, 'bonus'):
                    additional_info = f"Бонус: {getattr(employee, 'bonus')}"
                elif hasattr(employee, 'seniority_level'):
                    additional_info = f"Уровень: {getattr(employee, 'seniority_level')}"
                elif hasattr(employee, 'commission_rate'):
                    additional_info = f"Комиссия: {getattr(employee, 'commission_rate')}"
                
                writer.writerow([
                    employee.id,
                    employee.name,
                    employee.department,
                    emp_type,
                    f"{employee.base_salary:.2f}",
                    f"{employee.calculate_salary():.2f}",
                    additional_info
                ])


