def log_merge(func):
    def wrapper(dict_a, dict_b):
        print("\nНачало слияния")

        print("\ndict_a до слияния: ")
        for key in dict_a:
            print(f"{key}: {dict_a[key]}")

        print("\ndict_b до слияния: ")
        for key in dict_b:
            print(f"{key}: {dict_b[key]}")

        func(dict_a, dict_b)

        print("\nСписок после слияния: ")
        for key in dict_a:
            print(f"{key}: {dict_a[key]}")

        print("\nСлияние завершено\n")
    return wrapper

def merge_dicts(dict_a, dict_b):
    for key in dict_b:
        if key in dict_a:
            a_val = dict_a[key]
            b_val = dict_b[key]

            if isinstance(a_val, dict) and isinstance(b_val, dict):
                merge_dicts(a_val, b_val)
            elif isinstance(a_val, (int, float)) and isinstance(b_val, (int, float)):
                dict_a[key] = a_val + b_val
            elif isinstance(a_val, set) and isinstance(b_val, set):
                dict_a[key] = a_val | b_val
            elif isinstance(a_val, list) and isinstance(b_val, list):
                dict_a[key] = a_val + b_val
            elif isinstance(a_val, tuple) and isinstance(b_val, tuple):
                dict_a[key] = a_val + b_val
            else:
                dict_a[key] = b_val
        else:
            dict_a[key] = dict_b[key]

@log_merge
def merge_top(dict_a, dict_b):
    merge_dicts(dict_a, dict_b)

if __name__ == "__main__":
    dict_a = {
        "a": [1, 2],
        "b": {"a": 1},
        "c": {1, 2},
        "d": (10,),
        "e": 5,
        "f": {"list": [1, 2]}
    }

    dict_b = {
        "a": [3],
        "b": {"b": 2},
        "c": {2, 3},
        "d": (20,),
        "e": 7,
        "f": {"list": [3, 4]},
        "g": "new"
    }

    merge_top(dict_a, dict_b)
