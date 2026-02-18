import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
import os  # Добавляем импорт os

warnings.filterwarnings('ignore')

# Функция для форматирования больших чисел
def format_large_number(x):
    if x >= 1e9:
        return f'{x/1e9:.1f} млрд'
    elif x >= 1e6:
        return f'{x/1e6:.1f} млн'
    elif x >= 1e3:
        return f'{x/1e3:.1f} тыс'
    else:
        return f'{x:.0f}'

plt.style.use('default')

def generate_sales_data(n_records=5000, start_date='2023-01-01', end_date='2023-12-31'):
    np.random.seed(42)
    
    products = ['Ноутбук', 'Смартфон', 'Планшет', 'Наушники', 'Часы', 'Камера', 'Консоль', 'Монитор']
    stores = ['Магазин_Центр', 'Магазин_Север', 'Магазин_Юг', 'Магазин_Запад', 'Магазин_Восток', 'Онлайн']
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    records = []
    
    for date in dates:
        season_factor = 1.2 if date.month in [11, 12] else 1.0
        if date.month in [6, 7, 8]:
            season_factor = 0.9
        
        weekend_factor = 1.3 if date.weekday() >= 5 else 1.0
        
        for store in stores:
            store_factor = 1.5 if store == 'Онлайн' else np.random.uniform(0.8, 1.2)
            
            for product in products:
                base_price = {
                    'Ноутбук': 75000, 'Смартфон': 45000, 'Планшет': 35000,
                    'Наушники': 8000, 'Часы': 12000, 'Камера': 55000,
                    'Консоль': 40000, 'Монитор': 28000
                }[product]
                
                base_cost = base_price * np.random.uniform(0.6, 0.75)
                
                quantity = int(np.random.poisson(5 * season_factor * weekend_factor * store_factor))
                if quantity == 0:
                    quantity = np.random.randint(1, 3)
                
                price_variation = np.random.uniform(0.9, 1.1)
                price = base_price * price_variation
                cost = base_cost * (1 + np.random.uniform(-0.05, 0.05))
                
                records.append({
                    'date': date,
                    'product': product,
                    'store': store,
                    'quantity': quantity,
                    'price': round(price, 2),
                    'cost': round(cost, 2),
                    'revenue': round(price * quantity, 2),
                    'total_cost': round(cost * quantity, 2)
                })
    
    df = pd.DataFrame(records)
    df['profit'] = df['revenue'] - df['total_cost']
    df['margin'] = (df['profit'] / df['revenue'] * 100).round(2)
    
    return df

df = generate_sales_data()

print("=" * 90)
print("АНАЛИЗ ДИНАМИКИ ПРОДАЖ".center(90))
print("=" * 90)
print(f"\nПериод анализа: {df['date'].min().date()} - {df['date'].max().date()}")
print(f"Количество записей: {len(df):,}")
print(f"Товаров: {df['product'].nunique()}")
print(f"Точек продаж: {df['store'].nunique()}")

print("\n" + "=" * 90)
print("1. ОБЩИЕ ОПИСАТЕЛЬНЫЕ СТАТИСТИКИ".center(90))
print("=" * 90)

numeric_cols = ['quantity', 'price', 'cost', 'revenue', 'total_cost', 'profit', 'margin']
pd.set_option('display.float_format', '{:,.2f}'.format)
print("\n", df[numeric_cols].describe().round(2).to_string())

print("\n" + "=" * 90)
print("2. АНАЛИЗ ПО ТОВАРАМ".center(90))
print("=" * 90)

product_stats = df.groupby('product').agg({
    'quantity': ['sum', 'mean', 'count'],
    'revenue': ['sum', 'mean'],
    'total_cost': 'sum',
    'profit': ['sum', 'mean'],
    'margin': 'mean',
    'store': 'nunique'
}).round(2)

product_stats.columns = ['total_qty', 'avg_qty_per_sale', 'num_sales', 
                        'total_revenue', 'avg_revenue_per_sale',
                        'total_cost', 'total_profit', 'avg_profit_per_sale',
                        'avg_margin_pct', 'stores_count']

