text = input("Введите текст: ");
words = text.split();

word_count ={};
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

unique_words_count = len(word_count);

print();
for word in word_count:
    print (f"{word}: {word_count.get(word)}")
print("\nКоличество уникальных слов: ", unique_words_count);