def merge_sorted_list(a, b):
    result = []
    i = j = 0

    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1

    result.extend(a[i:])
    result.extend(b[j:])
    return result


list_first = list(map(int, input("Введи первый список: ").split()))
list_second = list(map(int, input("Введи второй список: ").split()))
print(merge_sorted_list(list_first, list_second))