product_stats['avg_price'] = (product_stats['total_revenue'] / product_stats['total_qty']).round(2)
product_stats['share_by_revenue'] = (product_stats['total_revenue'] / product_stats['total_revenue'].sum() * 100).round(2)
product_stats['share_by_quantity'] = (product_stats['total_qty'] / product_stats['total_qty'].sum() * 100).round(2)

# Форматирование для отображения
product_stats_display = product_stats.sort_values('total_revenue', ascending=False).copy()
for col in ['total_revenue', 'total_cost', 'total_profit', 'avg_revenue_per_sale', 'avg_profit_per_sale', 'avg_price']:
    if col in product_stats_display.columns:
        product_stats_display[col] = product_stats_display[col].apply(lambda x: f'{x:,.0f}')

print("\n", product_stats_display.to_string())

print("\n" + "=" * 90)
print("3. АНАЛИЗ ПО ТОЧКАМ ПРОДАЖ".center(90))
print("=" * 90)

store_stats = df.groupby('store').agg({
    'quantity': ['sum', 'mean'],
    'revenue': ['sum', 'mean'],
    'total_cost': 'sum',
    'profit': ['sum', 'mean'],
    'margin': 'mean',
    'product': 'nunique',
    'date': 'nunique'
}).round(2)

store_stats.columns = ['total_qty', 'avg_qty_per_sale', 'total_revenue', 
                      'avg_revenue_per_sale', 'total_cost', 'total_profit',
                      'avg_profit_per_sale', 'avg_margin_pct', 
                      'product_variety', 'active_days']

store_stats['avg_daily_revenue'] = (store_stats['total_revenue'] / store_stats['active_days']).round(2)
store_stats['avg_daily_quantity'] = (store_stats['total_qty'] / store_stats['active_days']).round(2)
store_stats['revenue_per_product'] = (store_stats['total_revenue'] / store_stats['product_variety']).round(2)

# Форматирование для отображения
store_stats_display = store_stats.sort_values('total_revenue', ascending=False).copy()
for col in ['total_revenue', 'avg_revenue_per_sale', 'total_cost', 'total_profit', 
            'avg_profit_per_sale', 'avg_daily_revenue', 'revenue_per_product']:
    if col in store_stats_display.columns:
        store_stats_display[col] = store_stats_display[col].apply(lambda x: f'{x:,.0f}')

print("\n", store_stats_display.to_string())

print("\n" + "=" * 90)
print("4. ДИНАМИКА ПО МЕСЯЦАМ".center(90))
print("=" * 90)

df['year_month'] = df['date'].dt.to_period('M')

monthly_dynamics = df.groupby('year_month').agg({
    'quantity': 'sum',
    'revenue': 'sum',
    'total_cost': 'sum',
    'profit': 'sum',
    'margin': 'mean',
    'product': 'nunique',
    'store': 'nunique'
}).round(2)

monthly_dynamics['avg_price'] = (monthly_dynamics['revenue'] / monthly_dynamics['quantity']).round(2)
monthly_dynamics['mom_revenue_growth'] = monthly_dynamics['revenue'].pct_change() * 100
monthly_dynamics['mom_quantity_growth'] = monthly_dynamics['quantity'].pct_change() * 100

# Форматирование для отображения
monthly_dynamics_display = monthly_dynamics.copy()
for col in ['revenue', 'total_cost', 'profit', 'avg_price']:
    if col in monthly_dynamics_display.columns:
        monthly_dynamics_display[col] = monthly_dynamics_display[col].apply(lambda x: f'{x:,.0f}')

print("\n", monthly_dynamics_display.to_string())

print("\n" + "=" * 90)
print("5. ДИНАМИКА ПО ТОВАРАМ И МЕСЯЦАМ".center(90))
print("=" * 90)

product_monthly = df.groupby(['product', 'year_month']).agg({
    'quantity': 'sum',
    'revenue': 'sum',
    'profit': 'sum'
}).reset_index()

product_pivot_qty = product_monthly.pivot(index='product', columns='year_month', values='quantity').fillna(0)
product_pivot_rev = product_monthly.pivot(index='product', columns='year_month', values='revenue').fillna(0)

