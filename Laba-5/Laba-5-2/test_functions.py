"""
Тесты для функций из модуля functions.py
"""

import pytest
from functions import (
    count_words, find_unique, is_palindrome, 
    are_anagrams, combine_dicts
)

# ========== Тесты для count_words ==========

class TestCountWords:
    """Тесты для функции подсчета слов"""
    
    def test_normal_sentence(self):
        """Обычное предложение"""
        assert count_words("Hello world") == 2
        assert count_words("This is a test sentence") == 5
    
    def test_empty_string(self):
        """Пустая строка"""
        assert count_words("") == 0
    
    def test_string_with_spaces(self):
        """Строка с пробелами"""
        assert count_words("   ") == 0
        assert count_words("  hello  world  ") == 2
    
    def test_single_word(self):
        """Одно слово"""
        assert count_words("Python") == 1
    
    def test_special_characters(self):
        """Специальные символы считаются частью слов"""
        assert count_words("Hello, world!") == 2
        assert count_words("one-two three") == 2
    
    def test_invalid_input(self):
        """Неверный тип входных данных"""
        with pytest.raises(TypeError):
            count_words(123)
        with pytest.raises(TypeError):
            count_words(None)

# ========== Тесты для find_unique ==========

class TestFindUnique:
    """Тесты для поиска уникальных элементов"""
    
    def test_numbers(self):
        """Список чисел"""
        assert find_unique([1, 2, 2, 3, 4, 4, 5]) == [1, 3, 5]
        assert find_unique([1, 1, 1, 1]) == []
    
    def test_strings(self):
        """Список строк"""
        assert find_unique(["a", "b", "a", "c"]) == ["b", "c"]
        assert find_unique(["x", "x", "y", "z", "z"]) == ["y"]
    
    def test_mixed_types(self):
        """Смешанные типы данных"""
        assert find_unique([1, "1", 1, "2", 2]) == ["1", "2", 2]
    
    def test_empty_list(self):
        """Пустой список"""
        assert find_unique([]) == []
    
    def test_all_unique(self):
        """Все элементы уникальны"""
        assert find_unique([1, 2, 3, 4]) == [1, 2, 3, 4]
    
    def test_invalid_input(self):
        """Неверный тип входных данных"""
        with pytest.raises(TypeError):
            find_unique("not a list")
        with pytest.raises(TypeError):
            find_unique(123)

# ========== Тесты для is_palindrome ==========

class TestIsPalindrome:
    """Тесты для проверки палиндромов"""
    
    def test_word_palindromes(self):
        """Слова-палиндромы"""
        assert is_palindrome("radar") == True
        assert is_palindrome("level") == True
        assert is_palindrome("madam") == True
    
    def test_non_palindromes(self):
        """Не палиндромы"""
        assert is_palindrome("hello") == False
        assert is_palindrome("world") == False
    
    def test_number_palindromes(self):
        """Числа-палиндромы"""
        assert is_palindrome(12321) == True
        assert is_palindrome(1221) == True
        assert is_palindrome(12345) == False
    
    def test_mixed_case(self):
        """Разный регистр (должен игнорироваться)"""
        assert is_palindrome("Radar") == True
        assert is_palindrome("Level") == True
    
    def test_with_spaces(self):
        """С пробелами"""
        assert is_palindrome("a man a plan a canal panama") == True
        assert is_palindrome("never odd or even") == True
    
    def test_empty_string(self):
        """Пустая строка"""
        assert is_palindrome("") == True
    
    def test_single_character(self):
        """Один символ"""
        assert is_palindrome("a") == True
        assert is_palindrome(1) == True

# ========== Тесты для are_anagrams ==========

class TestAreAnagrams:
    """Тесты для проверки анаграмм"""
    
    def test_simple_anagrams(self):
        """Простые анаграммы"""
        assert are_anagrams("listen", "silent") == True
        assert are_anagrams("hello", "olleh") == True
    
    def test_not_anagrams(self):
        """Не анаграммы"""
        assert are_anagrams("hello", "world") == False
        assert are_anagrams("cat", "dog") == False
    
    def test_with_spaces(self):
        """С пробелами"""
        assert are_anagrams("conversation", "voices rant on") == True
        assert are_anagrams("the eyes", "they see") == True
    
    def test_mixed_case(self):
        """Разный регистр"""
        assert are_anagrams("Listen", "Silent") == True
        assert are_anagrams("Python", "Typhon") == True
    
    def test_different_lengths(self):
        """Разная длина"""
        assert are_anagrams("abc", "abcd") == False
    
    def test_empty_strings(self):
        """Пустые строки"""
        assert are_anagrams("", "") == True
        assert are_anagrams("", "a") == False
    
    def test_same_word(self):
        """Одинаковые слова"""
        assert are_anagrams("same", "same") == True
    
    def test_invalid_input(self):
        """Неверный тип входных данных"""
        with pytest.raises(TypeError):
            are_anagrams(123, "abc")
        with pytest.raises(TypeError):
            are_anagrams("abc", 123)

# ========== Тесты для combine_dicts ==========

class TestCombineDicts:
    """Тесты для объединения словарей"""
    
    def test_different_keys(self):
        """Разные ключи"""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        result = combine_dicts(dict1, dict2)
        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}
    
    def test_overlapping_keys(self):
        """Пересекающиеся ключи (приоритет у dict2)"""
        dict1 = {"a": 1, "b": 2, "c": 3}
        dict2 = {"b": 20, "c": 30, "d": 40}
        result = combine_dicts(dict1, dict2)
        assert result == {"a": 1, "b": 20, "c": 30, "d": 40}
    
    def test_empty_dicts(self):
        """Пустые словари"""
        assert combine_dicts({}, {}) == {}
        assert combine_dicts({"a": 1}, {}) == {"a": 1}
        assert combine_dicts({}, {"b": 2}) == {"b": 2}
    
    def test_complex_values(self):
        """Сложные значения"""
        dict1 = {"list": [1, 2, 3], "dict": {"x": 10}}
        dict2 = {"set": {1, 2, 3}, "dict": {"y": 20}}
        result = combine_dicts(dict1, dict2)
        assert result == {
            "list": [1, 2, 3],
            "set": {1, 2, 3},
            "dict": {"y": 20}
        }
    
    def test_original_dicts_unchanged(self):
        """Проверка, что исходные словари не изменяются"""
        dict1 = {"a": 1}
        dict2 = {"b": 2}
        dict1_copy = dict1.copy()
        dict2_copy = dict2.copy()
        
        combine_dicts(dict1, dict2)
        
        assert dict1 == dict1_copy
        assert dict2 == dict2_copy
    
    def test_invalid_input(self):
        """Неверный тип входных данных"""
        with pytest.raises(TypeError):
            combine_dicts("not a dict", {})
        with pytest.raises(TypeError):
            combine_dicts({}, "not a dict")