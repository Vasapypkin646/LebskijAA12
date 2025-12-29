
"""
Вспомогательные функции.
"""

from typing import List, Callable, TypeVar, Any
from functools import cmp_to_key
from entities.employee import AbstractEmployee

T = TypeVar('T')


def sort_by_key(items: List[T], key_func: Callable[[T], Any], reverse: bool = False) -> List[T]:
    """Сортировка по ключу."""
    return sorted(items, key=key_func, reverse=reverse)


def compare_employees_by_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Сравнение сотрудников по имени."""
    if emp1.name < emp2.name:
        return -1
    elif emp1.name > emp2.name:
        return 1
    return 0


def compare_employees_by_salary(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Сравнение сотрудников по зарплате (по убыванию)."""
    salary1 = emp1.calculate_salary()
    salary2 = emp2.calculate_salary()
    if salary1 > salary2:
        return -1
    elif salary1 < salary2:
        return 1
    return 0


def get_name_key(employee: AbstractEmployee) -> str:
    """Ключ для сортировки по имени."""
    return employee.name


def get_salary_key(employee: AbstractEmployee) -> float:
    """Ключ для сортировки по зарплате (для убывания используем отрицательное значение)."""
    return -employee.calculate_salary()


def get_department_name_key(employee: AbstractEmployee) -> tuple:
    """Ключ для сортировки по отделу, затем по имени."""
    return (employee.department, employee.name)