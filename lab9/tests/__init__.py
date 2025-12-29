"""
Модуль тестов.

Содержит unit-тесты для проверки функциональности системы.
"""

import pytest

# Реэкспорт основных тестовых модулей
from .test_employee import (
    TestEmployee,
    TestManager,
    TestDeveloper,
    TestSalesperson
)

from .test_department import TestDepartment

__all__ = [
    'TestEmployee',
    'TestManager',
    'TestDeveloper',
    'TestSalesperson',
    'TestDepartment',
    'pytest',
]