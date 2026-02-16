import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def load_and_preprocess_data(file_path):
    df = pd.read_excel(file_path)
    
    df['ISSUE_DATE'] = pd.to_datetime(df['ISSUE_DATE'])
    df['FLIGHT_DATE_LOC'] = pd.to_datetime(df['FLIGHT_DATE_LOC'])
    
    df['DAYS_BEFORE_FLIGHT'] = (df['FLIGHT_DATE_LOC'] - df['ISSUE_DATE']).dt.days
    
    df['ISSUE_MONTH'] = df['ISSUE_DATE'].dt.month
    df['ISSUE_WEEKDAY'] = df['ISSUE_DATE'].dt.dayofweek  
    df['FLIGHT_MONTH'] = df['FLIGHT_DATE_LOC'].dt.month
    df['FLIGHT_WEEKDAY'] = df['FLIGHT_DATE_LOC'].dt.dayofweek
    
    df['FFP_FLAG'] = df['FFP_FLAG'].fillna('NO_FFP')
    df['ORIG_CITY_CODE'] = df['ORIG_CITY_CODE'].fillna('UNKNOWN')
    df['DEST_CITY_CODE'] = df['DEST_CITY_CODE'].fillna('UNKNOWN')
    
    df['FOP_PRIMARY'] = df['FOP_TYPE_CODE'].str.split(',').str[0]
    
    df['IS_INTERNATIONAL'] = (df['ROUTE_FLIGHT_TYPE'] == 'МВЛ').astype(int)
    
    df['ROUTE'] = df['ORIG_CITY_CODE'] + '-' + df['DEST_CITY_CODE']
    
    return df

df = load_and_preprocess_data('s7_data_sample_rev4_50k.xlsx')

print(f"Размер датасета: {df.shape}")
print(f"Колонки: {df.columns.tolist()}")


def descriptive_statistics(df):
    """
    Вывод общих описательных статистик
    """
    print("\n" + "="*60)
    print("ОБЩИЕ ОПИСАТЕЛЬНЫЕ СТАТИСТИКИ")
    print("="*60)
    
    print("\n--- Числовые показатели ---")
    numeric_stats = df[['REVENUE_AMOUNT', 'DAYS_BEFORE_FLIGHT']].describe()
    print(numeric_stats)
    
    print("\n--- Распределение по типам пассажиров ---")
    print(df['PAX_TYPE'].value_counts(normalize=True) * 100)
    
    print("\n--- Распределение по типам маршрутов ---")
    print(df['ROUTE_FLIGHT_TYPE'].value_counts(normalize=True) * 100)
    
    print("\n--- Каналы продаж ---")
    print(df['SALE_TYPE'].value_counts(normalize=True) * 100)
    
    print("\n--- Программа лояльности FFP ---")
    print(df['FFP_FLAG'].value_counts(normalize=True) * 100)
    
    print("\n--- Топ-10 способов оплаты ---")
    print(df['FOP_PRIMARY'].value_counts().head(10))
    
    return numeric_stats

stats = descriptive_statistics(df)

