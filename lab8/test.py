import pytest
from Zadanie import Employee, Manager, Developer, Saleperson, AbstractEmployee, Validator, DuplicateIdError, InvalidSalaryError

class TestEmployee:
    """Тесты для базового класса Employee"""

    def test_employee_creation_valid_data(self):
        """Тест создания сотрудника с валидными данными"""
        # Arrange
        emp = Employee(100, "Alice", "IT", 5000, skip_validation=True)
        
        # Assert
        assert emp.id == 100
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000

    def test_employee_invalid_id_raises_error(self):
        """Тест: отрицательный ID вызывает ValueError"""
        # Act & Assert
        with pytest.raises(ValueError):
            Employee(-1, "Alice", "IT", 5000)

    def test_employee_invalid_salary_raises_error(self):
        """Тест: отрицательная зарплата вызывает InvalidSalaryError"""
        # Act & Assert
        with pytest.raises(InvalidSalaryError):
            Employee(1, "Alice", "IT", -1000)

    def test_employee_empty_name_raises_error(self):
        """Тест: пустое имя вызывает ошибку при сеттере"""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000, skip_validation=True)
        
        # Act & Assert
        with pytest.raises(ValueError):
            emp.name = ""

    def test_employee_calculate_salary(self):
        """Тест расчета зарплаты обычного сотрудника"""
        # Arrange
        emp = Employee(101, "Alice", "IT", 5000, skip_validation=True)
        
        # Act
        salary = emp.calculate_salary()
        
        # Assert
        assert salary == 5000

    def test_employee_str_representation(self):
        """Тест строкового представления"""
        # Arrange
        emp = Employee(102, "Alice", "IT", 5000, skip_validation=True)
        
        # Act
        result = str(emp)
        
        # Assert
        expected = "Сотрудник id: 102, имя: Alice, отдел: IT, базовая зарплата:5000"
        assert result == expected

    def test_employee_equality(self):
        """Тест сравнения сотрудников по ID"""
        # Arrange
        emp1 = Employee(1, "John", "IT", 5000, skip_validation=True)
        emp2 = Employee(1, "Jane", "HR", 4000, skip_validation=True)
        emp3 = Employee(2, "Bob", "IT", 5000, skip_validation=True)
        
        # Assert
        assert emp1 == emp2  # одинаковый ID
        assert emp1 != emp3  # разный ID

    def test_employee_salary_comparison(self):
        """Тест сравнения сотрудников по зарплате"""
        # Arrange
        emp1 = Employee(1, "John", "IT", 5000, skip_validation=True)
        emp2 = Employee(2, "Jane", "HR", 6000, skip_validation=True)
        
        # Assert
        assert emp1 < emp2
        assert emp2 > emp1

    def test_employee_addition(self):
        """Тест сложения зарплат сотрудников"""
        # Arrange
        emp1 = Employee(1, "John", "IT", 5000, skip_validation=True)
        emp2 = Employee(2, "Jane", "HR", 6000, skip_validation=True)
        
        # Act
        total_salary = emp1 + emp2
        
        # Assert
        assert total_salary == 11000

    def test_employee_sum_in_list(self):
        """Тест использования в функции sum()"""
        # Arrange
        employees = [
            Employee(1, "John", "IT", 5000, skip_validation=True),
            Employee(2, "Jane", "HR", 6000, skip_validation=True),
            Employee(3, "Bob", "IT", 7000, skip_validation=True)
        ]
        
        # Act
        total = sum(employees)
        
        # Assert
        assert total == 18000

    @pytest.mark.parametrize("salary,expected", [
        (0, True),
        (1000, True),
        (500000, True),
        (1000000, True),
        (-100, False),
        (2000000, False)
    ])
    def test_validator_salary(self, salary, expected):
        """Параметризованный тест валидации зарплаты"""
        if expected:
            Validator.validate_salary(salary)
        else:
            with pytest.raises(InvalidSalaryError):
                Validator.validate_salary(salary)

    def test_employee_to_dict(self):
        """Тест сериализации в словарь"""
        # Arrange
        emp = Employee(105, "Alice", "IT", 5000, skip_validation=True)
        
        # Act
        data = emp.to_dict()
        
        # Assert
        assert data['id'] == 105
        assert data['name'] == "Alice"
        assert data['department'] == "IT"
        assert data['base_salary'] == 5000
        assert data['calculated_salary'] == 5000
        assert data['type'] == "Employee"

    def test_employee_from_dict(self):
        """Тест десериализации из словаря"""
        # Arrange
        original = Employee(106, "Bob", "HR", 4000, skip_validation=True)
        data = original.to_dict()
        
        # Act
        restored = Employee.from_dict(data)
        
        # Assert
        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.department == original.department
        assert restored.base_salary == original.base_salary



    class TestManager:
        """Тесты для класса Manager"""
        
    def test_manager_creation(self):
        """Тест создания менеджера"""
        # Arrange
        manager = Manager(200, "John", "Management", 5000, 1000, skip_validation=True)
        
        # Assert
        assert manager.id == 200
        assert manager.name == "John"
        assert manager.department == "Management"
        assert manager.base_salary == 5000
        assert manager.bonus == 1000

    def test_manager_salary_calculation(self):
        """Тест расчета зарплаты менеджера с бонусом"""
        # Arrange
        manager = Manager(201, "John", "Management", 5000, 1000, skip_validation=True)
        
        # Act
        salary = manager.calculate_salary()
        
        # Assert
        assert salary == 6000

    def test_manager_get_info(self, capsys):
        """Тест метода get_info для менеджера"""
        # Arrange
        manager = Manager(202, "John", "Management", 5000, 1000, skip_validation=True)
        
        # Act
        manager.get_info()
        captured = capsys.readouterr()
        
        # Assert
        assert "бонус: 1000" in captured.out
        assert "итоговая зарплата: 6000" in captured.out

    def test_manager_to_dict(self):
        """Тест сериализации менеджера"""
        # Arrange
        manager = Manager(203, "John", "Management", 5000, 1000, skip_validation=True)
        
        # Act
        data = manager.to_dict()
        
        # Assert
        assert data['type'] == "Manager"
        assert data['bonus'] == 1000
        assert data['calculated_salary'] == 6000

    def test_manager_from_dict(self):
        """Тест десериализации менеджера"""
        # Arrange
        original = Manager(204, "Alice", "Management", 6000, 1500, skip_validation=True)
        data = original.to_dict()
        
        # Act
        restored = Manager.from_dict(data)
        
        # Assert
        assert restored.id == original.id
        assert restored.bonus == original.bonus
        assert restored.calculate_salary() == original.calculate_salary()
    if __name__ == "__main__":
        pytest.main([__file__, "-v"])