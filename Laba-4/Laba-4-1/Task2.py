import numpy as np
import matplotlib.pyplot as plt
import os

x = np.linspace(-10, 10, 2000)
x = x[np.abs(x) > 0.01]
y = (x**2 - 9) / x**3

if not os.path.exists('images'):
    os.makedirs('images')

plt.figure(figsize=(12, 8))
plt.plot(x, y, 'g-', linewidth=2, label='f(x) = (x² - 9)/x³')
plt.axvline(x=0, color='red', linestyle='--', linewidth=1, alpha=0.5, label='x=0')
plt.axhline(y=0, color='blue', linestyle='--', linewidth=1, alpha=0.5, label='y=0')

zeros = [-3, 3]
for zero in zeros:
    plt.plot(zero, 0, 'ko', markersize=6)

plt.title('f(x) = (x² - 9) / x³')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xlim(-10, 10)
plt.ylim(-5, 5)
plt.tight_layout()
plt.savefig('images/task2_plot.png', dpi=120)
plt.show()
input("\nНажмите Enter для выхода")