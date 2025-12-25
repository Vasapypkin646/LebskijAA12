import pytest
import json
import os
from Zadanie import Employee, Manager, Developer, Saleperson, Department, AbstractEmployee
from Zadanie import EmployeeNotFoundError

class TestDepartment:
    """Тесты для класса Department"""

    @pytest.fixture
    def sample_department(self):
        """Фикстура: тестовый отдел с сотрудниками"""
        dept = Department("IT")
        dept.add_employee(Employee(1, "Alice", "IT", 5000, skip_validation=True))
        dept.add_employee(Manager(2, "Bob", "IT", 7000, 2000, skip_validation=True))
        dept.add_employee(Developer(3, "Charlie", "IT", 6000, ["Python"], "senior", skip_validation=True))
        return dept

    def test_department_creation(self):
        """Тест создания отдела"""
        # Arrange & Act
        dept = Department("Development")
        
        # Assert
        assert dept.name == "Development"
        assert len(dept) == 0

    def test_department_add_employee(self):
        """Тест добавления сотрудника в отдел"""
        # Arrange
        dept = Department("HR")
        emp = Employee(101, "John", "HR", 4000, skip_validation=True)
        
        # Act
        dept.add_employee(emp)
        
        # Assert
        assert len(dept) == 1
        assert dept[101] == emp

    def test_department_remove_employee(self):
        """Тест удаления сотрудника из отдела"""
        # Arrange
        dept = Department("Sales")
        emp = Employee(102, "Jane", "Sales", 4500, skip_validation=True)
        dept.add_employee(emp)
        assert len(dept) == 1
        
        # Act
        dept.remove_employee(102)
        
        # Assert
        assert len(dept) == 0

    def test_department_duplicate_id_error(self):
        """Тест: добавление сотрудника с дублирующимся ID вызывает ошибку"""
        # Arrange
        dept = Department("IT")
        emp1 = Employee(103, "Alice", "IT", 5000, skip_validation=True)
        emp2 = Employee(103, "Bob", "IT", 6000, skip_validation=True)
        dept.add_employee(emp1)
        
        # Act & Assert
        with pytest.raises(ValueError, match="уже существует в отделе"):
            dept.add_employee(emp2)

    def test_department_get_employees(self, sample_department):
        """Тест получения списка сотрудников"""
        # Act
        employees = sample_department.get_employees()
        
        # Assert
        assert len(employees) == 3
        assert all(isinstance(emp, AbstractEmployee) for emp in employees)

    def test_department_calculate_total_salary(self, sample_department):
        """Тест расчета общей зарплаты отдела"""
        # Act
        total = sample_department.calculate_total_salary()
        
        # Assert
        # Employee: 5000, Manager: 7000+2000=9000, Developer: 6000*2=12000
        expected = 5000 + 9000 + 12000
        assert total == expected

    def test_department_get_employee_count(self, sample_department):
        """Тест подсчета сотрудников по типам"""
        # Act
        counts = sample_department.get_employee_count()
        
        # Assert
        assert counts["Employee"] == 1
        assert counts["Manager"] == 1
        assert counts["Developer"] == 1
        assert counts["Salesperson"] == 0

    def test_department_find_employee_by_id(self, sample_department):
        """Тест поиска сотрудника по ID"""
        # Act
        found = sample_department.find_employee_by_id(2)
        
        # Assert
        assert found is not None
        assert found.name == "Bob"
        assert isinstance(found, Manager)

    def test_department_find_nonexistent_employee(self, sample_department):
        """Тест поиска несуществующего сотрудника"""
        # Act & Assert
        with pytest.raises(EmployeeNotFoundError):
            sample_department.find_employee_by_id(999)

    def test_department_len(self, sample_department):
        """Тест магического метода __len__"""
        assert len(sample_department) == 3

    def test_department_getitem(self, sample_department):
        """Тест магического метода __getitem__"""
        employee = sample_department[1]
        assert employee.name == "Alice"

    def test_department_contains(self, sample_department):
        """Тест магического метода __contains__"""
        emp = Employee(1, "Alice", "IT", 5000, skip_validation=True)
        assert emp in sample_department
        
        emp2 = Employee(999, "Nonexistent", "IT", 5000, skip_validation=True)
        assert emp2 not in sample_department

    def test_department_iteration(self, sample_department):
        """Тест итерации по отделу"""
        # Act
        count = 0
        names = []
        for employee in sample_department:
            count += 1
            names.append(employee.name)
        
        # Assert
        assert count == 3
        assert "Alice" in names
        assert "Bob" in names
        assert "Charlie" in names

    def test_department_serialization(self, sample_department, tmp_path):
        """Тест сериализации отдела в JSON"""
        # Arrange
        filename = tmp_path / "test_department.json"
        
        # Act
        sample_department.save_to_file(str(filename))
        
        # Assert
        assert os.path.exists(filename)
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data['name'] == "IT"
        assert data['employee_count'] == 3
        assert data['total_salary'] == 26000
        assert len(data['employees']) == 3

    def test_department_deserialization(self, sample_department, tmp_path):
        """Тест десериализации отдела из JSON"""
        # Arrange
        filename = tmp_path / "test_department.json"
        sample_department.save_to_file(str(filename))
        
        # Act
        loaded_dept = Department.load_from_file(str(filename))
        
        # Assert
        assert loaded_dept.name == "IT"
        assert len(loaded_dept) == 3
        assert loaded_dept.calculate_total_salary() == 26000

    def test_department_to_dict(self, sample_department):
        """Тест метода to_dict"""
        # Act
        data = sample_department.to_dict()
        
        # Assert
        assert 'name' in data
        assert 'employee_count' in data
        assert 'total_salary' in data
        assert 'employees_by_type' in data
        assert 'employees' in data
        assert len(data['employees']) == 3

    def test_department_from_dict(self):
        """Тест метода from_dict"""
        # Arrange
        employees = [
            Employee(901, "John", "IT", 5000, skip_validation=True).to_dict(),
            Manager(902, "Sarah", "IT", 7000, 2000, skip_validation=True).to_dict()
        ]
        test_data = {
            'name': 'TestDept',
            'employees': employees
        }
        
        # Act
        dept = Department.from_dict(test_data)
        
        # Assert
        assert dept.name == "TestDept"
        assert len(dept) == 2

    def test_department_has_employees(self):
        """Тест метода has_employees"""
        # Arrange
        dept1 = Department("EmptyDept")
        dept2 = Department("FullDept")
        dept2.add_employee(Employee(1001, "Test", "Dept", 3000, skip_validation=True))
        
        # Assert
        assert not dept1.has_employees()
        assert dept2.has_employees()

    def test_department_sorting(self):
        """Тест сортировки сотрудников в отделе"""
        # Arrange
        dept = Department("Test")
        employees = [
            Employee(1101, "Charlie", "Test", 7000, skip_validation=True),
            Employee(1102, "Alice", "Test", 5000, skip_validation=True),
            Employee(1103, "Bob", "Test", 6000, skip_validation=True)
        ]
        
        for emp in employees:
            dept.add_employee(emp)
        
        # Сортировка по имени через sorted
        sorted_by_name = sorted(dept.get_employees(), key=lambda x: x.name)
        assert sorted_by_name[0].name == "Alice"
        assert sorted_by_name[1].name == "Bob"
        assert sorted_by_name[2].name == "Charlie"
        
        # Сортировка по зарплате
        sorted_by_salary = sorted(dept.get_employees(), key=lambda x: x.calculate_salary())
        assert sorted_by_salary[0].calculate_salary() == 5000
        assert sorted_by_salary[2].calculate_salary() == 7000
if __name__ == "__main__":
    pytest.main([__file__, "-v"])