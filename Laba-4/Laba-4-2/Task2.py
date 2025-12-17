import numpy as np

lengths_input = input("Длины (км): ")
lengths = np.array(list(map(float, lengths_input.split())))

speeds_input = input("Скорости (км/ч): ")
speeds = np.array(list(map(float, speeds_input.split())))

k = int(input("Начальный участок (k): "))
p = int(input("Конечный участок (p): "))

start_idx = k - 1
end_idx = p - 1

selected_lengths = lengths[start_idx:end_idx + 1]
selected_speeds = speeds[start_idx:end_idx + 1]

total_length = selected_lengths.sum()
times = selected_lengths / selected_speeds
total_time = times.sum()
average_speed = total_length / total_time

print(f"S = {total_length:.1f} км")
print(f"T = {total_time:.2f} ч")
print(f"V = {average_speed:.2f} км/ч")