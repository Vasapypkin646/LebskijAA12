import pytest
from Zadanie import Employee, Manager, Developer, Saleperson, AbstractEmployee
from Zadanie import EmployeeFactory

class TestDeveloper:
    """Тесты для класса Developer"""

    def test_developer_creation(self):
        """Тест создания разработчика"""
        # Arrange
        dev = Developer(300, "Alice", "DEV", 5000, ["Python", "Java"], "senior", skip_validation=True)
        
        # Assert
        assert dev.id == 300
        assert dev.name == "Alice"
        assert dev.department == "DEV"
        assert dev.base_salary == 5000

    @pytest.mark.parametrize("level,expected_salary", [
        ("junior", 5000),
        ("middle", 7500),
        ("senior", 10000)
    ])
    def test_developer_salary_by_level(self, level, expected_salary):
        """Параметризованный тест зарплаты по уровню"""
        # Arrange
        dev = Developer(301, "Bob", "DEV", 5000, ["Python"], level, skip_validation=True)
        
        # Act & Assert
        assert dev.calculate_salary() == expected_salary

    def test_developer_add_skill(self):
        """Тест добавления навыка разработчику"""
        # Arrange
        dev = Developer(302, "Charlie", "DEV", 5000, ["Python"], "middle", skip_validation=True)
        
        # Act
        dev.add_skill("JavaScript")
        
        # Проверяем через итератор
        skills = list(dev)
        
        # Assert
        assert "JavaScript" in skills
        assert len(skills) == 2

    def test_developer_iteration(self):
        """Тест итерации по навыкам разработчика"""
        # Arrange
        dev = Developer(303, "Dave", "DEV", 5000, ["Python", "Java", "SQL"], "senior", skip_validation=True)
        
        # Act
        skills = []
        for skill in dev:
            skills.append(skill)
        
        # Assert
        assert skills == ["Python", "Java", "SQL"]

    def test_developer_get_info(self, capsys):
        """Тест метода get_info для разработчика"""
        # Arrange
        dev = Developer(304, "Eve", "DEV", 5000, ["Python", "Docker"], "senior", skip_validation=True)
        
        # Act
        dev.get_info()
        captured = capsys.readouterr()
        
        # Assert
        assert "список технологий:['Python', 'Docker']" in captured.out
        assert "уровень: senior" in captured.out
        assert "итоговая зарплата: 10000" in captured.out

    def test_developer_to_dict(self):
        """Тест сериализации разработчика"""
        # Arrange
        dev = Developer(305, "Frank", "DEV", 5000, ["Python", "Go"], "middle", skip_validation=True)
        
        # Act
        data = dev.to_dict()
        
        # Assert
        assert data['type'] == "Developer"
        assert data['tech_stack'] == ["Python", "Go"]
        assert data['seniority_level'] == "middle"
        assert data['calculated_salary'] == 7500

class TestSalesperson:
    """Тесты для класса Salesperson"""

    def test_salesperson_creation(self):
        """Тест создания продавца"""
        # Arrange
        sales = Saleperson(400, "Grace", "SALES", 4000, 0.1, 50000, skip_validation=True)
        
        # Assert
        assert sales.id == 400
        assert sales.name == "Grace"
        assert sales.department == "SALES"
        assert sales.base_salary == 4000

    def test_salesperson_salary_calculation(self):
        """Тест расчета зарплаты продавца"""
        # Arrange
        sales = Saleperson(401, "Hank", "SALES", 4000, 0.15, 50000, skip_validation=True)
        
        # Act
        salary = sales.calculate_salary()
        
        # Assert
        expected = 4000 + (0.15 * 50000)
        assert salary == expected

    def test_salesperson_update_sales(self):
        """Тест обновления объема продаж"""
        # Arrange
        sales = Saleperson(402, "Ivy", "SALES", 4000, 0.1, 50000, skip_validation=True)
        initial_salary = sales.calculate_salary()
        
        # Act
        sales.update_sales(20000)
        new_salary = sales.calculate_salary()
        
        # Assert
        assert new_salary > initial_salary
        assert new_salary == 4000 + (0.1 * 70000)

    def test_salesperson_get_info(self, capsys):
        """Тест метода get_info для продавца"""
        # Arrange
        sales = Saleperson(403, "Jack", "SALES", 4000, 0.12, 60000, skip_validation=True)
        
        # Act
        sales.get_info()
        captured = capsys.readouterr()
        
        # Assert
        assert "процент комиссии: 0.12" in captured.out
        assert "объем продаж: 60000" in captured.out

