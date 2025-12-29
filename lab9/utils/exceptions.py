# utils/exceptions.py
"""
Модуль с пользовательскими исключениями.
"""


class EmployeeNotFoundError(Exception):
    """Исключение для случая, когда сотрудник не найден."""
    pass


class DepartmentNotFoundError(Exception):
    """Исключение для случая, когда отдел не найден."""
    pass


class ProjectNotFoundError(Exception):
    """Исключение для случая, когда проект не найден."""
    pass


class InvalidStatusError(Exception):
    """Исключение для недопустимого статуса."""
    pass


class DuplicateIdError(Exception):
    """Исключение для дублирования ID."""
    pass


class InvalidDateError(Exception):
    """Исключение для некорректной даты."""
    pass


class InvalidSalaryError(Exception):
    """Исключение для некорректной зарплаты."""
    pass


class InvalidInputError(Exception):
    """Исключение для некорректных входных данных."""
    pass