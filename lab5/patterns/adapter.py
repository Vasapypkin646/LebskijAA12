from abc import ABC, abstractmethod
from typing import Dict, Any

class ExternalSalaryCalculator(ABC):
    """Абстрактный интерфейс внешней системы расчета зарплат"""
    
    @abstractmethod
    def compute_payment(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

class SimpleSalaryCalculator(ExternalSalaryCalculator):
    """Простая реализация внешнего калькулятора зарплат"""
    
    def compute_payment(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Вычисляет зарплату с использованием внешних правил"""
        base_salary = employee_data.get('base_salary', 0)
        employee_type = employee_data.get('type', 'Employee')
        
        # Внешние правила расчета
        multipliers = {
            'Employee': 1.0,
            'Manager': 1.2,
            'Developer': 1.3,
            'Saleperson': 1.1
        }
        
        multiplier = multipliers.get(employee_type, 1.0)
        
        # Дополнительные расчеты из внешней системы
        if employee_type == 'Manager':
            bonus = employee_data.get('bonus', 0)
            adjusted_salary = base_salary + bonus
        elif employee_type == 'Developer':
            seniority = employee_data.get('seniority_level', 'junior')
            seniority_multipliers = {
                'junior': 1.0,
                'middle': 1.5,
                'senior': 2.0
            }
            adjusted_salary = base_salary * seniority_multipliers.get(seniority, 1.0)
        elif employee_type == 'Saleperson':
            commission = employee_data.get('commission_rate', 0)
            sales = employee_data.get('sales_volume', 0)
            adjusted_salary = base_salary + (commission * sales)
        else:
            adjusted_salary = base_salary
        
        # Применяем внешний множитель
        total_amount = adjusted_salary * multiplier
        
        return {
            'base_amount': base_salary,
            'adjusted_amount': adjusted_salary,
            'multiplier': multiplier,
            'total_amount': total_amount,
            'currency': 'RUB',
            'calculation_method': 'external_system'
        }

class SalaryCalculatorAdapter:
    """
    Паттерн Adapter для адаптации внешней системы расчета зарплат
    к интерфейсу нашей системы.
    """
    
    def __init__(self, external_calculator: ExternalSalaryCalculator = None):
        self._external_calculator = external_calculator or SimpleSalaryCalculator()
    
    def calculate_salary(self, employee) -> float:
        """Адаптирует метод расчета зарплаты для внешней системы"""
        employee_data = employee.to_dict()
        external_result = self._external_calculator.compute_payment(employee_data)
        return external_result['total_amount']
    
    def get_detailed_calculation(self, employee) -> Dict[str, Any]:
        """Получает детальную информацию о расчете зарплаты"""
        employee_data = employee.to_dict()
        return self._external_calculator.compute_payment(employee_data)