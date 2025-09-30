def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]

def input_matrix(rows, cols):
    print(f"Введите {rows} строк по {cols} элементов (через пробел):")
    matrix = []
    for i in range(rows):
        row = list(map(int, input(f"Строка {i + 1}: ").split()))
        matrix.append(row)
    return matrix

def print_matrix(matrix, title):
    print(f"\n{title}:")
    for row in matrix:
        print(" ".join(map(str, row)))

rows = int(input("Введите количество строк: "))
cols = int(input("Введите количество столбцов: "))
original = input_matrix(rows, cols)
transposed = transpose_matrix(original)
print_matrix(original, "Исходная матрица")
print_matrix(transposed, "Транспонированная матрица")
