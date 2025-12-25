import numpy as np

print("Версия numpy:", np.__version__)

A_test = np.array([
    [-2.0, -8.5, -3.4, 3.5],
    [0.0, 2.4, 0.0, 8.2],
    [2.5, 1.6, 2.1, 3.0],
    [0.3, -0.4, -4.8, 4.6]
])

print(f"Определитель тестовой матрицы: {np.linalg.det(A_test):.6f}")
print(f"Ваш определитель: {det_yours}")
print(f"Разница: {np.linalg.det(A_test) - det_yours}")