def plot_general_statistics(df):
    """
    Создание дашборда с общими статистиками
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('S7 Airlines: Общие описательные статистики продаж', 
                 fontsize=16, fontweight='bold')
    
    axes[0, 0].hist(df['REVENUE_AMOUNT'], bins=50, color='steelblue', 
                    edgecolor='black', alpha=0.7)
    axes[0, 0].axvline(df['REVENUE_AMOUNT'].mean(), color='red', 
                       linestyle='--', linewidth=2, label=f'Среднее: {df["REVENUE_AMOUNT"].mean():.0f}')
    axes[0, 0].axvline(df['REVENUE_AMOUNT'].median(), color='green', 
                       linestyle='--', linewidth=2, label=f'Медиана: {df["REVENUE_AMOUNT"].median():.0f}')
    axes[0, 0].set_title('Распределение выручки на билет')
    axes[0, 0].set_xlabel('Выручка (руб.)')
    axes[0, 0].set_ylabel('Количество')
    axes[0, 0].legend()
    
    pax_counts = df['PAX_TYPE'].value_counts()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    axes[0, 1].pie(pax_counts.values, labels=['Взрослые (AD)', 'Дети (CHD)', 'Младенцы (INF)'], 
                   autopct='%1.1f%%', colors=colors, explode=(0.05, 0.02, 0.02))
    axes[0, 1].set_title('Структура пассажиров')
    
    route_counts = df['ROUTE_FLIGHT_TYPE'].value_counts()
    axes[0, 2].bar(['Внутренние (ВВЛ)', 'Международные (МВЛ)'], 
                   route_counts.values, color=['#96CEB4', '#FFEAA7'])
    axes[0, 2].set_title('Распределение маршрутов')
    for i, v in enumerate(route_counts.values):
        axes[0, 2].text(i, v + 500, f'{v:,}\n({v/len(df)*100:.1f}%)', 
                        ha='center', fontweight='bold')
    
    sale_counts = df['SALE_TYPE'].value_counts()
    axes[1, 0].bar(['ONLINE', 'OFFLINE'], sale_counts.values, 
                   color=['#74B9FF', '#A29BFE'])
    axes[1, 0].set_title('Каналы продаж')
    for i, v in enumerate(sale_counts.values):
        axes[1, 0].text(i, v + 500, f'{v:,}\n({v/len(df)*100:.1f}%)', 
                        ha='center', fontweight='bold')
    
    ffp_counts = df['FFP_FLAG'].value_counts()
    axes[1, 1].bar(['Не участники', 'Участники FFP'], ffp_counts.values, 
                   color=['#FAB1A0', '#55A3FF'])
    axes[1, 1].set_title('Программа лояльности FFP')
    for i, v in enumerate(ffp_counts.values):
        axes[1, 1].text(i, v + 500, f'{v:,}\n({v/len(df)*100:.1f}%)', 
                        ha='center', fontweight='bold')
    
    axes[1, 2].hist(df['DAYS_BEFORE_FLIGHT'], bins=50, color='#FD79A8', 
                    edgecolor='black', alpha=0.7)
    axes[1, 2].axvline(df['DAYS_BEFORE_FLIGHT'].mean(), color='red', 
                       linestyle='--', linewidth=2, label=f'Среднее: {df["DAYS_BEFORE_FLIGHT"].mean():.1f} дн.')
    axes[1, 2].axvline(df['DAYS_BEFORE_FLIGHT'].median(), color='green', 
                       linestyle='--', linewidth=2, label=f'Медиана: {df["DAYS_BEFORE_FLIGHT"].median():.0f} дн.')
    axes[1, 2].set_title('Заблаговременность покупки')
    axes[1, 2].set_xlabel('Дней до полёта')
    axes[1, 2].set_ylabel('Количество')
    axes[1, 2].legend()
    axes[1, 2].set_xlim(0, 100)
    
    plt.tight_layout()
    plt.savefig('s7_general_stats.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_general_statistics(df)

def analyze_airports(df):
    print("\n" + "="*60)
    print("АНАЛИЗ АЭРОПОРТОВ")
    print("="*60)
    
    print("\n--- Топ-15 аэропортов отправления ---")
    top_orig = df['ORIG_CITY_CODE'].value_counts().head(15)
    print(top_orig)
    
    print("\n--- Топ-15 аэропортов назначения ---")
    top_dest = df['DEST_CITY_CODE'].value_counts().head(15)
    print(top_dest)
    
    orig_stats = df.groupby('ORIG_CITY_CODE').agg({
        'REVENUE_AMOUNT': ['count', 'mean', 'sum'],
        'IS_INTERNATIONAL': 'mean'
    }).round(2)
    orig_stats.columns = ['Flights', 'Avg_Revenue', 'Total_Revenue', 'Intl_Share']
    orig_stats = orig_stats.sort_values('Flights', ascending=False)
    
    print("\n--- Статистика по аэропортам отправления ---")
    print(orig_stats.head(10))
    
    print("\n--- Топ-15 маршрутов ---")
    top_routes = df['ROUTE'].value_counts().head(15)
    print(top_routes)
    
    return orig_stats, top_routes

orig_stats, top_routes = analyze_airports(df)

def plot_airports_analysis(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('S7 Airlines: Анализ аэропортов и маршрутов', 
                 fontsize=16, fontweight='bold')
    
    top_10_orig = df['ORIG_CITY_CODE'].value_counts().head(10)
    axes[0, 0].barh(range(len(top_10_orig)), top_10_orig.values, color='skyblue')
    axes[0, 0].set_yticks(range(len(top_10_orig)))
    axes[0, 0].set_yticklabels(top_10_orig.index)
    axes[0, 0].set_xlabel('Количество рейсов')
    axes[0, 0].set_title('Топ-10 аэропортов отправления')
    axes[0, 0].invert_yaxis()
    
    top_airports = top_10_orig.index.tolist()
    avg_rev_by_airport = df[df['ORIG_CITY_CODE'].isin(top_airports)].groupby('ORIG_CITY_CODE')['REVENUE_AMOUNT'].mean()
    avg_rev_by_airport = avg_rev_by_airport.reindex(top_airports)
    axes[0, 1].bar(range(len(avg_rev_by_airport)), avg_rev_by_airport.values, color='coral')
    axes[0, 1].set_xticks(range(len(avg_rev_by_airport)))
    axes[0, 1].set_xticklabels(avg_rev_by_airport.index, rotation=45)
    axes[0, 1].set_ylabel('Средняя выручка (руб.)')
    axes[0, 1].set_title('Средняя выручка по аэропортам')
    
    top_10_routes = df['ROUTE'].value_counts().head(10)
    axes[1, 0].barh(range(len(top_10_routes)), top_10_routes.values, color='lightgreen')
    axes[1, 0].set_yticks(range(len(top_10_routes)))
    axes[1, 0].set_yticklabels(top_10_routes.index, fontsize=8)
    axes[1, 0].set_xlabel('Количество рейсов')
    axes[1, 0].set_title('Топ-10 маршрутов')
    axes[1, 0].invert_yaxis()
    
    top_5 = df['ORIG_CITY_CODE'].value_counts().head(5).index
    route_type_by_airport = df[df['ORIG_CITY_CODE'].isin(top_5)].groupby(['ORIG_CITY_CODE', 'ROUTE_FLIGHT_TYPE']).size().unstack(fill_value=0)
    route_type_by_airport.plot(kind='bar', stacked=True, ax=axes[1, 1], color=['#96CEB4', '#FFEAA7'])
    axes[1, 1].set_title('Структура маршрутов по топ-5 аэропортам')
    axes[1, 1].set_xlabel('Аэропорт')
    axes[1, 1].set_ylabel('Количество рейсов')
    axes[1, 1].legend(title='Тип маршрута')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('s7_airports_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_airports_analysis(df)

def analyze_seasonality(df):
    print("\n" + "="*60)
    print("АНАЛИЗ СЕЗОННОСТИ")
    print("="*60)
    
    monthly_sales = df.groupby('ISSUE_MONTH').agg({
        'REVENUE_AMOUNT': ['count', 'sum', 'mean'],
        'DAYS_BEFORE_FLIGHT': 'mean'
    }).round(2)
    monthly_sales.columns = ['Tickets_Sold', 'Total_Revenue', 'Avg_Revenue', 'Avg_Advance_Purchase']
    
    print("\n--- Статистика по месяцам продаж ---")
    print(monthly_sales)
    
    weekday_sales = df.groupby('ISSUE_WEEKDAY').agg({
        'REVENUE_AMOUNT': ['count', 'sum', 'mean']
    }).round(2)
    weekday_sales.columns = ['Tickets_Sold', 'Total_Revenue', 'Avg_Revenue']
    weekday_sales.index = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    
    print("\n--- Статистика по дням недели ---")
    print(weekday_sales)
    
    flight_monthly = df.groupby('FLIGHT_MONTH').agg({
        'REVENUE_AMOUNT': ['count', 'sum']
    }).round(2)
    flight_monthly.columns = ['Flights', 'Total_Revenue']
    
    print("\n--- Статистика по месяцам полётов ---")
    print(flight_monthly)
    
    return monthly_sales, weekday_sales, flight_monthly

monthly_sales, weekday_sales, flight_monthly = analyze_seasonality(df)

def plot_seasonality(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('S7 Airlines: Анализ сезонности', fontsize=16, fontweight='bold')
    
    monthly_data = df.groupby('ISSUE_MONTH').size()
    axes[0, 0].plot(monthly_data.index, monthly_data.values, marker='o', linewidth=2, markersize=8, color='steelblue')
    axes[0, 0].set_title('Динамика продаж по месяцам (дата покупки)')
    axes[0, 0].set_xlabel('Месяц')
    axes[0, 0].set_ylabel('Количество проданных билетов')
    axes[0, 0].set_xticks(range(1, 13))
    axes[0, 0].grid(True, alpha=0.3)
    
    monthly_revenue = df.groupby('ISSUE_MONTH')['REVENUE_AMOUNT'].sum()
    axes[0, 1].bar(monthly_revenue.index, monthly_revenue.values, color='coral', alpha=0.8)
    axes[0, 1].set_title('Выручка по месяцам')
    axes[0, 1].set_xlabel('Месяц')
    axes[0, 1].set_ylabel('Общая выручка (руб.)')
    axes[0, 1].set_xticks(range(1, 13))
    
    weekday_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    weekday_data = df.groupby('ISSUE_WEEKDAY').size()
    colors = ['#FF6B6B' if d >= 5 else '#4ECDC4' for d in weekday_data.index]
    axes[1, 0].bar(weekday_data.index, weekday_data.values, color=colors, alpha=0.8)
    axes[1, 0].set_title('Продажи по дням недели')
    axes[1, 0].set_xlabel('День недели')
    axes[1, 0].set_ylabel('Количество продаж')
    axes[1, 0].set_xticks(range(7))
    axes[1, 0].set_xticklabels(weekday_names)
    
    flight_month_data = df.groupby('FLIGHT_MONTH').size()
    axes[1, 1].plot(flight_month_data.index, flight_month_data.values, marker='s', 
                    linewidth=2, markersize=8, color='green')
    axes[1, 1].set_title('Распределение полётов по месяцам')
    axes[1, 1].set_xlabel('Месяц полёта')
    axes[1, 1].set_ylabel('Количество полётов')
    axes[1, 1].set_xticks(range(1, 13))
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('s7_seasonality.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_seasonality(df)

def analyze_passengers(df):
    print("\n" + "="*60)
    print("АНАЛИЗ ПАССАЖИРОВ")
    print("="*60)
    
    pax_analysis = df.groupby('PAX_TYPE').agg({
        'REVENUE_AMOUNT': ['count', 'mean', 'median', 'sum'],
        'DAYS_BEFORE_FLIGHT': 'mean',
        'IS_INTERNATIONAL': 'mean'
    }).round(2)
    pax_analysis.columns = ['Count', 'Avg_Revenue', 'Median_Revenue', 'Total_Revenue', 
                           'Avg_Advance', 'Intl_Share']
    
    print("\n--- Статистика по типам пассажиров ---")
    print(pax_analysis)
    
    ffp_analysis = df.groupby('FFP_FLAG').agg({
        'REVENUE_AMOUNT': ['count', 'mean', 'median'],
        'DAYS_BEFORE_FLIGHT': 'mean',
        'IS_INTERNATIONAL': 'mean'
    }).round(2)
    ffp_analysis.columns = ['Count', 'Avg_Revenue', 'Median_Revenue', 
                           'Avg_Advance', 'Intl_Share']
    
    print("\n--- Статистика по программе лояльности ---")
    print(ffp_analysis)
    
    cross_tab = pd.crosstab(df['PAX_TYPE'], df['FFP_FLAG'], normalize='index') * 100
    print("\n--- Распределение FFP по типам пассажиров (%) ---")
    print(cross_tab.round(2))
    
    sale_pax = pd.crosstab(df['PAX_TYPE'], df['SALE_TYPE'], normalize='index') * 100
    print("\n--- Каналы продаж по типам пассажиров (%) ---")
    print(sale_pax.round(2))
    
    return pax_analysis, ffp_analysis

pax_analysis, ffp_analysis = analyze_passengers(df)

def plot_passenger_analysis(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('S7 Airlines: Анализ пассажиров', fontsize=16, fontweight='bold')
    
    avg_rev_pax = df.groupby('PAX_TYPE')['REVENUE_AMOUNT'].mean()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    bars = axes[0, 0].bar(avg_rev_pax.index, avg_rev_pax.values, color=colors)
    axes[0, 0].set_title('Средняя выручка по типам пассажиров')
    axes[0, 0].set_ylabel('Средняя выручка (руб.)')
    axes[0, 0].set_xticklabels(['Взрослые (AD)', 'Дети (CHD)', 'Младенцы (INF)'])
    for bar, val in zip(bars, avg_rev_pax.values):
        axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                        f'{val:.0f}', ha='center', fontweight='bold')
    
    ffp_rev = df.groupby('FFP_FLAG')['REVENUE_AMOUNT'].mean()
    axes[0, 1].bar(['Не участники', 'Участники FFP'], ffp_rev.values, 
                   color=['#FAB1A0', '#55A3FF'])
    axes[0, 1].set_title('Средняя выручка: FFP vs Non-FFP')
    axes[0, 1].set_ylabel('Средняя выручка (руб.)')
    for i, v in enumerate(ffp_rev.values):
        axes[0, 1].text(i, v + 5, f'{v:.0f}', ha='center', fontweight='bold')
    
    df.boxplot(column='DAYS_BEFORE_FLIGHT', by='PAX_TYPE', ax=axes[1, 0])
    axes[1, 0].set_title('Заблаговременность покупки по типам пассажиров')
    axes[1, 0].set_xlabel('Тип пассажира')
    axes[1, 0].set_ylabel('Дней до полёта')
    axes[1, 0].set_xticklabels(['Взрослые (AD)', 'Дети (CHD)', 'Младенцы (INF)'])
    plt.suptitle('S7 Airlines: Анализ пассажиров', fontsize=16, fontweight='bold')
    
    ffp_crosstab = pd.crosstab(df['PAX_TYPE'], df['FFP_FLAG'])
    ffp_crosstab.plot(kind='bar', ax=axes[1, 1], color=['#FAB1A0', '#55A3FF'])
    axes[1, 1].set_title('Распределение FFP по типам пассажиров')
    axes[1, 1].set_xlabel('Тип пассажира')
    axes[1, 1].set_ylabel('Количество')
    axes[1, 1].legend(title='FFP статус')
    axes[1, 1].tick_params(axis='x', rotation=0)
    axes[1, 1].set_xticklabels(['Взрослые (AD)', 'Дети (CHD)', 'Младенцы (INF)'])
    
    plt.tight_layout()
    plt.savefig('s7_passenger_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_passenger_analysis(df)

def analyze_payment_methods(df):
    print("\n" + "="*60)
    print("АНАЛИЗ СПОСОБОВ ОПЛАТЫ")
    print("="*60)
    
    fop_stats = df.groupby('FOP_PRIMARY').agg({
        'REVENUE_AMOUNT': ['count', 'mean', 'median', 'sum'],
        'DAYS_BEFORE_FLIGHT': 'mean',
        'IS_INTERNATIONAL': 'mean'
    }).round(2)
    fop_stats.columns = ['Count', 'Avg_Revenue', 'Median_Revenue', 
                        'Total_Revenue', 'Avg_Advance', 'Intl_Share']
    fop_stats = fop_stats.sort_values('Count', ascending=False)
    
    print("\n--- Статистика по способам оплаты ---")
    print(fop_stats.head(10))
    
    df['FOP_COUNT'] = df['FOP_TYPE_CODE'].str.count(',') + 1
    multi_fop = df.groupby('FOP_COUNT').agg({
        'REVENUE_AMOUNT': ['count', 'mean'],
        'DAYS_BEFORE_FLIGHT': 'mean'
    }).round(2)
    multi_fop.columns = ['Count', 'Avg_Revenue', 'Avg_Advance']
    
    print("\n--- Использование комбинированных способов оплаты ---")
    print(multi_fop)
    
    fop_sale = pd.crosstab(df['FOP_PRIMARY'], df['SALE_TYPE'], normalize='columns') * 100
    print("\n--- Способы оплаты по каналам продаж (%) ---")
    print(fop_sale.head(10).round(2))
    
    return fop_stats, multi_fop

fop_stats, multi_fop = analyze_payment_methods(df)

def plot_payment_analysis(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('S7 Airlines: Анализ способов оплаты', fontsize=16, fontweight='bold')
    
    top_fop = df['FOP_PRIMARY'].value_counts().head(8)
    axes[0, 0].barh(range(len(top_fop)), top_fop.values, color='lightblue')
    axes[0, 0].set_yticks(range(len(top_fop)))
    axes[0, 0].set_yticklabels(top_fop.index)
    axes[0, 0].set_xlabel('Количество транзакций')
    axes[0, 0].set_title('Топ-8 способов оплаты')
    axes[0, 0].invert_yaxis()
    
    top_5_fop = top_fop.head(5).index
    avg_rev_fop = df[df['FOP_PRIMARY'].isin(top_5_fop)].groupby('FOP_PRIMARY')['REVENUE_AMOUNT'].mean()
    avg_rev_fop = avg_rev_fop.reindex(top_5_fop)
    axes[0, 1].bar(range(len(avg_rev_fop)), avg_rev_fop.values, color='coral')
    axes[0, 1].set_xticks(range(len(avg_rev_fop)))
    axes[0, 1].set_xticklabels(avg_rev_fop.index)
    axes[0, 1].set_ylabel('Средняя выручка (руб.)')
    axes[0, 1].set_title('Средняя выручка по способам оплаты')
    
    multi_fop_data = df['FOP_COUNT'].value_counts().sort_index()
    axes[1, 0].bar(multi_fop_data.index, multi_fop_data.values, color='lightgreen')
    axes[1, 0].set_xlabel('Количество способов оплаты')
    axes[1, 0].set_ylabel('Количество транзакций')
    axes[1, 0].set_title('Использование комбинированных способов оплаты')
    for i, v in enumerate(multi_fop_data.values):
        axes[1, 0].text(multi_fop_data.index[i], v + 100, str(v), 
                        ha='center', fontweight='bold')
    
    top_4_fop = df['FOP_PRIMARY'].value_counts().head(4).index
    fop_sale_crosstab = pd.crosstab(df[df['FOP_PRIMARY'].isin(top_4_fop)]['FOP_PRIMARY'], 
                                    df[df['FOP_PRIMARY'].isin(top_4_fop)]['SALE_TYPE'])
    fop_sale_crosstab.plot(kind='bar', ax=axes[1, 1], color=['#74B9FF', '#A29BFE'])
    axes[1, 1].set_title('Способы оплаты по каналам продаж')
    axes[1, 1].set_xlabel('Способ оплаты')
    axes[1, 1].set_ylabel('Количество')
    axes[1, 1].legend(title='Канал продаж')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('s7_payment_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_payment_analysis(df)

def prepare_features_for_prediction(df):
    daily_sales = df.groupby('ISSUE_DATE').agg({
        'REVENUE_AMOUNT': ['count', 'sum', 'mean'],
        'DAYS_BEFORE_FLIGHT': 'mean'
    }).reset_index()
    daily_sales.columns = ['DATE', 'TICKETS_SOLD', 'TOTAL_REVENUE', 'AVG_REVENUE', 'AVG_ADVANCE']
    
    daily_sales['DAY_OF_WEEK'] = daily_sales['DATE'].dt.dayofweek
    daily_sales['MONTH'] = daily_sales['DATE'].dt.month
    daily_sales['DAY_OF_MONTH'] = daily_sales['DATE'].dt.day
    daily_sales['IS_WEEKEND'] = (daily_sales['DAY_OF_WEEK'] >= 5).astype(int)
    
    daily_sales['TICKETS_LAG_1'] = daily_sales['TICKETS_SOLD'].shift(1)
    daily_sales['TICKETS_LAG_7'] = daily_sales['TICKETS_SOLD'].shift(7)
    daily_sales['REVENUE_LAG_1'] = daily_sales['TOTAL_REVENUE'].shift(1)
    
    daily_sales['TICKETS_MA_7'] = daily_sales['TICKETS_SOLD'].rolling(window=7).mean().shift(1)
    
    daily_sales = daily_sales.dropna()
    
    return daily_sales

def predict_sales(df):
    print("\n" + "="*60)
    print("ПРЕДСКАЗАНИЕ ОБЪЕМОВ ПРОДАЖ")
    print("="*60)
    
    daily_data = prepare_features_for_prediction(df)
    
    print(f"\nРазмер датасета для моделирования: {daily_data.shape}")
    print(f"Период: {daily_data['DATE'].min()} - {daily_data['DATE'].max()}")
    
    feature_cols = ['DAY_OF_WEEK', 'MONTH', 'DAY_OF_MONTH', 'IS_WEEKEND',
                    'TICKETS_LAG_1', 'TICKETS_LAG_7', 'REVENUE_LAG_1', 'TICKETS_MA_7']
    
    X = daily_data[feature_cols]
    y_tickets = daily_data['TICKETS_SOLD']
    y_revenue = daily_data['TOTAL_REVENUE']
    
    split_date = daily_data['DATE'].quantile(0.8)
    train_mask = daily_data['DATE'] < split_date
    
    X_train, X_test = X[train_mask], X[~train_mask]
    y_tickets_train, y_tickets_test = y_tickets[train_mask], y_tickets[~train_mask]
    y_revenue_train, y_revenue_test = y_revenue[train_mask], y_revenue[~train_mask]
    dates_test = daily_data[~train_mask]['DATE']
    
    print(f"\nTrain период: {daily_data[train_mask]['DATE'].min()} - {daily_data[train_mask]['DATE'].max()}")
    print(f"Test период: {dates_test.min()} - {dates_test.max()}")
    
    rf_tickets = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_tickets.fit(X_train, y_tickets_train)
    y_tickets_pred = rf_tickets.predict(X_test)
    
    rf_revenue = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_revenue.fit(X_train, y_revenue_train)
    y_revenue_pred = rf_revenue.predict(X_test)
    
    print("\n--- Метрики качества модели (Random Forest) ---")
    print(f"Предсказание количества билетов:")
    print(f"  MAE: {mean_absolute_error(y_tickets_test, y_tickets_pred):.2f}")
    print(f"  R²: {r2_score(y_tickets_test, y_tickets_pred):.4f}")
    
    print(f"\nПредсказание выручки:")
    print(f"  MAE: {mean_absolute_error(y_revenue_test, y_revenue_pred):.2f}")
    print(f"  R²: {r2_score(y_revenue_test, y_revenue_pred):.4f}")
    
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance_tickets': rf_tickets.feature_importances_,
        'importance_revenue': rf_revenue.feature_importances_
    }).sort_values('importance_tickets', ascending=False)
    
    print("\n--- Важность признаков (для предсказания количества билетов) ---")
    print(feature_importance[['feature', 'importance_tickets']].round(4))
    
    return daily_data, dates_test, y_tickets_test, y_tickets_pred, y_revenue_test, y_revenue_pred, feature_importance

daily_data, dates_test, y_tickets_test, y_tickets_pred, y_revenue_test, y_revenue_pred, feature_importance = predict_sales(df)

def plot_predictions(dates_test, y_tickets_test, y_tickets_pred, y_revenue_test, y_revenue_pred, feature_importance):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('S7 Airlines: Предсказание объемов продаж', fontsize=16, fontweight='bold')
    
    axes[0, 0].plot(dates_test, y_tickets_test.values, label='Факт', color='blue', alpha=0.7)
    axes[0, 0].plot(dates_test, y_tickets_pred, label='Прогноз', color='red', linestyle='--')
    axes[0, 0].set_title('Предсказание количества билетов')
    axes[0, 0].set_xlabel('Дата')
    axes[0, 0].set_ylabel('Количество билетов')
    axes[0, 0].legend()
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    axes[0, 1].plot(dates_test, y_revenue_test.values, label='Факт', color='green', alpha=0.7)
    axes[0, 1].plot(dates_test, y_revenue_pred, label='Прогноз', color='red', linestyle='--')
    axes[0, 1].set_title('Предсказание выручки')
    axes[0, 1].set_xlabel('Дата')
    axes[0, 1].set_ylabel('Выручка (руб.)')
    axes[0, 1].legend()
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    axes[1, 0].scatter(y_tickets_test, y_tickets_pred, alpha=0.5, color='purple')
    axes[1, 0].plot([y_tickets_test.min(), y_tickets_test.max()], 
                    [y_tickets_test.min(), y_tickets_test.max()], 'r--', lw=2)
    axes[1, 0].set_xlabel('Фактическое количество')
    axes[1, 0].set_ylabel('Предсказанное количество')
    axes[1, 0].set_title('Точность предсказания (количество билетов)')
    
    top_features = feature_importance.sort_values('importance_tickets', ascending=True).tail(8)
    axes[1, 1].barh(top_features['feature'], top_features['importance_tickets'], color='coral')
    axes[1, 1].set_title('Важность признаков')
    axes[1, 1].set_xlabel('Важность')
    
    plt.tight_layout()
    plt.savefig('s7_sales_prediction.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_predictions(dates_test, y_tickets_test, y_tickets_pred, y_revenue_test, y_revenue_pred, feature_importance)


def create_summary_dashboard(df):
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
    
    fig.suptitle('S7 Airlines: Итоговый аналитический дашборд', fontsize=20, fontweight='bold', y=0.98)
    
    total_revenue = df['REVENUE_AMOUNT'].sum()
    total_tickets = len(df)
    avg_ticket_price = df['REVENUE_AMOUNT'].mean()
    online_share = (df['SALE_TYPE'] == 'ONLINE').mean() * 100
    ffp_share = (df['FFP_FLAG'] == 'FFP').mean() * 100
    
    ax_kpi = fig.add_subplot(gs[0, :])
    ax_kpi.axis('off')
    kpi_text = f"""
    КЛЮЧЕВЫЕ МЕТРИКИ:
    • Общая выручка: {total_revenue:,.0f} руб.  |  • Всего билетов: {total_tickets:,}  |  • Средний чек: {avg_ticket_price:.0f} руб.
    • Доля онлайн-продаж: {online_share:.1f}%  |  • Доля FFP: {ffp_share:.1f}%  |  • Международных рейсов: {(df['IS_INTERNATIONAL'].mean()*100):.1f}%
    """
    ax_kpi.text(0.5, 0.5, kpi_text, transform=ax_kpi.transAxes, fontsize=14,
                verticalalignment='center', horizontalalignment='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    ax1 = fig.add_subplot(gs[1, 0])
    monthly = df.groupby('ISSUE_MONTH').size()
    ax1.plot(monthly.index, monthly.values, marker='o', linewidth=2, color='steelblue')
    ax1.set_title('Динамика продаж по месяцам', fontweight='bold')
    ax1.set_xlabel('Месяц')
    ax1.grid(True, alpha=0.3)
    
    ax2 = fig.add_subplot(gs[1, 1])
    top5_airports = df['ORIG_CITY_CODE'].value_counts().head(5)
    ax2.bar(top5_airports.index, top5_airports.values, color='coral')
    ax2.set_title('Топ-5 аэропортов', fontweight='bold')
    ax2.set_ylabel('Количество рейсов')
    
    ax3 = fig.add_subplot(gs[1, 2])
    pax_dist = df['PAX_TYPE'].value_counts()
    ax3.pie(pax_dist.values, labels=['Взрослые', 'Дети', 'Младенцы'], 
            autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax3.set_title('Структура пассажиров', fontweight='bold')
    
    ax4 = fig.add_subplot(gs[1, 3])
    sale_dist = df['SALE_TYPE'].value_counts()
    ax4.bar(sale_dist.index, sale_dist.values, color=['#74B9FF', '#A29BFE'])
    ax4.set_title('Каналы продаж', fontweight='bold')
    
    ax5 = fig.add_subplot(gs[2, 0])
    ax5.hist(df['REVENUE_AMOUNT'], bins=30, color='lightgreen', edgecolor='black', alpha=0.7)
    ax5.axvline(df['REVENUE_AMOUNT'].mean(), color='red', linestyle='--', label='Среднее')
    ax5.set_title('Распределение выручки', fontweight='bold')
    ax5.set_xlabel('Выручка (руб.)')
    ax5.legend()
    
    ax6 = fig.add_subplot(gs[2, 1])
    top_fop = df['FOP_PRIMARY'].value_counts().head(5)
    ax6.barh(top_fop.index, top_fop.values, color='skyblue')
    ax6.set_title('Топ-5 способов оплаты', fontweight='bold')
    ax6.invert_yaxis()
    
    ax7 = fig.add_subplot(gs[2, 2])
    ffp_dist = df['FFP_FLAG'].value_counts()
    ax7.bar(['Не участники', 'Участники'], ffp_dist.values, color=['#FAB1A0', '#55A3FF'])
    ax7.set_title('Программа лояльности', fontweight='bold')
    
    ax8 = fig.add_subplot(gs[2, 3])
    weekday_data = df.groupby('ISSUE_WEEKDAY').size()
    colors = ['#FF6B6B' if d >= 5 else '#4ECDC4' for d in weekday_data.index]
    ax8.bar(range(7), weekday_data.values, color=colors)
    ax8.set_title('Продажи по дням недели', fontweight='bold')
    ax8.set_xticks(range(7))
    ax8.set_xticklabels(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'])
    
    plt.savefig('s7_dashboard.png', dpi=150, bbox_inches='tight')
    plt.show()

create_summary_dashboard(df)

print("\nСохранённые файлы:")
print("• s7_general_stats.png - Общие статистики")
print("• s7_airports_analysis.png - Анализ аэропортов")
print("• s7_seasonality.png - Сезонность")
print("• s7_passenger_analysis.png - Анализ пассажиров")
print("• s7_payment_analysis.png - Анализ оплаты")
print("• s7_sales_prediction.png - Предсказание продаж")
print("• s7_dashboard.png - Итоговый дашборд")