print("\nКоличество по месяцам (шт.):")
print("\n", product_pivot_qty.round(0).to_string())

print("\nРост/спад по месяцам (%):")
growth_rates = product_pivot_rev.pct_change(axis=1) * 100
print("\n", growth_rates.round(2).to_string())

print("\n" + "=" * 90)
print("6. ДИНАМИКА ПО ТОЧКАМ И МЕСЯЦАМ".center(90))
print("=" * 90)

store_monthly = df.groupby(['store', 'year_month']).agg({
    'quantity': 'sum',
    'revenue': 'sum',
    'profit': 'sum'
}).reset_index()

store_pivot_rev = store_monthly.pivot(index='store', columns='year_month', values='revenue').fillna(0)

print("\nВыручка по точкам и месяцам (руб.):")
# Форматирование для отображения
store_pivot_display = store_pivot_rev.round(0).astype(int).map(lambda x: f'{x:,}')
print("\n", store_pivot_display.to_string())

print("\nСредние продажи на точку по месяцам (руб.):")
avg_per_store = df.groupby('year_month')['revenue'].sum() / df.groupby('year_month')['store'].nunique()
avg_per_store_display = avg_per_store.round(0).astype(int).map(lambda x: f'{x:,}')
print("\n", avg_per_store_display.to_string())

print("\n" + "=" * 90)
print("7. ПРОГНОЗИРОВАНИЕ ПРОДАЖ (Линейная регрессия)".center(90))
print("=" * 90)

def linear_trend_forecast(dates, values, periods_ahead=3):
    x = np.arange(len(values))
    y = values.values
    
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x * x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n
    
    last_date = dates.max()
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=periods_ahead, freq='MS')
    future_x = np.arange(len(x), len(x) + periods_ahead)
    future_predictions = slope * future_x + intercept
    
    return future_dates, future_predictions

monthly_revenue_series = df.groupby('year_month')['revenue'].sum()
monthly_dates = pd.to_datetime([p.to_timestamp() for p in monthly_revenue_series.index])

forecast_dates, forecast_revenue = linear_trend_forecast(monthly_dates, monthly_revenue_series, 3)

forecast_df = pd.DataFrame({
    'date': forecast_dates,
    'predicted_revenue': forecast_revenue.round(2)
})

print("\nПрогноз выручки на следующие 3 месяца:")
forecast_df_display = forecast_df.copy()
forecast_df_display['predicted_revenue'] = forecast_df_display['predicted_revenue'].apply(lambda x: f'{x:,.0f}')
forecast_df_display['date'] = forecast_df_display['date'].dt.strftime('%Y-%m')
print("\n", forecast_df_display.to_string(index=False))

monthly_quantity_series = df.groupby('year_month')['quantity'].sum()
forecast_dates_qty, forecast_quantity = linear_trend_forecast(monthly_dates, monthly_quantity_series, 3)

forecast_qty_df = pd.DataFrame({
    'date': forecast_dates_qty,
    'predicted_quantity': forecast_quantity.round(0)
})

print("\nПрогноз количества на следующие 3 месяца:")
forecast_qty_df_display = forecast_qty_df.copy()
forecast_qty_df_display['predicted_quantity'] = forecast_qty_df_display['predicted_quantity'].apply(lambda x: f'{x:,.0f}')
forecast_qty_df_display['date'] = forecast_qty_df_display['date'].dt.strftime('%Y-%m')
print("\n", forecast_qty_df_display.to_string(index=False))

print("\n" + "=" * 90)
print("ВИЗУАЛИЗАЦИЯ".center(90))
print("=" * 90)

# Очистка старых графиков
plt.close('all')

# УМЕНЬШАЕМ РАЗМЕР ГРАФИКОВ
fig = plt.figure(figsize=(18, 20))  # Было (24, 32), стало меньше

# Изменяем сетку для более компактного отображения
gs = fig.add_gridspec(5, 3, hspace=0.3, wspace=0.25)  # Было 6 строк, стало 5

