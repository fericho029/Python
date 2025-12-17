import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

if not os.path.exists('images'):
    os.makedirs('images')

#Tело
body = patches.Ellipse((5, 5), 5, 3, color='#808080', alpha=0.8)
ax.add_patch(body)

#Голоав
head = patches.Circle((5, 7), 2, color='#808080', alpha=0.8)
mask = patches.Wedge((5, 6.5), 1.5, 200, 340, color='black', alpha=0.7)
ax.add_patch(head)
ax.add_patch(mask)

#Глаза
left_eye_white = patches.Circle((4.2, 7.3), 0.4, color='white')
right_eye_white = patches.Circle((5.8, 7.3), 0.4, color='white')
left_eye = patches.Circle((4.2, 7.3), 0.2, color='black')
right_eye = patches.Circle((5.8, 7.3), 0.2, color='black')
ax.add_patch(left_eye_white)
ax.add_patch(right_eye_white)
ax.add_patch(left_eye)
ax.add_patch(right_eye)

#Нос
nose = patches.Circle((5, 6.4), 0.3, color='black')
ax.add_patch(nose)

#Уши
left_ear_outer = patches.Polygon([[3.5, 8.5], [3, 9.5], [4.5, 9]], color='#808080')
right_ear_outer = patches.Polygon([[6.5, 8.5], [7, 9.5], [5.5, 9]], color='#808080')
left_ear_inner = patches.Polygon([[3.7, 8.7], [3.3, 9.3], [4.3, 8.9]], color='white')
right_ear_inner = patches.Polygon([[6.3, 8.7], [6.7, 9.3], [5.7, 8.9]], color='white')
ax.add_patch(left_ear_inner)
ax.add_patch(right_ear_inner)
ax.add_patch(left_ear_outer)
ax.add_patch(right_ear_outer)

#Усы
for i in range(4):
    y = 6.6 - i * 0.15
    ax.plot([4, 2], [y, y - 0.2], 'k-', linewidth=1, alpha=0.7)
    ax.plot([6, 8], [y, y + 0.1], 'k-', linewidth=1, alpha=0.7)

#Лапы
paws = [
    patches.Ellipse((3.5, 3.5), 1, 0.8, color='#808080'),
    patches.Ellipse((6.5, 3.5), 1, 0.8, color='#808080'),
    patches.Ellipse((2.8, 4.5), 0.8, 1.2, color='#808080'),
    patches.Ellipse((7.2, 4.5), 0.8, 1.2, color='#808080')
]
for paw in paws:
    ax.add_patch(paw)

#Хвост
tail_x = np.linspace(7, 9, 100)
tail_y = 4.5 + 0.5 * np.sin(tail_x * 2)
ax.plot(tail_x, tail_y, color='#808080', linewidth=6, alpha=0.8)
for i in range(1, 6):
    stripe = patches.Rectangle((7.2 + i*0.3, 4 + 0.3), 0.2, 1, color='black', angle=15)
    ax.add_patch(stripe)

plt.tight_layout()
plt.savefig('images/task3_raccoon.png', dpi=150, bbox_inches='tight')
plt.show()

input("Нажмите Enter для выхода")