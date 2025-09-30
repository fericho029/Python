def flatten_list(lst):
    i = 0
    while i < len(lst):
        if type(lst[i]) == list:
            flatten_list(lst[i])
            lst[i:i+1] = lst[i]
        else:
            i += 1

    numbers = []
    for i in range(len(lst)):
        numbers.append(int(lst[i]))

    result = []
    for x in numbers:
        if x not in result:
            result.append(x)
    return sorted(result)
 

list_a = [1, 2, 3, [4, 3, 1], 5, [6, [7, [10], 8, [9, 2 ,3]]]]
print(f"Исходный список: {list_a}")
flatten_list(list_a)
print(f"Уникальный список: {flatten_list(list_a)}")