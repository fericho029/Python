text = input("Введите текст");
words = text.split();

word_count ={};
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

unique_words_count = len(word_count);

print(word_count, "\nКоличество уникальных слов: ", unique_words_count);