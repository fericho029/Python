import uuid
import json

# Исключения
class AccountExistsError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class UnauthorizedAccessError(Exception):
    pass

# Класс банковского счёта
class Account:
    def __init__(self, currency):
        self.currency = currency
        self.balance = 0.0
        self.id = str(uuid.uuid4())

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError("Недостаточно средств на счете.")
        self.balance -= amount

# Класс кредита
class Credit:
    def __init__(self, amount, currency, interest_rate):
        self.amount = amount
        self.currency = currency
        self.interest_rate = interest_rate
        self.remaining = amount * (1 + interest_rate)
        self.id = str(uuid.uuid4())

    def repay(self, payment):
        if payment > self.remaining:
            raise ValueError("Платёж превышает остаток по кредиту.")
        self.remaining -= payment

    def get_summary(self):
        return {
            "ID кредита": self.id,
            "Валюта": self.currency,
            "Сумма кредита": self.amount,
            "Процентная ставка": self.interest_rate,
            "Остаток долга": self.remaining
        }

# Класс клиента
class Client:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.accounts = {}  # currency -> Account
        self.credits = []   # список кредитов

    def open_account(self, currency):
        if currency in self.accounts:
            raise AccountExistsError("Счет в этой валюте уже существует.")
        self.accounts[currency] = Account(currency)

    def close_account(self, currency):
        if currency not in self.accounts:
            raise ValueError("Счет не найден.")
        del self.accounts[currency]

    def get_account(self, currency):
        return self.accounts.get(currency)

    def open_credit(self, amount, currency, interest_rate):
        credit = Credit(amount, currency, interest_rate)
        self.credits.append(credit)
        return credit

    def repay_credit(self, credit_id, amount):
        for credit in self.credits:
            if credit.id == credit_id:
                credit.repay(amount)
                return
        raise ValueError("Кредит не найден.")

    def get_credit_summary(self):
        return [credit.get_summary() for credit in self.credits]

    def get_summary(self):
        total = sum(acc.balance for acc in self.accounts.values())
        return {
            "ID клиента": self.id,
            "Имя": self.name,
            "Счета": {
                cur: acc.balance for cur, acc in self.accounts.items()
            },
            "Суммарный баланс": total
        }

# Класс банка
class Bank:
    def __init__(self):
        self.clients = {}  # id -> Client

    def register_client(self, name):
        client = Client(name)
        self.clients[client.id] = client
        return client

    def get_client(self, client_id):
        return self.clients.get(client_id)

    def transfer(self, from_client, from_currency, to_client, to_currency, amount):
        from_acc = from_client.get_account(from_currency)
        to_acc = to_client.get_account(to_currency)
        if not from_acc or not to_acc:
            raise ValueError("Один из счетов не найден.")
        from_acc.withdraw(amount)
        to_acc.deposit(amount)

# Терминальный интерфейс
def main():
    bank = Bank()
    print("Добро пожаловать в банковскую систему!")

    while True:
        print("\nГлавное меню:")
        print("1. Зарегистрировать клиента")
        print("2. Войти по ID")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Введите имя клиента: ")
            client = bank.register_client(name)
            print(f"Клиент зарегистрирован. Ваш ID: {client.id}")

        elif choice == "2":
            client_id = input("Введите ваш ID: ")
            client = bank.get_client(client_id)
            if not client:
                print("Клиент не найден.")
                continue

            while True:
                print(f"\nЗдравствуйте, {client.name}!")
                print("1. Просмотреть состояние баланса")
                print("2. Выписка по счетам (сохранить в файл)")
                print("3. Открыть счет")
                print("4. Закрыть счет")
                print("5. Пополнить счет")
                print("6. Снять со счета")
                print("7. Перевести между счетами")
                print("8. Открыть кредит")
                print("9. Погасить кредит")
                print("10. Выписка по кредитам (сохранить в файл)")
                print("0. Выйти")
                sub_choice = input("Выберите действие: ")

                if sub_choice == "1":
                    summary = client.get_summary()
                    print("\n📊 Состояние баланса:")
                    print(f"Имя клиента: {summary['Имя']}")
                    print(f"ID клиента: {summary['ID клиента']}")
                    print("Счета:")
                    for currency, balance in sorted(summary["Счета"].items()):
                        print(f"  {currency}: {balance:.2f}")
                    print(f"Суммарный баланс: {summary['Суммарный баланс']:.2f}")

                elif sub_choice == "2":
                    summary = client.get_summary()
                    filename = f"{client.id}_summary.json"
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(summary, f, indent=4, ensure_ascii=False)
                    print(f"Выписка сохранена в файл {filename}")

                elif sub_choice == "3":
                    currency = input("Введите валюту: ")
                    try:
                        client.open_account(currency)
                        print("Счет открыт.")
                    except AccountExistsError as e:
                        print(e)

                elif sub_choice == "4":
                    currency = input("Введите валюту: ")
                    try:
                        client.close_account(currency)
                        print("Счет закрыт.")
                    except ValueError as e:
                        print(e)

                elif sub_choice == "5":
                    currency = input("Введите валюту: ")
                    amount = float(input("Сумма пополнения: "))
                    acc = client.get_account(currency)
                    if acc:
                        acc.deposit(amount)
                        print("Счет пополнен.")
                    else:
                        print("Счет не найден.")

                elif sub_choice == "6":
                    currency = input("Введите валюту: ")
                    amount = float(input("Сумма снятия: "))
                    acc = client.get_account(currency)
                    if acc:
                        try:
                            acc.withdraw(amount)
                            print("Снятие выполнено.")
                        except InsufficientFundsError as e:
                            print(e)
                    else:
                        print("Счет не найден.")

                elif sub_choice == "7":
                    to_id = input("ID получателя: ")
                    to_client = bank.get_client(to_id)
                    if not to_client:
                        print("Получатель не найден.")
                        continue
                    from_currency = input("Ваша валюта: ")
                    to_currency = input("Валюта получателя: ")
                    amount = float(input("Сумма перевода: "))
                    try:
                        bank.transfer(client, from_currency, to_client, to_currency, amount)
                        print("Перевод выполнен.")
                    except Exception as e:
                        print(e)

                elif sub_choice == "8":
                    currency = input("Валюта кредита: ")
                    amount = float(input("Сумма кредита: "))
                    rate = float(input("Процентная ставка (например, 0.1 для 10%): "))
                    credit = client.open_credit(amount, currency, rate)
                    print(f"Кредит открыт. ID кредита: {credit.id}")

                elif sub_choice == "9":
                    credit_id = input("ID кредита: ")
                    amount = float(input("Сумма погашения: "))
                    try:
                        client.repay_credit(credit_id, amount)
                        print("Погашение выполнено.")
                    except Exception as e:
                        print(e)

                elif sub_choice == "10":
                    credits = client.get_credit_summary()
                    filename = f"{client.id}_credits.json"
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(credits, f, indent=4, ensure_ascii=False)
                    print(f"Выписка по кредитам сохранена в файл {filename}")

                elif sub_choice == "0":
                    break

        elif choice == "0":
            print("До свидания!")
            break

if __name__ == "__main__":
    main()