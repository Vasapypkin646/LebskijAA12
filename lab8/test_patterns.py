import pytest
from unittest.mock import Mock, patch
from patterns.singleton import DatabaseConnection
from patterns.strategy import PerformanceBonusStrategy, SeniorityBonusStrategy, ProjectBonusStrategy, BonusContext
from patterns.adapter import SalaryCalculatorAdapter, SimpleSalaryCalculator
from patterns.repository import EmployeeRepository
from Zadanie import Employee, Manager, Developer, Saleperson

class TestSingletonPattern:
    """Тесты для паттерна Singleton"""

    def test_singleton_pattern(self):
        """Тест: только один экземпляр DatabaseConnection"""
        # Arrange & Act
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        
        # Assert
        assert db1 is db2
        assert id(db1) == id(db2)

    def test_singleton_connection_management(self):
        """Тест управления подключением к БД"""
        # Arrange
        db = DatabaseConnection()
        
        # Act
        conn1 = db.get_connection()
        conn2 = db.get_connection()
        
        # Assert
        assert conn1 is conn2
        assert hasattr(conn1, 'cursor')
        
        # Cleanup
        db.close_connection()

class TestStrategyPattern:
    """Тесты для паттерна Strategy"""

    @pytest.fixture
    def sample_employees(self):
        """Фикстура: тестовые сотрудники"""
        return [
            Employee(1, "John", "IT", 5000, skip_validation=True),
            Manager(2, "Sarah", "MANAGEMENT", 7000, 2000, skip_validation=True),
            Developer(3, "Mike", "DEV", 6000, ["Python"], "senior", skip_validation=True)
        ]

    def test_performance_bonus_strategy(self, sample_employees):
        """Тест стратегии бонуса на основе производительности"""
        # Arrange
        strategy = PerformanceBonusStrategy()
        employee = sample_employees[1]  # Manager
        
        # Act
        bonus = strategy.calculate_bonus(employee, performance_score=1.5)
        
        # Assert
        expected_bonus = 2000 * 1.5  # base_bonus * performance_score
        assert bonus == expected_bonus

    def test_seniority_bonus_strategy(self, sample_employees):
        """Тест стратегии бонуса на основе стажа"""
        # Arrange
        strategy = SeniorityBonusStrategy()
        employee = sample_employees[2]  # Developer senior
        
        # Act
        bonus = strategy.calculate_bonus(employee, seniority_years=5)
        
        # Assert
        # base_salary * 0.05 * seniority_years * level_multiplier
        # 6000 * 0.05 * 5 * 2.0 = 3000
        assert bonus == 3000.0

    def test_project_bonus_strategy(self):
        """Тест стратегии бонуса на основе проектов"""
        # Arrange
        strategy = ProjectBonusStrategy()
        employee = Employee(4, "Test", "IT", 5000, skip_validation=True)
        
        # Act
        bonus = strategy.calculate_bonus(employee, successful_projects=3, project_importance=1.5)
        
        # Assert
        # base_bonus * successful_projects * project_importance
        # 1000 * 3 * 1.5 = 4500
        assert bonus == 4500.0

    def test_bonus_context_dynamic_strategy(self):
        """Тест динамической смены стратегии в контексте"""
        # Arrange
        context = BonusContext(PerformanceBonusStrategy())
        employee = Manager(5, "Test", "IT", 8000, 1500, skip_validation=True)
        
        # Act - Performance strategy
        bonus1 = context.calculate_bonus(employee, performance_score=1.2)
        
        # Change strategy
        context.strategy = SeniorityBonusStrategy()
        bonus2 = context.calculate_bonus(employee, seniority_years=4)
        
        # Assert
        assert bonus1 == 1800.0  # 1500 * 1.2
        assert bonus2 == 1600.0  # 8000 * 0.05 * 4 * 1.0

