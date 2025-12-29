"""
Паттерн Adapter.
"""
from typing import Dict, Any
from entities.employee import AbstractEmployee


class ExternalSalarySystem:
    """Внешняя система расчета зарплат."""
    
    def calculate_external_salary(self, employee_data: Dict[str, Any]) -> float:
        """Рассчитать зарплату во внешней системе."""
        # В реальной системе здесь был бы вызов API
        base = employee_data.get('base_salary', 0)
        
        if employee_data.get('type') == 'Manager':
            return base * 1.2 + employee_data.get('bonus', 0)
        elif employee_data.get('type') == 'Developer':
            level = employee_data.get('seniority_level', 'junior')
            multipliers = {'junior': 1.0, 'middle': 1.3, 'senior': 1.8}
            return base * multipliers.get(level, 1.0)
        elif employee_data.get('type') == 'Salesperson':
            return base + (employee_data.get('commission_rate', 0) * 
                          employee_data.get('sales_volume', 0) * 0.9)
        else:
            return base * 1.05  # Все остальные получают +5%


class SalaryCalculatorAdapter:
    """Адаптер для внешней системы расчета зарплат."""
    
    def __init__(self):
        self._external_system = ExternalSalarySystem()
    
    def calculate_salary(self, employee: AbstractEmployee) -> float:
        """Рассчитать зарплату через адаптер."""
        employee_data = employee.to_dict()
        return self._external_system.calculate_external_salary(employee_data)