"""
Тесты для класса Department.
"""

import pytest
import tempfile
import os
from entities.employee import Employee, EmployeeData
from entities.department import Department
from utils.exceptions import EmployeeNotFoundError


class TestDepartment:
    """Тесты для класса Department."""
    
    @pytest.fixture
    def sample_employees(self):
        """Фикстура с тестовыми сотрудниками."""
        return [
            Employee(EmployeeData(id=1, name="Alice", department="IT", base_salary=50000)),
            Employee(EmployeeData(id=2, name="Bob", department="IT", base_salary=60000)),
            Employee(EmployeeData(id=3, name="Charlie", department="IT", base_salary=55000))
        ]
    
    @pytest.fixture
    def sample_department(self, sample_employees):
        """Фикстура с тестовым отделом."""
        department = Department("IT")
        for emp in sample_employees:
            department.add_employee(emp)
        return department
    
    def test_create_department(self):
        """Тест создания отдела."""
        department = Department("IT")
        assert department.name == "IT"
        assert len(department) == 0
    
    def test_add_employee(self, sample_department):
        """Тест добавления сотрудника."""
        assert len(sample_department) == 3
        
        new_employee = Employee(EmployeeData(id=4, name="David", department="IT", base_salary=65000))
        sample_department.add_employee(new_employee)
        
        assert len(sample_department) == 4
        assert new_employee in sample_department
    
    def test_remove_employee(self, sample_department):
        """Тест удаления сотрудника."""
        removed = sample_department.remove_employee(2)
        
        assert removed.id == 2
        assert removed.name == "Bob"
        assert len(sample_department) == 2
    
    def test_remove_nonexistent_employee(self, sample_department):
        """Тест удаления несуществующего сотрудника."""
        with pytest.raises(EmployeeNotFoundError):
            sample_department.remove_employee(999)
    
    def test_find_employee_by_id(self, sample_department):
        """Тест поиска сотрудника по ID."""
        employee = sample_department.find_employee_by_id(1)
        assert employee is not None
        assert employee.id == 1
        assert employee.name == "Alice"
    
    def test_calculate_total_salary(self, sample_department):
        """Тест расчета общей зарплаты."""
        total = sample_department.calculate_total_salary()
        expected = 50000 + 60000 + 55000
        assert total == expected
    
    def test_get_employee_count_by_type(self, sample_department):
        """Тест подсчета сотрудников по типам."""
        counts = sample_department.get_employee_count_by_type()
        assert counts == {"Employee": 3}
    
    def test_has_employees(self):
        """Тест проверки наличия сотрудников."""
        empty_department = Department("HR")
        assert not empty_department.has_employees()
        
        populated_department = Department("IT")
        populated_department.add_employee(
            Employee(EmployeeData(id=1, name="Test", department="IT", base_salary=50000))
        )
        assert populated_department.has_employees()
    
    def test_department_iteration(self, sample_department):
        """Тест итерации по отделу."""
        employee_names = [emp.name for emp in sample_department]
        assert employee_names == ["Alice", "Bob", "Charlie"]
    
    def test_department_contains(self, sample_department, sample_employees):
        """Тест оператора in."""
        assert sample_employees[0] in sample_department
        assert sample_employees[1] in sample_department
    
    def test_save_and_load_department(self, sample_department):
        """Тест сохранения и загрузки отдела."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            # Сохраняем отдел
            sample_department.save_to_file(filename)
            assert os.path.exists(filename)
            
            # Загружаем отдел
            loaded_department = Department.load_from_file(filename)
            
            # Проверяем, что данные совпадают
            assert loaded_department.name == sample_department.name
            assert len(loaded_department) == len(sample_department)
            
            # Проверяем сотрудников
            original_employees = {emp.id: emp for emp in sample_department}
            loaded_employees = {emp.id: emp for emp in loaded_department}
            
            for emp_id in original_employees:
                assert emp_id in loaded_employees
                assert original_employees[emp_id].name == loaded_employees[emp_id].name
        
        finally:
            # Удаляем временный файл
            if os.path.exists(filename):
                os.unlink(filename)
    
    @pytest.fixture(autouse=True)
    def reset_ids(self):
        """Фикстура для сброса ID перед каждым тестом."""
        from entities.employee import AbstractEmployee
        AbstractEmployee.reset_ids()
        yield
        AbstractEmployee.reset_ids()