total_revenue = df['revenue'].sum()
total_profit = df['profit'].sum()
total_quantity = df['quantity'].sum()
avg_margin = df['margin'].mean()
num_products = df['product'].nunique()
num_stores = df['store'].nunique()

ax_kpi = fig.add_subplot(gs[0, :])
ax_kpi.axis('off')

# Уменьшаем шрифт в KPI
kpi_text = f"""
ОБЩИЙ ТОВАРООБОРОТ: {total_revenue:,.0f} руб.    |    ПРИБЫЛЬ: {total_profit:,.0f} руб.    |    КОЛИЧЕСТВО: {total_quantity:,.0f} шт.
СРЕДНЯЯ НАЦЕНКА: {avg_margin:.1f}%    |    ТОВАРОВ: {num_products}    |    ТОЧЕК ПРОДАЖ: {num_stores}
"""
ax_kpi.text(0.5, 0.5, kpi_text, transform=ax_kpi.transAxes, fontsize=14,
            verticalalignment='center', horizontalalignment='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
            family='monospace', fontweight='bold')

ax1 = fig.add_subplot(gs[1, 0])
monthly_revenue = df.groupby('year_month')['revenue'].sum()
ax1.plot(range(len(monthly_revenue)), monthly_revenue.values, marker='o', 
         linewidth=2, markersize=4, color='steelblue')
ax1.set_title('Выручка по месяцам', fontsize=10, fontweight='bold')
ax1.set_xlabel('Месяц', fontsize=8)
ax1.set_ylabel('Выручка (руб.)', fontsize=8)
ax1.set_xticks(range(len(monthly_revenue)))
ax1.set_xticklabels([str(m) for m in monthly_revenue.index], rotation=45, ha='right', fontsize=7)
ax1.grid(True, alpha=0.3)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
ax1.tick_params(axis='both', which='major', labelsize=7)

ax2 = fig.add_subplot(gs[1, 1])
monthly_quantity = df.groupby('year_month')['quantity'].sum()
ax2.bar(range(len(monthly_quantity)), monthly_quantity.values, color='coral', alpha=0.8)
ax2.set_title('Количество по месяцам', fontsize=10, fontweight='bold')
ax2.set_xlabel('Месяц', fontsize=8)
ax2.set_ylabel('Количество (шт.)', fontsize=8)
ax2.set_xticks(range(len(monthly_quantity)))
ax2.set_xticklabels([str(m) for m in monthly_quantity.index], rotation=45, ha='right', fontsize=7)
ax2.tick_params(axis='both', which='major', labelsize=7)

ax3 = fig.add_subplot(gs[1, 2])
monthly_profit = df.groupby('year_month')['profit'].sum()
colors = ['green' if p > 0 else 'red' for p in monthly_profit.values]
ax3.bar(range(len(monthly_profit)), monthly_profit.values, color=colors, alpha=0.7)
ax3.set_title('Прибыль по месяцам', fontsize=10, fontweight='bold')
ax3.set_xlabel('Месяц', fontsize=8)
ax3.set_ylabel('Прибыль (руб.)', fontsize=8)
ax3.set_xticks(range(len(monthly_profit)))
ax3.set_xticklabels([str(m) for m in monthly_profit.index], rotation=45, ha='right', fontsize=7)
ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
ax3.tick_params(axis='both', which='major', labelsize=7)

ax4 = fig.add_subplot(gs[2, 0])
product_revenue = df.groupby('product')['revenue'].sum().sort_values(ascending=True)
colors_prod = plt.cm.viridis(np.linspace(0, 1, len(product_revenue)))
bars = ax4.barh(range(len(product_revenue)), product_revenue.values, color=colors_prod)
ax4.set_yticks(range(len(product_revenue)))
ax4.set_yticklabels(product_revenue.index, fontsize=8)
ax4.set_xlabel('Выручка (руб.)', fontsize=8)
ax4.set_title('Выручка по товарам', fontsize=10, fontweight='bold')
ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
ax4.tick_params(axis='both', which='major', labelsize=7)
for i, (idx, val) in enumerate(product_revenue.items()):
    ax4.text(val + max(product_revenue.values)*0.01, i, f'{val/1e6:.1f}M', 
             va='center', fontsize=7, fontweight='bold')

