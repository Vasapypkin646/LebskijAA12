
#Напиши функцию validate_email(email: str) -> bool, которая проверяет корректность email-адреса...
def validate_email(email: str) -> bool:
    """
    Проверяет валидность email адреса

    :param email: строка, представляющая email адрес для проверки
    :return: True, если email валиден, иначе False
    """
    import re

    # Регулярное выражение для проверки формата email по стандарту RFC-5322
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    try:
        if not isinstance(email, str):
            raise ValueError("Переданный параметр должен быть строковым типом")

        return bool(re.fullmatch(pattern, email))
    
    except Exception as e:
        print(f"Произошла ошибка при проверке email: {str(e)}")
        return False

#Напиши функцию sort_by_key(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]...
from typing import List, Dict

def sort_by_key(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
    """
    Сортирует список словарей по указанному ключу.
    
    :param data: Список словарей для сортировки
    :type data: List[Dict]
    :param key: Ключевое поле для сортировки
    :type key: str
    :param reverse: Флаг для обратной сортировки (по умолчанию False)
    :type reverse: bool
    :return: Отсортированный список словарей
    :rtype: List[Dict]
    
    :raises KeyError: Если указанный ключ отсутствует хотя бы в одном словаре
    :raises TypeError: Если аргумент 'data' не является списком или элементы списка не являются словарями
    """
    # Проверка корректности входных данных
    if not isinstance(data, list):
        raise TypeError("Аргумент 'data' должен быть списком")
    for item in data:
        if not isinstance(item, dict):
            raise TypeError("Элементы списка 'data' должны быть словарями")
    
    try:
        # Сортируем по заданному ключу
        sorted_data = sorted(data, key=lambda x: x.get(key), reverse=reverse)
    except KeyError as e:
        # Обработка ошибки отсутствия ключа
        raise KeyError(f"Ключ '{key}' отсутствует в словаре") from e
    
    return sorted_data


#Напиши декоратор timer(func) для измерения времени выполнения функции...
from typing import Callable
import time

def timer(func: Callable) -> Callable:
    """
    Декоратор для измерения времени выполнения функции.
    
    Параметры:
    func (Callable): функция, время выполнения которой нужно измерить
    
    Возвращаемое значение:
    Callable: обернутая функция с замером времени исполнения
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка выполнения функции {func.__name__}: {str(e)}")
            raise
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения функции '{func.__name__}': {execution_time:.4f} секунд")
        return result
    return wrapper
