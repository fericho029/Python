"""
Модуль с функциями для лабораторной работы №5-2
"""

from collections import Counter
from typing import List, Dict, Any, Union

# Задача 1: Подсчет слов в предложении
def count_words(sentence: str) -> int:
    """
    Подсчитывает количество слов в предложении.
    
    Args:
        sentence: Строка с предложением
        
    Returns:
        int: Количество слов
        
    Examples:
        >>> count_words("Hello world")
        2
        >>> count_words("")
        0
    """
    if not isinstance(sentence, str):
        raise TypeError("Аргумент должен быть строкой")
    
    if not sentence.strip():
        return 0
    
    return len(sentence.split())

# Задача 2: Поиск уникальных элементов
def find_unique(elements: List[Any]) -> List[Any]:
    """
    Возвращает список элементов, которые встречаются только один раз.
    
    Args:
        elements: Список элементов
        
    Returns:
        List[Any]: Список уникальных элементов
        
    Examples:
        >>> find_unique([1, 2, 2, 3, 4, 4, 5])
        [1, 3, 5]
        >>> find_unique(["a", "b", "a", "c"])
        ["b", "c"]
    """
    if not isinstance(elements, list):
        raise TypeError("Аргумент должен быть списком")
    
    counts = Counter(elements)
    return [item for item in elements if counts[item] == 1]

# Задача 3: Палиндром
def is_palindrome(value: Union[str, int]) -> bool:
    """
    Проверяет, является ли строка или число палиндромом.
    
    Args:
        value: Строка или число для проверки
        
    Returns:
        bool: True если палиндром, иначе False
        
    Examples:
        >>> is_palindrome("radar")
        True
        >>> is_palindrome(12321)
        True
        >>> is_palindrome("hello")
        False
    """
    # Преобразуем в строку
    str_value = str(value)
    
    # Очищаем от пробелов и приводим к нижнему регистру (для строк с пробелами)
    if isinstance(value, str):
        str_value = str_value.replace(" ", "").lower()
    
    return str_value == str_value[::-1]

# Задача 4: Анаграммы
def are_anagrams(str1: str, str2: str) -> bool:
    """
    Проверяет, являются ли две строки анаграммами.
    
    Args:
        str1: Первая строка
        str2: Вторая строка
        
    Returns:
        bool: True если анаграммы, иначе False
        
    Examples:
        >>> are_anagrams("listen", "silent")
        True
        >>> are_anagrams("hello", "world")
        False
    """
    if not isinstance(str1, str) or not isinstance(str2, str):
        raise TypeError("Оба аргумента должны быть строками")
    
    # Убираем пробелы и приводим к нижнему регистру
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()
    
    # Если разная длина - не анаграммы
    if len(str1) != len(str2):
        return False
    
    return Counter(str1) == Counter(str2)

# Задача 5: Слияние словарей
def combine_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Объединяет два словаря в новый словарь.
    При совпадении ключей приоритет имеет значение из dict2.
    
    Args:
        dict1: Первый словарь
        dict2: Второй словарь
        
    Returns:
        Dict: Новый объединенный словарь
        
    Examples:
        >>> combine_dicts({"a": 1, "b": 2}, {"c": 3, "d": 4})
        {"a": 1, "b": 2, "c": 3, "d": 4}
        >>> combine_dicts({"a": 1}, {"a": 100, "b": 2})
        {"a": 100, "b": 2}
    """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        raise TypeError("Оба аргумента должны быть словарями")
    
    # Создаем новый словарь, объединяя dict1 и dict2
    # При совпадении ключей значение из dict2 перезаписывает dict1
    result = dict1.copy()
    result.update(dict2)
    return result