import pytest
from not_bad_code import (
    MAX_VALUE,
    add_numbers,
    calculate_value,
    double_even_numbers,
    fetch_user
)

def test_add_numbers():
    """Тест функции сложения"""
    assert add_numbers(5, 7) == 12
    assert add_numbers(-3, 4) == 1
    assert add_numbers(0, 0) == 0
    assert add_numbers(99, 1) == 100

def test_calculate_value():
    """Тест сложной операции: (a*b + c)/2"""
    # (2*4 + 6)/2 = (8+6)/2 = 14/2 = 7
    assert calculate_value(2, 4, 6) == 7
    # (0*0 + 0)/2 = 0
    assert calculate_value(0, 0, 0) == 0
    # (10*10 + 5)/2 = (100+5)/2 = 105/2 = 52.5
    assert calculate_value(10, 10, 5) == 52.5
    # (0.5*2 + 1)/2 = (1+1)/2 = 2/2 = 1
    assert calculate_value(0.5, 2, 1) == 1.0
    # (-1*-1 + 1)/2 = (1+1)/2 = 2/2 = 1
    assert calculate_value(-1, -1, 1) == 1.0

def test_double_even_numbers():
    """Тест: четные удваиваются, нечетные умножаются на 3"""
    # [1*3=3, 2*2=4, 3*3=9, 4*2=8]
    assert double_even_numbers([1, 2, 3, 4]) == [3, 4, 9, 8]
    # Пустой список
    assert double_even_numbers([]) == []
    # Один элемент
    assert double_even_numbers([1]) == [3]
    assert double_even_numbers([2]) == [4]
    # Отрицательные числа
    assert double_even_numbers([-2, -3]) == [-4, -9]

def test_fetch_user():
    """Тест получения пользователя"""
    assert fetch_user(1) == 'Alice'
    assert fetch_user(2) == 'Bob'
    assert fetch_user(3) is None
    assert fetch_user(999) is None

# Дополнительные тесты для граничных случаев
def test_add_numbers_max():
    """Тест с максимальным значением"""
    result = add_numbers(MAX_VALUE, 0)
    assert result == MAX_VALUE

def test_calculate_value_with_floats():
    """Тест с числами с плавающей точкой"""
    result = calculate_value(1.5, 2.5, 3.5)
    # (1.5*2.5 + 3.5)/2 = (3.75 + 3.5)/2 = 7.25/2 = 3.625
    assert result == 3.625

def test_double_even_numbers_mixed():
    """Тест со смешанными числами"""
    result = double_even_numbers([1, 2, 3, 4, 5, 6])
    expected = [3, 4, 9, 8, 15, 12]  # 1→3, 2→4, 3→9, 4→8, 5→15, 6→12
    assert result == expected