ax5 = fig.add_subplot(gs[2, 1])
product_margin = df.groupby('product')['margin'].mean().sort_values(ascending=True)
colors_margin = ['green' if m > 30 else 'orange' if m > 20 else 'red' for m in product_margin.values]
ax5.barh(range(len(product_margin)), product_margin.values, color=colors_margin)
ax5.set_yticks(range(len(product_margin)))
ax5.set_yticklabels(product_margin.index, fontsize=8)
ax5.set_xlabel('Наценка (%)', fontsize=8)
ax5.set_title('Средняя наценка по товарам', fontsize=10, fontweight='bold')
ax5.axvline(x=25, color='red', linestyle='--', alpha=0.5, linewidth=1)
ax5.tick_params(axis='both', which='major', labelsize=7)

ax6 = fig.add_subplot(gs[2, 2])
store_revenue = df.groupby('store')['revenue'].sum().sort_values(ascending=True)
colors_store = plt.cm.plasma(np.linspace(0, 1, len(store_revenue)))
ax6.barh(range(len(store_revenue)), store_revenue.values, color=colors_store)
ax6.set_yticks(range(len(store_revenue)))
ax6.set_yticklabels(store_revenue.index, fontsize=8)
ax6.set_xlabel('Выручка (руб.)', fontsize=8)
ax6.set_title('Выручка по точкам', fontsize=10, fontweight='bold')
ax6.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
ax6.tick_params(axis='both', which='major', labelsize=7)

ax7 = fig.add_subplot(gs[3, :2])
product_month_pivot = df.groupby(['product', 'year_month'])['revenue'].sum().unstack(fill_value=0)
im = ax7.imshow(product_month_pivot.values, cmap='YlOrRd', aspect='auto')
ax7.set_xticks(range(len(product_month_pivot.columns)))
ax7.set_xticklabels([str(c) for c in product_month_pivot.columns], rotation=45, ha='right', fontsize=7)
ax7.set_yticks(range(len(product_month_pivot.index)))
ax7.set_yticklabels(product_month_pivot.index, fontsize=8)
ax7.set_title('Тепловая карта: Выручка по товарам и месяцам', fontsize=10, fontweight='bold')
plt.colorbar(im, ax=ax7, label='Выручка (руб.)', shrink=0.8)

ax8 = fig.add_subplot(gs[3, 2])
daily_revenue = df.groupby('date')['revenue'].sum()
train_size = int(len(daily_revenue) * 0.8)
ax8.plot(range(train_size), daily_revenue.values[:train_size], label='Обучение', color='blue', alpha=0.7, linewidth=1)
ax8.plot(range(train_size, len(daily_revenue)), daily_revenue.values[train_size:], label='Тест', color='green', alpha=0.7, linewidth=1)
ax8.set_title('Разделение данных', fontsize=10, fontweight='bold')
ax8.set_xlabel('Дни', fontsize=8)
ax8.set_ylabel('Выручка (руб.)', fontsize=8)
ax8.legend(fontsize=7)
ax8.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
ax8.tick_params(axis='both', which='major', labelsize=7)

ax9 = fig.add_subplot(gs[4, 0])
forecast_dates = pd.to_datetime(forecast_df['date'])
forecast_values = forecast_df['predicted_revenue']
historical_monthly = df.groupby(df['date'].dt.to_period('M'))['revenue'].sum()
hist_dates = [p.to_timestamp() for p in historical_monthly.index]
ax9.plot(hist_dates, historical_monthly.values, marker='o', label='История', color='steelblue', linewidth=1.5, markersize=3)
ax9.plot(forecast_dates, forecast_values, marker='s', label='Прогноз', color='red', 
          linestyle='--', linewidth=1.5, markersize=4)
ax9.set_title('Прогноз выручки', fontsize=10, fontweight='bold')
ax9.set_xlabel('Месяц', fontsize=8)
ax9.set_ylabel('Выручка (руб.)', fontsize=8)
ax9.legend(fontsize=7)
ax9.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
plt.setp(ax9.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=7)

