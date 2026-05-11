from typing import List, Optional

# Константа вместо глобальной переменной
MAX_VALUE = 100

def add_numbers(num1: int, num2: int) -> int:
    """
    Суммирует два числа
    :param num1: Первое число
    :param num2: Второе число
    :return: Сумма двух чисел
    """
    return num1 + num2

def calculate_value(a: float, b: float, c: float) -> float:
    """
    Выполняет сложную операцию над числами
    :param a: Множимое 1
    :param b: Множимое 2
    :param c: Число для сложения
    :return: Результат вычислений
    """
    result_1 = a * b
    result_2 = result_1 + c
    result_3 = result_2 / 2
    return result_3

def double_even_numbers(lst: List[int]) -> List[int]:
    """
    Двойное увеличение четных элементов списка
    :param lst: Список целых чисел
    :return: Список удвоенных четных значений
    """
    result = []
    for item in lst:
        if item % 2 == 0:
            result.append(item * 2)
        else:
            result.append(item * 3)
    return result

def fetch_user(user_id: int) -> Optional[str]:
    """
    Заглушка получения пользователя по идентификатору
    :param user_id: Идентификатор пользователя
    :return: Имя пользователя или None
    """
    if user_id == 1:
        return 'Alice'
    elif user_id == 2:
        return 'Bob'
    else:
        return None
    
    # Обработка ошибки (например, некорректный ID)
    raise ValueError(f'Invalid user ID {user_id}')
