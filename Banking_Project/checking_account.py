"""
Project 11
James D. Rodgers 7/20/2025

This file defines the CheckingAccount class, which inherits from the Account class.
Checking accounts charge a transaction fee for every successful deposit or withdrawal.
"""

from account import Account
from decimal import Decimal

class CheckingAccount(Account):
    """
    Checking account charges a fee per transaction.
    """

    def __init__(self, name, balance, fee_per_transaction):
        """
        Initializes checking account with a name, balance, and fee.
        """
        super().__init__(name, balance)
        self.__fee_per_transaction = Decimal(str(fee_per_transaction))

    @property
    def fee_per_transaction(self):
        """
        Method to get the transaction fee.
        """
        return self.__fee_per_transaction

    def deposit(self, amount):
        """
        Deposits money into the account, subtracting the transaction fee.
        """
        amount = Decimal(str(amount))
        if amount <= self.__fee_per_transaction:
            print("Deposit amount must be greater than the transaction fee.")
        else:
            super().deposit(amount - self.__fee_per_transaction)

    def withdraw(self, amount):
        """
        Withdraws money from the account, subtracting the fee.
        """
        amount = Decimal(str(amount))
        total = amount + self.__fee_per_transaction
        if amount <= 0:
            print("Withdrawal amount must be positive.")
        elif total > self.balance:
            print("Insufficient funds for withdrawal and fee.")
        else:
            super().withdraw(total)

    def __str__(self):
        """
        Returns a formatted string with account info and transaction fee.
        """
        return f"Checking Account - Name: {self.name}, Balance: ${self.balance:.2f}, Fee per Transaction: ${self.__fee_per_transaction:.2f}"
