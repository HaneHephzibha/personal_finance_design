from abc import ABC, abstractmethod

# -------------------------
# ACCOUNT CLASSES
# -------------------------

class Account:
    def __init__(self, account_id, balance, account_password, account_holder):
        self._account_id = account_id
        self._balance = balance
        self.__account_password = account_password
        self.account_holder = account_holder
        self._transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient balance")
        self._balance -= amount

    def get_balance(self):
        return self._balance

    def add_transaction(self, transaction):
        self._transactions.append(transaction)

    def get_transactions(self):
        return self._transactions.copy()

    def set_password(self, new_password):
        self.__account_password = new_password

    def check_password(self, password):
        return self.__account_password == password

    @staticmethod
    def calculate_tax(amount):
        return amount * 0.18

    @staticmethod
    def format_currency(balance):
        return f"Your available balance is ₹{balance:.2f}"

    @staticmethod
    def calculate_savings_rate(income, expenses):
        if income <= 0:
            raise ValueError("Income must be greater than zero")
        savings = income - expenses
        return (savings / income) * 100


class SavingAccount(Account):
    def __init__(self, account_id, balance, account_password, account_holder, min_balance):
        super().__init__(account_id, balance, account_password, account_holder)
        self.min_balance = min_balance

    def withdraw(self, amount):
        if self._balance - amount < self.min_balance:
            raise ValueError("Minimum balance rule violated")
        super().withdraw(amount)


class ExpensesAccount(Account):
    def __init__(self, account_id, balance, account_password, account_holder, month_limit):
        super().__init__(account_id, balance, account_password, account_holder)
        self.month_limit = month_limit
        self.monthly_withdraw = 0

    def withdraw(self, amount):
        if self.monthly_withdraw + amount > self.month_limit:
            raise ValueError("Monthly limit exceeded")
        super().withdraw(amount)
        self.monthly_withdraw += amount


# -------------------------
# TRANSACTION CLASSES
# -------------------------

class Transaction(ABC):
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def process_transaction(self):
        pass


class IncomeTransaction(Transaction):
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def validate(self):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")

    def process_transaction(self):
        self.validate()
        self.account.deposit(self.amount)
        self.account.add_transaction(self)


class ExpenseTransaction(Transaction):
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def validate(self):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")

    def process_transaction(self):
        self.validate()
        self.account.withdraw(self.amount)
        self.account.add_transaction(self)


class TransferTransaction(Transaction):
    def __init__(self, from_account, to_account, amount):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def validate(self):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")

    def process_transaction(self):
        self.validate()
        self.from_account.withdraw(self.amount)
        self.to_account.deposit(self.amount)
        self.from_account.add_transaction(self)
        self.to_account.add_transaction(self)


# -------------------------
# BUDGET MANAGER
# -------------------------

class BudgetManager:
    def __init__(self):
        self._category_limits = {}
        self._spending = {}

    def set_budget_limit(self, category, limit):
        self._category_limits[category] = limit
        self._spending[category] = 0

    def add_expense(self, category, amount):
        if category not in self._spending:
            raise ValueError("Category not found")
        self._spending[category] += amount

        if self._spending[category] > self._category_limits[category]:
            print(f"⚠️ Warning: {category} budget exceeded!")

    def get_budget_status(self):
        return self._spending.copy()


# -------------------------
# MAIN PROGRAM (USAGE)
# -------------------------

if __name__ == "__main__":

    acc1 = SavingAccount(1, 5000, "pass1", "Ane", min_balance=1000)
    acc2 = ExpensesAccount(2, 3000, "pass2", "Esther", month_limit=2000)

    income = IncomeTransaction(acc1, 2000)
    income.process_transaction()

    expense = ExpenseTransaction(acc1, 500)
    expense.process_transaction()

    transfer = TransferTransaction(acc1, acc2, 1000)
    transfer.process_transaction()

    print(Account.format_currency(acc1.get_balance()))
    print(Account.format_currency(acc2.get_balance()))

    budget = BudgetManager()
    budget.set_budget_limit("Food", 2000)
    budget.set_budget_limit("Travel", 1500)

    budget.add_expense("Food", 1200)
    budget.add_expense("Food", 900)  # triggers warning

    print("Budget Status:", budget.get_budget_status())
