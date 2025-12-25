import pytest
import json
import os
import tempfile
from Zadanie import (
Employee, Manager, Developer, Saleperson,
Department, Project, Company,
EmployeeNotFoundError, DepartmentNotFoundError,
ProjectNotFoundError, DuplicateIdError,
InvalidDateError, InvalidStatusError, Validator
)

class TestProject:
    """Тесты для класса Project"""

    @pytest.fixture
    def sample_project(self):
        """Фикстура: тестовый проект с командой"""
        project = Project(
            "PRJ-001", 
            "AI Platform", 
            "Разработка AI системы", 
            "2024-12-31", 
            "active",
            []
        )
        project.add_team_member(Employee(1, "Alice", "DEV", 5000, skip_validation=True))
        project.add_team_member(Developer(2, "Bob", "DEV", 6000, ["Python"], "senior", skip_validation=True))
        return project

    def test_project_creation_valid(self):
        """Тест создания проекта с валидными данными"""
        # Arrange & Act
        project = Project("PRJ-002", "Web Portal", "Создание веб-портала", "2024-09-30", "planning", [])
        
        # Assert
        assert project.project_id == "PRJ-002"
        assert project.name == "Web Portal"
        assert project.description == "Создание веб-портала"
        assert project.deadline == "2024-09-30"
        assert project.status == "planning"

    def test_project_invalid_status_raises_error(self):
        """Тест: недопустимый статус вызывает исключение"""
        # Act & Assert
        with pytest.raises(InvalidStatusError):
            Project("PRJ-003", "Test", "Test", "2024-12-31", "invalid_status", [])

    @pytest.mark.parametrize("invalid_date", [
        "2024-13-01",  # Неверный месяц
        "2024-12-32",  # Неверный день
        "2024/12/31",  # Неверный формат
        "2024-12-31T10:30:00"  # Слишком подробно
    ])
    def test_project_invalid_date_raises_error(self, invalid_date):
        """Тест: некорректная дата вызывает исключение"""
        with pytest.raises(InvalidDateError):
            Project("PRJ-004", "Test", "Test", invalid_date, "planning", [])

    def test_project_duplicate_id_error(self):
        """Тест: дублирующийся ID проекта вызывает исключение"""
        # Создаем первый проект
        Project("PRJ-005", "Project A", "Desc A", "2024-12-31", "planning", [])
        
        # Второй проект с тем же ID должен вызвать ошибку
        with pytest.raises(DuplicateIdError):
            Project("PRJ-005", "Project B", "Desc B", "2024-12-31", "planning", [])

    def test_project_add_team_member(self, sample_project):
        """Тест добавления участника в команду проекта"""
        # Arrange
        initial_size = sample_project.get_team_size()
        new_member = Manager(3, "Charlie", "MAN", 7000, 2000, skip_validation=True)
        
        # Act
        sample_project.add_team_member(new_member)
        
        # Assert
        assert sample_project.get_team_size() == initial_size + 1
        assert len(sample_project.get_team()) == initial_size + 1

    def test_project_remove_team_member(self, sample_project):
        """Тест удаления участника из команды проекта"""
        # Arrange
        initial_size = sample_project.get_team_size()
        
        # Act
        sample_project.remove_team_member(1)  # Удаляем Alice
        
        # Assert
        assert sample_project.get_team_size() == initial_size - 1

    def test_project_calculate_total_salary(self, sample_project):
        """Тест расчета общей зарплаты команды проекта"""
        # Act
        total = sample_project.calculate_total_salary()
        
        # Assert
        # Alice (Employee): 5000, Bob (Developer senior): 6000 * 2 = 12000
        expected = 5000 + 12000
        assert total == expected

    def test_project_change_status_valid(self, sample_project):
        """Тест изменения статуса проекта на допустимый"""
        # Act
        sample_project.change_status("completed")
        
        # Assert
        assert sample_project.status == "completed"

    def test_project_change_status_invalid(self, sample_project):
        """Тест: изменение на недопустимый статус вызывает ошибку"""
        # Act & Assert
        with pytest.raises(ValueError, match="Недопустимый статус"):
            sample_project.change_status("invalid")

    def test_project_change_from_completed_error(self):
        """Тест: нельзя изменить статус завершенного проекта"""
        # Arrange
        project = Project("PRJ-006", "Test", "Test", "2024-12-31", "completed", [])
        
        # Act & Assert
        with pytest.raises(ValueError, match="Нельзя изменить статус проекта"):
            project.change_status("active")

    def test_project_has_team_members(self):
        """Тест метода has_team_members"""
        # Arrange
        project_empty = Project("PRJ-007", "Empty", "Desc", "2024-12-31", "planning", [])
        project_with_team = Project("PRJ-008", "WithTeam", "Desc", "2024-12-31", "planning", [])
        project_with_team.add_team_member(Employee(1, "Test", "DEV", 5000, skip_validation=True))
        
        # Assert
        assert not project_empty.has_team_members()
        assert project_with_team.has_team_members()

    def test_project_is_employee_in_project(self, sample_project):
        """Тест проверки участия сотрудника в проекте"""
        # Assert
        assert sample_project.is_employee_in_project(1)  # Alice
        assert sample_project.is_employee_in_project(2)  # Bob
        assert not sample_project.is_employee_in_project(999)  # Несуществующий

