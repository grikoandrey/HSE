from datetime import datetime
from typing import List, Dict, Any


class Account:
    """
    ЭТАП 1.
    Базовый класс банковского счёта.
    Содержит только структуру данных и инициализацию.
    """

    def __init__(self, account_holder: str, balance: float = 0.0) -> None:
        """
        Начальный конструктор класса Account.

        Аргументы:
            account_holder (str): имя владельца счёта
            balance (float): начальный баланс (неотрицательный)

        Исключения/обработка ошибок:
            ValueError: если баланс отрицательный
        """
        if balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")

        self.holder: str = account_holder
        self._balance: float = float(balance)

        # История операций хранится как список словарей
        self.operations_history: List[Dict[str, Any]] = []

    def _add_operation(
        self,
        operation_type: str,
        amount: float,
        status: str,
        **extra
    ) -> None:
        """
        Внутренний метод для добавления операции в историю.
        Принимает дополнительные данные через extra.
        """
        operation = {
            "тип операции": operation_type,
            "сумма": amount,
            "дата операции": datetime.now(),
            "баланс после": self._balance,
            "статус": status
        }

        # Добавляем дополнительные поля (например, credit_used)
        operation.update(extra)

        self.operations_history.append(operation)

    def print_history(self) -> None:
        """
        Вывод истории операций в человеко-читаемом виде.

        Метод НЕ изменяет данные и допустим на этапе 1.
        """
        if not self.operations_history:
            print("История операций пуста.")
            return

        for operation in self.operations_history:
            date_str = operation["дата операции"].strftime(
                "%d.%m.%Y %H:%M:%S"
            )

            print(
                f"[{date_str}] "
                f"Тип: {operation['тип операции']}, "
                f"Сумма: {operation['сумма']}, "
                f"Статус: {operation['статус']}, "
                f"Баланс после: {operation['баланс после']}"
            )

# ===== Демонстрация этапа 1 =====


if __name__ == "__main__":
    account = Account("Иван Иванов", 1000)

    # Добавим тестовую операцию вручную (допустимо на этапе 1)
    account._add_operation("пополнение", 500, "success")

    print("=======1 этап ======")
    print("Владелец:", account.holder)
    print("Баланс:", account._balance)

    print("\nИстория операций:")
    account.print_history()


class Account(Account):
    """
    ЭТАП 2.
    Расширение класса Account методами бизнес-логики.
    """

    def deposit(self, amount: float) -> None:
        """
        Пополнение счёта.

        Аргументы:
            amount (float): сумма пополнения

        Исключения/обработка ошибок:
            ValueError: если сумма некорректна
        """
        if amount <= 0:
            # Фиксируем неудачную попытку пополнения
            self._add_operation("пополнение", amount, "fail")
            raise ValueError("Сумма пополнения должна быть положительной")

        self._balance += amount
        self._add_operation("пополнение", amount, "success")

    def withdraw(self, amount: float) -> bool:
        """
        Снятие средств со счёта.

        Аргументы:
            amount (float): сумма снятия

        Возвращаемые значения:
            bool: True — операция выполнена успешно,
                  False — недостаточно средств

        Исключения/обработка ошибок:
            ValueError: если сумма некорректна
        """
        if amount <= 0:
            # Фиксируем неудачную попытку снятия
            self._add_operation("снятие", amount, "fail")
            raise ValueError("Сумма снятия должна быть положительной")

        if amount > self._balance:
            # Средств недостаточно — операция не выполнена
            self._add_operation("снятие", amount, "fail")
            return False

        self._balance -= amount
        self._add_operation("снятие", amount, "success")
        return True

    def get_balance(self) -> float:
        """
        Возвращает текущий баланс счёта.
        """
        return self._balance

    def get_history(self):
        """
        Возвращает копию истории операций.
        """
        return self.operations_history.copy()

# ===== Демонстрация этапа 2 =====


if __name__ == "__main__":
    account = Account("Иван Иванов", 1000)

    account.deposit(500)
    account.withdraw(300)
    account.withdraw(2000)  # недостаточно средств

    print("=======2 этап ======")
    print("Владелец:", account.holder)
    print("Текущий баланс:", account.get_balance())
    print("\nИстория операций:")
    account.print_history()