class TestAdapterPattern:
    """Тесты для паттерна Adapter"""

    @pytest.fixture
    def sample_employee(self):
        """Фикстура: тестовый сотрудник"""
        return Manager(6, "Alice", "IT", 7000, 2000, skip_validation=True)

    def test_adapter_calculate_salary(self, sample_employee):
        """Тест расчета зарплаты через адаптер"""
        # Arrange
        adapter = SalaryCalculatorAdapter()
        
        # Act
        external_salary = adapter.calculate_salary(sample_employee)
        
        # Assert
        # Внешняя система применяет множитель 1.2 для Manager
        internal_salary = sample_employee.calculate_salary()  # 9000
        expected = internal_salary * 1.2  # 10800
        assert external_salary == expected

    def test_adapter_detailed_calculation(self, sample_employee):
        """Тест детального расчета через адаптер"""
        # Arrange
        adapter = SalaryCalculatorAdapter()
        
        # Act
        details = adapter.get_detailed_calculation(sample_employee)
        
        # Assert
        assert 'base_amount' in details
        assert 'adjusted_amount' in details
        assert 'multiplier' in details
        assert 'total_amount' in details
        assert 'currency' in details
        assert 'calculation_method' in details
        assert details['calculation_method'] == 'external_system'

    def test_adapter_with_custom_calculator(self):
        """Тест адаптера с пользовательским калькулятором"""
        # Arrange
        mock_calculator = Mock()
        mock_calculator.compute_payment.return_value = {
            'total_amount': 15000.0,
            'currency': 'RUB'
        }
        adapter = SalaryCalculatorAdapter(mock_calculator)
        employee = Employee(7, "Test", "IT", 5000, skip_validation=True)
        
        # Act
        result = adapter.calculate_salary(employee)
        
        # Assert
        assert result == 15000.0
        mock_calculator.compute_payment.assert_called_once()