class TestCompany:
    """Тесты для класса Company"""

    @pytest.fixture
    def sample_company(self):
        """Фикстура: тестовая компания"""
        company = Company("TechCorp")
        
        # Создаем отделы
        dev_dept = Department("Development")
        sales_dept = Department("Sales")
        
        # Добавляем сотрудников
        dev_dept.add_employee(Manager(1, "Alice", "DEV", 7000, 2000, skip_validation=True))
        dev_dept.add_employee(Developer(2, "Bob", "DEV", 6000, ["Python"], "senior", skip_validation=True))
        sales_dept.add_employee(Saleperson(3, "Charlie", "SALES", 5000, 0.1, 40000, skip_validation=True))
        
        # Добавляем отделы в компанию
        company.add_department(dev_dept)
        company.add_department(sales_dept)
        
        # Создаем проекты
        project1 = Project("PRJ-101", "AI Platform", "AI system", "2024-12-31", "active", [])
        project2 = Project("PRJ-102", "Web Portal", "Web system", "2024-09-30", "planning", [])
        
        # Добавляем проекты в компанию
        company.add_project(project1)
        company.add_project(project2)
        
        return company

    def test_company_creation(self):
        """Тест создания компании"""
        # Arrange & Act
        company = Company("TestCorp")
        
        # Assert
        assert company.name == "TestCorp"
        assert len(company.get_all_employees()) == 0
        assert len(company.get_projects()) == 0

    def test_company_add_department(self):
        """Тест добавления отдела в компанию"""
        # Arrange
        company = Company("TestCorp")
        dept = Department("IT")
        
        # Act
        company.add_department(dept)
        
        # Assert
        assert len(company.get_departments()) > 0

    def test_company_add_department_duplicate_error(self):
        """Тест: добавление отдела с дублирующимся названием вызывает ошибку"""
        # Arrange
        company = Company("TestCorp")
        company.add_department(Department("IT"))
        
        # Act & Assert
        with pytest.raises(DuplicateIdError):
            company.add_department(Department("IT"))

    def test_company_remove_department(self):
        """Тест удаления отдела из компании"""
        # Arrange
        company = Company("TestCorp")
        company.add_department(Department("IT"))
        assert len(company.get_departments()) == 1
        
        # Act
        company.remove_department("IT")
        
        # Assert
        assert len(company.get_departments()) == 0

    def test_company_remove_department_with_employees_error(self, sample_company):
        """Тест: нельзя удалить отдел с сотрудниками"""
        # Act & Assert
        with pytest.raises(ValueError, match="Нельзя удалить отдел"):
            sample_company.remove_department("Development")

    def test_company_add_project(self):
        """Тест добавления проекта в компанию"""
        # Arrange
        company = Company("TestCorp")
        
        # Act
        project = company.add_project("PRJ-001", "Test Project", "Description", "2024-12-31", "planning")
        
        # Assert
        assert project is not None
        assert project.name == "Test Project"
        assert len(company.get_projects()) == 1

    def test_company_remove_project(self, sample_company):
        """Тест удаления проекта из компании"""
        # Arrange
        assert len(sample_company.get_projects()) == 2
        
        # Act
        sample_company.remove_project("PRJ-102")  # Web Portal
        
        # Assert
        assert len(sample_company.get_projects()) == 1
        assert "AI Platform" in sample_company.get_projects()

    def test_company_remove_project_with_team_error(self, sample_company):
        """Тест: нельзя удалить проект с участниками команды"""
        # Добавляем участника в проект
        project = sample_company.add_project("PRJ-103", "Test", "Desc", "2024-12-31", "planning")
        employee = Employee(99, "Test", "DEV", 5000, skip_validation=True)
        dept = Department("TestDept")
        dept.add_employee(employee)
        sample_company.add_department(dept)
        project.add_team_member(employee)
        
        # Попытка удалить проект с командой
        with pytest.raises(ValueError, match="Нельзя удалить проект"):
            sample_company.remove_project("PRJ-103")

    def test_company_find_employee_by_id(self, sample_company):
        """Тест поиска сотрудника по ID в компании"""
        # Act
        employee = sample_company.find_employee_by_id(2)  # Bob
        
        # Assert
        assert employee is not None
        assert employee.name == "Bob"
        assert isinstance(employee, Developer)

    def test_company_find_nonexistent_employee(self, sample_company):
        """Тест поиска несуществующего сотрудника"""
        with pytest.raises(EmployeeNotFoundError):
            sample_company.find_employee_by_id(999)

    def test_company_get_all_employees(self, sample_company):
        """Тест получения всех сотрудников компании"""
        # Act
        all_employees = sample_company.get_all_employees()
        
        # Assert
        assert len(all_employees) == 3
        assert any(emp.name == "Alice" for emp in all_employees)
        assert any(emp.name == "Bob" for emp in all_employees)
        assert any(emp.name == "Charlie" for emp in all_employees)

    def test_company_calculate_total_monthly_cost(self, sample_company):
        """Тест расчета общих месячных затрат"""
        # Act
        total_cost = sample_company.calculate_total_monthly_cost()
        
        # Assert
        # Alice (Manager): 7000 + 2000 = 9000
        # Bob (Developer senior): 6000 * 2 = 12000
        # Charlie (Salesperson): 5000 + (0.1 * 40000) = 9000
        expected = 9000 + 12000 + 9000
        assert total_cost == expected

    def test_company_get_projects_by_status(self, sample_company):
        """Тест фильтрации проектов по статусу"""
        # Act
        active_projects = sample_company.get_projects_by_status("active")
        planning_projects = sample_company.get_projects_by_status("planning")
        
        # Assert
        assert len(active_projects) == 1
        assert len(planning_projects) == 1
        assert active_projects[0].name == "AI Platform"
        assert planning_projects[0].name == "Web Portal"

    def test_company_is_employee_in_projects(self, sample_company):
        """Тест проверки участия сотрудника в проектах"""
        # Добавляем сотрудника в проект
        employee = sample_company.find_employee_by_id(1)  # Alice
        project = sample_company.add_project("PRJ-103", "Test", "Desc", "2024-12-31", "active")
        project.add_team_member(employee)
        
        # Assert
        assert sample_company.is_employee_in_projects(1)  # Alice
        assert not sample_company.is_employee_in_projects(3)  # Charlie (не в проектах)

    def test_company_remove_employee_from_company(self, sample_company):
        """Тест удаления сотрудника из компании"""
        # Act
        result = sample_company.remove_employee_from_company(3)  # Charlie
        
        # Assert
        assert result is True
        with pytest.raises(EmployeeNotFoundError):
            sample_company.find_employee_by_id(3)

    def test_company_remove_employee_in_projects_error(self, sample_company):
        """Тест: нельзя удалить сотрудника, участвующего в проектах"""
        # Добавляем сотрудника в проект
        employee = sample_company.find_employee_by_id(1)  # Alice
        project = sample_company.add_project("PRJ-103", "Test", "Desc", "2024-12-31", "active")
        project.add_team_member(employee)
        
        # Попытка удалить
        with pytest.raises(ValueError, match="Нельзя удалить сотрудника"):
            sample_company.remove_employee_from_company(1)

    def test_company_get_department_stats(self, sample_company):
        """Тест получения статистики по отделам"""
        # Act
        stats = sample_company.get_department_stats()
        
        # Assert
        assert "Development" in stats
        assert "Sales" in stats
        assert "_company_summary" in stats
        
        dev_stats = stats["Development"]
        assert dev_stats["total_employees"] == 2
        assert dev_stats["total_salary"] == 21000  # 9000 + 12000
        
        summary = stats["_company_summary"]
        assert summary["total_departments"] == 2
        assert summary["total_employees"] == 3

    def test_company_get_project_budget_analysis(self, sample_company):
        """Тест анализа бюджетов проектов"""
        # Act
        analysis = sample_company.get_project_budget_analysis()
        
        # Assert
        assert "PRJ-101" in analysis  # AI Platform
        assert "PRJ-102" in analysis  # Web Portal
        
        ai_project = analysis["PRJ-101"]
        assert ai_project["name"] == "AI Platform"
        assert ai_project["status"] == "active"
        assert ai_project["total_salary_cost"] == 0  # Пока нет команды

    def test_company_find_overloaded_employees(self, sample_company):
        """Тест поиска перегруженных сотрудников"""
        # Добавляем сотрудника в несколько проектов
        employee = sample_company.find_employee_by_id(1)  # Alice
        project1 = sample_company.add_project("PRJ-103", "Project 1", "Desc", "2024-12-31", "active")
        project2 = sample_company.add_project("PRJ-104", "Project 2", "Desc", "2024-12-31", "active")
        project3 = sample_company.add_project("PRJ-105", "Project 3", "Desc", "2024-12-31", "active")
        
        project1.add_team_member(employee)
        project2.add_team_member(employee)
        project3.add_team_member(employee)
        
        # Act
        overloaded = sample_company.find_overloaded_employees(max_projects=2)
        
        # Assert
        assert len(overloaded) == 1
        assert overloaded[0]["employee"].name == "Alice"
        assert overloaded[0]["project_count"] == 3

    def test_company_serialization_roundtrip(self, sample_company, tmp_path):
        """Тест полного цикла сериализации/десериализации компании"""
        # Arrange
        filename = tmp_path / "test_company.json"
        
        # Act - сохранение
        sample_company.save_to_json(str(filename))
        
        # Assert - файл создан
        assert os.path.exists(filename)
        
        # Act - загрузка
        loaded_company = Company.load_from_json(str(filename))
        
        # Assert
        assert loaded_company.name == "TechCorp"
        assert len(loaded_company.get_all_employees()) == 3
        assert len(loaded_company.get_projects()) == 2

    def test_company_export_import_csv(self, sample_company, tmp_path):
        """Тест экспорта/импорта CSV"""
        # Arrange
        employees_file = tmp_path / "employees.csv"
        projects_file = tmp_path / "projects.csv"
        
        # Act
        sample_company.export_employees_csv(str(employees_file))
        sample_company.export_projects_csv(str(projects_file))
        
        # Assert
        assert os.path.exists(employees_file)
        assert os.path.exists(projects_file)
        
        # Проверяем что файлы не пустые
        with open(employees_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 4  # Заголовок + 3 сотрудника
        
        with open(projects_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 3  # Заголовок + 2 проекта

    def test_company_generate_financial_report(self, sample_company, tmp_path):
        """Тест генерации финансового отчета"""
        # Arrange
        report_file = tmp_path / "financial_report.txt"
        
        # Act
        sample_company.generate_financial_report(str(report_file))
        
        # Assert
        assert os.path.exists(report_file)
        
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "ФИНАНСОВЫЙ ОТЧЕТ" in content
            assert "TechCorp" in content
            assert "ОБЩАЯ СТАТИСТИКА" in content

    def test_complex_company_integration(self):
        """Комплексный интеграционный тест"""
        # Создаем компанию
        company = Company("TechInnovations")
        
        # Создаем отделы
        dev_department = Department("Development")
        sales_department = Department("Sales")
        
        # Создаем сотрудников разных типов
        manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000, skip_validation=True)
        developer = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior", skip_validation=True)
        salesperson = Saleperson(3, "Charlie Brown", "SAL", 4000, 0.15, 50000, skip_validation=True)
        
        # Добавляем сотрудников в отделы
        dev_department.add_employee(manager)
        dev_department.add_employee(developer)
        sales_department.add_employee(salesperson)
        
        # Добавляем отделы в компанию
        company.add_department(dev_department)
        company.add_department(sales_department)
        
        # Проверяем
        assert company.calculate_total_monthly_cost() > 0
        assert len(company.get_all_employees()) == 3
        
        # Создаем проекты
        project1 = Project("AI-001", "AI Platform", "AI System", "2024-12-31", "active", [])
        project2 = Project("WEB-001", "Web Portal", "Web System", "2024-09-30", "planning", [])
        
        company.add_project(project1)
        company.add_project(project2)
        
        # Назначаем сотрудников на проекты
        project1.add_team_member(developer)
        project2.add_team_member(developer)
        
        # Проверяем перегруженных сотрудников
        overloaded = company.find_overloaded_employees(max_projects=1)
        assert len(overloaded) == 1
        assert overloaded[0]["employee"].name == "Bob Smith"
if __name__ == "__main__":
    pytest.main([__file__, "-v"])