ax10 = fig.add_subplot(gs[4, 1])
qty_forecast_dates = pd.to_datetime(forecast_qty_df['date'])
qty_forecast_values = forecast_qty_df['predicted_quantity']
historical_qty_monthly = df.groupby(df['date'].dt.to_period('M'))['quantity'].sum()
ax10.plot([p.to_timestamp() for p in historical_qty_monthly.index], historical_qty_monthly.values, 
          marker='o', label='История', color='coral', linewidth=1.5, markersize=3)
ax10.plot(qty_forecast_dates, qty_forecast_values, marker='s', label='Прогноз', 
          color='red', linestyle='--', linewidth=1.5, markersize=4)
ax10.set_title('Прогноз количества', fontsize=10, fontweight='bold')
ax10.set_xlabel('Месяц', fontsize=8)
ax10.set_ylabel('Количество (шт.)', fontsize=8)
ax10.legend(fontsize=7)
plt.setp(ax10.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=7)

ax11 = fig.add_subplot(gs[4, 2])
growth_data = monthly_dynamics['mom_revenue_growth'].dropna()
colors_growth = ['green' if g > 0 else 'red' for g in growth_data.values]
ax11.bar(range(len(growth_data)), growth_data.values, color=colors_growth, alpha=0.7)
ax11.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax11.set_title('Рост/спад выручки (%)', fontsize=10, fontweight='bold')
ax11.set_xlabel('Месяц', fontsize=8)
ax11.set_ylabel('Изменение (%)', fontsize=8)
ax11.set_xticks(range(len(growth_data)))
ax11.set_xticklabels([str(m) for m in growth_data.index], rotation=45, ha='right', fontsize=7)
ax11.tick_params(axis='both', which='major', labelsize=7)

# СОХРАНЕНИЕ С ОТЛАДКОЙ
from datetime import datetime

# Генерируем уникальное имя файла
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'sales_analysis_report_{timestamp}.png'

# Сохраняем с высоким DPI
plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')

# Проверяем сохранение
print(f"\nПопытка сохранения файла: {filename}")
print(f"Абсолютный путь: {os.path.abspath(filename)}")
print(f"Файл создан: {os.path.exists(filename)}")

# Показываем график
plt.show()

# Дополнительная проверка
if os.path.exists(filename):
    print(f"✅ Файл успешно сохранен! Размер: {os.path.getsize(filename)} байт")
else:
    print("❌ Файл НЕ сохранен!")

print("\n" + "=" * 90)
print(f"ОТЧЁТ СОХРАНЁН: {filename}".center(90))
print("=" * 90)

print("\n" + "=" * 90)
print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ".center(90))
print("=" * 90)

print(f"\n1. ОБЩИЙ ТОВАРООБОРОТ: {total_revenue:,.0f} руб.")
print(f"   - Прибыль: {total_profit:,.0f} руб.")
print(f"   - Наценка: {avg_margin:.1f}%")

print(f"\n2. ТОП-3 ТОВАРА ПО ВЫРУЧКЕ:")
for i, (prod, rev) in enumerate(product_revenue.tail(3).iloc[::-1].items(), 1):
    print(f"   {i}. {prod}: {rev:,.0f} руб.")

print(f"\n3. ТОП-3 ТОЧКИ ПО ВЫРУЧКЕ:")
for i, (store, rev) in enumerate(store_revenue.tail(3).iloc[::-1].items(), 1):
    print(f"   {i}. {store}: {rev:,.0f} руб.")

print(f"\n4. ПРОГНОЗ НА СЛЕДУЮЩИЙ КВАРТАЛ:")
total_forecast = forecast_df['predicted_revenue'].sum()
print(f"   - Ожидаемая выручка: {total_forecast:,.0f} руб.")
print(f"   - Ожидаемое количество: {forecast_qty_df['predicted_quantity'].sum():,.0f} шт.")

print("\n" + "=" * 90)
print("АНАЛИЗ ЗАВЕРШЁН".center(90))
print("=" * 90)