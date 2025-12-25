from patterns.singleton import DatabaseConnection
from patterns.strategy import PerformanceBonusStrategy, SeniorityBonusStrategy, BonusContext
from patterns.adapter import SalaryCalculatorAdapter
from patterns.repository import EmployeeRepository

# Импортируем классы из вашего Zadanie.py
import sys
sys.path.append('.')

# Импортируем нужные классы
try:
    from Zadanie import Manager, Developer, Employee, Saleperson
    from Zadanie import AbstractEmployee
except ImportError:
    # Если не можем импортировать напрямую, создадим фиктивные классы для демонстрации
    class AbstractEmployee:
        pass
    
    class Manager:
        def __init__(self, id, name, department, base_salary, bonus):
            self.id = id
            self.name = name
            self.department = department
            self.base_salary = base_salary
            self.bonus = bonus
        
        def calculate_salary(self):
            return self.base_salary + self.bonus
        
        def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'department': self.department,
                'base_salary': self.base_salary,
                'bonus': self.bonus,
                'type': 'Manager'
            }
    
    class Developer:
        def __init__(self, id, name, department, base_salary, tech_stack, seniority_level):
            self.id = id
            self.name = name
            self.department = department
            self.base_salary = base_salary
            self._Developer__tech_stack = tech_stack
            self._Developer__seniority_level = seniority_level
        
        def calculate_salary(self):
            if self._Developer__seniority_level == "junior":
                return self.base_salary
            if self._Developer__seniority_level == "middle":
                return self.base_salary * 1.5
            if self._Developer__seniority_level == "senior":
                return self.base_salary * 2
            return self.base_salary
        
        def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'department': self.department,
                'base_salary': self.base_salary,
                'tech_stack': self._Developer__tech_stack,
                'seniority_level': self._Developer__seniority_level,
                'type': 'Developer'
            }

def demonstrate_patterns():
    print("=== ДЕМОНСТРАЦИЯ ПАТТЕРНОВ ПРОЕКТИРОВАНИЯ ===\n")
    
    # 1. Демонстрация Singleton
    print("1. ПАТТЕРН SINGLETON:")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"Проверка Singleton: db1 is db2 = {db1 is db2}")
    print(f"ID объекта db1: {id(db1)}")
    print(f"ID объекта db2: {id(db2)}")
    
    # Тестируем подключение
    conn = db1.get_connection()
    print(f"Соединение с БД установлено: {conn is not None}")
    
    # 2. Демонстрация Strategy
    print("\n2. ПАТТЕРН STRATEGY:")
    
    # Создаем менеджера
    manager = Manager(100, "Иван Петров", "Управление", 50000, 10000)
    print(f"Менеджер создан: {manager.name}")
    print(f"Базовая зарплата: {manager.base_salary}")
    print(f"Бонус: {manager.bonus}")
    print(f"Общая зарплата: {manager.calculate_salary():.2f}")
    
    # Используем стратегию производительности
    bonus_context = BonusContext(PerformanceBonusStrategy())
    performance_bonus = bonus_context.calculate_bonus(manager, performance_score=1.3)
    print(f"\nБонус менеджера (стратегия производительности, коэффициент 1.3): {performance_bonus:.2f}")
    
    # Меняем стратегию на стажевую
    bonus_context.strategy = SeniorityBonusStrategy()
    seniority_bonus = bonus_context.calculate_bonus(manager, seniority_years=5)
    print(f"Бонус менеджера (стратегия стажа, 5 лет): {seniority_bonus:.2f}")
    
    # 3. Демонстрация Adapter
    print("\n3. ПАТТЕРН ADAPTER:")
    
    # Создаем адаптер
    salary_adapter = SalaryCalculatorAdapter()
    
    # Расчет зарплаты через адаптер
    external_salary = salary_adapter.calculate_salary(manager)
    print(f"Зарплата менеджера через внешнюю систему: {external_salary:.2f}")
    
    # Детальный расчет
    detailed_calc = salary_adapter.get_detailed_calculation(manager)
    print(f"\nДетали расчета:")
    print(f"  Базовая сумма: {detailed_calc['base_amount']:.2f}")
    print(f"  Скорректированная сумма: {detailed_calc['adjusted_amount']:.2f}")
    print(f"  Множитель: {detailed_calc['multiplier']}")
    print(f"  Итоговая сумма: {detailed_calc['total_amount']:.2f}")
    print(f"  Метод расчета: {detailed_calc['calculation_method']}")
    
    # 4. Демонстрация Repository
    print("\n4. ПАТТЕРН REPOSITORY:")
    
    # Создаем репозиторий
    employee_repo = EmployeeRepository()
    
    # Сохраняем менеджера в БД
    print(f"Сохранение менеджера в БД...")
    success = employee_repo.add(manager)
    print(f"Результат сохранения: {'Успешно' if success else 'Ошибка'}")
    
    # Получаем менеджера из БД
    print(f"Получение менеджера из БД...")
    retrieved = employee_repo.get(100)
    if retrieved:
        print(f"Сотрудник из БД: {retrieved.name}")
        print(f"Тип: {retrieved.__class__.__name__}")
        print(f"Отдел: {retrieved.department}")
        print(f"Зарплата: {retrieved.calculate_salary():.2f}")
    else:
        print("Сотрудник не найден в БД")
    
    # Создаем и сохраняем разработчика
    developer = Developer(101, "Анна Сидорова", "Разработка", 40000, 
                         ["Python", "Django", "PostgreSQL"], "senior")
    employee_repo.add(developer)
    
    # Поиск по отделу
    print(f"\nПоиск сотрудников по отделу 'Разработка':")
    dept_employees = employee_repo.find_by_department("Разработка")
    print(f"Найдено сотрудников: {len(dept_employees)}")
    for emp in dept_employees:
        print(f"  - {emp.name} ({emp.__class__.__name__}): {emp.calculate_salary():.2f}")
    
    # Поиск по типу
    print(f"\nПоиск всех разработчиков:")
    developers = employee_repo.find_by_type("Developer")
    print(f"Найдено разработчиков: {len(developers)}")
    
    # Общие затраты на зарплаты
    total_expenses = employee_repo.get_total_salary_expenses()
    print(f"\nОбщие затраты на зарплаты: {total_expenses:.2f}")
    
    # Получаем всех сотрудников
    all_employees = employee_repo.get_all()
    print(f"\nВсего сотрудников в БД: {len(all_employees)}")
    for i, emp in enumerate(all_employees, 1):
        salary = emp.calculate_salary()
        print(f"{i}. {emp.name} - {emp.__class__.__name__} - {emp.department} - {salary:.2f}")
    
    # 5. Удаление тестовых данных
    print(f"\n5. ОЧИСТКА ТЕСТОВЫХ ДАННЫХ:")
    employee_repo.delete(100)
    employee_repo.delete(101)
    print("Тестовые данные удалены")
    
    print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")

if __name__ == "__main__":
    demonstrate_patterns()