import numpy as np
import matplotlib.pyplot as plt
import os

x_deg = np.linspace(-360, 360, 1000) 
x_rad = np.deg2rad(x_deg) 

f = np.exp(np.cos(x_rad)) + np.log(np.cos(0.6 * x_rad)**2 + 1) * np.sin(x_rad)
h = -np.log((np.cos(x_rad) + np.sin(x_rad))**2 + 2.5) + 10

images_dir = 'images'
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(x_deg, f, 'b-', linewidth=1.5)
ax1.set_title(r'$f(x) = e^{\cos x} + \ln(\cos^2(0.6x) + 1) \cdot \sin x$')
ax1.set_xlabel('Градусы (°)')
ax1.set_ylabel('f(x)')
ax1.grid(True, alpha=0.3)

ax2.plot(x_deg, h, 'r-', linewidth=1.5)
ax2.set_title(r'$h(x) = -\ln((\cos x + \sin x)^2 + 2.5) + 10$')
ax2.set_xlabel('Градусы (°)')
ax2.set_ylabel('h(x)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()

image_path = os.path.join(images_dir, 'task1_plot.png')
plt.savefig(image_path, dpi=120)
plt.show()
input("\nНажмите Enter для выхода")