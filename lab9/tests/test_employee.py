"""
Тесты для классов сотрудников.
"""

import pytest
from entities.employee import (
    Employee, Manager, Developer, Salesperson, 
    EmployeeData, AbstractEmployee
)
from utils.exceptions import InvalidSalaryError, DuplicateIdError


class TestEmployee:
    """Тесты для класса Employee."""
    
    def test_create_employee(self):
        """Тест создания сотрудника."""
        data = EmployeeData(id=1, name="John", department="IT", base_salary=50000)
        employee = Employee(data)
        
        assert employee.id == 1
        assert employee.name == "John"
        assert employee.department == "IT"
        assert employee.base_salary == 50000
        assert employee.calculate_salary() == 50000
    
    def test_invalid_salary(self):
        """Тест некорректной зарплаты."""
        with pytest.raises(InvalidSalaryError):
            data = EmployeeData(id=2, name="Bob", department="HR", base_salary=-1000)
            Employee(data)
    
    def test_duplicate_id(self):
        """Тест дублирования ID."""
        data1 = EmployeeData(id=3, name="Alice", department="IT", base_salary=50000)
        Employee(data1)
        
        with pytest.raises(DuplicateIdError):
            data2 = EmployeeData(id=3, name="Bob", department="HR", base_salary=60000)
            Employee(data2)
    
    def test_employee_comparison(self):
        """Тест сравнения сотрудников."""
        data1 = EmployeeData(id=4, name="Alice", department="IT", base_salary=50000)
        data2 = EmployeeData(id=5, name="Bob", department="IT", base_salary=60000)
        
        emp1 = Employee(data1)
        emp2 = Employee(data2)
        
        assert emp1 < emp2
        assert not emp2 < emp1
        assert emp1 + emp2 == 110000


class TestManager:
    """Тесты для класса Manager."""
    
    def test_create_manager(self):
        """Тест создания менеджера."""
        data = EmployeeData(id=10, name="Manager", department="IT", base_salary=70000)
        manager = Manager(data, bonus=15000)
        
        assert manager.id == 10
        assert manager.bonus == 15000
        assert manager.calculate_salary() == 85000  # 70000 + 15000
    
    def test_manager_bonus_update(self):
        """Тест обновления бонуса менеджера."""
        data = EmployeeData(id=11, name="Manager2", department="IT", base_salary=60000)
        manager = Manager(data, bonus=10000)
        
        manager.bonus = 20000
        assert manager.bonus == 20000
        assert manager.calculate_salary() == 80000


class TestDeveloper:
    """Тесты для класса Developer."""
    
    def test_create_developer(self):
        """Тест создания разработчика."""
        data = EmployeeData(id=20, name="Dev", department="Dev", base_salary=50000)
        developer = Developer(data, tech_stack=["Python", "Java"], seniority_level="senior")
        
        assert developer.id == 20
        assert developer.seniority_level == "senior"
        assert set(developer.get_skills()) == {"Python", "Java"}
        assert developer.calculate_salary() == 100000  # 50000 * 2.0
    
    def test_developer_skills(self):
        """Тест управления навыками разработчика."""
        data = EmployeeData(id=21, name="Dev2", department="Dev", base_salary=40000)
        developer = Developer(data, tech_stack=["Python"], seniority_level="middle")
        
        developer.add_skill("Django")
        developer.add_skill("PostgreSQL")
        
        skills = developer.get_skills()
        assert "Python" in skills
        assert "Django" in skills
        assert "PostgreSQL" in skills
        assert len(skills) == 3
    
    def test_developer_salary_by_level(self):
        """Тест зарплаты разработчика по уровням."""
        data = EmployeeData(id=22, name="Dev3", department="Dev", base_salary=40000)
        
        # Junior
        dev_junior = Developer(data, tech_stack=[], seniority_level="junior")
        assert dev_junior.calculate_salary() == 40000  # 40000 * 1.0
        
        # Middle
        dev_middle = Developer(data, tech_stack=[], seniority_level="middle")
        assert dev_middle.calculate_salary() == 60000  # 40000 * 1.5
        
        # Senior
        dev_senior = Developer(data, tech_stack=[], seniority_level="senior")
        assert dev_senior.calculate_salary() == 80000  # 40000 * 2.0


class TestSalesperson:
    """Тесты для класса Salesperson."""
    
    def test_create_salesperson(self):
        """Тест создания продавца."""
        data = EmployeeData(id=30, name="Sales", department="Sales", base_salary=40000)
        salesperson = Salesperson(data, commission_rate=0.1, sales_volume=500000)
        
        assert salesperson.id == 30
        assert salesperson.commission_rate == 0.1
        assert salesperson.sales_volume == 500000
        assert salesperson.calculate_salary() == 90000  # 40000 + 0.1*500000
    
    def test_salesperson_update_sales(self):
        """Тест обновления продаж."""
        data = EmployeeData(id=31, name="Sales2", department="Sales", base_salary=35000)
        salesperson = Salesperson(data, commission_rate=0.15, sales_volume=300000)
        
        salesperson.update_sales(200000)
        assert salesperson.sales_volume == 500000
        assert salesperson.calculate_salary() == 110000  # 35000 + 0.15*500000
    
    @pytest.fixture(autouse=True)
    def reset_ids(self):
        """Фикстура для сброса ID перед каждым тестом."""
        AbstractEmployee.reset_ids()
        yield
        AbstractEmployee.reset_ids()