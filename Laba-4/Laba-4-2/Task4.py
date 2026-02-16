import numpy as np
from scipy import integrate

def f1(x):
    return np.exp(-x) * np.sin(2*x)

a, b = 0, 2*np.pi

result_definite, error_definite = integrate.quad(f1, a, b)

print("Опреденный")
print(f"e^(-x)·sin(2x) dx")
print(f"x от {a} до {b:.2f}")
print(f"Результат: {result_definite:.8f}")
print(f"Погрешность: {error_definite:.2e}")
print()

def f2(x, y):
    return np.sin(x) * np.cos(y)

x1, x2 = 0, np.pi
y1, y2 = 0, np.pi/2

result_double, error_double = integrate.dblquad(
    f2, y1, y2, lambda x: x1, lambda x: x2
)

print("Двойной")
print(f"sin(x)·cos(y) dx dy")
print(f"x от {x1} до {x2:.2f}, y от {y1} до {y2:.2f}")
print(f"Результат: {result_double:.8f}")
print(f"Погрешность: {error_double:.2e}")