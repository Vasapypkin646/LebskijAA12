
"""
Главный модуль системы учета сотрудников.
"""

import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.employee import Employee, Manager, Developer, Salesperson, EmployeeData
from entities.department import Department
from entities.project import Project
from entities.company import Company
from services.calculator import PerformanceBonusStrategy, BonusContext
from patterns.factory import EmployeeFactory
from patterns.repository import EmployeeRepository
from patterns.adapter import SalaryCalculatorAdapter
from services.serializer import CSVExporter


def demonstrate_system():
    """Демонстрация работы системы после рефакторинга."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ СИСТЕМЫ УЧЕТА СОТРУДНИКОВ (ПОСЛЕ РЕФАКТОРИНГА)")
    print("=" * 60)
    
    # 1. Создание сотрудников
    print("\n1. СОЗДАНИЕ СОТРУДНИКОВ:")
    print("-" * 40)
    
    # Использование фабрики
    emp1 = EmployeeFactory.create_employee(
        'employee',
        id=1,
        name="Иван Иванов",
        department="IT",
        base_salary=50000
    )
    
    manager = EmployeeFactory.create_employee(
        'manager',
        id=2,
        name="Петр Петров",
        department="IT",
        base_salary=70000,
        bonus=15000
    )
    
    developer = EmployeeFactory.create_employee(
        'developer',
        id=3,
        name="Анна Сидорова",
        department="Разработка",
        base_salary=60000,
        tech_stack=["Python", "Django", "PostgreSQL"],
        seniority_level="senior"
    )
    
    salesperson = EmployeeFactory.create_employee(
        'salesperson',
        id=4,
        name="Мария Козлова",
        department="Продажи",
        base_salary=40000,
        commission_rate=0.15,
        sales_volume=500000
    )
    
    print(f"Создано {4} сотрудников разных типов")
    
    # 2. Создание отдела
    print("\n2. УПРАВЛЕНИЕ ОТДЕЛАМИ:")
    print("-" * 40)
    
    it_department = Department("IT")
    it_department.add_employee(emp1)
    it_department.add_employee(manager)
    
    dev_department = Department("Разработка")
    dev_department.add_employee(developer)
    
    sales_department = Department("Продажи")
    sales_department.add_employee(salesperson)
    
    print(f"Создано {3} отдела:")
    print(f"  - {it_department.name}: {len(it_department)} сотрудников")
    print(f"  - {dev_department.name}: {len(dev_department)} сотрудников")
    print(f"  - {sales_department.name}: {len(sales_department)} сотрудников")
    
    # 3. Создание компании
    print("\n3. СОЗДАНИЕ КОМПАНИИ:")
    print("-" * 40)
    
    company = Company("ТехноИнновации")
    company.add_department(it_department)
    company.add_department(dev_department)
    company.add_department(sales_department)
    
    # 4. Создание проектов
    print("\n4. УПРАВЛЕНИЕ ПРОЕКТАМИ:")
    print("-" * 40)
    
    project1 = Project(
        project_id="P001",
        name="Разработка CRM системы",
        description="Создание системы управления клиентами",
        deadline="2024-06-30",
        status="active"
    )
    
    project1.add_team_member(developer)
    project1.add_team_member(manager)
    
    project2 = Project(
        project_id="P002",
        name="Маркетинговая кампания",
        description="Продвижение продуктов компании",
        deadline="2024-05-15",
        status="planning"
    )
    
    project2.add_team_member(salesperson)
    
    company.add_project(project1)
    company.add_project(project2)
    
    print(f"Создано {2} проекта:")
    print(f"  - {project1.name}: {len(project1)} участников")
    print(f"  - {project2.name}: {len(project2)} участников")
    
    # 5. Расчеты и статистика
    print("\n5. ФИНАНСОВЫЕ РАСЧЕТЫ:")
    print("-" * 40)
    
    total_cost = company.calculate_total_monthly_cost()
    print(f"Общие месячные затраты: {total_cost:,.2f} руб.")
    
    print("\nЗарплаты сотрудников:")
    for employee in company.get_all_employees():
        salary = employee.calculate_salary()
        print(f"  - {employee.name}: {salary:,.2f} руб.")
    
    # 6. Использование паттерна Strategy для бонусов
    print("\n6. РАСЧЕТ БОНУСОВ (ПАТТЕРН STRATEGY):")
    print("-" * 40)
    
    bonus_context = BonusContext(PerformanceBonusStrategy())
    for employee in company.get_all_employees():
        bonus = bonus_context.calculate_bonus(employee, performance_score=1.2)
        print(f"  - {employee.name}: бонус {bonus:,.2f} руб.")
    
    # 7. Использование паттерна Adapter
    print("\n7. РАСЧЕТ ЗАРПЛАТ ЧЕРЕЗ ВНЕШНЮЮ СИСТЕМУ (ПАТТЕРН ADAPTER):")
    print("-" * 40)
    
    adapter = SalaryCalculatorAdapter()
    for employee in company.get_all_employees()[:2]:  # Первые два для примера
        internal_salary = employee.calculate_salary()
        external_salary = adapter.calculate_salary(employee)
        difference = external_salary - internal_salary
        print(f"  - {employee.name}:")
        print(f"    Внутренняя: {internal_salary:,.2f} руб.")
        print(f"    Внешняя:    {external_salary:,.2f} руб.")
        print(f"    Разница:    {difference:+,.2f} руб.")
    
    # 8. Использование паттерна Repository
    print("\n8. РАБОТА С БАЗОЙ ДАННЫХ (ПАТТЕРН REPOSITORY):")
    print("-" * 40)
    
    repository = EmployeeRepository()
    
    # Сохранение сотрудников в БД
    saved_count = 0
    for employee in company.get_all_employees():
        if repository.add(employee):
            saved_count += 1
    
    print(f"Сохранено в БД: {saved_count} сотрудников")
    
    # Получение сотрудника из БД
    retrieved = repository.get(3)
    if retrieved:
        print(f"Получен из БД: {retrieved.name}, зарплата: {retrieved.calculate_salary():,.2f} руб.")
    
    # 9. Экспорт данных
    print("\n9. ЭКСПОРТ ДАННЫХ:")
    print("-" * 40)
    
    # Сохранение компании в JSON
    company.save_to_json("company_data.json")
    print(f"Компания сохранена в JSON файл")
    
    # Экспорт сотрудников в CSV
    CSVExporter.export_employees_to_csv(company.get_all_employees(), "employees.csv")
    print(f"Сотрудники экспортированы в CSV файл")
    
    # 10. Статистика
    print("\n10. СТАТИСТИКА КОМПАНИИ:")
    print("-" * 40)
    
    stats = company.get_department_stats()
    for dept_name, dept_stats in stats.items():
        print(f"\n{dept_name}:")
        print(f"  Сотрудников: {dept_stats['total_employees']}")
        print(f"  Общая зарплата: {dept_stats['total_salary']:,.2f} руб.")
        print(f"  Средняя зарплата: {dept_stats['average_salary']:,.2f} руб.")
    
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_system()