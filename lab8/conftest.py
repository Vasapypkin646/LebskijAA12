import pytest
from Zadanie import Employee, Manager, Developer, Saleperson, Department, Project, Company

@pytest.fixture
def sample_employee():
    """Фикстура: тестовый сотрудник"""
    return Employee(9999, "Test Employee", "TEST", 5000, skip_validation=True)

@pytest.fixture
def sample_manager():
    """Фикстура: тестовый менеджер"""
    return Manager(9998, "Test Manager", "MANAGEMENT", 7000, 2000, skip_validation=True)

@pytest.fixture
def sample_developer():
    """Фикстура: тестовый разработчик"""
    return Developer(9997, "Test Developer", "DEV", 6000, ["Python", "Java"], "senior", skip_validation=True)

@pytest.fixture
def sample_salesperson():
    """Фикстура: тестовый продавец"""
    return Saleperson(9996, "Test Salesperson", "SALES", 5000, 0.1, 40000, skip_validation=True)

@pytest.fixture
def sample_department():
    """Фикстура: тестовый отдел с сотрудниками"""
    dept = Department("Test Department")
    dept.add_employee(Employee(1001, "Alice", "TEST", 5000, skip_validation=True))
    dept.add_employee(Manager(1002, "Bob", "TEST", 7000, 2000, skip_validation=True))
    return dept

@pytest.fixture
def sample_project():
    """Фикстура: тестовый проект"""
    project = Project("TEST-001", "Test Project", "Test Description", "2024-12-31", "planning", [])
    project.add_team_member(Employee(2001, "Project Member", "DEV", 5000, skip_validation=True))
    return project

@pytest.fixture
def sample_company():
    """Фикстура: тестовая компания"""
    company = Company("Test Corp")
    # Создаем и добавляем отдел
    dept = Department("Development")
    dept.add_employee(Developer(3001, "Dev 1", "DEV", 5000, ["Python"], "middle", skip_validation=True))
    company.add_department(dept)

    # Создаем и добавляем проект
    project = Project("PRJ-001", "Test Project", "Test", "2024-12-31", "planning", [])
    company.add_project(project)

    return company

@pytest.fixture
def cleanup_ids():
    """
    Фикстура для очистки ID перед тестами
    (предотвращает конфликты из-за статических коллекций)
    """
    # Сохраняем оригинальные коллекции
    from Zadanie import AbstractEmployee, Project
    original_employee_ids = AbstractEmployee._existing_ids.copy()
    original_project_ids = Project._existing_project_ids.copy()

    yield
    # Восстанавливаем оригинальные коллекции
    AbstractEmployee._existing_ids = original_employee_ids
    Project._existing_project_ids = original_project_ids


@pytest.fixture(autouse=True)
def reset_static_collections(cleanup_ids):
    """
    Автоматически очищает статические коллекции перед каждым тестом
    """
    from Zadanie import AbstractEmployee, Project
    AbstractEmployee._existing_ids.clear()
    Project._existing_project_ids.clear()