class TestRepositoryPattern:
    """Тесты для паттерна Repository"""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Настройка и очистка перед/после каждого теста"""
        # Cleanup before test
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees")
        conn.commit()
        
        yield
        
        # Cleanup after test
        cursor.execute("DELETE FROM employees")
        conn.commit()
        db.close_connection()

    def test_repository_add_employee(self):
        """Тест добавления сотрудника в репозиторий"""
        # Arrange
        repo = EmployeeRepository()
        employee = Employee(100, "John", "IT", 5000, skip_validation=True)
        
        # Act
        success = repo.add(employee)
        
        # Assert
        assert success is True
        
        # Verify in DB
        saved = repo.get(100)
        assert saved is not None
        assert saved.name == "John"
        assert saved.department == "IT"

    def test_repository_add_developer(self):
        """Тест добавления разработчика в репозиторий"""
        # Arrange
        repo = EmployeeRepository()
        developer = Developer(101, "Mike", "DEV", 6000, ["Python", "Java"], "senior", skip_validation=True)
        
        # Act
        success = repo.add(developer)
        
        # Assert
        assert success is True
        
        saved = repo.get(101)
        assert isinstance(saved, Developer)
        assert saved._Developer__seniority_level == "senior"
        assert "Python" in saved._Developer__tech_stack

    def test_repository_get_all(self):
        """Тест получения всех сотрудников"""
        # Arrange
        repo = EmployeeRepository()
        employees = [
            Employee(200, "Alice", "HR", 4000, skip_validation=True),
            Manager(201, "Bob", "MANAGEMENT", 7000, 2000, skip_validation=True),
            Developer(202, "Charlie", "DEV", 6000, ["Python"], "middle", skip_validation=True)
        ]
        
        for emp in employees:
            repo.add(emp)
        
        # Act
        all_employees = repo.get_all()
        
        # Assert
        assert len(all_employees) == 3
        assert any(emp.name == "Alice" for emp in all_employees)
        assert any(emp.name == "Bob" for emp in all_employees)
        assert any(emp.name == "Charlie" for emp in all_employees)

    def test_repository_update_employee(self):
        """Тест обновления сотрудника"""
        # Arrange
        repo = EmployeeRepository()
        employee = Employee(300, "John", "IT", 5000, skip_validation=True)
        repo.add(employee)
        
        # Update employee
        employee.name = "John Updated"
        employee.base_salary = 5500
        
        # Act
        success = repo.update(employee)
        
        # Assert
        assert success is True
        
        updated = repo.get(300)
        assert updated.name == "John Updated"
        assert updated.base_salary == 5500

    def test_repository_delete_employee(self):
        """Тест удаления сотрудника"""
        # Arrange
        repo = EmployeeRepository()
        employee = Employee(400, "Test", "IT", 5000, skip_validation=True)
        repo.add(employee)
        assert repo.get(400) is not None
        
        # Act
        success = repo.delete(400)
        
        # Assert
        assert success is True
        assert repo.get(400) is None

    def test_repository_find_by_department(self):
        """Тест поиска сотрудников по отделу"""
        # Arrange
        repo = EmployeeRepository()
        employees = [
            Employee(500, "Alice", "IT", 5000, skip_validation=True),
            Employee(501, "Bob", "HR", 4000, skip_validation=True),
            Employee(502, "Charlie", "IT", 6000, skip_validation=True)
        ]
        
        for emp in employees:
            repo.add(emp)
        
        # Act
        it_employees = repo.find_by_department("IT")
        
        # Assert
        assert len(it_employees) == 2
        assert all(emp.department == "IT" for emp in it_employees)

    def test_repository_find_by_type(self):
        """Тест поиска сотрудников по типу"""
        # Arrange
        repo = EmployeeRepository()
        employees = [
            Employee(600, "Alice", "IT", 5000, skip_validation=True),
            Manager(601, "Bob", "MANAGEMENT", 7000, 2000, skip_validation=True),
            Developer(602, "Charlie", "DEV", 6000, ["Python"], "senior", skip_validation=True)
        ]
        
        for emp in employees:
            repo.add(emp)
        
        # Act
        managers = repo.find_by_type("Manager")
        
        # Assert
        assert len(managers) == 1
        assert managers[0].name == "Bob"
        assert isinstance(managers[0], Manager)

    def test_repository_get_total_salary_expenses(self):
        """Тест расчета общих затрат на зарплаты"""
        # Arrange
        repo = EmployeeRepository()
        employees = [
            Employee(700, "Alice", "IT", 5000, skip_validation=True),
            Manager(701, "Bob", "MANAGEMENT", 7000, 2000, skip_validation=True),
            Developer(702, "Charlie", "DEV", 6000, ["Python"], "senior", skip_validation=True)
        ]
        
        for emp in employees:
            repo.add(emp)
        
        # Act
        total_expenses = repo.get_total_salary_expenses()
        
        # Assert
        expected = 5000 + 9000 + 12000  # 5000 + (7000+2000) + (6000*2)
        assert total_expenses == expected
        
class TestPatternsIntegration:
    """Интеграционные тесты паттернов"""

    def test_complex_pattern_interaction(self):
        """Тест взаимодействия нескольких паттернов"""
        # 1. Singleton для БД
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2
        
        # 2. Repository для сотрудников
        repo = EmployeeRepository()
        
        # 3. Создаем сотрудников разных типов
        developer = Developer(800, "John Doe", "DEV", 5000, ["Python", "Java"], "senior", skip_validation=True)
        manager = Manager(801, "Alice Smith", "MANAGEMENT", 7000, 2000, skip_validation=True)
        
        # 4. Сохраняем через Repository
        assert repo.add(developer) is True
        assert repo.add(manager) is True
        
        # 5. Используем Strategy для расчета бонусов
        context = BonusContext(PerformanceBonusStrategy())
        manager_bonus = context.calculate_bonus(manager, performance_score=1.3)
        
        # 6. Используем Adapter для расчета внешних зарплат
        adapter = SalaryCalculatorAdapter()
        developer_external_salary = adapter.calculate_salary(developer)
        
        # Проверяем результаты
        assert manager_bonus == 2600.0  # 2000 * 1.3
        assert developer_external_salary > 0
        
        # 7. Проверяем через Repository
        all_employees = repo.get_all()
        assert len(all_employees) == 2
        
        # Cleanup
        repo.delete(800)
        repo.delete(801)

    def test_patterns_with_mocks(self):
        """Тест с использованием mock объектов"""
        # Arrange
        mock_strategy = Mock()
        mock_strategy.calculate_bonus.return_value = 1000.0
        
        mock_adapter = Mock()
        mock_adapter.calculate_salary.return_value = 15000.0
        
        mock_repo = Mock()
        mock_repo.add.return_value = True
        mock_repo.get_all.return_value = []
        
        context = BonusContext(mock_strategy)
        employee = Employee(900, "Test", "IT", 5000, skip_validation=True)
        
        # Act
        bonus = context.calculate_bonus(employee)
        salary = mock_adapter.calculate_salary(employee)
        repo_success = mock_repo.add(employee)
        
        # Assert
        assert bonus == 1000.0
        assert salary == 15000.0
        assert repo_success is True
        
        mock_strategy.calculate_bonus.assert_called_once_with(employee)
        mock_adapter.calculate_salary.assert_called_once_with(employee)
        mock_repo.add.assert_called_once_with(employee)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])