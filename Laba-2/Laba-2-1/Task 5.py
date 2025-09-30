first_word = input("Введите первое слово: ").lower()
second_word = input("Введите второе слово: ").lower()

is_anagram = sorted(first_word) == sorted(second_word)

print(f"\nАнаграмма: {is_anagram}")
