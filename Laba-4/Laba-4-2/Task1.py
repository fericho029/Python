import os
import numpy as np
import matplotlib.pyplot as plt


months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", 
          "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]

expenses = []

print("\nВведите расходы на проезд по месяцам:")
for month in months:
    expense = float(input(f"  {month}: "))
    expenses.append(expense)

expenses = np.array(expenses)

winter_months = [0, 1, 11]
summer_months = [5, 6, 7]

winter_expenses = expenses[winter_months].sum()
summer_expenses = expenses[summer_months].sum()

print(f"\nСравнение периодов:")
print(f"Зимние месяцы (дек-фев): {winter_expenses}")
print(f"Летние месяцы (июн-авг): {summer_expenses}")

if winter_expenses > summer_expenses:
    print(f"Зимой тратится больше на {winter_expenses - summer_expenses}")
elif summer_expenses > winter_expenses:
    print(f"Летом тратится больше на {summer_expenses - winter_expenses}")
else:
    print("Расходы равны")

max_expense = expenses.max()
max_months_indices = np.where(expenses == max_expense)[0]

print(f"\nМесяцы с наибольшими расходами ({max_expense}): ")
for idx in max_months_indices:
    print('-',months[idx])

plt.figure(figsize=(12, 6))
    
plt.subplot(1, 2, 1)
bars = plt.bar(months, expenses, color='skyblue', edgecolor='black')
    
for idx in winter_months:
    bars[idx].set_color('lightblue')
for idx in summer_months:
    bars[idx].set_color('lightcoral')
    
plt.title('Расходы на проезд по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Рублей')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
    
plt.subplot(1, 2, 2)
seasons = ['Зима', 'Весна', 'Лето', 'Осень']
season_expenses = [
    expenses[[0, 1, 11]].sum(),
    expenses[[2, 3, 4]].sum(),
    expenses[[5, 6, 7]].sum(),
    expenses[[8, 9, 10]].sum()
]
    
colors = ['lightblue', 'lightgreen', 'lightcoral', 'gold']
plt.pie(season_expenses, labels=seasons, colors=colors, autopct='%1.1f%%')
plt.title('Расходы по сезонам')
    
plt.tight_layout()
    
if not os.path.exists('data'):
    os.makedirs('data')
    
plt.savefig('data/expenses_analysis.png', dpi=120, bbox_inches='tight')
plt.show()