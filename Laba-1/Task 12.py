base_price = 24.99
base_minutes = 60
base_sms = 30
base_data_mb = 1024

extra_minute_price = 0.89
extra_sms_price = 0.59
extra_mb_price = 0.79
tax_rate = 0.02

used_minutes = int(input("Введите количество использованных минут: "))
used_sms = int(input("Введите количество отправленных SMS: "))
used_data_mb = int(input("Введите объем использованного интернет-трафика (в МБ): "))

extra_minutes = max(0, used_minutes - base_minutes)
extra_sms = max(0, used_sms - base_sms)
extra_data_mb = max(0, used_data_mb - base_data_mb)

extra_minutes_cost = round(extra_minutes * extra_minute_price, 2)
extra_sms_cost = round(extra_sms * extra_sms_price, 2)
extra_data_cost = round(extra_data_mb * extra_mb_price, 2)

subtotal = round(base_price + extra_minutes_cost + extra_sms_cost + extra_data_cost, 2)
tax = round(subtotal * tax_rate, 2)
total = round(subtotal + tax, 2)

print()
print("Базовая сумма тарифа:", round(base_price, 2), "руб.")
if extra_minutes > 0:
    print("Доп. минуты:", extra_minutes, "шт. →", extra_minutes_cost, "руб.")
if extra_sms > 0:
    print("Доп. SMS:", extra_sms, "шт. →", extra_sms_cost, "руб.")
if extra_data_mb > 0:
    print("Доп. интернет:", extra_data_mb, "МБ →", extra_data_cost, "руб.")
print("Налог (2%):", tax, "руб.")
print("Итоговая сумма к оплате:", total, "руб.")
