import numpy as np
import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

YEARS = list(range(2021, 2026))
SPECIALTIES = ['Программная инженерия', 'Экономика', 'Медицина', 'Педагогика', 'Право']
FORMS = ['бюджет', 'платное', 'целевое']
SUBJECTS = ['Математика', 'Русский язык', 'Физика', 'Химия', 'Биология']

data = []
for year in YEARS:
    for _ in range(100):  
        name = f"{random.choice(['Иван', 'Петр', 'Сергей', 'Анна', 'Мария'])} {random.choice(['Иванов', 'Петров', 'Сидоров'])}"
        
        ct_scores = [random.randint(40, 100) for _ in range(3)]
        avg_ct = np.mean(ct_scores)
        cert_avg = round(random.uniform(6.0, 10.0), 2)
        total = avg_ct * 3 + cert_avg * 10
        
        if total > 350:
            form = random.choices(FORMS, weights=[0.8, 0.1, 0.1])[0]
        elif total > 300:
            form = random.choices(FORMS, weights=[0.5, 0.4, 0.1])[0]
        else:
            form = random.choices(FORMS, weights=[0.2, 0.7, 0.1])[0]
        
        specialty = random.choice(SPECIALTIES)
        
        data.append({
            'Год': year,
            'ФИО': name,
            'Форма': form,
            'Специальность': specialty,
            'Ср_ЦТ': round(avg_ct, 2),
            'Ср_аттестат': cert_avg,
            'Общий_балл': round(total, 2),
            'Проходной': random.randint(250, 350),
            'Математика': ct_scores[0],
            'Русский': ct_scores[1],
            'Физика': ct_scores[2]
        })

df = pd.DataFrame(data)
print(f"Сгенерировано {len(df)} записей\n")

plt.style.use('seaborn-v0_8')
fig = plt.figure(figsize=(15, 10))

ax1 = plt.subplot(2, 3, 1)
for subject in ['Математика', 'Русский', 'Физика']:
    yearly = df.groupby('Год')[subject].mean()
    ax1.plot(yearly.index, yearly.values, marker='o', label=subject)
ax1.set_title('Средний балл ЦТ по предметам')
ax1.legend()
ax1.grid(True)

ax2 = plt.subplot(2, 3, 2)
cert_yearly = df.groupby('Год')['Ср_аттестат'].mean()
ax2.bar(cert_yearly.index, cert_yearly.values, color='green', alpha=0.7)
ax2.set_title('Средний балл аттестата')
ax2.grid(True, axis='y')

ax3 = plt.subplot(2, 3, 3)
pass_yearly = df.groupby('Год')['Проходной'].mean()
ax3.plot(pass_yearly.index, pass_yearly.values, 'r-o', linewidth=2)
ax3.set_title('Средний проходной балл')
ax3.grid(True)

ax4 = plt.subplot(2, 3, 4)
df['Специальность'].value_counts().plot(kind='pie', ax=ax4, autopct='%1.1f%%')
ax4.set_title('Распределение по специальностям')

ax5 = plt.subplot(2, 3, 5)
form_counts = df.groupby(['Год', 'Форма']).size().unstack()
form_counts.plot(kind='bar', ax=ax5, color=['green', 'orange', 'blue'])
ax5.set_title('Формы обучения по годам')
ax5.legend()
ax5.grid(True, axis='y')

plt.tight_layout()
plt.savefig('admission_stats.png', dpi=150)
plt.show()

print(f"\nВсего студентов: {len(df)}")
print(f"\nСредние баллы по годам:")
print(df.groupby('Год')[['Ср_ЦТ', 'Ср_аттестат', 'Общий_балл']].mean().round(2))

print(f"\nРаспределение по формам обучения:")
print(df['Форма'].value_counts())
print(f"\nТоп специальностей:")
print(df['Специальность'].value_counts().head())
df.to_csv('students.csv', index=False)