class TestEmployeeFactory:
    """Тесты для фабрики сотрудников"""

    def test_factory_create_employee(self, capsys):
        """Тест создания обычного сотрудника через фабрику"""
        # Act
        EmployeeFactory.create_employee(employee=[501, "Tom", "HR", 3000])
        captured = capsys.readouterr()
        
        # Assert
        assert "Сотрудник id: 501" in captured.out

    def test_factory_create_manager(self, capsys):
        """Тест создания менеджера через фабрику"""
        # Act
        EmployeeFactory.create_employee(manager=[502, "Sarah", "MANAGEMENT", 7000, 2000])
        captured = capsys.readouterr()
        
        # Assert
        assert "бонус: 2000" in captured.out

    def test_factory_create_developer(self, capsys):
        """Тест создания разработчика через фабрику"""
        # Act
        EmployeeFactory.create_employee(developer=[503, "Mike", "DEV", 6000, ["Python", "Java"], "senior"])
        captured = capsys.readouterr()
        
        # Assert
        assert "список технологий:['Python', 'Java']" in captured.out

    def test_factory_create_salesperson(self, capsys):
        """Тест создания продавца через фабрику"""
        # Act
        EmployeeFactory.create_employee(salesperson=[504, "Lisa", "SALES", 5000, 0.1, 40000])
        captured = capsys.readouterr()
        
        # Assert
        assert "процент комиссии: 0.1" in captured.out

class TestPolymorphism:
    """Тесты полиморфного поведения"""


    def test_polymorphic_salary_calculation(self):
        """Тест полиморфного расчета зарплат"""
        # Arrange
        employees = [
            Employee(601, "John", "IT", 5000, skip_validation=True),
            Manager(602, "Sarah", "MANAGEMENT", 7000, 2000, skip_validation=True),
            Developer(603, "Mike", "DEV", 6000, ["Python"], "senior", skip_validation=True),
            Saleperson(604, "Lisa", "SALES", 5000, 0.1, 40000, skip_validation=True)
        ]
        
        # Act
        salaries = [emp.calculate_salary() for emp in employees]
        
        # Assert
        assert salaries[0] == 5000      # Employee
        assert salaries[1] == 9000      # Manager
        assert salaries[2] == 12000     # Developer
        assert salaries[3] == 9000      # Salesperson

    def test_polymorphic_collection(self):
        """Тест работы с коллекцией разных типов сотрудников"""
        # Arrange
        employees = [
            Manager(701, "Alice", "MANAGEMENT", 8000, 1500, skip_validation=True),
            Developer(702, "Bob", "DEV", 5500, ["Java"], "middle", skip_validation=True),
            Saleperson(703, "Charlie", "SALES", 4500, 0.12, 30000, skip_validation=True)
        ]
        
        # Act
        total_salary = sum(emp.calculate_salary() for emp in employees)
        
        # Assert
        manager_salary = 8000 + 1500
        developer_salary = 5500 * 1.5
        sales_salary = 4500 + (0.12 * 30000)
        expected_total = manager_salary + developer_salary + sales_salary
        assert total_salary == expected_total

    def test_polymorphic_to_dict(self):
        """Тест полиморфной сериализации"""
        # Arrange
        employees = [
            Employee(801, "John", "IT", 5000, skip_validation=True),
            Manager(802, "Sarah", "MANAGEMENT", 7000, 2000, skip_validation=True),
            Developer(803, "Mike", "DEV", 6000, ["Python"], "senior", skip_validation=True)
        ]
        
        # Act
        dicts = [emp.to_dict() for emp in employees]
        
        # Assert
        assert dicts[0]['type'] == "Employee"
        assert dicts[1]['type'] == "Manager"
        assert dicts[2]['type'] == "Developer"
        
        # Десериализация
        restored = [AbstractEmployee.from_dict(d) for d in dicts]
        assert isinstance(restored[0], Employee)
        assert isinstance(restored[1], Manager)
        assert isinstance(restored[2], Developer)
if __name__ == "__main__":
    pytest.main([__file__, "-v"])